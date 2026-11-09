import 'package:flutter/material.dart';

/// Unidad 3 - Apartado 03: Segunda Pantalla receptora de parámetros
/// Demuestra:
/// - Recepción de argumentos por constructor y por RouteSettings (Named Routes).
/// - Devolución de valores a la pantalla anterior mediante Navigator.pop(context, result).
/// - Uso seguro de canPop() y maybePop().
class NavigationDetailScreen extends StatefulWidget {
  final String? userName;
  final String? userEmail;
  final String? notes;

  const NavigationDetailScreen({
    super.key,
    this.userName,
    this.userEmail,
    this.notes,
  });

  @override
  State<NavigationDetailScreen> createState() => _NavigationDetailScreenState();
}

class _NavigationDetailScreenState extends State<NavigationDetailScreen> {
  final _responseController = TextEditingController(text: '¡Aprobado con éxito!');

  @override
  void dispose() {
    _responseController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    // Si no se pasaron por constructor, intentar obtenerlos de RouteSettings (Named Routes)
    final routeArgs = ModalRoute.of(context)?.settings.arguments as Map<String, dynamic>?;
    final name = widget.userName ?? routeArgs?['name'] ?? 'Usuario Anónimo';
    final email = widget.userEmail ?? routeArgs?['email'] ?? 'correo@ejemplo.com';
    final notes = widget.notes ?? routeArgs?['notes'] ?? 'Sin observaciones adicionales';

    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Detalle & Retorno Asíncrono'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Card(
              elevation: 2,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
              child: Padding(
                padding: const EdgeInsets.all(20.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        CircleAvatar(
                          backgroundColor: theme.colorScheme.primaryContainer,
                          child: Icon(Icons.person, color: theme.colorScheme.primary),
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                name,
                                style: theme.textTheme.titleMedium?.copyWith(
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              Text(
                                email,
                                style: theme.textTheme.bodyMedium?.copyWith(
                                  color: theme.colorScheme.outline,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                    const Divider(height: 32),
                    Text(
                      'Observaciones recibidas:',
                      style: theme.textTheme.labelLarge?.copyWith(
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 6),
                    Text(
                      notes,
                      style: theme.textTheme.bodyMedium,
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 32),
            Text(
              'Respuesta para devolver a la Pantalla Anterior:',
              style: theme.textTheme.titleSmall?.copyWith(
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            TextField(
              controller: _responseController,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'Mensaje de confirmación / código de estado',
                prefixIcon: Icon(Icons.reply),
              ),
            ),
            const SizedBox(height: 20),
            FilledButton.icon(
              onPressed: () {
                // Devolvemos el resultado mediante Navigator.pop(context, resultado)
                Navigator.pop(context, _responseController.text);
              },
              icon: const Icon(Icons.check_circle_outline),
              label: const Text('Devolver Respuesta con Navigator.pop()'),
            ),
            const SizedBox(height: 12),
            OutlinedButton.icon(
              onPressed: () {
                // Comprobación de seguridad recomendada en el curso:
                if (Navigator.canPop(context)) {
                  Navigator.pop(context, 'Operación Cancelada por el usuario');
                }
              },
              icon: const Icon(Icons.close),
              label: const Text('Cancelar y Volver'),
            ),
          ],
        ),
      ),
    );
  }
}
