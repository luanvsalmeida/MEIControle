import 'package:shared_preferences/shared_preferences.dart';

class GerUi{
  static GerUi? _singleInstance;

  GerUi._internal();

  static GerUi getInstance() {
    _singleInstance ??= GerUi._internal();
    return _singleInstance!;
  }

  Future<bool> getDarkModeState() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getBool('darkModeState') ?? false;
  }

  Future<int> getFontSize() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getInt('fontSize') ?? 18;
  }

  Future<void> saveDarkModeState(bool value) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('darkModeState', value);
  }

  Future<void> saveFontSize(int value) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setInt('fontSize', value);
  }
}