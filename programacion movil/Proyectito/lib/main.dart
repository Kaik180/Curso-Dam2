import 'package:flutter/material.dart';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      // The initial page of MaterialApp
      // is the Pantalla1 widget.
      debugShowCheckedModeBanner: false,
      home: Pantalla1(),
    );
  }
}

// Screen 1: Contains a button to navigate
// to the second screen

class Pantalla1 extends StatelessWidget {
  const Pantalla1({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
       backgroundColor: const Color.fromARGB(255, 255, 7, 7),
      appBar: AppBar(
        title: const Text('Primera Pantalla'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              child: const Text('Anar a pantalla 2'),
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => const Pantalla2(),
                  ),
                );
              },
            ),
          ],
        ),
      ),
    );
  }
}

// Screen 2: Contains a button to return to
// the first screen and another to navigate to the third

class Pantalla2 extends StatelessWidget {
  const Pantalla2({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.indigo,
      appBar: AppBar(
        title: const Text("Segona Pantalla"),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              child: const Text('Tornar a Pantalla 1'),
              onPressed: () {
                // Use canPop to avoid leaving the
                // application without a visible screen.
                if (Navigator.canPop(context)) Navigator.pop(context);
              },
            ),
            Center(
              child: Counter(),
            ),
            const Divider(height: 100),
            ElevatedButton(
              child: const Text('Anar a Pantalla 3'),
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => const Pantalla3(),
                  ),
                );
              },
            )
          ],
        ),
      ),
    );
  }
}

class Pantalla3 extends StatelessWidget {
  const Pantalla3({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.amber,
      appBar: AppBar(
        title: const Text("Pantalla 3"),
      ),
      body: Center(
        child: ElevatedButton(
          child: const Text('Tornar a Pantalla 1'),
          onPressed: () {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => const Pantalla1(),
              ),
            );
          },
        ),
      ),
    );
  }
  
}

class Counter extends StatefulWidget {
  const Counter({super.key});

  @override
  State<Counter> createState() => _CounterState();
}
class _CounterState extends State<Counter> {
  int counter = 0;
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text("Contador = $counter"),
        ElevatedButton(onPressed: ()=>setState(() {
          counter += 1;
        }), child: Icon(Icons.add),)
      ],

    );
  }
}