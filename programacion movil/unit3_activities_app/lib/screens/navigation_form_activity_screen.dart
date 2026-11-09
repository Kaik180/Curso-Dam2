import 'package:flutter/material.dart';
import 'navigation_detail_screen.dart';

/// Unidad 3 - Apartado 03: Navegación, Formularios y Retorno de Valores
/// Demuestra:
/// - Formularios con validación (`GlobalKey<FormState>`, `TextEditingController`).
/// - Navegación clásica con MaterialPageRoute y espera asíncrona de datos:
///   `final resultado = await Navigator.push(...)`
/// - Actualización del estado local con el resultado devuelto.
/// - Rutas con nombres (pushNamed) y RouteSettings.
class NavigationFormActivityScreen extends StatefulWidget {
  const NavigationFormActivityScreen({super.key});

  @override
  State<NavigationFormActivityScreen> createState() =>
      _NavigationFormActivityScreenState();
}

class _NavigationFormActivityScreenState
    extends State<NavigationFormActivityScreen> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController(text: 'Kevin Alumno DAM2');
  final _emailController = TextEditingController(text: 'alumno@dam2.es');
  final _notesController =
      TextEditingController(text: 'Entrega de prácticas y proyectos de la Unidad 3.');

  String _returnedValue = '';

  @override
  void dispose() {
    _nameController.dispose();
    _emailController.dispose();
    _notesController.dispose();
    super.dispose();
  }

  // Método asíncrono para enviar formulario y esperar la respuesta
  Future<void> _submitFormAndNavigate() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    // Navegación asíncrona con Navigator.push esperando retorno
    final dynamic response = await Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => NavigationDetailScreen(
          userName: _nameController.text,
          userEmail: _emailController.text,
          notes: _notesController.text,
        ),
      ),
    );

    if (response != null && mounted) {
      setState(() {
        _returnedValue = response.toString();
      });

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Respuesta recibida: $_returnedValue'),
          backgroundColor: Colors.teal.shade800,
          behavior: SnackBarBehavior.floating,
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Actividad 3.3: Formularios y Rutas'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Banner de estado con respuesta recibida
            if (_returnedValue.isNotEmpty)
              Container(
                margin: const EdgeInsets.only(bottom: 20),
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.teal.shade50,
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: Colors.teal.shade300),
                ),
                child: Row(
                  children: [
                    Icon(Icons.check_circle, color: Colors.teal.shade700),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Valor retornado de la pantalla destino:',
                            style: TextStyle(
                              fontWeight: FontWeight.bold,
                              color: Colors.teal.shade900,
                            ),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            _returnedValue,
                            style: TextStyle(color: Colors.teal.shade800),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),

            Card(
              elevation: 2,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(16),
              ),
              child: Padding(
                padding: const EdgeInsets.all(20.0),
                child: Form(
                  key: _formKey,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Formulario de Entrada (User Input)',
                        style: theme.textTheme.titleMedium?.copyWith(
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 16),
                      TextFormField(
                        controller: _nameController,
                        decoration: const InputDecoration(
                          labelText: 'Nombre completo *',
                          prefixIcon: Icon(Icons.person),
                          border: OutlineInputBorder(),
                        ),
                        validator: (value) {
                          if (value == null || value.trim().isEmpty) {
                            return 'Por favor ingresa un nombre.';
                          }
                          return null;
                        },
                      ),
                      const SizedBox(height: 16),
                      TextFormField(
                        controller: _emailController,
                        decoration: const InputDecoration(
                          labelText: 'Correo electrónico *',
                          prefixIcon: Icon(Icons.email),
                          border: OutlineInputBorder(),
                        ),
                        keyboardType: TextInputType.emailAddress,
                        validator: (value) {
                          if (value == null || !value.contains('@')) {
                            return 'Ingresa un correo electrónico válido.';
                          }
                          return null;
                        },
                      ),
                      const SizedBox(height: 16),
                      TextFormField(
                        controller: _notesController,
                        maxLines: 3,
                        decoration: const InputDecoration(
                          labelText: 'Observaciones / Argumentos a transmitir',
                          prefixIcon: Icon(Icons.notes),
                          border: OutlineInputBorder(),
                        ),
                      ),
                      const SizedBox(height: 24),
                      SizedBox(
                        width: double.infinity,
                        height: 48,
                        child: FilledButton.icon(
                          onPressed: _submitFormAndNavigate,
                          icon: const Icon(Icons.send_rounded),
                          label: const Text('Validar y Enviar a Pantalla 2'),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
            const SizedBox(height: 24),

            // Tarjeta explicativa de Navigator 1.0 y retorno asíncrono
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: theme.colorScheme.surfaceContainerHighest.withValues(alpha: 0.4),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: theme.colorScheme.outlineVariant),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Patrón de Comunicación (Navigator 1.0):',
                    style: theme.textTheme.titleSmall?.copyWith(
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 8),
                  const Text('1. Pantalla 1 valida el formulario con GlobalKey<FormState>.'),
                  const Text('2. Llama a: final res = await Navigator.push(context, route).'),
                  const Text('3. Pantalla 2 recibe los datos en constructor o RouteSettings.'),
                  const Text('4. Pantalla 2 devuelve datos con: Navigator.pop(context, "OK").'),
                  const Text('5. Pantalla 1 despierta tras el await y actualiza con setState().'),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
