package org.example;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Inheritance(strategy = InheritanceType.JOINED)
@DiscriminatorColumn(name = "type")
@Data
@NoArgsConstructor
@AllArgsConstructor
public abstract class Pokemon {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
    private int health;
    private int damage;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "trainer_id")
    private Trainer trainer;

    @Transient
    private boolean immuneNextTurn;

    @Transient
    private int damageReduction;

    @Transient
    private int counterDamage;

    @Transient
    private Pokemon lastAttacker;

    public abstract void attack(Pokemon target);

    public abstract void defend();

    public abstract void evolve();

    public abstract void ability();

    public void takeDamage(int damage) {
        if (immuneNextTurn) {
            immuneNextTurn = false;
            return;
        }
        int finalDamage = Math.max(0, damage - damageReduction);
        health = Math.max(0, health - finalDamage);
    }

    public void unImmune() {
        immuneNextTurn = false;
    }
}
