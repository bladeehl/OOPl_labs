package org.example;

import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.Transaction;
import org.hibernate.cfg.Configuration;

import java.util.function.Consumer;
import java.util.function.Function;

public class DatabaseHelper {
    private static final SessionFactory sessionFactory = new Configuration().configure().buildSessionFactory();

    public static void shutdown() {
        sessionFactory.close();
    }

    public static void doInTransaction(Consumer<Session> action) {
        try (Session session = sessionFactory.openSession()) {
            Transaction tx = session.beginTransaction();
            action.accept(session);
            tx.commit();
        }
    }

    public static <T> T returnInTransaction(Function<Session, T> action) {
        try (Session session = sessionFactory.openSession()) {
            Transaction tx = session.beginTransaction();
            T result = action.apply(session);
            tx.commit();
            return result;
        }
    }

    public static <T> T returnNoTransaction(Function<Session, T> action) {
        try (Session session = sessionFactory.openSession()) {
            return action.apply(session);
        }
    }
}
