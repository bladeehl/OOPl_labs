import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from pokemon_dao import (
    get_pokemons_by_trainer,
    create_fire_pokemon,
    create_water_pokemon,
    delete_pokemon_by_id,
    update_pokemon
)

def refresh_table(tree, trainer_id):
    for item in tree.get_children():
        tree.delete(item)
    pokemons = get_pokemons_by_trainer(trainer_id)
    for p in pokemons:
        values = [
            p.name,
            p.type,
            p.health,
            p.damage,
            getattr(p, "firepower", "") or getattr(p, "waterpower", ""),
            getattr(p, "fireresistance", "") or getattr(p, "waterresistance", "")
        ]
        tree.insert('', 'end', values=values, tags=(p.id,))

def prompt_stat(name):
    value = simpledialog.askinteger("Введите параметр", f"{name}:", minvalue=1)
    if value is None:
        raise Exception("Операция отменена")
    return value

def add_fire(trainer_id, tree):
    try:
        name = simpledialog.askstring("Имя", "Введите имя покемона:")
        health = prompt_stat("Здоровье")
        damage = prompt_stat("Урон")
        firepower = prompt_stat("Огненная сила")
        fireresistance = prompt_stat("Огненная защита")
        create_fire_pokemon(name, health, damage, firepower, fireresistance, trainer_id)
        refresh_table(tree, trainer_id)
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

def add_water(trainer_id, tree):
    try:
        name = simpledialog.askstring("Имя", "Введите имя покемона:")
        health = prompt_stat("Здоровье")
        damage = prompt_stat("Урон")
        waterpower = prompt_stat("Водная сила")
        waterresistance = prompt_stat("Водная защита")
        create_water_pokemon(name, health, damage, waterpower, waterresistance, trainer_id)
        refresh_table(tree, trainer_id)
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

def delete_selected(tree, trainer_id):
    selected = tree.focus()
    if not selected:
        return
    tags = tree.item(selected)['tags']
    if not tags:
        return
    pokemon_id = int(tags[0])
    delete_pokemon_by_id(pokemon_id)
    refresh_table(tree, trainer_id)

def on_cell_double_click(event, tree, trainer_id):
    item_id = tree.identify_row(event.y)
    column = tree.identify_column(event.x)
    if not item_id or not column:
        return

    col_index = int(column[1:]) - 1
    if col_index == 1:  # "Тип" нельзя редактировать
        return

    columns = ["name", "type", "health", "damage", "power", "resistance"]
    col_name = columns[col_index]

    current_value = tree.item(item_id)['values'][col_index]
    new_value = simpledialog.askstring("Изменить значение", f"{col_name}:", initialvalue=str(current_value))
    if new_value is None:
        return

    try:
        if col_name != "name":
            new_value = int(new_value)
        tags = tree.item(item_id)['tags']
        if not tags:
            return
        pokemon_id = int(tags[0])

        attr_map = {
            "name": "name",
            "health": "health",
            "damage": "damage",
            "power": "firepower",  # или waterpower
            "resistance": "fireresistance"  # или waterresistance
        }
        real_attr = attr_map.get(col_name)
        if real_attr:
            update_pokemon(pokemon_id, **{real_attr: new_value})
            refresh_table(tree, trainer_id)
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

def open_pokemon_window(trainer, main_menu_window):
    win = tk.Toplevel()
    win.title(f"Покемоны тренера {trainer.name}")
    win.geometry("700x400")

    def on_close():
        win.destroy()
        main_menu_window.deiconify()

    columns = ("Имя", "Тип", "Здоровье", "Урон", "Стихийная сила", "Стихийная защита")
    tree = ttk.Treeview(win, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col, anchor="center")
        tree.column(col, width=100, anchor="center", stretch=False)
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    tree.bind("<Double-1>", lambda e: on_cell_double_click(e, tree, trainer.id))
    refresh_table(tree, trainer.id)

    btn_frame = tk.Frame(win)
    btn_frame.pack(pady=5)

    tk.Button(btn_frame, text="Добавить огненного", command=lambda: add_fire(trainer.id, tree)).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Добавить водного", command=lambda: add_water(trainer.id, tree)).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="Удалить выбранного", command=lambda: delete_selected(tree, trainer.id)).grid(row=0, column=2, padx=5)
    tk.Button(btn_frame, text="Назад", command=lambda: (win.destroy(), main_menu_window.deiconify())).grid(row=0, column=3, padx=5)

    win.protocol("WM_DELETE_WINDOW", on_close)
