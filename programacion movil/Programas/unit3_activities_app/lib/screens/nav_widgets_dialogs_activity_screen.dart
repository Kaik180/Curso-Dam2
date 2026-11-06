import 'package:flutter/material.dart';

/// Unidad 3 - Apartado 04: Widgets de Navegación (NavigationBar, Rail, Drawer, Tabs) y Diálogos
class NavWidgetsDialogsActivityScreen extends StatefulWidget {
  const NavWidgetsDialogsActivityScreen({super.key});

  @override
  State<NavWidgetsDialogsActivityScreen> createState() =>
      _NavWidgetsDialogsActivityScreenState();
}

class _NavWidgetsDialogsActivityScreenState
    extends State<NavWidgetsDialogsActivityScreen> {
  int _navIndex = 0;

  // Diálogo 1: AlertDialog estándar de confirmación
  Future<void> _showAlertDialog(BuildContext context) async {
    final messenger = ScaffoldMessenger.of(context);
    final result = await showDialog<bool>(
      context: context,
      barrierDismissible: false,
      builder: (BuildContext dialogContext) {
        return AlertDialog(
          icon: const Icon(Icons.warning_amber_rounded, size: 36),
          title: const Text('Confirmar Eliminación'),
          content: const Text(
            '¿Estás seguro de que deseas eliminar este registro? Esta acción no se puede deshacer.',
          ),
          actions: <Widget>[
            TextButton(
              onPressed: () => Navigator.pop(dialogContext, false),
              child: const Text('Cancelar'),
            ),
            FilledButton(
              style: FilledButton.styleFrom(
                backgroundColor: Colors.red.shade700,
              ),
              onPressed: () => Navigator.pop(dialogContext, true),
              child: const Text('Eliminar Definitivamente'),
            ),
          ],
        );
      },
    );

    if (result != null && mounted) {
      messenger.showSnackBar(
        SnackBar(
          content: Text(
            result
                ? 'Acción confirmada: Registro eliminado.'
                : 'Acción cancelada por el usuario.',
          ),
          backgroundColor: result ? Colors.red.shade800 : Colors.grey.shade800,
          behavior: SnackBarBehavior.floating,
        ),
      );
    }
  }

  // Diálogo 2: SimpleDialog con selección entre múltiples opciones
  Future<void> _showSimpleDialog(BuildContext context) async {
    final messenger = ScaffoldMessenger.of(context);
    final option = await showDialog<String>(
      context: context,
      builder: (BuildContext dialogContext) {
        return SimpleDialog(
          title: const Text('Seleccionar Perfil de Usuario'),
          children: <Widget>[
            SimpleDialogOption(
              onPressed: () => Navigator.pop(dialogContext, 'Administrador'),
              child: const Row(
                children: [
                  Icon(Icons.admin_panel_settings, color: Colors.blue),
                  SizedBox(width: 12),
                  Text('Administrador del Sistema'),
                ],
              ),
            ),
            SimpleDialogOption(
              onPressed: () => Navigator.pop(dialogContext, 'Desarrollador Flutter'),
              child: const Row(
                children: [
                  Icon(Icons.developer_mode, color: Colors.teal),
                  SizedBox(width: 12),
                  Text('Desarrollador Flutter (DAM2)'),
                ],
              ),
            ),
            SimpleDialogOption(
              onPressed: () => Navigator.pop(dialogContext, 'Invitado'),
              child: const Row(
                children: [
                  Icon(Icons.person_outline, color: Colors.grey),
                  SizedBox(width: 12),
                  Text('Invitado / Visitante'),
                ],
              ),
            ),
          ],
        );
      },
    );

    if (option != null && mounted) {
      messenger.showSnackBar(
        SnackBar(
          content: Text('Has seleccionado el rol: $option'),
          backgroundColor: Colors.teal.shade800,
          behavior: SnackBarBehavior.floating,
        ),
      );
    }
  }

  // Diálogo 3: Diálogo personalizado con Dialog
  Future<void> _showCustomDialog(BuildContext context) async {
    final controller = TextEditingController();
    await showDialog(
      context: context,
      builder: (BuildContext dialogContext) {
        return Dialog(
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
          child: Padding(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const Row(
                  children: [
                    Icon(Icons.edit_note_rounded, size: 28, color: Colors.indigo),
                    SizedBox(width: 8),
                    Text(
                      'Nuevo Apunte Rápido',
                      style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                  ],
                ),
                const SizedBox(height: 16),
                TextField(
                  controller: controller,
                  decoration: const InputDecoration(
                    labelText: 'Título del apunte',
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 20),
                Row(
                  mainAxisAlignment: MainAxisAlignment.end,
                  children: [
                    TextButton(
                      onPressed: () => Navigator.pop(dialogContext),
                      child: const Text('Cerrar'),
                    ),
                    const SizedBox(width: 8),
                    FilledButton(
                      onPressed: () {
                        final text = controller.text;
                        Navigator.pop(dialogContext);
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(
                            content: Text('Apunte guardado: "$text"'),
                            behavior: SnackBarBehavior.floating,
                          ),
                        );
                      },
                      child: const Text('Guardar'),
                    ),
                  ],
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isWideScreen = MediaQuery.of(context).size.width >= 700;

    // Vistas principales según el índice de navegación seleccionado
    final views = [
      // Vista 1: Demostración de Diálogos Material 3
      _buildDialogsDemo(context, theme),

      // Vista 2: Demostración de Pestañas (TabBar y TabBarView)
      _buildTabsDemo(context, theme),

      // Vista 3: Demostración de Información de Arquitectura
      _buildArchitectureNotes(context, theme),
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text('Actividad 3.4: Nav Widgets & Dialogs'),
      ),
      drawer: NavigationDrawer(
        selectedIndex: _navIndex,
        onDestinationSelected: (index) {
          setState(() {
            _navIndex = index;
          });
          Navigator.pop(context); // Cierra el Drawer
        },
        children: const [
          Padding(
            padding: EdgeInsets.fromLTRB(28, 20, 16, 10),
            child: Text(
              'Menú Lateral (NavigationDrawer)',
              style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
            ),
          ),
          NavigationDrawerDestination(
            icon: Icon(Icons.forum_outlined),
            selectedIcon: Icon(Icons.forum),
            label: Text('Diálogos Interactivos'),
          ),
          NavigationDrawerDestination(
            icon: Icon(Icons.tab_outlined),
            selectedIcon: Icon(Icons.tab),
            label: Text('Pestañas (Tabs)'),
          ),
          NavigationDrawerDestination(
            icon: Icon(Icons.info_outline),
            selectedIcon: Icon(Icons.info),
            label: Text('Guía de Componentes'),
          ),
        ],
      ),
      body: isWideScreen
          ? Row(
              children: [
                NavigationRail(
                  selectedIndex: _navIndex,
                  onDestinationSelected: (int index) {
                    setState(() {
                      _navIndex = index;
                    });
                  },
                  labelType: NavigationRailLabelType.all,
                  destinations: const [
                    NavigationRailDestination(
                      icon: Icon(Icons.forum_outlined),
                      selectedIcon: Icon(Icons.forum),
                      label: Text('Diálogos'),
                    ),
                    NavigationRailDestination(
                      icon: Icon(Icons.tab_outlined),
                      selectedIcon: Icon(Icons.tab),
                      label: Text('Pestañas'),
                    ),
                    NavigationRailDestination(
                      icon: Icon(Icons.info_outline),
                      selectedIcon: Icon(Icons.info),
                      label: Text('Info'),
                    ),
                  ],
                ),
                const VerticalDivider(thickness: 1, width: 1),
                Expanded(child: views[_navIndex]),
              ],
            )
          : views[_navIndex],
      bottomNavigationBar: isWideScreen
          ? null
          : NavigationBar(
              selectedIndex: _navIndex,
              onDestinationSelected: (int index) {
                setState(() {
                  _navIndex = index;
                });
              },
              destinations: const [
                NavigationDestination(
                  icon: Icon(Icons.forum_outlined),
                  selectedIcon: Icon(Icons.forum),
                  label: 'Diálogos',
                ),
                NavigationDestination(
                  icon: Icon(Icons.tab_outlined),
                  selectedIcon: Icon(Icons.tab),
                  label: 'Pestañas',
                ),
                NavigationDestination(
                  icon: Icon(Icons.info_outline),
                  selectedIcon: Icon(Icons.info),
                  label: 'Guía',
                ),
              ],
            ),
    );
  }

  Widget _buildDialogsDemo(BuildContext context, ThemeData theme) {
    return ListView(
      padding: const EdgeInsets.all(20),
      children: [
        Card(
          elevation: 1,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
          child: Padding(
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Catálogo de Diálogos Material 3',
                  style: theme.textTheme.titleMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 8),
                const Text(
                  'Prueba los diferentes tipos de ventanas emergentes explicadas en la unidad:',
                ),
                const SizedBox(height: 20),
                ListTile(
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                    side: BorderSide(color: theme.colorScheme.outlineVariant),
                  ),
                  leading: const CircleAvatar(
                    backgroundColor: Colors.amber,
                    child: Icon(Icons.notification_important, color: Colors.black87),
                  ),
                  title: const Text('1. AlertDialog'),
                  subtitle: const Text('Confirmación con acciones y valor booleano'),
                  trailing: const Icon(Icons.chevron_right),
                  onTap: () => _showAlertDialog(context),
                ),
                const SizedBox(height: 12),
                ListTile(
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                    side: BorderSide(color: theme.colorScheme.outlineVariant),
                  ),
                  leading: const CircleAvatar(
                    backgroundColor: Colors.teal,
                    child: Icon(Icons.list_alt, color: Colors.white),
                  ),
                  title: const Text('2. SimpleDialog'),
                  subtitle: const Text('Selección entre opciones con SimpleDialogOption'),
                  trailing: const Icon(Icons.chevron_right),
                  onTap: () => _showSimpleDialog(context),
                ),
                const SizedBox(height: 12),
                ListTile(
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                    side: BorderSide(color: theme.colorScheme.outlineVariant),
                  ),
                  leading: const CircleAvatar(
                    backgroundColor: Colors.indigo,
                    child: Icon(Icons.dashboard_customize, color: Colors.white),
                  ),
                  title: const Text('3. Custom Dialog'),
                  subtitle: const Text('Diseño libre con widget child personalizado'),
                  trailing: const Icon(Icons.chevron_right),
                  onTap: () => _showCustomDialog(context),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildTabsDemo(BuildContext context, ThemeData theme) {
    return DefaultTabController(
      length: 3,
      child: Column(
        children: [
          const TabBar(
            tabs: [
              Tab(icon: Icon(Icons.phone_android), text: 'Móvil'),
              Tab(icon: Icon(Icons.tablet), text: 'Tablet'),
              Tab(icon: Icon(Icons.laptop), text: 'Escritorio'),
            ],
          ),
          Expanded(
            child: TabBarView(
              children: [
                _buildTabContent('Navegación Móvil', 'Se recomienda NavigationBar en la parte inferior con 3 a 5 destinos.', Icons.phone_android, theme),
                _buildTabContent('Navegación Tablet', 'Se recomienda NavigationRail lateral en orientación horizontal.', Icons.tablet, theme),
                _buildTabContent('Navegación Desktop', 'Combinación de NavigationRail o Drawer amplio con atajos de teclado.', Icons.laptop, theme),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildTabContent(String title, String desc, IconData icon, ThemeData theme) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 64, color: theme.colorScheme.primary),
            const SizedBox(height: 16),
            Text(title, style: theme.textTheme.titleLarge?.copyWith(fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            Text(desc, textAlign: TextAlign.center, style: theme.textTheme.bodyMedium),
          ],
        ),
      ),
    );
  }

  Widget _buildArchitectureNotes(BuildContext context, ThemeData theme) {
    return ListView(
      padding: const EdgeInsets.all(20),
      children: [
        Card(
          elevation: 1,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
          child: Padding(
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Resumen Técnico de Componentes (Unit 03 - 04)',
                  style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold),
                ),
                const Divider(height: 24),
                const Text('• NavigationBar: Sustituye al antiguo BottomNavigationBar en Material 3.'),
                const SizedBox(height: 8),
                const Text('• NavigationRail: Optimizado para pantallas anchas (> 640px) y modo apaisado.'),
                const SizedBox(height: 8),
                const Text('• DefaultTabController: Simplifica el control sincronizado de TabBar y TabBarView.'),
                const SizedBox(height: 8),
                const Text('• showDialog: Inserta una ruta modal sobre la pila del Navigator y devuelve un Future con el valor retornado por Navigator.pop().'),
              ],
            ),
          ),
        ),
      ],
    );
  }
}
