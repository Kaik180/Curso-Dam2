
import 'package:unit3_activities_app/main.dart';
import 'package:go_router/go_router.dart';


final GoRouter appRouter = GoRouter(
  initialLocation: '/',
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const Pantalla1(),
    ),
    GoRoute(
      path: '/pantalla2',
      builder: (context, state) => const Pantalla2(),
    ),
    GoRoute(
      path: '/pantalla3',
      builder: (context, state) => const Pantalla3(),
    ),
  ],
);
