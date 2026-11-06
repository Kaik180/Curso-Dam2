import 'package:flutter/material.dart';

/// Unidad 3 - Apartado 01: Introducción a Widgets y Estado Declarativo
/// Actividad solicitada:
/// "Add another button to decrement the counter and another button to reset its value to 0."
class CounterActivityScreen extends StatefulWidget {
  const CounterActivityScreen({super.key});

  @override
  State<CounterActivityScreen> createState() => _CounterActivityScreenState();
}

class _CounterActivityScreenState extends State<CounterActivityScreen> {
  int _counter = 0;

  void _increment() {
    setState(() {
      _counter++;
    });
  }

  void _decrement() {
    setState(() {
      _counter--;
    });
  }

  void _reset() {
    setState(() {
      _counter = 0;
    });
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Actividad 3.1: Contador Extendido'),
        actions: [
          IconButton(
            icon: const Icon(Icons.info_outline),
            tooltip: 'Explicación del ejercicio',
            onPressed: () => _showExplanationDialog(context),
          ),
        ],
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              Card(
                elevation: 3,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Padding(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 24,
                    vertical: 32,
                  ),
                  child: Column(
                    children: [
                      Icon(
                        Icons.touch_app_rounded,
                        size: 48,
                        color: theme.colorScheme.primary,
                      ),
                      const SizedBox(height: 16),
                      Text(
                        'Número de clics registrados:',
                        style: theme.textTheme.titleMedium?.copyWith(
                          color: theme.colorScheme.onSurfaceVariant,
                        ),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: 12),
                      AnimatedSwitcher(
                        duration: const Duration(milliseconds: 300),
                        transitionBuilder: (child, animation) {
                          return ScaleTransition(
                            scale: animation,
                            child: child,
                          );
                        },
                        child: Text(
                          '$_counter',
                          key: ValueKey<int>(_counter),
                          style: theme.textTheme.displayLarge?.copyWith(
                            fontWeight: FontWeight.bold,
                            color: _counter > 0
                                ? Colors.green.shade700
                                : _counter < 0
                                    ? Colors.red.shade700
                                    : theme.colorScheme.primary,
                          ),
                        ),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        _counter == 1 ? 'clic efectuado' : 'clics efectuados',
                        style: theme.textTheme.bodyMedium?.copyWith(
                          fontStyle: FontStyle.italic,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 32),
              // Explicación de conceptos clave
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: theme.colorScheme.surfaceContainerHighest.withValues(alpha: 0.5),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(
                    color: theme.colorScheme.outlineVariant,
                  ),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Icon(
                          Icons.lightbulb,
                          size: 20,
                          color: Colors.amber.shade700,
                        ),
                        const SizedBox(width: 8),
                        Text(
                          'Conceptos aplicados (Unit 03 - 01):',
                          style: theme.textTheme.titleSmall?.copyWith(
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 8),
                    const Text('• UI Declarativa: Interfaz como función del estado (UI = f(s)).'),
                    const Text('• StatefulWidget y ciclo de vida con createState() y build().'),
                    const Text('• Notificación reactiva con setState().'),
                    const Text('• Contenedor Row en floatingActionButton con múltiples acciones.'),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
      // Solución recomendada en la guía: usar un Row dentro de floatingActionButton
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
      floatingActionButton: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 16.0),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // Botón decrementar (-)
            FloatingActionButton.extended(
              heroTag: 'btn_decrement',
              onPressed: _decrement,
              backgroundColor: Colors.red.shade100,
              foregroundColor: Colors.red.shade900,
              icon: const Icon(Icons.remove),
              label: const Text('Restar'),
            ),
            const SizedBox(width: 12),
            // Botón reset (0)
            FloatingActionButton.extended(
              heroTag: 'btn_reset',
              onPressed: _reset,
              backgroundColor: Colors.grey.shade200,
              foregroundColor: Colors.grey.shade900,
              icon: const Icon(Icons.refresh),
              label: const Text('Reiniciar'),
            ),
            const SizedBox(width: 12),
            // Botón incrementar (+)
            FloatingActionButton.extended(
              heroTag: 'btn_increment',
              onPressed: _increment,
              backgroundColor: theme.colorScheme.primaryContainer,
              foregroundColor: theme.colorScheme.onPrimaryContainer,
              icon: const Icon(Icons.add),
              label: const Text('Sumar'),
            ),
          ],
        ),
      ),
    );
  }

  void _showExplanationDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Actividad Unit 03 - 01'),
        content: const Text(
          'Enunciado oficial:\n\n'
          '"Añadir otro botón para decrementar el contador y otro botón para reiniciar su valor a 0."\n\n'
          'Pista resuelta:\n'
          'La propiedad floatingActionButton del Scaffold contiene un Row con 3 FloatingActionButton con heroTag únicos '
          'y posición centrada con FloatingActionButtonLocation.centerFloat.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Entendido'),
          ),
        ],
      ),
    );
  }
}
