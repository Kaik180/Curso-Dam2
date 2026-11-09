/*
File: lib/presentation/screens/home_screen.dart
Contains the application's home screen.
*/

import 'package:flutter/material.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Material Application',
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Bar Text'),
        ),
        body: const Center(
          child: Text('Hello World'),
        ),
      ),
    );
  }
}