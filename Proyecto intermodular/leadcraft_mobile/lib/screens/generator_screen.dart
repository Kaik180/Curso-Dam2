import 'package:flutter/material.dart';
import '../models/business.dart';

class GeneratorScreen extends StatefulWidget {
  final BusinessLead lead;
  final VoidCallback onAdvanceToProposal;

  const GeneratorScreen({
    super.key,
    required this.lead,
    required this.onAdvanceToProposal,
  });

  @override
  State<GeneratorScreen> createState() => _GeneratorScreenState();
}

class _GeneratorScreenState extends State<GeneratorScreen> {
  late String headline;
  String selectedService = 'Corte Clásico a Tijera (18 €)';
  String selectedDate = 'Hoy (29 Oct)';
  String selectedTime = '16:30 h';
  bool isBooked = false;

  @override
  void initState() {
    super.initState();
    headline = widget.lead.headline;
  }

  @override
  Widget build(BuildContext context) {
    final b = widget.lead;
    final brandColor = Color(b.primaryColorValue);

    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Header Status
          Row(
            children: [
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(
                  color: const Color(0xFF00D2B4).withOpacity(0.15),
                  borderRadius: BorderRadius.circular(6),
                  border: Border.all(color: const Color(0xFF00D2B4).withOpacity(0.4)),
                ),
                child: const Text('Gemini 1.5 Pro', style: TextStyle(color: Color(0xFF00D2B4), fontSize: 10, fontWeight: FontWeight.bold)),
              ),
              const SizedBox(width: 8),
              const Text('Redactado en 22 segundos', style: TextStyle(color: Color(0xFF94A3B8), fontSize: 11)),
            ],
          ),
          const SizedBox(height: 6),
          Text(
            'Web y Sistema de Citas: ${b.name}',
            style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white),
          ),
          const Text(
            'Solución lista para presentar al comerciante con reservas en vivo.',
            style: TextStyle(fontSize: 12, color: Color(0xFF94A3B8)),
          ),
          const SizedBox(height: 12),

          // Customization summary bar
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            decoration: BoxDecoration(
              color: const Color(0xFF0E2038),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: const Color(0xFF1E3A5F)),
            ),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Row(
                  children: [
                    Container(width: 14, height: 14, decoration: BoxDecoration(color: brandColor, shape: BoxShape.circle)),
                    const SizedBox(width: 6),
                    const Text('Color de identidad', style: TextStyle(color: Colors.white, fontSize: 11)),
                  ],
                ),
                TextButton(
                  onPressed: () {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('Modo edición rápida activado')),
                    );
                  },
                  child: const Text('✏️ Editar eslogan', style: TextStyle(color: Color(0xFF00D2B4), fontSize: 11)),
                ),
              ],
            ),
          ),
          const SizedBox(height: 12),

          // LIVE WEBSITE PREVIEW CARD
          ClipRRect(
            borderRadius: BorderRadius.circular(16),
            child: Container(
              decoration: BoxDecoration(
                color: const Color(0xFFFAF7F2), // Light website background
                border: Border.all(color: const Color(0xFFCBD5E1), width: 2),
                boxShadow: [
                  BoxShadow(color: Colors.black.withOpacity(0.5), blurRadius: 15, offset: const Offset(0, 8)),
                ],
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  // Fake Browser Bar
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                    color: const Color(0xFFE2E8F0),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          '🔒 ${b.name.toLowerCase().replaceAll(' ', '')}.es',
                          style: const TextStyle(color: Color(0xFF475569), fontSize: 10, fontFamily: 'monospace'),
                        ),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                          decoration: BoxDecoration(
                            color: Colors.teal.shade100,
                            borderRadius: BorderRadius.circular(4),
                          ),
                          child: const Text('Demo Activa', style: TextStyle(color: Color(0xFF0F766E), fontSize: 9, fontWeight: FontWeight.bold)),
                        ),
                      ],
                    ),
                  ),

                  // Website Content
                  Padding(
                    padding: const EdgeInsets.all(14.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        // Site Header
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(b.name.toUpperCase(), style: const TextStyle(color: Color(0xFF1C1917), fontWeight: FontWeight.w900, fontSize: 13, letterSpacing: 0.5)),
                            const Text('Madrid Centro', style: TextStyle(color: Color(0xFF78716C), fontSize: 11)),
                          ],
                        ),
                        const Divider(color: Color(0xFFE7E5E4), height: 16),

                        // Hero
                        Center(
                          child: Column(
                            children: [
                              Text(b.heroTag.toUpperCase(), style: TextStyle(color: brandColor, fontSize: 9, fontWeight: FontWeight.bold, letterSpacing: 1.2)),
                              const SizedBox(height: 2),
                              Text(
                                headline,
                                textAlign: TextAlign.center,
                                style: const TextStyle(color: Color(0xFF1C1917), fontSize: 18, fontWeight: FontWeight.w900, height: 1.1),
                              ),
                              const SizedBox(height: 4),
                              Text(
                                'Cortes con carácter y afeitados a navaja en el corazón de Malasaña. Tu momento de pausa y cuidado.',
                                textAlign: TextAlign.center,
                                style: TextStyle(color: Colors.grey.shade600, fontSize: 11),
                              ),
                            ],
                          ),
                        ),
                        const SizedBox(height: 12),

                        // Banner image placeholder
                        Container(
                          height: 110,
                          width: double.infinity,
                          decoration: BoxDecoration(
                            color: const Color(0xFF292524),
                            borderRadius: BorderRadius.circular(10),
                            gradient: LinearGradient(
                              colors: [brandColor.withOpacity(0.7), const Color(0xFF1C1917)],
                              begin: Alignment.topLeft,
                              end: Alignment.bottomRight,
                            ),
                          ),
                          child: Center(
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                const Text('✂️', style: TextStyle(fontSize: 28)),
                                const SizedBox(height: 4),
                                Text(b.address, style: const TextStyle(color: Colors.white70, fontSize: 10)),
                              ],
                            ),
                          ),
                        ),
                        const SizedBox(height: 14),

                        // Services
                        Text('CARTA DE SERVICIOS', style: TextStyle(color: Colors.grey.shade600, fontSize: 10, fontWeight: FontWeight.bold, letterSpacing: 1)),
                        const SizedBox(height: 6),
                        ...b.services.map(
                          (s) => Container(
                            margin: const EdgeInsets.only(bottom: 6),
                            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
                            decoration: BoxDecoration(
                              color: Colors.white,
                              borderRadius: BorderRadius.circular(8),
                              border: Border.all(color: const Color(0xFFE7E5E4)),
                            ),
                            child: Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(s.name, style: const TextStyle(color: Color(0xFF1C1917), fontWeight: FontWeight.bold, fontSize: 11)),
                                    Text(s.description, style: const TextStyle(color: Color(0xFF78716C), fontSize: 9)),
                                  ],
                                ),
                                Text(s.price, style: TextStyle(color: brandColor, fontWeight: FontWeight.w900, fontSize: 13)),
                              ],
                            ),
                          ),
                        ),
                        const SizedBox(height: 12),

                        // WIDGET INTERACTIVO DE CITAS ONLINE
                        Container(
                          padding: const EdgeInsets.all(12),
                          decoration: BoxDecoration(
                            color: Colors.white,
                            borderRadius: BorderRadius.circular(12),
                            border: Border.all(color: brandColor.withOpacity(0.4), width: 1.5),
                            boxShadow: [
                              BoxShadow(color: brandColor.withOpacity(0.08), blurRadius: 8, offset: const Offset(0, 3)),
                            ],
                          ),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Row(
                                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                children: [
                                  const Row(
                                    children: [
                                      Text('📅', style: TextStyle(fontSize: 14)),
                                      SizedBox(width: 6),
                                      Text('Reservar Cita Online 24/7', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 11, color: Color(0xFF1C1917))),
                                    ],
                                  ),
                                  Container(
                                    padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                                    decoration: BoxDecoration(color: Colors.teal.shade50, borderRadius: BorderRadius.circular(4)),
                                    child: const Text('Instantáneo', style: TextStyle(color: Colors.teal, fontSize: 9, fontWeight: FontWeight.bold)),
                                  ),
                                ],
                              ),
                              const SizedBox(height: 8),

                              // Date & Time pickers
                              Row(
                                children: [
                                  Expanded(
                                    child: Container(
                                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 6),
                                      decoration: BoxDecoration(color: const Color(0xFFF5F5F4), borderRadius: BorderRadius.circular(6)),
                                      child: Text(selectedDate, style: const TextStyle(fontSize: 10, color: Color(0xFF1C1917), fontWeight: FontWeight.w500)),
                                    ),
                                  ),
                                  const SizedBox(width: 6),
                                  Expanded(
                                    child: Container(
                                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 6),
                                      decoration: BoxDecoration(color: const Color(0xFFF5F5F4), borderRadius: BorderRadius.circular(6)),
                                      child: Text(selectedTime, style: const TextStyle(fontSize: 10, color: Color(0xFF1C1917), fontWeight: FontWeight.w500)),
                                    ),
                                  ),
                                ],
                              ),
                              const SizedBox(height: 8),

                              // Book button
                              SizedBox(
                                width: double.infinity,
                                height: 36,
                                child: ElevatedButton(
                                  onPressed: () {
                                    setState(() => isBooked = true);
                                    ScaffoldMessenger.of(context).showSnackBar(
                                      const SnackBar(
                                        backgroundColor: Color(0xFF0F766E),
                                        content: Text('✅ ¡Cita confirmada en la demo! Notificación lista para el dueño.'),
                                      ),
                                    );
                                  },
                                  style: ElevatedButton.styleFrom(
                                    backgroundColor: brandColor,
                                    foregroundColor: Colors.white,
                                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                                    elevation: 0,
                                  ),
                                  child: const Text('Confirmar Cita Ahora →', style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold)),
                                ),
                              ),
                              if (isBooked) ...[
                                const SizedBox(height: 6),
                                const Text(
                                  '✓ Cita registrada en la agenda del comerciante.',
                                  style: TextStyle(color: Colors.teal, fontSize: 9, fontWeight: FontWeight.bold),
                                ),
                              ],
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),

          // Advance to Proposal Button
          SizedBox(
            width: double.infinity,
            height: 46,
            child: ElevatedButton(
              onPressed: widget.onAdvanceToProposal,
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF00D2B4),
                foregroundColor: const Color(0xFF050B14),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                elevation: 4,
              ),
              child: const Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text('🚀', style: TextStyle(fontSize: 16)),
                  SizedBox(width: 8),
                  Text('Preparar Propuesta Comercial y WhatsApp', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
