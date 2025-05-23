import createModule from "./pokemon.js";
import promptSync from "prompt-sync";

const prompt = promptSync();

createModule().then((Module) => {
    // Создаем покемонов
    const squirtle = new Module.WaterPokemon("Squirtle", 120, 10);
    squirtle.setWaterResistance(50);
    squirtle.setWaterPower(30);

    const charizard = new Module.FirePokemon("Charizard", 150, 50);
    charizard.setFireResistance(80);
    charizard.setFirePower(60);

    console.log("\n⚔️  Битва началась! ⚔️");
    console.log(`🔥 ${charizard.getName()} (HP: ${charizard.getHealth()}) VS 🌊 ${squirtle.getName()} (HP: ${squirtle.getHealth()})\n`);

    let turn = 0;
    while (squirtle.getHealth() > 0 && charizard.getHealth() > 0) {
        const attacker = turn % 2 === 0 ? charizard : squirtle;
        const defender = turn % 2 === 0 ? squirtle : charizard;

        console.log(`🎮 Ходит: ${attacker.getName()}`);
        console.log("1️⃣ Атаковать");
        console.log("2️⃣ Защититься");
        console.log("3️⃣ Использовать способность");
        if (attacker instanceof Module.FirePokemon) {
            console.log("4️⃣ Fire Ball (🔥 огненный шар)");
            console.log("5️⃣ Fire Thorns (🔥 огненные шипы)");
        }
        if (attacker instanceof Module.WaterPokemon) {
            console.log("4️⃣ Wave Attack (🌊 атака волной)");
            console.log("5️⃣ Water Hide (🌊 водная маскировка)");
        }
        console.log("6️⃣ Эволюция");

        const choice = prompt("Выбери действие (1-6): ");
        let damageDealt = 0;
        let healthRestored = 0;

        switch (choice) {
            case "1":  // Обычная атака
                const beforeHP = defender.getHealth();
                attacker.attack(defender);
                damageDealt = beforeHP - defender.getHealth();
                console.log(`💥 ${attacker.getName()} атаковал ${defender.getName()} и нанёс ${damageDealt} урона!`);
                break;

            case "2":  // Защита
                attacker.defend();
                console.log(`🛡️ ${attacker.getName()} приготовился к защите!`);
                break;

            case "3":  // Уникальная способность
                const beforeAbilityHP = attacker.getHealth();
                attacker.ability();
                healthRestored = attacker.getHealth() - beforeAbilityHP;
                console.log(`✨ ${attacker.getName()} использовал способность!`);
                if (healthRestored > 0) {
                    console.log(`❤️ Восстановлено ${healthRestored} HP!`);
                }
                break;

            case "4":  // Специальная атака
                if (attacker instanceof Module.FirePokemon) {
                    const beforeHP_Fire = defender.getHealth();
                    attacker.fireBall(defender);
                    damageDealt = beforeHP_Fire - defender.getHealth();
                    console.log(`🔥 ${attacker.getName()} запустил огненный шар и нанёс ${damageDealt} урона!`);
                } else {
                    const beforeHP_Water = defender.getHealth();
                    attacker.waveAttack(defender);
                    damageDealt = beforeHP_Water - defender.getHealth();
                    console.log(`🌊 ${attacker.getName()} использовал атаку волной и нанёс ${damageDealt} урона!`);
                }
                break;

            case "5":  // Защитные способности
                if (attacker instanceof Module.FirePokemon) {
                    attacker.fireThorns();
                    console.log(`🔥 ${attacker.getName()} активировал огненные шипы!`);
                } else {
                    attacker.waterHide();
                    console.log(`🌊 ${attacker.getName()} скрылся в воде и будет неуязвим в следующий ход!`);
                }
                break;

            case "6":  // Эволюция
                attacker.evolve();
                console.log(`🆙 ${attacker.getName()} эволюционировал!`);
                break;

            default:
                console.log("⛔ Некорректный ввод. Пропуск хода.");
        }

        console.log(`📊 Статистика после хода:`);
        console.log(`   🔥 ${charizard.getName()} - HP: ${charizard.getHealth()}, Атака: ${charizard.getDamage()}, Сопротивление: ${charizard.getFireResistance()}`);
        console.log(`   🌊 ${squirtle.getName()} - HP: ${squirtle.getHealth()}, Атака: ${squirtle.getDamage()}, Сопротивление: ${squirtle.getWaterResistance()}`);
        console.log(`--------------------------------------------------\n`);

        turn++;
    }

    const winner = squirtle.getHealth() > 0 ? squirtle : charizard;
    console.log(`🏆 ${winner.getName()} победил! 🎉`);

}).catch((err) => {
    console.error("Ошибка загрузки модуля:", err);
});
