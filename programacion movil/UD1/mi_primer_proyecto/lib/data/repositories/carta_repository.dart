import '../../domain/entities/entrant.dart';
import '../../domain/entities/principal.dart';
import '../../domain/entities/beguda.dart';
import '../services/healthys_api.dart';

/// Repositori encarregat de subministrar les entitats de la carta del restaurant
class CartaRepository {
  final HealthysApi _api;

  CartaRepository({HealthysApi? api}) : _api = api ?? HealthysApi();

  /// Obté la llista d'entrants transformats en instàncies d'Entrant
  Future<List<Entrant>> getEntrants([String? tipus]) async {
    final List<Map<String, dynamic>> raw = await _api.getEntrantsRaw(tipus);
    return raw.map((json) => Entrant.fromJSON(json)).toList();
  }

  /// Obté la llista de plats principals transformats en instàncies de Principal
  Future<List<Principal>> getPrincipals([String? tipus]) async {
    final List<Map<String, dynamic>> raw = await _api.getPrincipalsRaw(tipus);
    return raw.map((json) => Principal.fromJSON(json)).toList();
  }

  /// Obté la llista de begudes transformades en instàncies de Beguda
  Future<List<Beguda>> getBegudes([String? tipus]) async {
    final List<Map<String, dynamic>> raw = await _api.getBegudesRaw(tipus);
    return raw.map((json) => Beguda.fromJSON(json)).toList();
  }

  /// Obté la llista de subtipus disponibles d'entrants
  Future<List<String>> getSubtipusEntrants() async {
    final List<Entrant> entrants = await getEntrants();
    final Set<String> subtipus = entrants.map((e) => e.tipus).toSet();
    return subtipus.where((s) => s.isNotEmpty).toList()..sort();
  }

  /// Obté la llista de subtipus disponibles de principals
  Future<List<String>> getSubtipusPrincipals() async {
    final List<Principal> principals = await getPrincipals();
    final Set<String> subtipus = principals.map((p) => p.tipus).toSet();
    return subtipus.where((s) => s.isNotEmpty).toList()..sort();
  }

  /// Obté la llista de subtipus disponibles de begudes
  Future<List<String>> getSubtipusBegudes() async {
    final List<Beguda> begudes = await getBegudes();
    final Set<String> subtipus = begudes.map((b) => b.tipus).toSet();
    return subtipus.where((s) => s.isNotEmpty).toList()..sort();
  }
}
