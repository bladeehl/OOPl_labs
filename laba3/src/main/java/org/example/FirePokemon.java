package org.example;

import jakarta.persistence.*;
import lombok.*;

@Entity
@DiscriminatorValue("Fire")
@Data
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(callSuper = true)
public class FirePokemon extends Pokemon {
    private int fireResistance;
    private int firePower;

    public FirePokemon(String name, int health, int damage, int fireResistance, int firePower) {
        this.setName(name);
        this.setHealth(health);
        this.setDamage(damage);
        this.fireResistance = Math.max(0, fireResistance);
        this.firePower = Math.max(0, firePower);
    }
    public void fireBall(Pokemon target) {
        target.takeDamage(firePower + 20);
    }

    public void fireThorns() {
        fireResistance += 20;
    }

    @Override
    public void attack(Pokemon target) {
        target.takeDamage(getDamage());
    }

    @Override
    public void defend() {
        setDamage(getDamage() - fireResistance / 3);
    }

    @Override
    public void evolve() {
        setDamage((int) (getDamage() * 1.5));
    }

    @Override
    public void ability() {
        setDamage(getDamage() + 5);
    }

    @Override
    public String toString() {
        return String.format("Fire | %-10s | HP:%-4d | DMG:%-3d | FireRes:%-3d | FirePwr:%-3d",
                getName(), getHealth(), getDamage(), fireResistance, firePower);
    }
}