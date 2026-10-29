enum AppointmentStatus {
  confirmed,
  pending,
  completed,
  cancelled,
}

class Appointment {
  final String id;
  final String clientName;
  final String clientPhone;
  final String serviceName;
  final double price;
  final DateTime dateTime;
  final String timeSlot;
  AppointmentStatus status;

  Appointment({
    required this.id,
    required this.clientName,
    required this.clientPhone,
    required this.serviceName,
    required this.price,
    required this.dateTime,
    required this.timeSlot,
    this.status = AppointmentStatus.confirmed,
  });

  // Backward compatibility getters
  String get time => timeSlot;
  String get date => 'Hoy, ${dateTime.day} Oct';
  bool get isConfirmed => status == AppointmentStatus.confirmed;

  static List<Appointment> get sampleAppointments => getSampleAppointments();

  static List<Appointment> getSampleAppointments() {
    return [
      Appointment(
        id: 'apt-1',
        clientName: 'Marcos Villanueva',
        clientPhone: '+34 654 112 233',
        serviceName: 'Corte Clásico a Tijera',
        price: 18.0,
        dateTime: DateTime.now(),
        timeSlot: '11:30 h',
        status: AppointmentStatus.confirmed,
      ),
      Appointment(
        id: 'apt-2',
        clientName: 'Carlos Ruiz',
        clientPhone: '+34 687 990 112',
        serviceName: 'Experiencia Completa (Corte + Barba)',
        price: 27.0,
        dateTime: DateTime.now(),
        timeSlot: '16:30 h',
        status: AppointmentStatus.confirmed,
      ),
      Appointment(
        id: 'apt-3',
        clientName: 'David Lozano',
        clientPhone: '+34 622 334 455',
        serviceName: 'Arreglo de Barba Tradicional',
        price: 12.0,
        dateTime: DateTime.now(),
        timeSlot: '18:00 h',
        status: AppointmentStatus.pending,
      ),
      Appointment(
        id: 'apt-4',
        clientName: 'Alejandro Morales',
        clientPhone: '+34 699 887 766',
        serviceName: 'Corte Clásico a Tijera',
        price: 18.0,
        dateTime: DateTime.now(),
        timeSlot: '19:15 h',
        status: AppointmentStatus.confirmed,
      ),
    ];
  }
}
