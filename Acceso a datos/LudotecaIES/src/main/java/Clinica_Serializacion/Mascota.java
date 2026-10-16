package Clinica_Serializacion;

import java.io.Serial;
import java.io.Serializable;

public class Mascota implements Serializable {
    @Serial
    private static final long serialVersionUID = 1L;

    int id;
    String nombre;
    String specie;
    int edad;
    @Override
    public String toString() {
        return "Mascota{" +
                "id=" + id +
                ", nombre='" + nombre + '\'' +
                ", specie='" + specie + '\'' +
                ", edad=" + edad +
                '}';
    }



    public Mascota(int id, String nombre, String specie, int edad) {
        this.id = id;
        this.nombre = nombre;
        this.specie = specie;
        this.edad = edad;
    }


    public String getSpecie() {
        return specie;
    }

    public void setSpecie(String specie) {
        this.specie = specie;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public int getEdad() {
        return edad;
    }

    public void setEdad(int edad) {
        this.edad = edad;
    }


}
