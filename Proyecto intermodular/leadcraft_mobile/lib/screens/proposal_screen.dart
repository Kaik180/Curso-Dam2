import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../models/business.dart';

class ProposalScreen extends StatefulWidget {
  final BusinessLead business;
  final VoidCallback? onGoToMerchantDashboard;

  const ProposalScreen({
    super.key,
    required this.business,
    this.onGoToMerchantDashboard,
  });

  @override
  State<ProposalScreen> createState() => _ProposalScreenState();
}

class _ProposalScreenState extends State<ProposalScreen> {
  late TextEditingController _pitchController;
  bool _pitchCopied = false;

  @override
  void initState() {
    super.initState();
    _pitchController = TextEditingController(
      text: _generateDefaultPitch(widget.business),
    );
  }

  @override
  void didUpdateWidget(covariant ProposalScreen oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.business.id != widget.business.id) {
      _pitchController.text = _generateDefaultPitch(widget.business);
      _pitchCopied = false;
    }
  }

  @override
  void dispose() {
    _pitchController.dispose();
    super.dispose();
  }

  String _generateDefaultPitch(BusinessLead b) {
    return '¡Hola ${b.contactPerson}! 👋 He visto la excelente reputación de ${b.name} en Google Maps (${b.rating}⭐ con ${b.reviewsCount} reseñas).\n\n'
        'Hemos analizado vuestra presencia digital y vemos una gran oportunidad: actualmente no disponéis de sistema de citas 24/7 ni web propia, por lo que muchos clientes potenciales se pierden fuera del horario comercial.\n\n'
        'Os hemos preparado sin ningún coste una demo funcional con agenda en tiempo real y aviso por WhatsApp:\n'
        '👉 https://leadcraft.app/demo/${b.name.toLowerCase().replaceAll(RegExp(r'[^a-z0-9]'), '-')}\n\n'
        '¿Os gustaría probarla durante 15 días gratis o agendamos una llamada de 5 min?';
  }

  void _copyPitch() {
    Clipboard.setData(ClipboardData(text: _pitchController.text));
    setState(() => _pitchCopied = true);
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Row(
          children: [
            Icon(Icons.check_circle, color: Color(0xFF10B981)),
            SizedBox(width: 8),
            Text('¡Mensaje copiado al portapapeles!'),
          ],
        ),
        backgroundColor: Color(0xFF1E293B),
        duration: Duration(seconds: 2),
      ),
    );
  }

  void _simulateSendWhatsApp() {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(
          'Simulando apertura de WhatsApp Web/App para ${widget.business.phone}...',
        ),
        backgroundColor: const Color(0xFF10B981),
        duration: const Duration(seconds: 3),
        action: SnackBarAction(
          label: 'OK',
          textColor: Colors.white,
          onPressed: () {},
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final b = widget.business;

    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      appBar: AppBar(
        backgroundColor: const Color(0xFF1E293B),
        elevation: 0,
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Propuesta Comercial y Cierre',
              style: TextStyle(
                fontSize: 17,
                fontWeight: FontWeight.bold,
                color: Colors.white,
              ),
            ),
            Text(
              b.name,
              style: const TextStyle(
                fontSize: 12,
                color: Color(0xFF06B6D4),
              ),
            ),
          ],
        ),
        actions: [
          IconButton(
            tooltip: 'Exportar informe PDF',
            icon: const Icon(Icons.picture_as_pdf_outlined, color: Colors.white70),
            onPressed: () {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(
                  content: Text('Generando PDF de propuesta comercial...'),
                  backgroundColor: Color(0xFF3B82F6),
                ),
              );
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Business banner card
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                gradient: const LinearGradient(
                  colors: [Color(0xFF1E293B), Color(0xFF0F2B48)],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: const Color(0xFF334155)),
              ),
              child: Row(
                children: [
                  Container(
                    width: 52,
                    height: 52,
                    decoration: BoxDecoration(
                      color: const Color(0xFF06B6D4).withOpacity(0.15),
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: const Color(0xFF06B6D4).withOpacity(0.4)),
                    ),
                    child: const Icon(Icons.handshake_outlined, color: Color(0xFF06B6D4), size: 28),
                  ),
                  const SizedBox(width: 14),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          b.name,
                          style: const TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                            color: Colors.white,
                          ),
                        ),
                        const SizedBox(height: 3),
                        Text(
                          'Contacto: ${b.contactPerson} • ${b.phone}',
                          style: const TextStyle(fontSize: 12, color: Colors.white70),
                        ),
                        const SizedBox(height: 3),
                        Text(
                          'Puntuación Salud Actual: ${b.digitalHealthScore}% (Oportunidad alta)',
                          style: const TextStyle(
                            fontSize: 11,
                            fontWeight: FontWeight.w600,
                            color: Color(0xFFF59E0B),
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 18),

            // Comparison table: Antes vs Después
            const Text(
              'COMPARATIVA DE VALOR PARA EL CLIENTE',
              style: TextStyle(
                fontSize: 12,
                fontWeight: FontWeight.bold,
                letterSpacing: 1.1,
                color: Color(0xFF94A3B8),
              ),
            ),
            const SizedBox(height: 10),
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Expanded(
                  child: Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: const Color(0xFF1E293B),
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: const Color(0xFFEF4444).withOpacity(0.4)),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Row(
                          children: [
                            Icon(Icons.cancel_outlined, color: Color(0xFFEF4444), size: 16),
                            SizedBox(width: 6),
                            Text(
                              'Sin LeadCraft',
                              style: TextStyle(
                                fontSize: 13,
                                fontWeight: FontWeight.bold,
                                color: Color(0xFFEF4444),
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 10),
                        _comparisonItem(Icons.close, 'Sin web propia ni catálogo digital', false),
                        _comparisonItem(Icons.close, 'Reservas solo por llamada o presencial', false),
                        _comparisonItem(Icons.close, 'Pierde clientes en fines de semana', false),
                        _comparisonItem(Icons.close, 'Sin recordatorios automáticos de cita', false),
                      ],
                    ),
                  ),
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: const Color(0xFF1E293B),
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: const Color(0xFF10B981).withOpacity(0.5)),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Row(
                          children: [
                            Icon(Icons.check_circle_outline, color: Color(0xFF10B981), size: 16),
                            SizedBox(width: 6),
                            Text(
                              'Con LeadCraft AI',
                              style: TextStyle(
                                fontSize: 13,
                                fontWeight: FontWeight.bold,
                                color: Color(0xFF10B981),
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 10),
                        _comparisonItem(Icons.check, 'Web adaptada a móvil con IA en 3 min', true),
                        _comparisonItem(Icons.check, 'Citas online 24/7 sin interrumpir cortes', true),
                        _comparisonItem(Icons.check, 'Notificaciones instantáneas por WhatsApp', true),
                        _comparisonItem(Icons.check, 'Panel de control sencillo para el dueño', true),
                      ],
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 20),

            // Plan & pricing proposal
            Container(
              padding: const EdgeInsets.all(16),
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
                      const Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Propuesta Plan PYME Local',
                            style: TextStyle(
                              fontSize: 15,
                              fontWeight: FontWeight.bold,
                              color: Colors.white,
                            ),
                          ),
                          SizedBox(height: 2),
                          Text(
                            'Servicio todo en uno gestionado',
                            style: TextStyle(fontSize: 11, color: Colors.white60),
                          ),
                        ],
                      ),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                        decoration: BoxDecoration(
                          color: const Color(0xFF10B981).withOpacity(0.15),
                          borderRadius: BorderRadius.circular(20),
                          border: Border.all(color: const Color(0xFF10B981).withOpacity(0.4)),
                        ),
                        child: const Text(
                          '39 € / mes',
                          style: TextStyle(
                            fontSize: 14,
                            fontWeight: FontWeight.bold,
                            color: Color(0xFF10B981),
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                  const Text(
                    'Incluye alojamiento web ultrarrápido, módulo de citas 24/7, soporte por WhatsApp y panel de comerciante para gestionar citas y clientes.',
                    style: TextStyle(fontSize: 12, color: Colors.white70, height: 1.4),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 20),

            // WhatsApp Pitch Box
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text(
                  'GUION DE CONTACTO POR WHATSAPP',
                  style: TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 1.1,
                    color: Color(0xFF94A3B8),
                  ),
                ),
                TextButton.icon(
                  onPressed: _copyPitch,
                  icon: Icon(
                    _pitchCopied ? Icons.check : Icons.copy,
                    size: 15,
                    color: const Color(0xFF06B6D4),
                  ),
                  label: Text(
                    _pitchCopied ? 'Copiado' : 'Copiar',
                    style: const TextStyle(fontSize: 12, color: Color(0xFF06B6D4)),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 6),
            Container(
              decoration: BoxDecoration(
                color: const Color(0xFF1E293B),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: const Color(0xFF334155)),
              ),
              child: TextField(
                controller: _pitchController,
                maxLines: 7,
                style: const TextStyle(fontSize: 13, color: Colors.white, height: 1.4),
                decoration: const InputDecoration(
                  contentPadding: EdgeInsets.all(14),
                  border: InputBorder.none,
                ),
              ),
            ),
            const SizedBox(height: 16),

            // Action Buttons
            SizedBox(
              width: double.infinity,
              height: 48,
              child: ElevatedButton.icon(
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF25D366), // WhatsApp color
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
                onPressed: _simulateSendWhatsApp,
                icon: const Icon(Icons.chat),
                label: const Text(
                  'Enviar propuesta por WhatsApp',
                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14),
                ),
              ),
            ),
            const SizedBox(height: 10),
            if (widget.onGoToMerchantDashboard != null)
              SizedBox(
                width: double.infinity,
                height: 46,
                child: OutlinedButton.icon(
                  style: OutlinedButton.styleFrom(
                    foregroundColor: const Color(0xFF06B6D4),
                    side: const BorderSide(color: Color(0xFF06B6D4)),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  ),
                  onPressed: widget.onGoToMerchantDashboard,
                  icon: const Icon(Icons.storefront_outlined),
                  label: const Text(
                    'Ver Panel de Gestión del Comercio (Cliente)',
                    style: TextStyle(fontWeight: FontWeight.w600, fontSize: 13),
                  ),
                ),
              ),
            const SizedBox(height: 24),
          ],
        ),
      ),
    );
  }

  Widget _comparisonItem(IconData icon, String text, bool positive) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(
            icon,
            size: 14,
            color: positive ? const Color(0xFF10B981) : const Color(0xFFEF4444),
          ),
          const SizedBox(width: 6),
          Expanded(
            child: Text(
              text,
              style: TextStyle(
                fontSize: 11,
                color: positive ? Colors.white : Colors.white60,
                height: 1.3,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
