import tkinter as tk
from tkinter import messagebox
from trainer_dao import get_all_trainers, create_trainer
from main_menu import open_main_menu

def refresh_trainer_list(listbox):
    listbox.delete(0, tk.END)
    for trainer in get_all_trainers():
        listbox.insert(tk.END, trainer.name)

def on_select_trainer(listbox, root):
    selection = listbox.curselection()
    if not selection:
        messagebox.showwarning("Выбор тренера", "Пожалуйста, выберите тренера.")
        return
    index = selection[0]
    trainer = get_all_trainers()[index]
    root.withdraw()
    open_main_menu(trainer, root)

def on_add_trainer(entry, listbox):
    name = entry.get().strip()
    if not name:
        messagebox.showerror("Ошибка", "Имя тренера не может быть пустым.")
        return
    create_trainer(name)
    entry.delete(0, tk.END)
    refresh_trainer_list(listbox)

def start_app():
    root = tk.Tk()
    root.title("Выбор тренера")
    root.geometry("300x400")

    trainer_listbox = tk.Listbox(root)
    trainer_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    refresh_trainer_list(trainer_listbox)

    name_entry = tk.Entry(root)
    name_entry.pack(padx=10, pady=(0, 5))

    add_button = tk.Button(root, text="Добавить тренера", command=lambda: on_add_trainer(name_entry, trainer_listbox))
    add_button.pack(padx=10, pady=5)

    select_button = tk.Button(root, text="Выбрать", command=lambda: on_select_trainer(trainer_listbox, root))
    select_button.pack(padx=10, pady=5)

    root.mainloop()

if __name__ == "__main__":
    start_app()
