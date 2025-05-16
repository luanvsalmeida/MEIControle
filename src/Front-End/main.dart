import 'package:flutter/material.dart';
import 'package:mei_controle/ui/home-page.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  late bool isDarkMode = false;

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
      } else {
        isDarkMode = true;
      }
    });
  }
}
