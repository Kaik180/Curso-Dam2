import 'package:flutter/material.dart';
import '../models/business.dart';

class ExploreScreen extends StatefulWidget {
  final BusinessLead selectedLead;
  final Function(BusinessLead) onSelectLead;
  final VoidCallback onStartGeneration;

  const ExploreScreen({
    super.key,
    required this.selectedLead,
    required this.onSelectLead,
    required this.onStartGeneration,
  });

  @override
  State<ExploreScreen> createState() => _ExploreScreenState();
}

class _ExploreScreenState extends State<ExploreScreen> {
  final List<BusinessLead> leads = BusinessLead.getSampleLeads();
  String selectedCategory = 'Peluquerías y Barberías';

  @override
  Widget build(BuildContext context) {
    final b = widget.selectedLead;

    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Header titles
          const Text(
            'Tu próxima oportunidad está cerca',
            style: TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.bold,
              color: Colors.white,
              letterSpacing: -0.3,
            ),
          ),
          const SizedBox(height: 4),
          const Text(
            'Encuentra comercios locales y convierte sus carencias en una propuesta de servicio.',
            style: TextStyle(fontSize: 12, color: Color(0xFF94A3B8)),
          ),
          const SizedBox(height: 12),

          // Search & Filter Box
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: const Color(0xFF0E2038),
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: const Color(0xFF1E3A5F)),
            ),
            child: Column(
              children: [
                // Location Input
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                  decoration: BoxDecoration(
                    color: const Color(0xFF071326),
                    borderRadius: BorderRadius.circular(10),
                    border: Border.all(color: const Color(0xFF1E3A5F).withOpacity(0.5)),
                  ),
                  child: const Row(
                    children: [
                      Text('📍', style: TextStyle(fontSize: 14)),
                      SizedBox(width: 8),
                      Expanded(
                        child: Text(
                          'Madrid, Centro (Malasaña)',
                          style: TextStyle(fontSize: 12, color: Colors.white),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 8),

                // Category & Search Button
                Row(
                  children: [
                    Expanded(
                      child: Container(
                        padding: const EdgeInsets.symmetric(horizontal: 10),
                        decoration: BoxDecoration(
                          color: const Color(0xFF071326),
                          borderRadius: BorderRadius.circular(10),
                          border: Border.all(color: const Color(0xFF1E3A5F).withOpacity(0.5)),
                        ),
                        child: DropdownButtonHideUnderline(
                          child: DropdownButton<String>(
                            value: selectedCategory,
                            dropdownColor: const Color(0xFF0E2038),
                            isExpanded: true,
                            style: const TextStyle(fontSize: 12, color: Colors.white),
                            items: const [
                              DropdownMenuItem(
                                value: 'Peluquerías y Barberías',
                                child: Text('Peluquerías y Barberías (8)'),
                              ),
                              DropdownMenuItem(
                                value: 'Mecánica Rápida y Neumáticos',
                                child: Text('Talleres Mecánicos (4)'),
                              ),
                              DropdownMenuItem(
                                value: 'Salud y Fisioterapia',
                                child: Text('Clínicas y Fisioterapia (5)'),
                              ),
                            ],
                            onChanged: (val) {
                              if (val != null) {
                                setState(() => selectedCategory = val);
                                final match = leads.firstWhere(
                                  (l) => l.category == val,
                                  orElse: () => leads.first,
                                );
                                widget.onSelectLead(match);
                              }
                            },
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(width: 8),
                    ElevatedButton(
                      onPressed: () {},
                      style: ElevatedButton.styleFrom(
                        backgroundColor: const Color(0xFF00D2B4),
                        foregroundColor: const Color(0xFF050B14),
                        elevation: 0,
                        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                      ),
                      child: const Text('Buscar', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
                    ),
                  ],
                ),
                const SizedBox(height: 8),

                // Filter Tags
                SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Row(
                    children: [
                      _buildFilterBadge('✓ Sin web activa', const Color(0xFF00D2B4)),
                      const SizedBox(width: 6),
                      _buildFilterBadge('✓ Sin reservas online', const Color(0xFF00D2B4)),
                      const SizedBox(width: 6),
                      _buildFilterBadge('4.5★+ Google Maps', const Color(0xFF94A3B8)),
                    ],
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 14),

          // Simulated Interactive Map Card
          ClipRRect(
            borderRadius: BorderRadius.circular(16),
            child: Container(
              height: 200,
              width: double.infinity,
              decoration: BoxDecoration(
                color: const Color(0xFF0A1628),
                border: Border.all(color: const Color(0xFF1E3A5F)),
              ),
              child: Stack(
                children: [
                  CustomPaint(
                    size: const Size(double.infinity, 200),
                    painter: _MapGridPainter(),
                  ),

                  // Pin 1: Barbería Clásica
                  Positioned(
                    top: 60,
                    left: 120,
                    child: GestureDetector(
                      onTap: () => widget.onSelectLead(leads[0]),
                      child: _buildMapPin(
                        '✂️',
                        'Barbería Clásica (45%)',
                        b.id == 'barberia_clasica',
                        const Color(0xFF00D2B4),
                      ),
                    ),
                  ),

                  // Pin 2: Taller Hermanos Gómez
                  Positioned(
                    top: 110,
                    left: 40,
                    child: GestureDetector(
                      onTap: () => widget.onSelectLead(leads[1]),
                      child: _buildMapPin(
                        '🔧',
                        'Taller Gómez (38%)',
                        b.id == 'taller_gomez',
                        const Color(0xFF0D6EFD),
                      ),
                    ),
                  ),

                  // Pin 3: Clínica Fisioterapia Sol
                  Positioned(
                    top: 40,
                    right: 40,
                    child: GestureDetector(
                      onTap: () => widget.onSelectLead(leads[2]),
                      child: _buildMapPin(
                        '💆',
                        'Fisioterapia Sol (52%)',
                        b.id == 'clinica_sol',
                        const Color(0xFF00B496),
                      ),
                    ),
                  ),

                  // Floating Counter
                  Positioned(
                    top: 10,
                    left: 10,
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                      decoration: BoxDecoration(
                        color: Colors.black.withOpacity(0.7),
                        borderRadius: BorderRadius.circular(8),
                        border: Border.all(color: Colors.white10),
                      ),
                      child: const Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Icon(Icons.radar, color: Color(0xFF00D2B4), size: 12),
                          SizedBox(width: 4),
                          Text('12 negocios en esta zona', style: TextStyle(color: Colors.white, fontSize: 10)),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 14),

          // Bottom Sheet: Auditoría Express
          Container(
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(
              color: const Color(0xFF0E2038),
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: const Color(0xFF1E3A5F)),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.4),
                  blurRadius: 10,
                  offset: const Offset(0, 4),
                ),
              ],
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            'AUDITORÍA DIGITAL EXPRESS',
                            style: TextStyle(
                              fontSize: 10,
                              fontWeight: FontWeight.bold,
                              color: Color(0xFF00D2B4),
                              letterSpacing: 1.0,
                            ),
                          ),
                          const SizedBox(height: 2),
                          Text(
                            b.name,
                            style: const TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                              color: Colors.white,
                            ),
                          ),
                          Text(
                            '${b.address} · ${b.phone}',
                            style: const TextStyle(fontSize: 11, color: Color(0xFF94A3B8)),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(width: 8),

                    // Health Score Circular Widget
                    Column(
                      children: [
                        Stack(
                          alignment: Alignment.center,
                          children: [
                            SizedBox(
                              width: 50,
                              height: 50,
                              child: CircularProgressIndicator(
                                value: b.healthScore / 100,
                                backgroundColor: const Color(0xFF1E3A5F),
                                valueColor: AlwaysStoppedAnimation<Color>(
                                  b.healthScore < 40 ? Colors.redAccent : Colors.amber,
                                ),
                                strokeWidth: 4,
                              ),
                            ),
                            Text(
                              '${b.healthScore}%',
                              style: const TextStyle(
                                color: Colors.white,
                                fontWeight: FontWeight.bold,
                                fontSize: 12,
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 2),
                        const Text(
                          'Score',
                          style: TextStyle(fontSize: 9, color: Color(0xFF94A3B8)),
                        ),
                      ],
                    ),
                  ],
                ),
                const SizedBox(height: 12),

                // Digital Gaps Grid
                Row(
                  children: [
                    Expanded(child: _buildCheckItem('🌐 Web Propia', 'Ausente', Colors.redAccent)),
                    const SizedBox(width: 8),
                    Expanded(child: _buildCheckItem('📅 Citas Online', 'Ausente', Colors.redAccent)),
                  ],
                ),
                const SizedBox(height: 6),
                Row(
                  children: [
                    Expanded(child: _buildCheckItem('⭐ Reseñas Maps', '${b.rating} (${b.reviewsCount})', const Color(0xFF00D2B4))),
                    const SizedBox(width: 8),
                    Expanded(child: _buildCheckItem('💬 WhatsApp', 'Manual', Colors.amber)),
                  ],
                ),
                const SizedBox(height: 14),

                // Action Button: Generar con IA
                SizedBox(
                  width: double.infinity,
                  height: 44,
                  child: ElevatedButton(
                    onPressed: widget.onStartGeneration,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color(0xFF00D2B4),
                      foregroundColor: const Color(0xFF050B14),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                      elevation: 4,
                    ),
                    child: const Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Text('⚡', style: TextStyle(fontSize: 16)),
                        SizedBox(width: 8),
                        Text(
                          'Generar solución de tienda con IA',
                          style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 4),
                const Center(
                  child: Text(
                    'Crea la web con citas y dossier de venta en 20 segundos',
                    style: TextStyle(fontSize: 10, color: Color(0xFF94A3B8)),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 14),

          // Other Opportunities
          const Text(
            'Otras oportunidades detectadas cerca:',
            style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Colors.white),
          ),
          const SizedBox(height: 6),
          ...leads.where((l) => l.id != b.id).map(
                (other) => GestureDetector(
                  onTap: () => widget.onSelectLead(other),
                  child: Container(
                    margin: const EdgeInsets.only(bottom: 6),
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                    decoration: BoxDecoration(
                      color: const Color(0xFF0E2038),
                      borderRadius: BorderRadius.circular(10),
                      border: Border.all(color: const Color(0xFF1E3A5F).withOpacity(0.5)),
                    ),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(other.name, style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.w600)),
                            Text(other.address, style: const TextStyle(color: Color(0xFF94A3B8), fontSize: 10)),
                          ],
                        ),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                          decoration: BoxDecoration(
                            color: Colors.redAccent.withOpacity(0.15),
                            borderRadius: BorderRadius.circular(6),
                            border: Border.all(color: Colors.redAccent.withOpacity(0.4)),
                          ),
                          child: Text('${other.healthScore}% Score', style: const TextStyle(color: Colors.redAccent, fontSize: 11, fontWeight: FontWeight.bold)),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
        ],
      ),
    );
  }

  Widget _buildFilterBadge(String text, Color color) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: color.withOpacity(0.15),
        borderRadius: BorderRadius.circular(6),
        border: Border.all(color: color.withOpacity(0.4)),
      ),
      child: Text(text, style: TextStyle(color: color, fontSize: 10, fontWeight: FontWeight.w500)),
    );
  }

  Widget _buildCheckItem(String label, String value, Color valueColor) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
      decoration: BoxDecoration(
        color: const Color(0xFF071326),
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: const Color(0xFF1E3A5F).withOpacity(0.5)),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: const TextStyle(color: Color(0xFFCBD5E1), fontSize: 11)),
          Text(value, style: TextStyle(color: valueColor, fontSize: 10, fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }

  Widget _buildMapPin(String emoji, String title, bool isSelected, Color pinColor) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          width: isSelected ? 34 : 26,
          height: isSelected ? 34 : 26,
          decoration: BoxDecoration(
            color: pinColor,
            shape: BoxShape.circle,
            border: Border.all(color: Colors.white, width: 2),
            boxShadow: [
              BoxShadow(color: pinColor.withOpacity(0.5), blurRadius: 8, spreadRadius: 2),
            ],
          ),
          child: Center(
            child: Text(emoji, style: TextStyle(fontSize: isSelected ? 14 : 11)),
          ),
        ),
        if (isSelected)
          Container(
            margin: const EdgeInsets.only(top: 2),
            padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
            decoration: BoxDecoration(
              color: const Color(0xFF050B14).withOpacity(0.9),
              borderRadius: BorderRadius.circular(4),
              border: Border.all(color: pinColor.withOpacity(0.5)),
            ),
            child: Text(
              title,
              style: TextStyle(color: pinColor, fontSize: 9, fontWeight: FontWeight.bold),
            ),
          ),
      ],
    );
  }
}

class _MapGridPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = const Color(0xFF172D4D)
      ..strokeWidth = 10
      ..strokeCap = StrokeCap.round;

    // Major streets
    canvas.drawLine(Offset(0, size.height * 0.3), Offset(size.width, size.height * 0.3), paint);
    canvas.drawLine(Offset(0, size.height * 0.75), Offset(size.width, size.height * 0.75), paint);
    canvas.drawLine(Offset(size.width * 0.35, 0), Offset(size.width * 0.35, size.height), paint);
    canvas.drawLine(Offset(size.width * 0.75, 0), Offset(size.width * 0.75, size.height), paint);

    // Minor streets
    paint.strokeWidth = 4;
    paint.color = const Color(0xFF1E3A5F).withOpacity(0.5);
    canvas.drawLine(Offset(size.width * 0.35, size.height * 0.3), Offset(size.width * 0.75, size.height * 0.75), paint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
