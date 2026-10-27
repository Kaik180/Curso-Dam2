package TF7;

import java.util.List;

public class EquipoDocente {
    private String equipo;
    private String instituto;
    private List<Profesor> profesores;

    public EquipoDocente() {
    }

    public EquipoDocente(String equipo, String instituto, List<Profesor> profesores) {
        this.equipo = equipo;
        this.instituto = instituto;
        this.profesores = profesores;
    }

    public String getEquipo() {
        return equipo;
    }

    public void setEquipo(String equipo) {
        this.equipo = equipo;
    }

    public String getInstituto() {
        return instituto;
    }

    public void setInstituto(String instituto) {
        this.instituto = instituto;
    }

    public List<Profesor> getProfesores() {
        return profesores;
    }

    public void setProfesores(List<Profesor> profesores) {
        this.profesores = profesores;
    }

    @Override
    public String toString() {
        return "EquipoDocente{" +
                "equipo='" + equipo + '\'' +
                ", instituto='" + instituto + '\'' +
                ", profesores=\n  " + profesores +
                '}';
    }
}
