import tkinter as tk

state={
    "userName": "User",
    "current_dir": "~",
    "NetName": "Net"
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
    tokens = command.split()
    comm = tokens[0]
    args = tokens[1:]
    handler = commands.get(comm)
    if (handler):
        handler(args)
    else:
        print_text_to_lable(f"Команда {comm} не найдена!")

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

root.mainloop()

