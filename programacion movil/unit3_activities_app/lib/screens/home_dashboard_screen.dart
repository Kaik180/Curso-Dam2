import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class HomeDashboardScreen extends StatelessWidget {
  const HomeDashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    final activities = [
      _ActivityItem(
        title: '3.1 Contador Extendido & Widgets',
        subtitle: 'Actividad oficial: Botones de incremento (+), decremento (-) y reinicio (0) en Scaffold.',
        icon: Icons.exposure,
        color: Colors.indigo,
        route: '/counter',
        tag: 'Unit 03 - 01',
      ),
      _ActivityItem(
        title: '3.2 FutureBuilder & Pull-to-refresh',
        subtitle: 'Carga asíncrona, RefreshIndicator, gestión de errores y prevención del anti-patrón de rebuild.',
        icon: Icons.sync,
        color: Colors.teal,
        route: '/future-builder',
        tag: 'Unit 03 - 02',
      ),
      _ActivityItem(
        title: '3.3 Formularios & Retorno Asíncrono',
        subtitle: 'Validación con FormState, paso de parámetros entre pantallas y captura con Navigator.pop().',
        icon: Icons.input_rounded,
        color: Colors.blueAccent,
        route: '/navigation-form',
        tag: 'Unit 03 - 03',
      ),
      _ActivityItem(
        title: '3.4 Nav Widgets, Tabs & Diálogos',
        subtitle: 'NavigationBar, NavigationRail responsive, Drawer, pestañas y diálogos interactivos (Alert, Simple, Dialog).',
        icon: Icons.dashboard_rounded,
        color: Colors.orange.shade800,
        route: '/nav-widgets',
        tag: 'Unit 03 - 04',
      ),
      _ActivityItem(
        title: '3.5 GoRouter & Hero Animations',
        subtitle: 'Rutas declarativas, parámetros dinámicos y animaciones de transición compartida (Hero).',
        icon: Icons.auto_awesome,
        color: Colors.purple,
        route: '/gorouter-hero',
        tag: 'Unit 03 - 05',
      ),
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text('PMDM DAM2 • Prácticas Unit 3'),
        elevation: 0,
        centerTitle: false,
        actions: [
          IconButton(
            icon: const Icon(Icons.help_outline),
            tooltip: 'Acerca del proyecto',
            onPressed: () => _showAboutAppDialog(context),
          ),
        ],
      ),
      body: CustomScrollView(
        slivers: [
          SliverToBoxAdapter(
            child: Container(
              margin: const EdgeInsets.all(16),
              padding: const EdgeInsets.all(24),
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  colors: [
                    theme.colorScheme.primary,
                    theme.colorScheme.tertiary,
                  ],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
                borderRadius: BorderRadius.circular(20),
                boxShadow: [
                  BoxShadow(
                    color: theme.colorScheme.primary.withValues(alpha: 0.3),
                    blurRadius: 12,
                    offset: const Offset(0, 4),
                  ),
                ],
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Container(
                        padding: const EdgeInsets.all(10),
                        decoration: BoxDecoration(
                          color: Colors.white.withValues(alpha: 0.2),
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: const Icon(
                          Icons.flutter_dash,
                          color: Colors.white,
                          size: 32,
                        ),
                      ),
                      const SizedBox(width: 14),
                      const Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'Unidad 3: Interfaces & Navegación',
                              style: TextStyle(
                                color: Colors.white,
                                fontSize: 18,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            SizedBox(height: 4),
                            Text(
                              'Programación Móvil (DAM2)',
                              style: TextStyle(
                                color: Colors.white70,
                                fontSize: 13,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  const Text(
                    'Proyecto integrador que compila todas las actividades prácticas, conceptos de estado, FutureBuilder, navegación y widgets de la Unidad 3 del temario oficial.',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 14,
                      height: 1.4,
                    ),
                  ),
                ],
              ),
            ),
          ),
          SliverPadding(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            sliver: SliverList(
              delegate: SliverChildBuilderDelegate(
                (context, index) {
                  final act = activities[index];
                  return Card(
                    margin: const EdgeInsets.only(bottom: 14),
                    elevation: 1.5,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(16),
                      side: BorderSide(
                        color: theme.colorScheme.outlineVariant.withValues(alpha: 0.6),
                      ),
                    ),
                    child: InkWell(
                      borderRadius: BorderRadius.circular(16),
                      onTap: () => context.push(act.route),
                      child: Padding(
                        padding: const EdgeInsets.all(16),
                        child: Row(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Container(
                              padding: const EdgeInsets.all(12),
                              decoration: BoxDecoration(
                                color: act.color.withValues(alpha: 0.12),
                                borderRadius: BorderRadius.circular(12),
                              ),
                              child: Icon(act.icon, color: act.color, size: 28),
                            ),
                            const SizedBox(width: 16),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Row(
                                    children: [
                                      Container(
                                        padding: const EdgeInsets.symmetric(
                                          horizontal: 8,
                                          vertical: 2,
                                        ),
                                        decoration: BoxDecoration(
                                          color: act.color.withValues(alpha: 0.1),
                                          borderRadius: BorderRadius.circular(6),
                                        ),
                                        child: Text(
                                          act.tag,
                                          style: TextStyle(
                                            color: act.color,
                                            fontWeight: FontWeight.bold,
                                            fontSize: 11,
                                          ),
                                        ),
                                      ),
                                    ],
                                  ),
                                  const SizedBox(height: 6),
                                  Text(
                                    act.title,
                                    style: theme.textTheme.titleMedium?.copyWith(
                                      fontWeight: FontWeight.bold,
                                    ),
                                  ),
                                  const SizedBox(height: 4),
                                  Text(
                                    act.subtitle,
                                    style: theme.textTheme.bodyMedium?.copyWith(
                                      color: theme.colorScheme.onSurfaceVariant,
                                    ),
                                  ),
                                ],
                              ),
                            ),
                            const SizedBox(width: 8),
                            Icon(
                              Icons.arrow_forward_ios_rounded,
                              size: 16,
                              color: theme.colorScheme.outline,
                            ),
                          ],
                        ),
                      ),
                    ),
                  );
                },
                childCount: activities.length,
              ),
            ),
          ),
          const SliverToBoxAdapter(child: SizedBox(height: 24)),
        ],
      ),
    );
  }

  void _showAboutAppDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Proyecto Unit 3 PMDM'),
        content: const Text(
          'Este proyecto contiene la resolución completa y documentada de todas las actividades de la Unidad 3:\n\n'
          '• 3.1 Contador con botones extra (+, -, reset) y Scaffold con floatingActionButton.\n'
          '• 3.2 FutureBuilder seguro con RefreshIndicator.\n'
          '• 3.3 Formulario con validación y retorno de datos.\n'
          '• 3.4 Catálogo de NavigationBar, NavigationRail, Tabs y Diálogos.\n'
          '• 3.5 Navegación declarativa con GoRouter y animación Hero.\n\n'
          'Desarrollado para la asignatura de Programación Móvil (DAM2).',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cerrar'),
          ),
        ],
      ),
    );
  }
}

class _ActivityItem {
  final String title;
  final String subtitle;
  final IconData icon;
  final Color color;
  final String route;
  final String tag;

  const _ActivityItem({
    required this.title,
    required this.subtitle,
    required this.icon,
    required this.color,
    required this.route,
    required this.tag,
  });
}
