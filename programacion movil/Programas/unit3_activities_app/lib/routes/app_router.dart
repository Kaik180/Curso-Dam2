import 'package:go_router/go_router.dart';
import '../models/item_model.dart';
import '../screens/counter_activity_screen.dart';
import '../screens/future_builder_activity_screen.dart';
import '../screens/gorouter_hero_activity_screen.dart';
import '../screens/hero_detail_screen.dart';
import '../screens/home_dashboard_screen.dart';
import '../screens/nav_widgets_dialogs_activity_screen.dart';
import '../screens/navigation_form_activity_screen.dart';

final GoRouter appRouter = GoRouter(
  initialLocation: '/',
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomeDashboardScreen(),
    ),
    GoRoute(
      path: '/counter',
      builder: (context, state) => const CounterActivityScreen(),
    ),
    GoRoute(
      path: '/future-builder',
      builder: (context, state) => const FutureBuilderActivityScreen(),
    ),
    GoRoute(
      path: '/navigation-form',
      builder: (context, state) => const NavigationFormActivityScreen(),
    ),
    GoRoute(
      path: '/nav-widgets',
      builder: (context, state) => const NavWidgetsDialogsActivityScreen(),
    ),
    GoRoute(
      path: '/gorouter-hero',
      builder: (context, state) => const GoRouterHeroActivityScreen(),
    ),
    GoRoute(
      path: '/detail/:id',
      builder: (context, state) {
        final id = state.pathParameters['id'] ?? 'item-0';
        final item = state.extra as ItemModel? ??
            ItemModel(
              id: id,
              title: 'Detalle de Plato $id',
              category: 'Platos Destacados',
              description:
                  'Descripción detallada cargada a través del parámetro de ruta GoRouter.',
              price: 12.50,
              imageUrl: '',
            );
        return HeroDetailScreen(itemId: id, item: item);
      },
    ),
  ],
);
