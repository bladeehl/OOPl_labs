
function selectPokemon(type) {
    document.querySelector(".cards").style.display = "none";
    let form = document.getElementById("pokemonForm");
    form.style.display = "flex";

    let img = document.getElementById("pokemonImage");
    
    document.getElementById("name").value = "";
    document.getElementById("health").value = "";
    document.getElementById("damage").value = "";
    document.getElementById("fireAttack").value = "";
    document.getElementById("fireResist").value = "";
    document.getElementById("waterAttack").value = "";
    document.getElementById("waterResist").value = "";
    document.getElementById("electricCharge").value = "";
    document.getElementById("electricPower").value = "";

    document.getElementById("fireAttack").style.display = "none";
    document.getElementById("fireResist").style.display = "none";
    document.getElementById("waterAttack").style.display = "none";
    document.getElementById("waterResist").style.display = "none";
    document.getElementById("electricCharge").style.display = "none";
    document.getElementById("electricPower").style.display = "none";

    if (type === "fire") {
        img.src = "charm.png";
        document.getElementById("fireAttack").style.display = "block";
        document.getElementById("fireResist").style.display = "block";
    } else if (type === "water") {
        img.src = "sqr.png";
        document.getElementById("waterAttack").style.display = "block";
        document.getElementById("waterResist").style.display = "block";
    } else if (type === "electric") {
        img.src = "pikachu.png";
        document.getElementById("electricCharge").style.display = "block";
        document.getElementById("electricPower").style.display = "block";
    }
}


function validateForm() { //Соотвественно валидация
    let name = document.getElementById("name").value;
    
    let healthField = document.getElementById("health");
    let damageField = document.getElementById("damage");

    let fireAttack = document.getElementById("fireAttack");
    let fireResist = document.getElementById("fireResist");
    let waterAttack = document.getElementById("waterAttack");
    let waterResist = document.getElementById("waterResist");
    let electricCharge = document.getElementById("electricCharge");
    let electricPower = document.getElementById("electricPower");

    let inputFields = [healthField, damageField, fireAttack, fireResist, waterAttack, waterResist, electricCharge, electricPower];
    inputFields.forEach(field => {
        field.value = field.value.replace(/[^0-9]/g, '');
    });

    let health = healthField.value;
    let damage = damageField.value;

    let extraFields = [];
    if (fireAttack.style.display !== "none") extraFields.push(fireAttack.value, fireResist.value);
    if (waterAttack.style.display !== "none") extraFields.push(waterAttack.value, waterResist.value);
    if (electricCharge.style.display !== "none") extraFields.push(electricCharge.value, electricPower.value);

    let allFieldsFilled = [name, health, damage, ...extraFields].every(value => value.trim() !== "");
    let noZeros = [health, damage, ...extraFields].every(value => Number(value) > 0); 

    let nameValid = /^[A-Za-zА-Яа-яЁё]+$/.test(name);
    let numbersValid = [...extraFields, health, damage].every(value => !isNaN(value) && Number(value) >= 0);

    document.getElementById("createButton").disabled = !(allFieldsFilled && nameValid && numbersValid && noZeros);
}




function goBack() { //Функционал кнопки назад
    let form = document.getElementById("pokemonForm");
    let cards = document.querySelector(".cards");

    if (form.style.display === "flex") {
        form.style.display = "none";
        cards.style.display = "flex";
    } else {
        window.location.href = "index.html";
    }
}

document.addEventListener("DOMContentLoaded", function () {  //Сохранения покемона в кэш
    let createButton = document.getElementById("createButton");
    
    if (createButton) {
        createButton.addEventListener("click", function () {
            let name = document.getElementById("name").value;
            let health = document.getElementById("health").value;
            let damage = document.getElementById("damage").value;

            let fireAttack = document.getElementById("fireAttack").value;
            let fireResist = document.getElementById("fireResist").value;
            let waterAttack = document.getElementById("waterAttack").value;
            let waterResist = document.getElementById("waterResist").value;
            let electricCharge = document.getElementById("electricCharge").value;
            let electricPower = document.getElementById("electricPower").value;

            let type = "unknown";
            if (document.getElementById("fireAttack").style.display !== "none") type = "fire";
            if (document.getElementById("waterAttack").style.display !== "none") type = "water";
            if (document.getElementById("electricCharge").style.display !== "none") type = "electric";

            let pokemonData = {
                name,
                health: Number(health),
                damage: Number(damage),
                type,
                fireAttack: Number(fireAttack) || 0,
                fireResist: Number(fireResist) || 0,
                waterAttack: Number(waterAttack) || 0,
                waterResist: Number(waterResist) || 0,
                electricCharge: Number(electricCharge) || 0,
                electricPower: Number(electricPower) || 0
            };

            savePokemonData(pokemonData);
            localStorage.setItem("savedPokemon", JSON.stringify(pokemonData));
            window.location.href = "index.html";
        });
    } 
});