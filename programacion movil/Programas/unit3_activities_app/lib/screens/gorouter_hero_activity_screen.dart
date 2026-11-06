import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../models/item_model.dart';

/// Unidad 3 - Apartado 05: Navegación avanzada con GoRouter y Animaciones Hero
class GoRouterHeroActivityScreen extends StatefulWidget {
  const GoRouterHeroActivityScreen({super.key});

  @override
  State<GoRouterHeroActivityScreen> createState() =>
      _GoRouterHeroActivityScreenState();
}

class _GoRouterHeroActivityScreenState
    extends State<GoRouterHeroActivityScreen> {
  final List<ItemModel> _catalog = [
    const ItemModel(
      id: 'ENT01',
      title: 'Ensalada César Gourmet',
      category: 'Entrantes',
      description:
          'Lechuga romana crujiente, croutons al romero, parmesano reggiano y salsa césar casera con anchoas del Cantábrico.',
      price: 9.50,
      imageUrl: '',
      rating: 5,
    ),
    const ItemModel(
      id: 'PRI02',
      title: 'Solomillo al Foie con Reducción',
      category: 'Principales',
      description:
          'Solomillo de ternera gallega marcado a la brasa, coronado con medallón de foie fresco y salsa reducida al vino Pedro Ximénez.',
      price: 22.00,
      imageUrl: '',
      rating: 5,
    ),
    const ItemModel(
      id: 'POS03',
      title: 'Coulant de Chocolate Belga',
      category: 'Postres',
      description:
          'Bizcocho caliente relleno de chocolate fundido 70% cacao, acompañado de quenelle de helado de vainilla Bourbon de Madagascar.',
      price: 7.20,
      imageUrl: '',
      rating: 5,
    ),
  ];

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Actividad 3.5: GoRouter & Hero'),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Container(
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(
              color: theme.colorScheme.primaryContainer.withValues(alpha: 0.4),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: theme.colorScheme.primaryContainer),
            ),
            child: const Row(
              children: [
                Icon(Icons.auto_awesome, color: Colors.deepPurple),
                SizedBox(width: 12),
                Expanded(
                  child: Text(
                    'Haz clic en cualquier plato: observa cómo el icono y cabecera vuelan fluidamente a la pantalla de detalle gracias a Hero Animations.',
                    style: TextStyle(fontSize: 13),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 16),
          ..._catalog.map((item) => _buildItemCard(context, item, theme)),
        ],
      ),
    );
  }

  Widget _buildItemCard(BuildContext context, ItemModel item, ThemeData theme) {
    return Card(
      margin: const EdgeInsets.only(bottom: 16),
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      clipBehavior: Clip.antiAlias,
      child: InkWell(
        onTap: () {
          // Navegación declarativa mediante GoRouter usando rutas dinámicas y parámetros
          context.push('/detail/${item.id}', extra: item);
        },
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Elemento Hero en la lista de origen
            Hero(
              tag: 'hero-${item.id}',
              child: Container(
                height: 140,
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    colors: [
                      theme.colorScheme.primary,
                      theme.colorScheme.tertiary,
                    ],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  ),
                ),
                child: Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Icon(Icons.restaurant_menu_rounded,
                          size: 48, color: Colors.white),
                      const SizedBox(height: 6),
                      Text(
                        item.category.toUpperCase(),
                        style: const TextStyle(
                          color: Colors.white70,
                          fontSize: 12,
                          letterSpacing: 1.5,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: Row(
                children: [
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          item.title,
                          style: theme.textTheme.titleMedium?.copyWith(
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 4),
                        Text(
                          item.description,
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                          style: theme.textTheme.bodySmall,
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(width: 12),
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.end,
                    children: [
                      Text(
                        '${item.price.toStringAsFixed(2)} €',
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                          color: Colors.green.shade700,
                        ),
                      ),
                      const SizedBox(height: 6),
                      Icon(Icons.arrow_forward_ios,
                          size: 16, color: theme.colorScheme.outline),
                    ],
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
