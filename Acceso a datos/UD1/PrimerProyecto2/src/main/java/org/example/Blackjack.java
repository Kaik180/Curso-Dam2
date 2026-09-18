package org.example;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Scanner;

public class Blackjack {

    // Representación individual de cada carta
    static class Carta {
        private final String valor;
        private final String palo;

        public Carta(String valor, String palo) {
            this.valor = valor;
            this.palo = palo;
        }

        public int getPuntos() {
            switch (valor) {
                case "A": return 11;
                case "K":
                case "Q":
                case "J":
                case "10": return 10;
                default: return Integer.parseInt(valor);
            }
        }

        public boolean esAs() {
            return "A".equals(valor);
        }

        @Override
        public String toString() {
            return "[" + valor + " de " + palo + "]";
        }
    }

    static class Baraja {
        private final List<Carta> cartas = new ArrayList<>();

        public Baraja() {
            String[] palos = {"Corazones", "Diamantes", "Tréboles", "Picas"};
            String[] valores = {"2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"};

            for (String palo : palos) {
                for (String valor : valores) {
                    cartas.add(new Carta(valor, palo));
                }
            }
            Collections.shuffle(cartas);
        }

        public Carta robar() {
            if (cartas.isEmpty()) {
                throw new IllegalStateException("No quedan cartas en la baraja.");
            }
            return cartas.remove(cartas.size() - 1);
        }
    }

    static class Mano {
        private final List<Carta> cartas = new ArrayList<>();

        public void agregar(Carta carta) {
            cartas.add(carta);
        }

        public int calcularPuntaje() {
            int total = 0;
            int ases = 0;

            for (Carta c : cartas) {
                total += c.getPuntos();
                if (c.esAs()) {
                    ases++;
                }
            }
            while (total > 21 && ases > 0) {
                total -= 10;
                ases--;
            }

            return total;
        }

        public Carta get(int index) {
            return cartas.get(index);
        }

        @Override
        public String toString() {
            return cartas.toString();
        }
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Baraja baraja = new Baraja();

        Mano manoJugador = new Mano();
        Mano manoDealer = new Mano();
        manoJugador.agregar(baraja.robar());
        manoDealer.agregar(baraja.robar());
        manoJugador.agregar(baraja.robar());
        manoDealer.agregar(baraja.robar());

        System.out.println("=== BIENVENIDO AL BLACKJACK ===");
        System.out.println("Carta visible del Crupier: " + manoDealer.get(0));
        System.out.println("Tus cartas: " + manoJugador + " | Total: " + manoJugador.calcularPuntaje());

        while (manoJugador.calcularPuntaje() < 21) {
            System.out.print("\n¿Deseas pedir carta (P) o plantarte (S)? ");
            String decision = scanner.nextLine().trim().toUpperCase();

            if (decision.equals("P")) {
                Carta nueva = baraja.robar();
                manoJugador.agregar(nueva);
                System.out.println("Robaste: " + nueva);
                System.out.println("Tus cartas: " + manoJugador + " | Total: " + manoJugador.calcularPuntaje());
            } else if (decision.equals("S")) {
                break;
            } else {
                System.out.println("Opción no válida. Escribe 'P' para pedir o 'S' para plantarte.");
            }
        }

        int scoreJugador = manoJugador.calcularPuntaje();

        if (scoreJugador > 21) {
            System.out.println("\n¡Te has pasado de 21! Has perdido.");
            scanner.close();
            return;
        }

        System.out.println("\n=== TURNO DEL CRUPIER ===");
        System.out.println("Cartas completas del Crupier: " + manoDealer + " | Total: " + manoDealer.calcularPuntaje());

        while (manoDealer.calcularPuntaje() < 17) {
            Carta nueva = baraja.robar();
            manoDealer.agregar(nueva);
            System.out.println("El Crupier roba: " + nueva);
            System.out.println("Cartas del Crupier: " + manoDealer + " | Total: " + manoDealer.calcularPuntaje());
        }

        int scoreDealer = manoDealer.calcularPuntaje();

        System.out.println("\n=== RESULTADO FINAL ===");
        System.out.println("Puntuación Jugador: " + scoreJugador);
        System.out.println("Puntuación Crupier: " + scoreDealer);

        if (scoreDealer > 21) {
            System.out.println("¡El Crupier se pasó de 21! ¡Ganaste!");
        } else if (scoreJugador > scoreDealer) {
            System.out.println("¡Has ganado la partida!");
        } else if (scoreJugador < scoreDealer) {
            System.out.println("Gana la casa (Crupier).");
        } else {
            System.out.println("¡Empate (Push)! Recuperas tu apuesta.");
        }

        scanner.close();
    }
}
