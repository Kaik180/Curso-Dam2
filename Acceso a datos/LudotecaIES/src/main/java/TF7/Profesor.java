package TF7;

import java.util.List;

public class Profesor {
    private String nombre;
    private List<Integer> cursos;
    private List<String> modulos;

    public Profesor() {
    }

    public Profesor(String nombre, List<Integer> cursos, List<String> modulos) {
        this.nombre = nombre;
        this.cursos = cursos;
        this.modulos = modulos;
    }

    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public List<Integer> getCursos() {
        return cursos;
    }

    public void setCursos(List<Integer> cursos) {
        this.cursos = cursos;
    }

    public List<String> getModulos() {
        return modulos;
    }

    public void setModulos(List<String> modulos) {
        this.modulos = modulos;
    }

    @Override
    public String toString() {
        return "Profesor{" +
                "nombre='" + nombre + '\'' +
                ", cursos=" + cursos +
                ", modulos=" + modulos +
                '}';
    }
}
