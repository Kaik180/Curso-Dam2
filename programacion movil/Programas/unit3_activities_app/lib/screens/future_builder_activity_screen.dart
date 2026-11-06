import 'dart:math';
import 'package:flutter/material.dart';
import '../models/item_model.dart';

/// Unidad 3 - Apartado 02: Operaciones Asíncronas con FutureBuilder
/// Implementa:
/// - Buena práctica: Guardar el Future en una variable de estado en initState()
///   en vez de instanciarlo dentro de build() para evitar re-ejecuciones continuas.
/// - Manejo riguroso de ConnectionState (waiting, done), snapshot.hasError, snapshot.hasData.
/// - Pull-to-refresh con RefreshIndicator.
/// - Posibilidad de forzar errores y recargas manuales.
class FutureBuilderActivityScreen extends StatefulWidget {
  const FutureBuilderActivityScreen({super.key});

  @override
  State<FutureBuilderActivityScreen> createState() =>
      _FutureBuilderActivityScreenState();
}

class _FutureBuilderActivityScreenState
    extends State<FutureBuilderActivityScreen> {
  late Future<List<ItemModel>> _itemsFuture;
  bool _forceError = false;

  @override
  void initState() {
    super.initState();
    // Buena práctica documentada en el curso:
    // El Future se inicializa en initState para no recrearlo en cada invocación de build().
    _itemsFuture = _fetchMockData();
  }

  // Simulación de petición de red asíncrona con latencia de 1.5s
  Future<List<ItemModel>> _fetchMockData() async {
    await Future.delayed(const Duration(milliseconds: 1500));

    if (_forceError) {
      throw Exception('Fallo simulado de conexión con el servidor (HTTP 500).');
    }

    final rng = Random();
    final categories = ['Comida Mediterránea', 'Postres', 'Bebidas', 'Especialidades'];
    
    return List.generate(
      6,
      (index) => ItemModel(
        id: 'ITEM-${index + 1}',
        title: 'Plato Especial #${index + 1}',
        category: categories[index % categories.length],
        description:
            'Delicioso plato preparado con ingredientes frescos y técnicas de alta cocina.',
        price: 8.50 + rng.nextInt(15),
        imageUrl: 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=150',
        rating: 4 + (index % 2),
      ),
    );
  }

  // Función para recargar el Future bajo demanda (o con Pull-to-refresh)
  Future<void> _reloadFuture() async {
    setState(() {
      _itemsFuture = _fetchMockData();
    });
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Actividad 3.2: FutureBuilder & Pull'),
        actions: [
          IconButton(
            icon: Icon(
              _forceError ? Icons.error : Icons.check_circle,
              color: _forceError ? Colors.red : Colors.green,
            ),
            tooltip: _forceError ? 'Modo Error Activado' : 'Modo Normal Activado',
            onPressed: () {
              setState(() {
                _forceError = !_forceError;
              });
              _reloadFuture();
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: Text(_forceError
                      ? 'Simulación de error activada.'
                      : 'Simulación normal activada.'),
                  duration: const Duration(seconds: 2),
                ),
              );
            },
          ),
          IconButton(
            icon: const Icon(Icons.refresh),
            tooltip: 'Recargar manualmente',
            onPressed: _reloadFuture,
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: _reloadFuture,
        child: FutureBuilder<List<ItemModel>>(
          future: _itemsFuture,
          builder: (BuildContext context, AsyncSnapshot<List<ItemModel>> snapshot) {
            // 1. Estado de Espera (Loading)
            if (snapshot.connectionState == ConnectionState.waiting) {
              return Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const CircularProgressIndicator(),
                    const SizedBox(height: 20),
                    Text(
                      'Obteniendo datos del servidor...',
                      style: theme.textTheme.bodyLarge,
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'ConnectionState.waiting',
                      style: theme.textTheme.bodySmall?.copyWith(
                        fontFamily: 'monospace',
                        color: theme.colorScheme.primary,
                      ),
                    ),
                  ],
                ),
              );
            }

            // 2. Estado de Error
            if (snapshot.hasError) {
              return ListView(
                physics: const AlwaysScrollableScrollPhysics(),
                children: [
                  SizedBox(height: MediaQuery.of(context).size.height * 0.2),
                  Center(
                    child: Padding(
                      padding: const EdgeInsets.all(24.0),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(
                            Icons.cloud_off_rounded,
                            size: 64,
                            color: Colors.red.shade400,
                          ),
                          const SizedBox(height: 16),
                          Text(
                            'Error al cargar información',
                            style: theme.textTheme.titleLarge?.copyWith(
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          const SizedBox(height: 8),
                          Text(
                            '${snapshot.error}',
                            textAlign: TextAlign.center,
                            style: theme.textTheme.bodyMedium?.copyWith(
                              color: Colors.red.shade700,
                            ),
                          ),
                          const SizedBox(height: 24),
                          FilledButton.icon(
                            onPressed: () {
                              setState(() {
                                _forceError = false;
                              });
                              _reloadFuture();
                            },
                            icon: const Icon(Icons.refresh),
                            label: const Text('Reintentar conexión'),
                          ),
                          const SizedBox(height: 12),
                          const Text(
                            '(También puedes deslizar hacia abajo para refrescar)',
                            style: TextStyle(fontSize: 12, fontStyle: FontStyle.italic),
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              );
            }

            // 3. Estado con datos satisfactorios
            if (snapshot.hasData && snapshot.data != null) {
              final items = snapshot.data!;
              if (items.isEmpty) {
                return const Center(child: Text('No hay elementos disponibles.'));
              }

              return ListView.builder(
                physics: const AlwaysScrollableScrollPhysics(),
                padding: const EdgeInsets.all(16),
                itemCount: items.length + 1,
                itemBuilder: (context, index) {
                  if (index == 0) {
                    return Container(
                      margin: const EdgeInsets.only(bottom: 16),
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: theme.colorScheme.primaryContainer.withValues(alpha: 0.4),
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(color: theme.colorScheme.primaryContainer),
                      ),
                      child: Row(
                        children: [
                          Icon(Icons.swipe_down_rounded, color: theme.colorScheme.primary),
                          const SizedBox(width: 12),
                          const Expanded(
                            child: Text(
                              'Demostración de Pull-to-refresh (RefreshIndicator): arrastra la lista hacia abajo para refrescar.',
                              style: TextStyle(fontSize: 13),
                            ),
                          ),
                        ],
                      ),
                    );
                  }

                  final item = items[index - 1];
                  return Card(
                    margin: const EdgeInsets.only(bottom: 12),
                    elevation: 1,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: ListTile(
                      contentPadding: const EdgeInsets.all(12),
                      leading: CircleAvatar(
                        radius: 26,
                        backgroundColor: theme.colorScheme.primary.withValues(alpha: 0.1),
                        child: Text(
                          item.id.replaceAll('ITEM-', '#'),
                          style: TextStyle(
                            fontWeight: FontWeight.bold,
                            color: theme.colorScheme.primary,
                          ),
                        ),
                      ),
                      title: Text(
                        item.title,
                        style: const TextStyle(fontWeight: FontWeight.bold),
                      ),
                      subtitle: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const SizedBox(height: 4),
                          Text(item.category,
                              style: TextStyle(color: theme.colorScheme.secondary)),
                          const SizedBox(height: 4),
                          Text(
                            item.description,
                            maxLines: 2,
                            overflow: TextOverflow.ellipsis,
                          ),
                        ],
                      ),
                      trailing: Text(
                        '${item.price.toStringAsFixed(2)} €',
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                          color: Colors.green.shade700,
                        ),
                      ),
                    ),
                  );
                },
              );
            }

            // Caso base por defecto
            return const Center(child: Text('Sin datos disponibles.'));
          },
        ),
      ),
    );
  }
}
