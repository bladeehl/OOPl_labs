package org.example;

import jakarta.persistence.*;
import lombok.*;

@Entity
@DiscriminatorValue("Water")
@Data
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(callSuper = true)
public class WaterPokemon extends Pokemon {
    private int waterResistance;
    private int waterPower;

    public WaterPokemon(String name, int health, int damage, int waterResistance, int waterPower) {
        this.setName(name);
        this.setHealth(health);
        this.setDamage(damage);
        this.waterResistance = Math.max(0, waterResistance);
        this.waterPower = Math.max(0, waterPower);
    }

    public void waterHide() {
        setImmuneNextTurn(true);
    }

    public void waveAttack(Pokemon target) {
        target.takeDamage(waterPower + 10);
    }

    @Override
    public void attack(Pokemon target) {
        target.takeDamage(getDamage());
    }

    @Override
    public void defend() {
        setDamage(getDamage() - waterResistance / 3);
    }

    @Override
    public void evolve() {
        setDamage((int) (getDamage() * 1.5));
    }

    @Override
    public void ability() {
        setHealth(getHealth() + waterPower);
    }

    @Override
    public String toString() {
        return String.format("Water | %-10s | HP:%-4d | DMG:%-3d | WaterRes:%-3d | WaterPwr:%-3d",
                getName(), getHealth(), getDamage(), waterResistance, waterPower);
    }
}