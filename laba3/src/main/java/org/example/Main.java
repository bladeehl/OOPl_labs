package org.example;

import java.util.List;
import java.util.Scanner;

public class Main {
    private static final Scanner scanner = new Scanner(System.in);
    private static Trainer currentTrainer = null;

    public static void main(String[] args) {
        while (true) {
            currentTrainer = null;
            while (currentTrainer == null) {
                System.out.println("\n--- Тренерское меню ---");
                System.out.println("1. Создать нового тренера");
                System.out.println("2. Выбрать существующего тренера");
                System.out.println("0. Выход");
                System.out.print("Выберите действие: ");
                int choice = safeIntInput();
                switch (choice) {
                    case 1 -> createTrainer();
                    case 2 -> selectTrainer();
                    case 0 -> {
                        DatabaseHelper.shutdown();
                        System.out.println("Выход...");
                        return;
                    }
                    default -> System.out.println("Некорректный выбор.");
                }
            }
            boolean backToTrainerMenu = false;
            while (!backToTrainerMenu) {
                System.out.println("\n--- Меню для тренера: " + currentTrainer.getName() + " ---");
                System.out.println("1. Начать игру");
                System.out.println("2. Создать покемона");
                System.out.println("3. Изменить покемона");
                System.out.println("4. Удалить покемона");
                System.out.println("5. Показать всех покемонов");
                System.out.println("0. Назад к выбору тренера");
                System.out.print("Выберите действие: ");
                int choice = safeIntInput();
                switch (choice) {
                    case 1 -> startBattle();
                    case 2 -> createPokemon();
                    case 3 -> updatePokemon();
                    case 4 -> deletePokemon();
                    case 5 -> showAllPokemons();
                    case 0 -> backToTrainerMenu = true;
                    default -> System.out.println("Некорректный выбор.");
                }
            }
        }
    }

    private static void showAllPokemons() {
        List<Pokemon> pokemons = PokemonDAO.getPokemonsByTrainer(currentTrainer);

        if (pokemons.isEmpty()) {
            System.out.println("У этого тренера нет покемонов.");
            return;
        }

        System.out.println("\n--- Список покемонов тренера " + currentTrainer.getName() + " ---");
        for (Pokemon pokemon : pokemons) {
            System.out.println(pokemon.toString()); // Будет вызывать соответствующий toString()
        }
        System.out.println("Всего покемонов: " + pokemons.size());
    }

    private static void createTrainer() {
        System.out.print("Введите имя тренера: ");
        String name = scanner.next();

        Trainer trainer = new Trainer();
        trainer.setName(name);

        TrainerDAO.saveTrainer(trainer);
        currentTrainer = trainer;
        System.out.println("Тренер создан и выбран.");
    }

    private static void startBattle() {
        List<Pokemon> pokemons = PokemonDAO.getPokemonsByTrainer(currentTrainer);

        if (pokemons.size() < 2) {
            System.out.println("У тренера должно быть хотя бы 2 покемона для боя.");
            return;
        }

        System.out.println("Выберите двух покемонов для сражения:");
        for (int i = 0; i < pokemons.size(); i++) {
            System.out.printf("%d - %s (%s, HP: %d)\n", i + 1, pokemons.get(i).getName(),
                    pokemons.get(i).getClass().getSimpleName(), pokemons.get(i).getHealth());
        }

        System.out.print("Первый покемон (номер): ");
        int firstIndex = safeIntInput() - 1;
        System.out.print("Второй покемон (номер): ");
        int secondIndex = safeIntInput() - 1;

        if (firstIndex == secondIndex || firstIndex < 0 || secondIndex < 0 ||
                firstIndex >= pokemons.size() || secondIndex >= pokemons.size()) {
            System.out.println("Неверный выбор покемонов.");
            return;
        }

        Pokemon p1 = pokemons.get(firstIndex);
        Pokemon p2 = pokemons.get(secondIndex);

        System.out.printf("\n⚔️ Битва началась: %s VS %s ⚔️\n", p1.getName(), p2.getName());
        int turn = 0;

        while (p1.getHealth() > 0 && p2.getHealth() > 0) {
            Pokemon attacker = (turn % 2 == 0) ? p1 : p2;
            Pokemon defender = (turn % 2 == 0) ? p2 : p1;

            System.out.printf("\n🎮 Ходит: %s\n", attacker.getName());
            System.out.println("1. Атаковать");
            System.out.println("2. Защититься");
            System.out.println("3. Способность");
            System.out.println("4. Спец. атака");
            System.out.println("5. Защитная способность");
            System.out.println("6. Эволюция");
            System.out.print("Выберите действие: ");
            String choice = scanner.next();

            switch (choice) {
                case "1" -> {
                    int before = defender.getHealth();
                    attacker.attack(defender);
                    System.out.printf("💥 %s атаковал %s на %d урона\n", attacker.getName(), defender.getName(), before - defender.getHealth());
                }
                case "2" -> {
                    attacker.defend();
                    System.out.printf("🛡️ %s встал в защиту\n", attacker.getName());
                }
                case "3" -> {
                    int before = attacker.getHealth();
                    attacker.ability();
                    int healed = attacker.getHealth() - before;
                    System.out.printf("✨ %s использовал способность (+%d HP)\n", attacker.getName(), healed);
                }
                case "4" -> {
                    if (attacker instanceof FirePokemon fire) {
                        int before = defender.getHealth();
                        fire.fireBall(defender);
                        System.out.printf("🔥 Fire Ball! Нанесено %d урона\n", before - defender.getHealth());
                    } else if (attacker instanceof WaterPokemon water) {
                        int before = defender.getHealth();
                        water.waveAttack(defender);
                        System.out.printf("🌊 Wave Attack! Нанесено %d урона\n", before - defender.getHealth());
                    } else {
                        System.out.println("Нет спец. атаки.");
                    }
                }
                case "5" -> {
                    if (attacker instanceof FirePokemon fire) {
                        fire.fireThorns();
                        System.out.println("🔥 Fire Thorns активирован");
                    } else if (attacker instanceof WaterPokemon water) {
                        water.waterHide();
                        System.out.println("🌊 Water Hide активирован");
                    } else {
                        System.out.println("Нет защитной способности.");
                    }
                }
                case "6" -> {
                    attacker.evolve();
                    System.out.println("🆙 Эволюция завершена!");
                }
                default -> System.out.println("⛔ Неверный ввод, пропуск хода.");
            }

            System.out.printf("📊 %s (HP: %d) VS %s (HP: %d)\n", p1.getName(), p1.getHealth(), p2.getName(), p2.getHealth());
            turn++;
        }

        Pokemon winner = (p1.getHealth() > 0) ? p1 : p2;
        System.out.printf("🏆 Победитель: %s!\n", winner.getName());
    }

    private static void selectTrainer() {
        List<Trainer> trainers = TrainerDAO.getAllTrainers();
        if (trainers.isEmpty()) {
            System.out.println("Нет доступных тренеров.");
            return;
        }
        System.out.println("Список тренеров:");
        for (int i = 0; i < trainers.size(); i++) {
            System.out.printf("%d - %s\n", i + 1, trainers.get(i).getName());
        }
        System.out.print("Выберите номер тренера (0 - назад): ");
        int index = safeIntInput();

        if (index == 0 || index < 0 || index > trainers.size()) {
            System.out.println("Неверный выбор.");
            return;
        }
        currentTrainer = trainers.get(index - 1);
        System.out.println("Выбран тренер: " + currentTrainer.getName());
    }

    private static void createPokemon() {
        System.out.println("Выберите тип покемона:");
        System.out.println("1. Огненный");
        System.out.println("2. Водяной");
        int type = safeIntInput();
        String name = promptForName("Имя: ");
        int health = promptForNatural("Здоровье: ");
        int damage = promptForNatural("Урон: ");

        switch (type) {
            case 1 -> {
                int fireRes = promptForNatural("Огненная защита: ");
                int firePower = promptForNatural("Огненная сила: ");
                FirePokemon fire = new FirePokemon(name, health, damage, fireRes, firePower);
                fire.setTrainer(currentTrainer);
                PokemonDAO.savePokemon(fire);
            }
            case 2 -> {
                int waterRes = promptForNatural("Водная защита: ");
                int waterPower = promptForNatural("Водная сила: ");
                WaterPokemon water = new WaterPokemon(name, health, damage, waterRes, waterPower);
                water.setTrainer(currentTrainer);
                PokemonDAO.savePokemon(water);
            }
            default -> System.out.println("Неверный выбор.");
        }
        System.out.println("Покемон создан.");
    }

    private static void updatePokemon() {
        List<Pokemon> pokemons = PokemonDAO.getPokemonsByTrainer(currentTrainer);

        if (pokemons.isEmpty()) {
            System.out.println("Нет покемонов для изменения.");
            return;
        }
        System.out.println("Список покемонов:");
        for (int i = 0; i < pokemons.size(); i++) {
            Pokemon p = pokemons.get(i);
            System.out.printf("%d - %s (%s)\n", i + 1, p.getName(), p.getClass().getSimpleName());
        }
        System.out.print("Введите номер покемона (0 - назад): ");
        int index = safeIntInput();
        if (index == 0 || index < 0 || index > pokemons.size()) {
            System.out.println("Неверный выбор.");
            return;
        }
        Pokemon selected = pokemons.get(index - 1);

        System.out.println("Что изменить?");
        System.out.println("1. Имя");
        System.out.println("2. Здоровье");
        System.out.println("3. Урон");

        if (selected instanceof FirePokemon) {
            System.out.println("4. Огненная защита");
            System.out.println("5. Огненная сила");
        } else if (selected instanceof WaterPokemon) {
            System.out.println("4. Водная защита");
            System.out.println("5. Водная сила");
        }

        int opt = safeIntInput();
        switch (opt) {
            case 1 -> selected.setName(promptForName("Новое имя: "));
            case 2 -> selected.setHealth(promptForNatural("Новое здоровье: "));
            case 3 -> selected.setDamage(promptForNatural("Новый урон: "));
            case 4 -> {
                int val = promptForNatural("Новое значение защиты: ");
                if (selected instanceof FirePokemon fire) fire.setFireResistance(val);
                else if (selected instanceof WaterPokemon water) water.setWaterResistance(val);
            }
            case 5 -> {
                int val = promptForNatural("Новое значение силы: ");
                if (selected instanceof FirePokemon fire) fire.setFirePower(val);
                else if (selected instanceof WaterPokemon water) water.setWaterPower(val);
            }
            default -> System.out.println("Неверный выбор.");
        }

        PokemonDAO.updatePokemon(selected);
        System.out.println("Покемон обновлён.");
    }

    private static void deletePokemon() {
        List<Pokemon> pokemons = PokemonDAO.getPokemonsByTrainer(currentTrainer);

        if (pokemons.isEmpty()) {
            System.out.println("Нет покемонов для удаления.");
            return;
        }

        System.out.println("Список покемонов:");
        for (int i = 0; i < pokemons.size(); i++) {
            Pokemon p = pokemons.get(i);
            System.out.printf("%d - %s (%s)\n", i + 1, p.getName(), p.getClass().getSimpleName());
        }

        System.out.print("Введите номер покемона (0 - назад): ");
        int index = safeIntInput();
        if (index == 0 || index < 0 || index > pokemons.size()) {
            System.out.println("Неверный выбор.");
            return;
        }

        Pokemon selected = pokemons.get(index - 1);
        PokemonDAO.deletePokemon(selected);
        System.out.println("Покемон удалён.");
    }

    private static int promptForNatural(String prompt) {
        int val;
        while (true) {
            System.out.print(prompt);
            try {
                val = Integer.parseInt(scanner.next());
                if (val > 0) return val;
                else System.out.println("Введите натуральное число (целое и > 0).");
            } catch (NumberFormatException e) {
                System.out.println("Введите корректное натуральное число.");
            }
        }
    }

    private static String promptForName(String prompt) {
        while (true) {
            System.out.print(prompt);
            String name = scanner.next();
            if (name.matches("[A-Za-zА-Яа-яЁё]{2,20}")) {
                return name;
            } else {
                System.out.println("Имя должно содержать только буквы и быть длиной от 2 до 20 символов.");
            }
        }
    }

    private static int safeIntInput() {
        try {
            return Integer.parseInt(scanner.next());
        } catch (NumberFormatException e) {
            return -1;
        }
    }
}