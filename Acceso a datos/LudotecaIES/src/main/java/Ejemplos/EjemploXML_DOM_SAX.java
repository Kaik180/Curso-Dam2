package Ejemplos;

import java.io.File;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;
import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import org.xml.sax.Attributes;
import org.xml.sax.helpers.DefaultHandler;

// Ejemplo del PDF: UP1_Ficheros_XML.pdf (Lectura de XML con DOM y con SAX)
public class EjemploXML_DOM_SAX {

    public static void main(String[] args) {
        File archivoXML = new File("libros.xml");

        // --- A. Lectura con DOM (carga el árbol completo en memoria) ---
        System.out.println("=== LECTURA CON DOM ===");
        try {
            Document doc = DocumentBuilderFactory.newInstance()
                    .newDocumentBuilder().parse(archivoXML);
            NodeList titulos = doc.getElementsByTagName("titulo");
            for (int i = 0; i < titulos.getLength(); i++) {
                System.out.println("Título (DOM): " + titulos.item(i).getTextContent());
            }
        } catch (Exception e) {
            System.out.println("Error al leer con DOM: " + e.getMessage());
        }

        // --- B. Lectura con SAX (recorre secuencialmente mediante eventos) ---
        System.out.println("\n=== LECTURA CON SAX ===");
        try {
            SAXParserFactory fabrica = SAXParserFactory.newInstance();
            SAXParser analizador = fabrica.newSAXParser();
            analizador.parse(archivoXML, new ManejadorLibrosSAX());
        } catch (Exception e) {
            System.out.println("Error al leer con SAX: " + e.getMessage());
        }
    }
}

class ManejadorLibrosSAX extends DefaultHandler {
    private StringBuilder contenido = new StringBuilder();

    @Override
    public void startElement(String uri, String localName, String qName, Attributes atributos) {
        contenido.setLength(0);
    }

    @Override
    public void characters(char[] caracteres, int inicio, int longitud) {
        contenido.append(caracteres, inicio, longitud);
    }

    @Override
    public void endElement(String uri, String localName, String qName) {
        if (qName.equals("titulo")) {
            System.out.println("Título: " + contenido.toString().trim());
        } else if (qName.equals("autor")) {
            System.out.println("Autor: " + contenido.toString().trim());
        } else if (qName.equals("libro")) {
            System.out.println("--------------------");
        }
        contenido.setLength(0);
    }
}
