import 'package:flutter/material.dart';
import 'package:mei_controle/ui/home-page.dart';
import 'package:mei_controle/management/ger-ui.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  GerUi gerUi = GerUi.getInstance();
  bool isDarkMode = false;

  @override
  void initState() {
    super.initState();
    obterTema();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: ThemeData(
        brightness: isDarkMode ? Brightness.dark : Brightness.light,
        hintColor: Colors.white30,
        primaryColor: Colors.white,
        inputDecorationTheme: InputDecorationTheme(
          enabledBorder:
              OutlineInputBorder(borderSide: BorderSide(color: isDarkMode ? Colors.white : Colors.black)),
          focusedBorder:
              OutlineInputBorder(borderSide: BorderSide(color: isDarkMode ? Colors.white54 : Colors.black)),
          hintStyle: TextStyle(color: isDarkMode ? Colors.white54: Colors.black),
        ),
      ),
      debugShowCheckedModeBanner: false,
      home: HomePage(
        onToogleTheme: toogleTheme,
      ),
    );
  }

  void toogleTheme() {
    setState(() {
      if (isDarkMode) {
        isDarkMode = false;
        salvarTema(false);
      } else {
        isDarkMode = true;
        salvarTema(true);
      }
    });
  }

  Future<void> salvarTema(bool value) async {
    gerUi.saveDarkModeState(value);
    print('tema salvo');
  }

  Future<void> obterTema() async {
    await gerUi.getDarkModeState().then((tema) {
      setState(() {
        isDarkMode = tema;
      });
    });
  }
}
