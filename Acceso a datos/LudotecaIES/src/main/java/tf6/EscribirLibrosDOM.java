package tf6;

import java.io.File;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;

public class EscribirLibrosDOM {
    public static void main(String[] args) {
        try {
            // 1. Crear documento XML vacío
            Document doc = DocumentBuilderFactory.newInstance()
                    .newDocumentBuilder().newDocument();

            // 2. Crear elemento raíz <libros>
            Element libros = doc.createElement("libros");
            doc.appendChild(libros);

            // Primer libro
            Element libro1 = doc.createElement("libro");
            libro1.setAttribute("id", "1");

            Element titulo1 = doc.createElement("titulo");
            titulo1.setTextContent("1984");
            libro1.appendChild(titulo1);

            Element autor1 = doc.createElement("autor");
            autor1.setTextContent("George Orwell");
            libro1.appendChild(autor1);

            Element anio1 = doc.createElement("anio");
            anio1.setTextContent("1949");
            libro1.appendChild(anio1);

            libros.appendChild(libro1);

            // Segundo libro
            Element libro2 = doc.createElement("libro");
            libro2.setAttribute("id", "2");

            Element titulo2 = doc.createElement("titulo");
            titulo2.setTextContent("Cien años de soledad");
            libro2.appendChild(titulo2);

            Element autor2 = doc.createElement("autor");
            autor2.setTextContent("Gabriel García Márquez");
            libro2.appendChild(autor2);

            Element anio2 = doc.createElement("anio");
            anio2.setTextContent("1967");
            libro2.appendChild(anio2);

            libros.appendChild(libro2);

            // 3. Guardar el documento XML en el disco con Transformer
            Transformer transformer = TransformerFactory.newInstance().newTransformer();
            transformer.setOutputProperty(OutputKeys.INDENT, "yes");
            transformer.transform(new DOMSource(doc), new StreamResult(new File("nuevos_libros.xml")));

            System.out.println("Fichero nuevos_libros.xml guardado correctamente.\n");

            // 4. Leer nuevos_libros.xml con DOM y mostrar los libros
            Document docLeido = DocumentBuilderFactory.newInstance()
                    .newDocumentBuilder().parse(new File("nuevos_libros.xml"));
            NodeList listaLibros = docLeido.getElementsByTagName("libro");

            for (int i = 0; i < listaLibros.getLength(); i++) {
                Element libro = (Element) listaLibros.item(i);
                System.out.println("ID: " + libro.getAttribute("id"));
                System.out.println("Título: " + libro.getElementsByTagName("titulo").item(0).getTextContent());
                System.out.println("Autor: " + libro.getElementsByTagName("autor").item(0).getTextContent());
                if (i < listaLibros.getLength() - 1) {
                    System.out.println("------------------------");
                }
            }
        } catch (Exception e) {
            System.out.println("Error con el XML: " + e.getMessage());
        }
    }
}
