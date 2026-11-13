package ud2.model;

import java.sql.Timestamp;

public class Incidencia {
    private int id;
    private int softwareCodigo;
    private String descripcion;
    private Timestamp fecha;

    public Incidencia() {
    }

    public Incidencia(int softwareCodigo, String descripcion) {
        this.softwareCodigo = softwareCodigo;
        this.descripcion = descripcion;
    }

    public Incidencia(int id, int softwareCodigo, String descripcion, Timestamp fecha) {
        this.id = id;
        this.softwareCodigo = softwareCodigo;
        this.descripcion = descripcion;
        this.fecha = fecha;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public int getSoftwareCodigo() {
        return softwareCodigo;
    }

    public void setSoftwareCodigo(int softwareCodigo) {
        this.softwareCodigo = softwareCodigo;
    }

    public String getDescripcion() {
        return descripcion;
    }

    public void setDescripcion(String descripcion) {
        this.descripcion = descripcion;
    }

    public Timestamp getFecha() {
        return fecha;
    }

    public void setFecha(Timestamp fecha) {
        this.fecha = fecha;
    }

    @Override
    public String toString() {
        return String.format("Incidencia [ID=%d | SoftwareCódigo=%d | Descripción=%s | Fecha=%s]",
                id, softwareCodigo, descripcion, fecha);
    }
}
