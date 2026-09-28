package es.iesmutxamel.ludoteca;

import java.util.ArrayList;

public class Catalogo {
    private ArrayList<Videojuego> videojuegos;

    public Catalogo() {
        this.videojuegos = new ArrayList<>();
    }

    public boolean agregarVideojuego(Videojuego videojuego) {
        if (videojuego == null) {
            return false;
        }
        if (buscarPorId(videojuego.getId()) != null) {
            return false;
        }
        return videojuegos.add(videojuego);
    }

    public Videojuego buscarPorId(int id) {
        for (Videojuego v : videojuegos) {
            if (v.getId() == id) {
                return v;
            }
        }
        return null;
    }

    public boolean eliminarPorId(int id) {
        Videojuego v = buscarPorId(id);
        if (v != null) {
            return videojuegos.remove(v);
        }
        return false;
    }

    public int obtenerCantidad() {
        return videojuegos.size();
    }

    public ArrayList<Videojuego> obtenerVideojuegos() {
        return videojuegos;
    }

    public int obtenerTotalUnidades() {
        int total = 0;
        for (Videojuego v : videojuegos) {
            total += v.getStock();
        }
        return total;
    }

    public double obtenerValorTotalStock() {
        double total = 0.0;
        for (Videojuego v : videojuegos) {
            total += v.getPrecio() * v.getStock();
        }
        return total;
    }

    public ArrayList<Videojuego> buscarPorStockMaximo(int stockMaximo) {
        ArrayList<Videojuego> resultado = new ArrayList<>();
        for (Videojuego v : videojuegos) {
            if (v.getStock() <= stockMaximo) {
                resultado.add(v);
            }
        }
        return resultado;
    }
}
