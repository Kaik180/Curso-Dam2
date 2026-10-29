class ServiceItem {
  final String name;
  final String price;
  final String duration;
  final String description;

  const ServiceItem({
    required this.name,
    required this.price,
    required this.duration,
    required this.description,
  });
}

class BusinessLead {
  final String id;
  final String name;
  final String category;
  final String address;
  final String phone;
  final String contactPerson;
  final int healthScore;
  final bool hasWeb;
  final bool hasBooking;
  final double rating;
  final int reviewsCount;
  final String headline;
  final String heroTag;
  final int primaryColorValue;
  final List<ServiceItem> services;

  const BusinessLead({
    required this.id,
    required this.name,
    required this.category,
    required this.address,
    required this.phone,
    required this.contactPerson,
    required this.healthScore,
    required this.hasWeb,
    required this.hasBooking,
    required this.rating,
    required this.reviewsCount,
    required this.headline,
    required this.heroTag,
    required this.primaryColorValue,
    required this.services,
  });

  int get digitalHealthScore => healthScore;

  static List<BusinessLead> get sampleLeads => getSampleLeads();

  static List<BusinessLead> getSampleLeads() {
    return [
      const BusinessLead(
        id: 'barberia_clasica',
        name: 'Barbería Clásica',
        category: 'Peluquería y Barbería',
        address: 'C. Mayor, 14 - Albacete',
        phone: '+34 612 345 678',
        contactPerson: 'Carlos Méndez',
        healthScore: 45,
        hasWeb: false,
        hasBooking: false,
        rating: 4.7,
        reviewsCount: 86,
        headline: 'Tu estilo. Nuestro oficio.',
        heroTag: 'El arte del buen corte tradicional',
        primaryColorValue: 0xFFA67C52, // Tono cuero / madera
        services: [
          ServiceItem(
            name: 'Corte Clásico a Tijera',
            price: '18 €',
            duration: '30 min',
            description: 'Lavado, corte personalizado y peinado.',
          ),
          ServiceItem(
            name: 'Arreglo de Barba Tradicional',
            price: '12 €',
            duration: '20 min',
            description: 'Toalla caliente y perfilado a navaja clásica.',
          ),
          ServiceItem(
            name: 'Experiencia Completa (Corte + Barba)',
            price: '27 €',
            duration: '45 min',
            description: 'Sesión integral de cuidado y acabado premium.',
          ),
        ],
      ),
      const BusinessLead(
        id: 'taller_gomez',
        name: 'Taller Hermanos Gómez',
        category: 'Mecánica Rápida y Neumáticos',
        address: 'C. Rosario, 48 - Albacete',
        phone: '+34 620 987 654',
        contactPerson: 'Javier Gómez',
        healthScore: 38,
        hasWeb: false,
        hasBooking: false,
        rating: 4.5,
        reviewsCount: 42,
        headline: 'Tu coche en las mejores manos.',
        heroTag: 'Mecánica de confianza en tu barrio',
        primaryColorValue: 0xFF0D6EFD,
        services: [
          ServiceItem(
            name: 'Revisión Pre-ITV Completa',
            price: '45 €',
            duration: '60 min',
            description: 'Chequeo de 40 puntos de seguridad.',
          ),
          ServiceItem(
            name: 'Cambio de Aceite y Filtros',
            price: '65 €',
            duration: '45 min',
            description: 'Aceite sintético y filtros de calidad.',
          ),
        ],
      ),
      const BusinessLead(
        id: 'clinica_sol',
        name: 'Clínica Fisioterapia Sol',
        category: 'Salud y Fisioterapia',
        address: 'Paseo de la Libertad, 8 - Albacete',
        phone: '+34 633 456 789',
        contactPerson: 'Dra. Marta Soler',
        healthScore: 52,
        hasWeb: false,
        hasBooking: false,
        rating: 4.9,
        reviewsCount: 110,
        headline: 'Recupera tu bienestar y vitalidad.',
        heroTag: 'Fisioterapia y osteopatía avanzada',
        primaryColorValue: 0xFF00B496,
        services: [
          ServiceItem(
            name: 'Sesión de Fisioterapia Manual',
            price: '40 €',
            duration: '50 min',
            description: 'Tratamiento de contracturas y lesiones.',
          ),
          ServiceItem(
            name: 'Masaje Descontracturante Profundo',
            price: '35 €',
            duration: '45 min',
            description: 'Alivio de sobrecarga cervical y lumbar.',
          ),
        ],
      ),
    ];
  }
}
