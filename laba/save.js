import createModule from "./pokemon.js";

createModule().then((Module) => {
    function savePokemonData(pokemon) {
        let newPokemon;
        if (pokemon.type === "fire") {
            newPokemon = new Module.FirePokemon(pokemon.name, pokemon.health, pokemon.damage);
            newPokemon.setFirePower(pokemon.fireAttack);
            newPokemon.setFireResistance(pokemon.fireResist);
        } else if (pokemon.type === "water") {
            newPokemon = new Module.WaterPokemon(pokemon.name, pokemon.health, pokemon.damage);
            newPokemon.setWaterPower(pokemon.waterAttack);
            newPokemon.setWaterResistance(pokemon.waterResist);
        } else if (pokemon.type === "electric") {
            newPokemon = new Module.ElectricPokemon(pokemon.name, pokemon.health, pokemon.damage);
            newPokemon.setElectricCharge(pokemon.electricCharge);
            newPokemon.setElectricPower(pokemon.electricPower);
        }
        console.log(`${newPokemon.getName()} создан с ${newPokemon.getHealth()} HP и уроном ${newPokemon.getDamage()}`);
        if (pokemon.type === "fire") {
            console.log(`Сопротивление огню: ${newPokemon.getFireResistance()}`);
            console.log(`Сила огня: ${newPokemon.getFirePower()}`);
        } else if (pokemon.type === "water") {
            console.log(`Сопротивление воде: ${newPokemon.getWaterResistance()}`);
            console.log(`Сила воды: ${newPokemon.getWaterPower()}`);
        } else if (pokemon.type === "electric") {
            console.log(`Заряд электричества: ${newPokemon.getElectricCharge()}`);
            console.log(`Мощность электричества: ${newPokemon.getElectricPower()}`);
        }
    }
    window.savePokemonData = savePokemonData;
}).catch((err) => {
    console.error("", err);
});
