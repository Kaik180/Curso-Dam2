package tf6;

import java.io.File;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;

public class LeerLibrosDOM {
    public static void main(String[] args) {
        try {
            Document doc = DocumentBuilderFactory.newInstance()
                    .newDocumentBuilder().parse(new File("libros.xml"));

            NodeList libros = doc.getElementsByTagName("libro");

            for (int i = 0; i < libros.getLength(); i++) {
                Element libro = (Element) libros.item(i);

                String id = libro.getAttribute("id");
                String titulo = libro.getElementsByTagName("titulo").item(0).getTextContent();
                String autor = libro.getElementsByTagName("autor").item(0).getTextContent();

                System.out.println("ID: " + id);
                System.out.println("Título: " + titulo);
                System.out.println("Autor: " + autor);
                if (i < libros.getLength() - 1) {
                    System.out.println("------------------------");
                }
            }
        } catch (Exception e) {
            System.out.println("Error al leer el XML: " + e.getMessage());
        }
    }
}
