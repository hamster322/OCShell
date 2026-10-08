import argparse
import tkinter as tk
import shlex
import os
import zipfile
import datetime
import platform

state={
    "userName": "User",
    "current_dir": "/",
    "NetName": "Net",
    "vfs_path": "",
    "script_path": "",
    "vfs":None
}


def load_vfs(vfs_path):
    """Загрузка VFS из ZIP-архива в память"""
    vfs = {}
    if not os.path.exists(vfs_path):
        try:
            with zipfile.ZipFile(vfs_path, 'w') as zf:
                pass
            print_text_to_lable(f"Файл '{vfs_path}' не найден. Создан пустой архив.")
            vfs["/"]={
                'is_dir': True,
                'size': 0,
                'date': datetime.datetime,
                'content': None
            }
            return {}, None
        except Exception as e:
            return None, f"Ошибка при создании пустого архива '{vfs_path}': {str(e)}"

    if not zipfile.is_zipfile(vfs_path):
        return None, f"Ошибка: '{vfs_path}' не является ZIP-архивом!"

    if vfs_path=="":
        return None, "Ошибка: путь к vfs не указан!"

    try:
        with zipfile.ZipFile(vfs_path, 'r') as zip_ref:
            for info in zip_ref.infolist():
                path = info.filename
                vfs["/"+path] = {
                    'is_dir': info.is_dir(),
                    'size': info.file_size,
                    'date': datetime.datetime(*info.date_time[0:6]).strftime('%Y-%m-%d %H:%M'),
                    'content': zip_ref.read(path) if not info.is_dir() else None
                }
            vfs["/"] = {
                'is_dir': True,
                'size': 0,
                'date': "0",
                'content': None
            }
        return vfs, None
    except Exception as e:
        return None, f"Ошибка при чтении архива: {str(e)}"


def normalize_path(path):
    """Нормализация пути"""
    if not path.startswith('/'):
        path = state['current_dir'] + '/' + path if state['current_dir'] != '/' else '/' + path

    parts = path.split('/')
    normalized = []

    for part in parts:
        if part == '..':
            if normalized:
                normalized.pop()
        elif part and part != '.':
            normalized.append(part)

    return '/' + '/'.join(normalized)

def get_vfs_entry(path):
    """Получить запись из VFS"""
    path = normalize_path(path)
    if path in state['vfs']:
        return state['vfs'][path]
    if path + '/' in state['vfs']:
        return state['vfs'][path + '/']
    return None


def list_directory(dir_path):
    """Список содержимого директории"""
    dir_path = normalize_path(dir_path)
    if not dir_path.endswith('/'):
        dir_path += '/'

    entry = get_vfs_entry(dir_path)
    if entry is None:
        return None, f"Невозможно получить доступ к '{dir_path}': Нет такого файла или каталога"

    if not entry['is_dir']:
        return None, f"Невозможно получить доступ к '{dir_path}': Не является каталогом"

    contents = []
    for path, info in state['vfs'].items():
        if path.startswith(dir_path) and path != dir_path:
            relative = path[len(dir_path):]
            if '/' not in relative.rstrip('/'):
                contents.append((relative.rstrip('/'), info))

    return contents, None

def print_text_to_lable(text_):
    """Вывод тектса в окно консоли"""
    output.config(state=tk.NORMAL)
    output.insert(tk.END, text_ + "\n")
    output.see(tk.END)
    output.config(state=tk.DISABLED)

def on_enter_pressed(event):
    """Обработка нажатия Enter при вводе команды"""
    command = entry.get()
    entry.delete(0, tk.END)
    system_greeting = f"{state['userName']}@{state['NetName']}:{state['current_dir']}$ "
    text = system_greeting+command
    print_text_to_lable(text)
    execute_command(command)

def execute_command(command):
    """Выполнение команды"""
    try:
        tokens = shlex.split(command)
    except ValueError:
        print_text_to_lable("Не получилось извлечь аргумент!!!")
        return

    comm = tokens[0]
    args = tokens[1:]

    handler = commands.get(comm)
    if (handler):
        handler(args)
        return True
    else:
        print_text_to_lable(f"Команда {comm} не найдена!")
        return False

def ls_comm(args):
    """Описание команды ls"""
    print_text_to_lable(f"ls args: {args}")

def cd_comm(args):
    """Описание команды cd"""
    print_text_to_lable(f"cd args: {args}")

def exit_comm(args):
    """Описание команды exit"""
    exit()

def look_comm(args, ofset=0):
    """Описание команды look для проверки работы с архивом"""
    try:
        contents, error = list_directory(args[0])
    except IndexError:
        print_text_to_lable("Неверный флаг!!!")
        return
    if error:
        print_text_to_lable(error)
        return

    if not contents and ofset==0:
        print_text_to_lable("(пусто)")
        return

    for name, info in sorted(contents):
        marker = '/' if info['is_dir'] else ''
        size = f"  {info['size']} bytes" if not info['is_dir'] else ""
        print_text_to_lable(" "*ofset*4+f"{name}{marker}{size}")
        if info['is_dir']:
            look_comm([args[0]+"/"+name], ofset=ofset+1)

commands = {
    "ls":ls_comm,
    "cd":cd_comm,
    "exit":exit_comm,
    "look":look_comm
}

def run_script(script_path):
    """Выполняет команды из стартового скрипта"""
    if not os.path.exists(script_path):
        print_text_to_lable(f"Ошибка: скрипт '{script_path}' не найден!")
        return

    print_text_to_lable(f"Выполнение стартового скрипта: {script_path}")

    with open(script_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line_num, line in enumerate(lines, 1):
        line = line.strip()

        if not line or line[0]=='#':
            continue

        print_text_to_lable(f"\n--- Строка {line_num}: {line} ---")

        success = execute_command(line)

        if not success:
            print_text_to_lable(f"Ошибка при выполнении строки {line_num}: '{line}'")
            print_text_to_lable("Выполнение скрипта остановлено!!!")
            break

def debug_print_params():
    """Вывод параметров командной строки"""
    print_text_to_lable("Параметры запуска эмулятора:")
    print_text_to_lable(f"Путь к VFS: {state['vfs_path']}")
    if (state["script_path"]):
        print_text_to_lable(f"Путь к скрипту: {state['script_path']}")
    else:
        print_text_to_lable(f"Путь к скрипту не указан")
    print_text_to_lable(f"Имя пользователя: {state['userName']}")
    print_text_to_lable(f"Сеть: {state['NetName']}")
    print_text_to_lable(f"Текущая директория: {state['current_dir']}")
    print_text_to_lable("Конец показа параметров\n\n")

def parse_args():
    """Парсинг аргументов из скрипта запуска"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--vfs-path', type=str, default="")
    parser.add_argument('--script', type=str, default="")
    return parser.parse_args()

args = parse_args()
state['vfs_path'] = args.vfs_path
state['script_path'] = args.script

root = tk.Tk()
root.title("VFS")
root.geometry("800x600")

output = tk.Text(root, height=20 ,state=tk.DISABLED, wrap=tk.WORD)
output.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=5, padx=10)

input_frame = tk.Frame(root)
input_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

system_greeting = tk.Label(
    input_frame,
    text=f"{state['userName']}@{state['NetName']}:{state['current_dir']}$ ",
    anchor="w"
)
system_greeting.pack(side=tk.LEFT)

entry = tk.Entry(input_frame)
entry.pack(side=tk.LEFT,fill=tk.X, expand=True)
entry.bind('<Return>', on_enter_pressed)
entry.focus_set()

debug_print_params()

vfs, error = load_vfs(state["vfs_path"])
if (error):
    print_text_to_lable(error)
    input_frame.destroy()
    root.after(3000, root.destroy)
else:
    state["vfs"]=vfs
    if (state['script_path']):
        run_script(state['script_path'])

root.mainloop()

