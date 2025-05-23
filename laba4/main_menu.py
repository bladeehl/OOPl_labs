import tkinter as tk
from pokemon_gui import open_pokemon_window
from battle_window import open_battle_window

def open_main_menu(trainer, root_app_window):
    root_app_window.withdraw()

    menu_win = tk.Toplevel()
    menu_win.title(f"Главное меню - {trainer.name}")
    menu_win.geometry("300x250")

    def on_close():
        menu_win.destroy()
        root_app_window.deiconify()

    def open_pokemon_gui():
        menu_win.withdraw()
        open_pokemon_window(trainer, menu_win)

    def start_battle_gui():
        open_battle_window(trainer, menu_win)

    def go_back():
        menu_win.destroy()
        root_app_window.deiconify()

    # Заголовок
    tk.Label(menu_win, text=f"Тренер: {trainer.name}", font=("Arial", 14)).pack(pady=10)

    # Кнопка "Играть"
    tk.Button(menu_win, text="Играть", width=20, command=start_battle_gui).pack(pady=5)

    # Кнопка "Покемоны"
    tk.Button(menu_win, text="Покемоны", width=20, command=open_pokemon_gui).pack(pady=5)

    # Кнопка "Назад"
    tk.Button(menu_win, text="Назад", width=20, command=go_back).pack(pady=20)

    menu_win.protocol("WM_DELETE_WINDOW", on_close)
