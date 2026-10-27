void main() {
  print('================================================================');
  print('     ACTIVITAT 2: LES 30 PREGUNTES DE PROGRAMACIÓ FUNCIONAL');
  print('================================================================\n');

  // --- DADES BASE DE PROVA ---
  List<int> listI = [-3, 2, -1, 0, 4, 23, 17, -90, 8, 12];
  List<double> listF = [50.75, 20.84, 1000.99, 100.01, 275.42, 15.50];
  List<String> listS = [
    'Juan',
    'Pedro',
    'Aureliana',
    'Esternocleidomastoideo',
    'Souvenir',
    'Amadeus',
    'Francia',
    'A',
    'Bé',
    'Ceh',
    'Dehe',
    'Arnold'
  ];

  List<Map<String, dynamic>> products = [
    {'name': 'Portàtil Pro', 'price': 1200.0, 'category': 'Electrònica', 'stock': 5},
    {'name': 'Ratolí Òptic', 'price': 15.0, 'category': 'Accessoris', 'stock': 25},
    {'name': 'Teclat Mecànic', 'price': 85.0, 'category': 'Accessoris', 'stock': 0},
    {'name': 'Monitor 4K', 'price': 350.0, 'category': 'Electrònica', 'stock': 8},
    {'name': 'Auriculars Bluetooth', 'price': 45.0, 'category': 'Àudio', 'stock': 12},
    {'name': 'Cable HDMI', 'price': 8.5, 'category': 'Cables', 'stock': 50},
    {'name': 'Altaveu Intel·ligent', 'price': 60.0, 'category': 'Àudio', 'stock': 0},
    {'name': 'Tauleta Gràfica', 'price': 180.0, 'category': 'Electrònica', 'stock': 3},
    {'name': 'Cadira Gaming', 'price': 220.0, 'category': 'Mobiliari', 'stock': 4},
    {'name': 'Lluminària LED USB', 'price': 12.0, 'category': 'Accessoris', 'stock': 15},
    {'name': 'Disc SSD 1TB', 'price': 95.0, 'category': 'Electrònica', 'stock': 10},
    {'name': 'Webcam HD', 'price': 30.0, 'category': 'Accessoris', 'stock': 6},
  ];

  // Question #1: Given a collection of integers, obtain a new collection containing only the even numbers.
  print('Question #1: Parells de listI');
  print(listI.where((n) => n % 2 == 0).toList());
  print('---');

  // Question #2: Given a collection of integers, obtain only those that are greater than zero.
  print('Question #2: Majors que zero de listI');
  print(listI.where((n) => n > 0).toList());
  print('---');

  // Question #3: Given a collection of numbers, create another collection where each number is doubled.
  print('Question #3: Nombres duplicats (* 2)');
  print(listI.map((n) => n * 2).toList());
  print('---');

  // Question #4: Given a collection of integers, create a new collection containing the square of each number.
  print('Question #4: Quadrat de cada nombre');
  print(listI.map((n) => n * n).toList());
  print('---');

  // Question #5: Given a collection of words, create a collection containing the length of each word.
  print('Question #5: Longitud de cada paraula');
  print(listS.map((s) => s.length).toList());
  print('---');

  // Question #6: Given a collection of words, obtain only those that contain more than 5 characters.
  print('Question #6: Paraules amb més de 5 caràcters');
  print(listS.where((s) => s.length > 5).toList());
  print('---');

  // Question #7: Given a collection of words, create another collection with all the words converted to uppercase.
  print('Question #7: Paraules en majúscules');
  print(listS.map((s) => s.toUpperCase()).toList());
  print('---');

  // Question #8: Given a collection of integers, filter the even numbers and calculate the square of each one.
  print('Question #8: Parells elevats al quadrat');
  print(listI.where((n) => n % 2 == 0).map((n) => n * n).toList());
  print('---');

  // Question #9: Given a collection of words, keep the words with more than 4 characters and convert them to uppercase.
  print('Question #9: Paraules > 4 caràcters en majúscules');
  print(listS.where((s) => s.length > 4).map((s) => s.toUpperCase()).toList());
  print('---');

  // Question #10: Given a collection of numbers, keep only the positive numbers and multiply each one by 10.
  print('Question #10: Positius multiplicats per 10');
  print(listI.where((n) => n > 0).map((n) => n * 10).toList());
  print('---');

  // Question #11: Given a collection of names, obtain the names that start with the letter A and convert them to uppercase.
  print('Question #11: Noms que comencen per A en majúscules');
  print(listS.where((s) => s.toUpperCase().startsWith('A')).map((s) => s.toUpperCase()).toList());
  print('---');

  // Question #12: Given a collection of prices, create a new collection applying a 20% discount only to prices greater than 100.
  print('Question #12: Descompte del 20% a preus > 100');
  print(listF.where((p) => p > 100.0).map((p) => (p * 0.80).toStringAsFixed(2)).toList());
  print('---');

  // Question #13: Given a collection of numbers, calculate the sum of all its elements.
  print('Question #13: Suma de tots els elements');
  print(listF.reduce((acc, n) => acc + n));
  print('---');

  // Question #14: Given a collection of numbers, calculate the product of all its elements.
  final List<int> smallNums = [2, 3, 4, 5];
  print('Question #14: Producte de $smallNums');
  print(smallNums.reduce((acc, n) => acc * n));
  print('---');

  // Question #15: Given a collection of numbers, obtain the largest number.
  print('Question #15: Nombre més gran');
  print(listF.reduce((acc, n) => acc > n ? acc : n));
  print('---');

  // Question #16: Given a collection of numbers, obtain the smallest number.
  print('Question #16: Nombre més xicotet');
  print(listF.reduce((acc, n) => acc < n ? acc : n));
  print('---');

  // Question #17: Given a collection of numbers, filter the even numbers and calculate their sum.
  print('Question #17: Suma dels números parells');
  print(listI.where((n) => n % 2 == 0).reduce((acc, n) => acc + n));
  print('---');

  // Question #18: Given a collection of numbers, calculate their arithmetic mean using functional operations instead of an explicit loop.
  print('Question #18: Mitjana aritmètica funcional');
  print(listI.reduce((acc, n) => acc + n) / listI.length);
  print('---');

  // Question #19: Given a collection of numbers, calculate the square of each number and sum all the results.
  print('Question #19: Suma dels quadrats');
  print(listI.map((n) => n * n).reduce((acc, n) => acc + n));
  print('---');

  // Question #20: Given a collection of numbers, keep the even numbers, square each one, and sum the results.
  print('Question #20: Suma dels quadrats dels parells');
  print(listI.where((n) => n % 2 == 0).map((n) => n * n).reduce((acc, n) => acc + n));
  print('---');

  // Question #21: Given a collection of numbers, determine whether there is at least one negative number.
  print('Question #21: Hi ha algun nombre negatiu?');
  print(listI.any((n) => n < 0) ? 'Sí, hi ha negatius' : 'No hi ha negatius');
  print('---');

  // Question #22: Given a collection of numbers, determine whether all its elements are greater than zero.
  print('Question #22: Són tots majors que zero?');
  print(listI.every((n) => n > 0));
  print('Amb [1, 2, 3]: ${[1, 2, 3].every((n) => n > 0)}');
  print('---');

  // Question #23: Given a collection of numbers, determine whether none of them is equal to zero.
  print('Question #23: Cap és igual a zero?');
  print(listI.every((n) => n != 0));
  print('---');

  // Question #24: Given a collection of numbers, find the first even number. If there is none, return a result representing the absence of a value.
  print('Question #24: Primer parell o absència');
  final int? firstEven = listI.where((n) => n % 2 == 0).isNotEmpty
      ? listI.firstWhere((n) => n % 2 == 0)
      : null;
  print(firstEven != null ? 'Primer parell trobat: $firstEven' : 'Cap parell');
  print('---');

  // Question #25: Given a collection of words and a specific word, determine whether that word is present in the collection.
  print('Question #25: "Amadeus" és present?');
  print(listS.contains('Amadeus'));
  print('---');

  // Question #26: Given a collection of names, find the first name that contains more than 7 characters.
  print('Question #26: Primer nom amb més de 7 lletres');
  final String firstNameOver7 = listS.firstWhere(
    (s) => s.length > 7,
    orElse: () => 'Cap nom trobat',
  );
  print(firstNameOver7);
  print('---');

  // Question #27: Given a collection of products, where each product has a name, price, category, and stock quantity, obtain all products whose price is greater than 100.
  print('Question #27: Productes amb preu > 100');
  print(products.where((p) => p['price'] > 100).toList());
  print('---');

  // Question #28: Given a collection of products, obtain a collection containing only the names of all the products.
  print('Question #28: Només noms dels productes');
  print(products.map((p) => p['name']).toList());
  print('---');

  // Question #29: Given a collection of products, obtain the products whose stock quantity is zero.
  print('Question #29: Productes esgotats (stock == 0)');
  print(products.where((p) => p['stock'] == 0).map((p) => p['name']).toList());
  print('---');

  // Question #30: Given a collection of products, obtain a collection containing the price of each product increased by 21%.
  print('Question #30: Preus amb IVA (+21%)');
  print(products.map((p) => (p['price'] * 1.21).toStringAsFixed(2)).toList());
  print('---');

  print('================================================================');
  print('     TOTES LES 30 PREGUNTES RESOLTES CORRECTAMENT!');
  print('================================================================');
}
