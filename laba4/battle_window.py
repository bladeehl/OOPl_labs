import tkinter as tk
from tkinter import messagebox, scrolledtext
from random import randint, choice
from pokemon_dao import get_pokemons_by_trainer
from models import FirePokemon, WaterPokemon


def generate_dummy_bot():
    name = choice(["Infernosaur", "Hydromancer", "Scorchtail", "Waveclaw"])
    base_health = randint(100, 150)
    base_damage = randint(15, 25)

    if randint(0, 1) == 0:
        return FirePokemon(name=name, health=base_health, damage=base_damage,
                           firepower=randint(10, 30), fireresistance=randint(10, 30))
    else:
        return WaterPokemon(name=name, health=base_health, damage=base_damage,
                            waterpower=randint(10, 30), waterresistance=randint(10, 30))


def open_battle_window(trainer, main_menu_window):
    pokemons = get_pokemons_by_trainer(trainer.id)
    if not pokemons:
        messagebox.showwarning("Нет покемонов", "Сначала создайте хотя бы одного покемона.")
        return

    main_menu_window.withdraw()
    battle_win = tk.Toplevel()
    battle_win.title("Сражение")
    battle_win.geometry("700x700")

    def go_back():
        battle_win.destroy()
        main_menu_window.deiconify()

    tk.Label(battle_win, text="Выберите покемона", font=("Arial", 14)).pack(pady=10)
    listbox = tk.Listbox(battle_win)
    for p in pokemons:
        listbox.insert(tk.END, f"{p.name} (HP: {p.health})")
    listbox.pack(pady=10)

    def start_battle():
        selection = listbox.curselection()
        if not selection:
            messagebox.showerror("Ошибка", "Выберите покемона.")
            return

        player_pokemon = pokemons[selection[0]]
        bot_pokemon = generate_dummy_bot()

        for widget in battle_win.winfo_children():
            widget.destroy()

        player_stats = tk.StringVar()
        bot_stats = tk.StringVar()

        log_text = scrolledtext.ScrolledText(battle_win, height=10, state='disabled', wrap='word')
        log_text.pack(padx=10, pady=10, fill='both', expand=True)

        def log(message):
            log_text.config(state='normal')
            log_text.insert(tk.END, message + '\n')
            log_text.see(tk.END)
            log_text.config(state='disabled')

        def update_stats():
            stats = f"{player_pokemon.name} — HP: {player_pokemon.health}, Урон: {player_pokemon.damage}"
            if isinstance(player_pokemon, FirePokemon):
                stats += f", Сопр. огню: {player_pokemon.fireresistance}, Сила огня: {player_pokemon.firepower}"
            elif isinstance(player_pokemon, WaterPokemon):
                stats += f", Сопр. воде: {player_pokemon.waterresistance}, Сила воды: {player_pokemon.waterpower}"
            player_stats.set(stats)
            bot_stats.set(f"{bot_pokemon.name} — HP: {bot_pokemon.health}, Урон: {bot_pokemon.damage}")

        def check_victory():
            if bot_pokemon.health <= 0:
                log(f"{bot_pokemon.name} повержен! Победа!")
                disable_buttons()
                return True
            elif player_pokemon.health <= 0:
                log(f"{player_pokemon.name} проиграл! Поражение!")
                disable_buttons()
                return True
            return False

        def bot_turn():
            if bot_pokemon.health > 0:
                old_health = player_pokemon.health
                player_pokemon.take_damage(bot_pokemon.damage)
                real_damage = old_health - player_pokemon.health
                log(f"{bot_pokemon.name} атакует и наносит {real_damage} урона.")
                update_stats()
                check_victory()

        def disable_buttons():
            for btn in action_buttons:
                btn.config(state="disabled")

        def perform_action(action_func):
            if player_pokemon.health <= 0 or bot_pokemon.health <= 0:
                return
            player_pokemon.damage_reduction = 0
            action_func()
            update_stats()
            if not check_victory():
                bot_turn()

        def attack():
            player_pokemon.attack(bot_pokemon)
            log(f"{player_pokemon.name} атакует и наносит {player_pokemon.damage} урона.")

        def use_ability():
            player_pokemon.ability()
            log(f"{player_pokemon.name} использует способность!")

        def special_attack():
            if isinstance(player_pokemon, FirePokemon):
                player_pokemon.fire_ball(bot_pokemon)
                log(f"{player_pokemon.name} использует Огненный шар!")
            elif isinstance(player_pokemon, WaterPokemon):
                player_pokemon.wave_attack(bot_pokemon)
                log(f"{player_pokemon.name} использует Водную волну!")

        def defend():
            player_pokemon.defend()
            log(f"{player_pokemon.name} активирует защиту!")

        def evolve():
            player_pokemon.evolve()
            log(f"{player_pokemon.name} эволюционирует!")

        update_stats()

        tk.Label(battle_win, text=f"{player_pokemon.name} VS {bot_pokemon.name}", font=("Arial", 16)).pack(pady=10)
        tk.Label(battle_win, textvariable=player_stats, fg='blue').pack()
        tk.Label(battle_win, textvariable=bot_stats, fg='red').pack()

        button_frame = tk.Frame(battle_win)
        button_frame.pack(pady=15)

        action_buttons = [
            tk.Button(button_frame, text="Атака", width=15, command=lambda: perform_action(attack)),
            tk.Button(button_frame, text="Способность", width=15, command=lambda: perform_action(use_ability)),
            tk.Button(button_frame, text="Спец. атака", width=15, command=lambda: perform_action(special_attack)),
            tk.Button(button_frame, text="Защита", width=15, command=lambda: perform_action(defend)),
            tk.Button(button_frame, text="Эволюция", width=15, command=lambda: perform_action(evolve))
        ]

        for idx, btn in enumerate(action_buttons):
            btn.grid(row=idx // 2, column=idx % 2, padx=5, pady=5)

        tk.Button(battle_win, text="Назад", command=go_back).pack(pady=10)

    tk.Button(battle_win, text="Начать бой", command=start_battle).pack(pady=10)
    tk.Button(battle_win, text="Назад", command=go_back).pack(pady=10)