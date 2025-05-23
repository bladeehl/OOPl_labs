import createModule from "./pokemon.js";

createModule().then((Module) => {
    let savedPokemon = JSON.parse(localStorage.getItem("savedPokemon"));
    console.log(savedPokemon.fireAttack);
    let playerPokemon;
    let turnsPassed = 0; 
    const evolveBtn = document.getElementById("evolveBtn"); 
    evolveBtn.style.display = "none"; 

    if (savedPokemon.type === "fire") {
        playerPokemon = new Module.FirePokemon(savedPokemon.name, savedPokemon.health, savedPokemon.damage);
        playerPokemon.setFireResistance(savedPokemon.fireResist);
        playerPokemon.setFirePower(savedPokemon.fireAttack);

        console.log(playerPokemon.getFireResistance());
        document.getElementById("fireBallBtn").style.display = "block";
        document.getElementById("fireThornsBtn").style.display = "block";
    } else if (savedPokemon.type === "water") {
        playerPokemon = new Module.WaterPokemon(savedPokemon.name, savedPokemon.health, savedPokemon.damage);
        playerPokemon.setWaterResistance(savedPokemon.waterResist);
        playerPokemon.setWaterPower(savedPokemon.waterAttack);
        document.getElementById("waveAttackBtn").style.display = "block";
        document.getElementById("waterHideBtn").style.display = "block";
    } else {
        playerPokemon = new Module.ElectricPokemon(savedPokemon.name, savedPokemon.health, savedPokemon.damage);
        playerPokemon.setElectricCharge(savedPokemon.electricCharge);
        playerPokemon.setElectricPower(savedPokemon.electricPower);
        document.getElementById("thunderboltBtn").style.display = "block";
        document.getElementById("chargeBtn").style.display = "block";
    }

    let enemy = new Module.ElectricPokemon("Enemy", 650, 50);
    enemy.setElectricCharge(30);

        document.getElementById("playerName").innerText = playerPokemon.getName();
    if (savedPokemon.type === "fire") {
        playerImage.src = "charm.png"; 
    } else if (savedPokemon.type === "water") {
        playerImage.src = "sqr.png"; 
    } else if (savedPokemon.type === "electric") {
        playerImage.src = "pikachu.png"; 
    } 

    let turn = 0; 
    
    function updateHealthBars() {
        document.getElementById("playerHP").innerText = playerPokemon.getHealth();
        document.getElementById("enemyHP").innerText = enemy.getHealth();

        document.getElementById("playerHPBar").style.width = (playerPokemon.getHealth() / savedPokemon.health) * 100 + "%";
        document.getElementById("enemyHPBar").style.width = (enemy.getHealth() / 650) * 100 + "%";
    }

    let gameOver = false; 

function disableButtons() {
    let buttons = document.querySelectorAll("button"); 
    buttons.forEach(button => button.disabled = true); 
}

function checkGameOver() {
    if (playerPokemon.getHealth() <= 0) {
        logAction(`💀 ${playerPokemon.getName()} проиграл!`);
        gameOver = true;
        disableButtons(); 
        return true;
    }
    if (enemy.getHealth() <= 0) {
        logAction(`🏆 Противник повержен! ${playerPokemon.getName()} победил!`);
        gameOver = true;
        disableButtons(); 
        return true;
    }
    return false;
}

    function logAction(message) {
        let logDiv = document.getElementById("battleLog");
        let newEntry = document.createElement("p");
        newEntry.innerText = message;
        logDiv.appendChild(newEntry);
        logDiv.scrollTop = logDiv.scrollHeight;
    }


    function nextTurn() {
        if (checkGameOver()) return; 
         turnsPassed++; 
        if (turnsPassed === 6) {
        evolveBtn.style.display = "block";
    }
        turn = (turn + 1) % 2; 
        
        if (turn === 1) {
            setTimeout(enemyTurn, 1000); 
        }
    }

    function enemyTurn() {
        if (turn !== 1) return; 

        if (Math.random() > 0.3) {
            enemy.attack(playerPokemon);
            playerPokemon.unImmune();
            logAction(`❌ Противник атаковал!`);
        } else {
            enemy.defend();
            logAction(`🛡️ Противник использует защиту!`);
        }
        
        updateHealthBars();
        nextTurn();
    }

    document.getElementById("attackBtn").addEventListener("click", () => {
        if (turn !== 0) return;
        playerPokemon.attack(enemy);
        logAction(`🔥 ${playerPokemon.getName()} атакует!`);
        enemy.unImmune();
        updateHealthBars();
        nextTurn();
    });

    document.getElementById("defendBtn").addEventListener("click", () => {
        if (turn !== 0) return;

        playerPokemon.defend();
        logAction(`🛡️ ${playerPokemon.getName()} использует защиту!`);
        enemy.unImmune();
        nextTurn();
    });

    document.getElementById("abilityBtn").addEventListener("click", () => {
        if (turn !== 0) return;

        playerPokemon.ability();
        logAction(`✨ ${playerPokemon.getName()} использует способность!`);
        updateHealthBars();
        enemy.unImmune();
        nextTurn();
    });

    document.getElementById("evolveBtn").addEventListener("click", () => {
        if (turn !== 0) return;

        playerPokemon.evolve();
        logAction(`⚡ ${playerPokemon.getName()} эволюционирует!`);
        updateHealthBars();
        if (savedPokemon.type === "fire") {
            playerImage.src = "fEvolve.png"; 
        } else if (savedPokemon.type === "water") {
            playerImage.src = "wEvolve.png"; 
        } else if (savedPokemon.type === "electric") {
            playerImage.src = "eEvolve.png"; 
        } 
        evolveBtn.style.display = "none"; 
        nextTurn();
    });

    if (savedPokemon.type === "water") {
        document.getElementById("waveAttackBtn").addEventListener("click", () => {
            if (turn !== 0) return;

            playerPokemon.waveAttack(enemy);
            logAction(`🌊 ${playerPokemon.getName()} использует атаку волной!`);
            updateHealthBars();
            enemy.unImmune();
            nextTurn();
        });

        document.getElementById("waterHideBtn").addEventListener("click", () => {
            if (turn !== 0) return;

            playerPokemon.waterHide();
            logAction(`💦 ${playerPokemon.getName()} скрывается в воде!`);
            nextTurn();
        });
    }

    if (savedPokemon.type === "fire") {
        document.getElementById("fireBallBtn").addEventListener("click", () => {
            if (turn !== 0) return;

            playerPokemon.fireBall(enemy);
            logAction(`🔥 ${playerPokemon.getName()} использует Огненный шар!`);
            enemy.unImmune();
            updateHealthBars();
            nextTurn();
        });

        document.getElementById("fireThornsBtn").addEventListener("click", () => {
            if (turn !== 0) return;

            playerPokemon.fireThorns();
            logAction(`🌵 ${playerPokemon.getName()} покрывается огненными шипами!`);
            enemy.unImmune();
            nextTurn();
        });
    }

    if (savedPokemon.type === "electric") {
        document.getElementById("thunderboltBtn").addEventListener("click", () => {
            if (turn !== 0) return;

            playerPokemon.thunderbolt(enemy);
            logAction(`⚡ ${playerPokemon.getName()} использует Громовой удар!`);
            updateHealthBars();
            enemy.unImmune();
            nextTurn();
        });

        document.getElementById("chargeBtn").addEventListener("click", () => {
            if (turn !== 0) return;

            playerPokemon.ability();
            logAction(`🔋 ${playerPokemon.getName()} заряжает энергию!`);
            nextTurn();
        });
    }
    updateHealthBars(); 
});
