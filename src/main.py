import argparse
import tkinter as tk
import shlex
import os
from os import wait
from time import sleep

state={
    "userName": "User",
    "current_dir": "~",
    "NetName": "Net",
    "vfs_path": "",
    "script_path": ""
}

def print_text_to_lable(text_):
    output.config(state=tk.NORMAL)
    output.insert(tk.END, text_ + "\n")
    output.see(tk.END)
    output.config(state=tk.DISABLED)

def on_enter_pressed(event):
    command = entry.get()
    entry.delete(0, tk.END)
    systemGreeting = f"{state['userName']}@{state['NetName']}:{state['current_dir']}$ "
    text = systemGreeting+command
    print_text_to_lable(text)
    execute_command(command)

def execute_command(command):
    tokens = shlex.split(command)
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
    print_text_to_lable(f"ls args: {args}")

def cd_comm(args):
    print_text_to_lable(f"cd args: {args}")

def exit_comm(args):
    exit()

commands = {
    "ls":ls_comm,
    "cd":cd_comm,
    "exit":exit_comm
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
    print_text_to_lable(f"Путь к VFS: {state['vfs_path'] if state['vfs_path'] else '(не указан)'}")
    print_text_to_lable(f"Путь к скрипту: {state['script_path'] if state['script_path'] else '(не указан)'}")
    print_text_to_lable(f"Имя пользователя: {state['userName']}")
    print_text_to_lable(f"Сеть: {state['NetName']}")
    print_text_to_lable(f"Текущая директория: {state['current_dir']}")
    print_text_to_lable("Конец показа параметров\n\n")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--vfs-path', type=str, default="",help='Путь к физическому расположению VFS')
    parser.add_argument('--script', type=str, default="",help='Путь к стартовому скрипту')
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

systemGreeting = tk.Label(
    input_frame,
    text=f"{state['userName']}@{state['NetName']}:{state['current_dir']}$ ",
    anchor="w"
)

systemGreeting.pack(side=tk.LEFT)

entry = tk.Entry(input_frame)
entry.pack(side=tk.LEFT,fill=tk.X, expand=True)
entry.bind('<Return>', on_enter_pressed)
entry.focus_set()

if state["vfs_path"] == "":
    print_text_to_lable("Ошибка!!! Укажите путь для распололжнеия VFS!!!")
    input_frame.destroy()
    root.after(2000, root.destroy)

else:
    debug_print_params()
    if (state['script_path']):
        run_script(state['script_path'])

root.mainloop()

