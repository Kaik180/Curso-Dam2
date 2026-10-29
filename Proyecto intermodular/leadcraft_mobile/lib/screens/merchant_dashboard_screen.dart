import 'package:flutter/material.dart';
import '../models/business.dart';
import '../models/appointment.dart';

class MerchantDashboardScreen extends StatefulWidget {
  final BusinessLead business;

  const MerchantDashboardScreen({
    super.key,
    required this.business,
  });

  @override
  State<MerchantDashboardScreen> createState() => _MerchantDashboardScreenState();
}

class _MerchantDashboardScreenState extends State<MerchantDashboardScreen> {
  late List<Appointment> _appointments;
  bool _autoAccept = true;
  bool _whatsappReminders = true;

  @override
  void initState() {
    super.initState();
    _appointments = List.from(Appointment.sampleAppointments);
  }

  void _addNewAppointmentDialog() {
    final nameController = TextEditingController();
    final phoneController = TextEditingController(text: '+34 600 ');
    String selectedService = widget.business.services.first.name;
    double selectedPrice = double.tryParse(widget.business.services.first.price.replaceAll(RegExp(r'[^0-9.]'), '')) ?? 18.0;
    String selectedTime = '18:00';

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: const Color(0xFF1E293B),
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (ctx) {
        return StatefulBuilder(
          builder: (context, setSheetState) {
            return Padding(
              padding: EdgeInsets.only(
                left: 20,
                right: 20,
                top: 20,
                bottom: MediaQuery.of(context).viewInsets.bottom + 20,
              ),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text(
                        'Añadir Cita Manual',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                          color: Colors.white,
                        ),
                      ),
                      IconButton(
                        icon: const Icon(Icons.close, color: Colors.white60),
                        onPressed: () => Navigator.pop(ctx),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                  TextField(
                    controller: nameController,
                    style: const TextStyle(color: Colors.white),
                    decoration: InputDecoration(
                      labelText: 'Nombre del Cliente',
                      labelStyle: const TextStyle(color: Colors.white70),
                      filled: true,
                      fillColor: const Color(0xFF0F172A),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(10),
                      ),
                    ),
                  ),
                  const SizedBox(height: 12),
                  TextField(
                    controller: phoneController,
                    style: const TextStyle(color: Colors.white),
                    keyboardType: TextInputType.phone,
                    decoration: InputDecoration(
                      labelText: 'Teléfono',
                      labelStyle: const TextStyle(color: Colors.white70),
                      filled: true,
                      fillColor: const Color(0xFF0F172A),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(10),
                      ),
                    ),
                  ),
                  const SizedBox(height: 12),
                  DropdownButtonFormField<String>(
                    value: selectedService,
                    dropdownColor: const Color(0xFF1E293B),
                    style: const TextStyle(color: Colors.white),
                    decoration: InputDecoration(
                      labelText: 'Servicio',
                      labelStyle: const TextStyle(color: Colors.white70),
                      filled: true,
                      fillColor: const Color(0xFF0F172A),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(10),
                      ),
                    ),
                    items: widget.business.services.map((s) {
                      return DropdownMenuItem(
                        value: s.name,
                        child: Text('${s.name} (${s.price})'),
                      );
                    }).toList(),
                    onChanged: (val) {
                      if (val != null) {
                        final found = widget.business.services.firstWhere((s) => s.name == val);
                        setSheetState(() {
                          selectedService = found.name;
                          selectedPrice = double.tryParse(found.price.replaceAll(RegExp(r'[^0-9.]'), '')) ?? 18.0;
                        });
                      }
                    },
                  ),
                  const SizedBox(height: 12),
                  Row(
                    children: [
                      const Icon(Icons.access_time, color: Color(0xFF06B6D4), size: 20),
                      const SizedBox(width: 8),
                      const Text('Hora:', style: TextStyle(color: Colors.white)),
                      const SizedBox(width: 12),
                      ChoiceChip(
                        label: const Text('17:30'),
                        selected: selectedTime == '17:30',
                        onSelected: (s) => setSheetState(() => selectedTime = '17:30'),
                      ),
                      const SizedBox(width: 8),
                      ChoiceChip(
                        label: const Text('18:00'),
                        selected: selectedTime == '18:00',
                        onSelected: (s) => setSheetState(() => selectedTime = '18:00'),
                      ),
                      const SizedBox(width: 8),
                      ChoiceChip(
                        label: const Text('19:00'),
                        selected: selectedTime == '19:00',
                        onSelected: (s) => setSheetState(() => selectedTime = '19:00'),
                      ),
                    ],
                  ),
                  const SizedBox(height: 18),
                  SizedBox(
                    width: double.infinity,
                    height: 48,
                    child: ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: const Color(0xFF06B6D4),
                        foregroundColor: const Color(0xFF0F172A),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                      ),
                      onPressed: () {
                        if (nameController.text.trim().isEmpty) return;
                        setState(() {
                          _appointments.add(
                            Appointment(
                              id: 'apt-${DateTime.now().millisecondsSinceEpoch}',
                              clientName: nameController.text.trim(),
                              clientPhone: phoneController.text.trim(),
                              serviceName: selectedService,
                              price: selectedPrice,
                              dateTime: DateTime.now(),
                              timeSlot: selectedTime,
                              status: AppointmentStatus.confirmed,
                            ),
                          );
                        });
                        Navigator.pop(ctx);
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(
                            content: Text('Cita creada para ${nameController.text.trim()} a las $selectedTime'),
                            backgroundColor: const Color(0xFF10B981),
                          ),
                        );
                      },
                      child: const Text('Guardar Cita en la Agenda', style: TextStyle(fontWeight: FontWeight.bold)),
                    ),
                  ),
                ],
              ),
            );
          },
        );
      },
    );
  }

  void _toggleAppointmentStatus(int index) {
    setState(() {
      final cur = _appointments[index].status;
      if (cur == AppointmentStatus.pending) {
        _appointments[index].status = AppointmentStatus.confirmed;
      } else if (cur == AppointmentStatus.confirmed) {
        _appointments[index].status = AppointmentStatus.completed;
      } else {
        _appointments[index].status = AppointmentStatus.confirmed;
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final b = widget.business;
    final totalEarnings = _appointments.fold<double>(0, (sum, a) => sum + a.price);
    final confirmedCount = _appointments.where((a) => a.status != AppointmentStatus.cancelled).length;

    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      appBar: AppBar(
        backgroundColor: const Color(0xFF1E293B),
        elevation: 0,
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Text(
                  b.name,
                  style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white),
                ),
                const SizedBox(width: 8),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                  decoration: BoxDecoration(
                    color: const Color(0xFF10B981).withOpacity(0.2),
                    borderRadius: BorderRadius.circular(10),
                    border: Border.all(color: const Color(0xFF10B981)),
                  ),
                  child: const Text(
                    'ONLINE',
                    style: TextStyle(color: Color(0xFF10B981), fontSize: 9, fontWeight: FontWeight.bold),
                  ),
                ),
              ],
            ),
            const Text(
              'Panel de Gestión del Comercio',
              style: TextStyle(fontSize: 11, color: Colors.white60),
            ),
          ],
        ),
        actions: [
          IconButton(
            tooltip: 'Añadir cita manual',
            icon: const Icon(Icons.add_circle_outline, color: Color(0xFF06B6D4)),
            onPressed: _addNewAppointmentDialog,
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // KPI Grid
            Row(
              children: [
                Expanded(
                  child: _kpiCard(
                    title: 'Citas Hoy',
                    value: '$confirmedCount',
                    subtitle: '100% capacidad',
                    icon: Icons.calendar_today,
                    iconColor: const Color(0xFF06B6D4),
                  ),
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: _kpiCard(
                    title: 'Facturación Hoy',
                    value: '${totalEarnings.toStringAsFixed(0)} €',
                    subtitle: '+35% vs sin web',
                    icon: Icons.euro,
                    iconColor: const Color(0xFF10B981),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 10),
            Row(
              children: [
                Expanded(
                  child: _kpiCard(
                    title: 'Vía Web 24/7',
                    value: '4 citas',
                    subtitle: 'Generadas anoche',
                    icon: Icons.language,
                    iconColor: const Color(0xFF8B5CF6),
                  ),
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: _kpiCard(
                    title: 'Reseñas 5★',
                    value: '${b.rating} (${b.reviewsCount})',
                    subtitle: 'Google Maps activo',
                    icon: Icons.star,
                    iconColor: const Color(0xFFF59E0B),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 18),

            // Quick automation switches
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
              decoration: BoxDecoration(
                color: const Color(0xFF1E293B),
                borderRadius: BorderRadius.circular(14),
                border: Border.all(color: const Color(0xFF334155)),
              ),
              child: Column(
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Row(
                        children: [
                          Icon(Icons.bolt, color: Color(0xFF06B6D4), size: 18),
                          SizedBox(width: 8),
                          Text(
                            'Aceptar citas automáticas',
                            style: TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.w600),
                          ),
                        ],
                      ),
                      Switch(
                        value: _autoAccept,
                        activeColor: const Color(0xFF06B6D4),
                        onChanged: (v) => setState(() => _autoAccept = v),
                      ),
                    ],
                  ),
                  const Divider(color: Color(0xFF334155), height: 8),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Row(
                        children: [
                          Icon(Icons.chat, color: Color(0xFF10B981), size: 18),
                          SizedBox(width: 8),
                          Text(
                            'Recordatorios WhatsApp automáticos',
                            style: TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.w600),
                          ),
                        ],
                      ),
                      Switch(
                        value: _whatsappReminders,
                        activeColor: const Color(0xFF10B981),
                        onChanged: (v) => setState(() => _whatsappReminders = v),
                      ),
                    ],
                  ),
                ],
              ),
            ),
            const SizedBox(height: 20),

            // Agenda Header
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text(
                  'AGENDA DE CITAS - HOY',
                  style: TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 1.1,
                    color: Color(0xFF94A3B8),
                  ),
                ),
                Text(
                  '${_appointments.length} registradas',
                  style: const TextStyle(fontSize: 12, color: Colors.white60),
                ),
              ],
            ),
            const SizedBox(height: 10),

            // Appointments List
            ListView.separated(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: _appointments.length,
              separatorBuilder: (_, __) => const SizedBox(height: 8),
              itemBuilder: (context, index) {
                final apt = _appointments[index];
                return _appointmentTile(apt, index);
              },
            ),
            const SizedBox(height: 20),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        backgroundColor: const Color(0xFF06B6D4),
        foregroundColor: const Color(0xFF0F172A),
        icon: const Icon(Icons.add),
        label: const Text('Añadir Cita', style: TextStyle(fontWeight: FontWeight.bold)),
        onPressed: _addNewAppointmentDialog,
      ),
    );
  }

  Widget _kpiCard({
    required String title,
    required String value,
    required String subtitle,
    required IconData icon,
    required Color iconColor,
  }) {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: const Color(0xFF1E293B),
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: const Color(0xFF334155)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(title, style: const TextStyle(fontSize: 12, color: Colors.white70)),
              Icon(icon, color: iconColor, size: 18),
            ],
          ),
          const SizedBox(height: 8),
          Text(
            value,
            style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.white),
          ),
          const SizedBox(height: 2),
          Text(
            subtitle,
            style: const TextStyle(fontSize: 10, color: Color(0xFF06B6D4)),
          ),
        ],
      ),
    );
  }

  Widget _appointmentTile(Appointment apt, int index) {
    Color statusColor = const Color(0xFF10B981);
    String statusLabel = 'Confirmada';

    switch (apt.status) {
      case AppointmentStatus.confirmed:
        statusColor = const Color(0xFF10B981);
        statusLabel = 'Confirmada';
        break;
      case AppointmentStatus.pending:
        statusColor = const Color(0xFFF59E0B);
        statusLabel = 'Pendiente';
        break;
      case AppointmentStatus.completed:
        statusColor = const Color(0xFF6B7280);
        statusLabel = 'Completada';
        break;
      case AppointmentStatus.cancelled:
        statusColor = const Color(0xFFEF4444);
        statusLabel = 'Cancelada';
        break;
    }

    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: const Color(0xFF1E293B),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: const Color(0xFF334155)),
      ),
      child: Row(
        children: [
          // Time badge
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
            decoration: BoxDecoration(
              color: const Color(0xFF0F172A),
              borderRadius: BorderRadius.circular(8),
              border: Border.all(color: const Color(0xFF334155)),
            ),
            child: Text(
              apt.timeSlot,
              style: const TextStyle(
                fontWeight: FontWeight.bold,
                fontSize: 13,
                color: Color(0xFF06B6D4),
              ),
            ),
          ),
          const SizedBox(width: 12),
          // Client info
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Flexible(
                      child: Text(
                        apt.clientName,
                        style: const TextStyle(
                          fontSize: 14,
                          fontWeight: FontWeight.bold,
                          color: Colors.white,
                        ),
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                    const SizedBox(width: 6),
                    InkWell(
                      onTap: () => _toggleAppointmentStatus(index),
                      child: Container(
                        padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                        decoration: BoxDecoration(
                          color: statusColor.withOpacity(0.15),
                          borderRadius: BorderRadius.circular(6),
                          border: Border.all(color: statusColor.withOpacity(0.5)),
                        ),
                        child: Text(
                          statusLabel,
                          style: TextStyle(color: statusColor, fontSize: 10, fontWeight: FontWeight.bold),
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 4),
                Text(
                  '${apt.serviceName} • ${apt.price.toStringAsFixed(0)} €',
                  style: const TextStyle(fontSize: 12, color: Colors.white70),
                ),
                Text(
                  apt.clientPhone,
                  style: const TextStyle(fontSize: 10, color: Colors.white54),
                ),
              ],
            ),
          ),
          // Action button
          IconButton(
            icon: const Icon(Icons.phone, color: Color(0xFF10B981), size: 20),
            onPressed: () {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: Text('Llamando a ${apt.clientName} (${apt.clientPhone})...'),
                  backgroundColor: const Color(0xFF1E293B),
                ),
              );
            },
          ),
        ],
      ),
    );
  }
}
