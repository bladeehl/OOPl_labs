package org.example;

import org.hibernate.Session;
import java.util.List;

public class PokemonDAO {
    public static List<Pokemon> getAllPokemons() {
        return DatabaseHelper.returnInTransaction(session ->
                session.createQuery("from Pokemon", Pokemon.class).list());
    }

    public static List<Pokemon> getPokemonsByTrainer(Trainer trainer) {
        return DatabaseHelper.returnInTransaction(session -> {
            Trainer managedTrainer = session.merge(trainer);
            session.refresh(managedTrainer);
            return managedTrainer.getPokemons();
        });
    }

    public static void savePokemon(Pokemon pokemon) {
        DatabaseHelper.doInTransaction(session -> session.persist(pokemon));
    }

    public static void updatePokemon(Pokemon pokemon) {
        DatabaseHelper.doInTransaction(session -> session.merge(pokemon));
    }

    public static void deletePokemon(Pokemon pokemon) {
        DatabaseHelper.doInTransaction(session -> {
            Pokemon managed = session.merge(pokemon);
            session.remove(managed);
        });
    }
}