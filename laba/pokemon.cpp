#include <emscripten/bind.h>
#include <string>

using namespace emscripten;

class Pokemon {
protected:
    std::string name;
    int health;
    int damage;
    bool immune_next_turn = false;
    int damage_reduction = 0;
    int counter_damage = 0;
    Pokemon* last_attacker = nullptr;

public:
    Pokemon(const std::string& name, int health, int damage) : name(name), health(health), damage(damage) {}

    virtual ~Pokemon() {}

    //всякие сеттеры геттеры
    void set_name(const std::string& new_name) {
        name = new_name;
    }

    std::string get_name() const {
        return name;
    }
    void set_health(int new_health) {
        health = (new_health > 0) ? new_health : 0;
    }
    
    void set_damage(int new_damage) {
        damage = (new_damage >= 0) ? new_damage : 0;
    }
    
    int get_health() const {
        return health;
    }

    int get_damage() const {
        return damage;
    }

    void unImmune(){
        immune_next_turn = false;
        damage_reduction = 0;
    }

    virtual void attack(Pokemon& target) {
        target.last_attacker = this;
        target.take_damage(damage);
    }

    virtual void defend() {
       
    }

    virtual void evolve() {
    }

    virtual void ability() {
    }

    void take_damage(int dmg) {
        if (immune_next_turn) {
            immune_next_turn = false; // блокирование
            return;
        }
    
        dmg -= damage_reduction;
    
        if (dmg > 0) {
            health -= dmg;
            if (health < 0) health = 0;
            //контр атака
            if (counter_damage > 0 && last_attacker) {
                last_attacker->take_damage(counter_damage);
                counter_damage = 0;
            }
        }
    }
    

};

class WaterPokemon : public Pokemon {
private:
    int water_resistance = 0;
    int water_power = 0;

public:
    WaterPokemon(const std::string& name, int health, int damage) : Pokemon(name, health, damage) {}

    void set_water_resistance(int resistance) {
        water_resistance = (resistance >= 0) ? resistance : 0;
    }

    int get_water_resistance() const {
        return water_resistance;
    }

    void set_water_power(int power) {
        water_power = (power >= 0) ? power : 0;
    }

    int get_water_power() const {
        return water_power;
    }

    void ability() override {
        health += 50;  // Уникальная способность реген
    }

    void water_hide(){
        immune_next_turn = true; 
    }

    void wave_attack(Pokemon& target) {
        target.take_damage(water_power + 10); // Водная атака
    }

    void evolve() override {
        health *= 2;  // Удваиваем здоровье при эволюции
    }

    void defend() override {
        damage_reduction = water_resistance / 2; 
    }

};

class FirePokemon : public Pokemon {
private:
    int fire_resistance = 0;
    int fire_power = 0;

public:
    FirePokemon(const std::string& name, int health, int damage) : Pokemon(name, health, damage) {}

    void set_fire_resistance(int resistance) {
        fire_resistance = (resistance >= 0) ? resistance : 0;
    }

    int get_fire_resistance() const {
        return fire_resistance;
    }

    void set_fire_power(int power) {
        fire_power = (power >= 0) ? power : 0;
    }

    int get_fire_power() const {
        return fire_power;
    }

    void ability() override {
        damage += 5;
    }

    void fire_ball (Pokemon& target) {
        target.take_damage(fire_power + 20); // Огненный шар
    }

    void fire_thorns(){
        counter_damage = fire_resistance / 4;
    }

    void evolve() override {
        damage = static_cast<int>(damage * 1.5); // Увеличиваем урон в 1.5 раза
    }

    void defend() override {
        damage_reduction = fire_resistance / 3; 
    }

};

class ElectricPokemon : public Pokemon {
    private:
        int electric_charge = 0;  // Заряд электричества
        int electric_power = 0;   // Сила электрической атаки
    
    public:
        ElectricPokemon(const std::string& name, int health, int damage) 
            : Pokemon(name, health, damage) {}
    
        void set_electric_charge(int charge) {
            electric_charge = (charge >= 0) ? charge : 0;
        }
    
        int get_electric_charge() const {
            return electric_charge;
        }
    
        void set_electric_power(int power) {
            electric_power = (power >= 0) ? power : 0;
        }
    
        int get_electric_power() const {
            return electric_power;
        }
    
        void ability() override {
            electric_charge += 10; // Копим заряд
        }
    
        void thunderbolt(Pokemon& target) {
            target.take_damage(electric_power + electric_charge);
            electric_charge = 0; // После атаки заряд тратится
        }
    
        void evolve() override {
            electric_power += 40; // Увеличиваем стихийный урон при эволюции
            health += 100;
        }
    
        void defend() override {
            damage_reduction = electric_charge / 2; 
        }
    };
    

// Привязка классов к JavaScript
EMSCRIPTEN_BINDINGS(pokemon) {
    class_<Pokemon>("Pokemon")
        .constructor<std::string, int, int>()
        .function("setName", &Pokemon::set_name)
        .function("getName", &Pokemon::get_name)
        .function("getHealth", &Pokemon::get_health)
        .function("getDamage", &Pokemon::get_damage)
        .function("setHealth", &Pokemon::set_health)  
        .function("setDamage", &Pokemon::set_damage)  
        .function("attack", &Pokemon::attack)
        .function("defend", &Pokemon::defend)
        .function("evolve", &Pokemon::evolve)
        .function("unImmune", &Pokemon::unImmune)
        .function("ability", &Pokemon::ability);

    class_<WaterPokemon, base<Pokemon>>("WaterPokemon")
        .constructor<std::string, int, int>()
        .function("waveAttack", &WaterPokemon::wave_attack)
        .function("setWaterResistance", &WaterPokemon::set_water_resistance)
        .function("getWaterResistance", &WaterPokemon::get_water_resistance)
        .function("setWaterPower", &WaterPokemon::set_water_power)
        .function("getWaterPower", &WaterPokemon::get_water_power)
        .function("evolve", &WaterPokemon::evolve)
        .function("waterHide", &WaterPokemon::water_hide)
        .function("defend", &WaterPokemon::defend);

    class_<FirePokemon, base<Pokemon>>("FirePokemon")
        .constructor<std::string, int, int>()
        .function("fireBall", &FirePokemon::fire_ball)
        .function("setFireResistance", &FirePokemon::set_fire_resistance)
        .function("getFireResistance", &FirePokemon::get_fire_resistance)
        .function("setFirePower", &FirePokemon::set_fire_power)
        .function("getFirePower", &FirePokemon::get_fire_power)
        .function("fireThorns", &FirePokemon::fire_thorns)
        .function("evolve", &FirePokemon::evolve)
        .function("defend", &FirePokemon::defend);

    class_<ElectricPokemon, base<Pokemon>>("ElectricPokemon")
        .constructor<std::string, int, int>()
        .function("setElectricCharge", &ElectricPokemon::set_electric_charge)
        .function("getElectricCharge", &ElectricPokemon::get_electric_charge)
        .function("setElectricPower", &ElectricPokemon::set_electric_power)
        .function("getElectricPower", &ElectricPokemon::get_electric_power)
        .function("thunderbolt", &ElectricPokemon::thunderbolt)
        .function("evolve", &ElectricPokemon::evolve)
        .function("defend", &ElectricPokemon::defend);
    
}
