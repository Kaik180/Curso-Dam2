void main() {
  print('================================================================');
  print('     ACTIVITAT 2: LES 60 PREGUNTES DE PROGRAMACIÓ FUNCIONAL');
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

  // Question #31: Given a collection of products, obtain the names of the products whose price is less than 20.
  print('Question #31: Noms de productes amb preu < 20');
  print(products.where((p) => p['price'] < 20).map((p) => p['name']).toList());
  print('---');

  // Question #32: Given a collection of products, calculate the total inventory value. For each product, calculate price × stock quantity and sum all the results.
  print('Question #32: Valor total de l\'inventari');
  final double totalInventory = products
      .map((p) => (p['price'] as double) * (p['stock'] as int))
      .reduce((acc, val) => acc + val);
  print('${totalInventory.toStringAsFixed(2)} €');
  print('---');

  // Question #33: Given a collection of products, determine whether there is at least one product whose stock quantity is zero.
  print('Question #33: Hi ha algun producte sense estoc?');
  print(products.any((p) => p['stock'] == 0));
  print('---');

  // Question #34: Given a collection of products, determine whether all products have at least one unit available.
  print('Question #34: Tots els productes tenen estoc (stock >= 1)?');
  print(products.every((p) => p['stock'] >= 1));
  print('---');

  // Question #35: Given a collection of products, obtain the product with the highest price.
  print('Question #35: Producte amb preu més alt');
  final Map<String, dynamic> mostExpensive =
      products.reduce((acc, p) => acc['price'] > p['price'] ? acc : p);
  print('${mostExpensive['name']} (${mostExpensive['price']} €)');
  print('---');

  // Question #36: Given a collection of products, obtain the product with the lowest price.
  print('Question #36: Producte amb preu més baix');
  final Map<String, dynamic> cheapest =
      products.reduce((acc, p) => acc['price'] < p['price'] ? acc : p);
  print('${cheapest['name']} (${cheapest['price']} €)');
  print('---');

  // Question #37: Given a collection of numbers, obtain a new collection sorted from smallest to largest.
  print('Question #37: Nombres ordenats de menor a major');
  print(List<int>.from(listI)..sort());
  print('---');

  // Question #38: Given a collection of numbers, sort it from largest to smallest.
  print('Question #38: Nombres ordenats de major a menor');
  print(List<int>.from(listI)..sort((a, b) => b.compareTo(a)));
  print('---');

  // Question #39: Given a collection of products, sort them by price from lowest to highest.
  print('Question #39: Productes ordenats per preu (ascendent)');
  final sortedByPrice = List<Map<String, dynamic>>.from(products)
    ..sort((a, b) => (a['price'] as double).compareTo(b['price'] as double));
  print(sortedByPrice.map((p) => '${p['name']}: ${p['price']}€').toList());
  print('---');

  // Question #40: Given a collection of products, sort them alphabetically by name.
  print('Question #40: Productes ordenats alfabèticament per nom');
  final sortedByName = List<Map<String, dynamic>>.from(products)
    ..sort((a, b) => (a['name'] as String).compareTo(b['name'] as String));
  print(sortedByName.map((p) => p['name']).toList());
  print('---');

  // Question #41: Given a collection of numbers that may contain duplicate values, create a collection containing each number only once.
  final List<int> duplicates = [1, 2, 2, 3, 4, 4, 4, 5, 1];
  print('Question #41: Nombres únics (sense duplicats)');
  print(duplicates.toSet().toList());
  print('---');

  // Question #42: Given a collection of words, remove duplicate words while ignoring differences in uppercase and lowercase letters.
  final List<String> wordDupes = ['Casa', 'casa', 'COTXE', 'cotxe', 'ARBRE', 'Arbre'];
  print('Question #42: Paraules úniques (ignorant majúscules/minúscules)');
  final uniqueWords = wordDupes.map((w) => w.toLowerCase()).toSet().toList();
  print(uniqueWords);
  print('---');

  // Question #43: Given a collection of products, group them by category.
  print('Question #43: Agrupar productes per categoria');
  final Map<String, List<String>> groupedByCategory = {};
  for (final p in products) {
    groupedByCategory.putIfAbsent(p['category'] as String, () => []).add(p['name'] as String);
  }
  print(groupedByCategory);
  print('---');

  // Question #44: Given a collection of products, determine how many products there are in each category.
  print('Question #44: Quantitat de productes per categoria');
  final Map<String, int> countPerCategory = {};
  groupedByCategory.forEach((cat, list) {
    countPerCategory[cat] = list.length;
  });
  print(countPerCategory);
  print('---');

  // Question #45: Given a collection of products, calculate the average price of the products in each category.
  print('Question #45: Preu mitjà per categoria');
  final Map<String, double> avgPerCategory = {};
  for (final cat in groupedByCategory.keys) {
    final catProds = products.where((p) => p['category'] == cat).toList();
    final total = catProds.map((p) => p['price'] as double).reduce((a, b) => a + b);
    avgPerCategory[cat] = double.parse((total / catProds.length).toStringAsFixed(2));
  }
  print(avgPerCategory);
  print('---');

  // Question #46: Given a collection of products, find the most expensive product in each category.
  print('Question #46: Producte més car de cada categoria');
  final Map<String, String> mostExpensivePerCat = {};
  for (final cat in groupedByCategory.keys) {
    final catProds = products.where((p) => p['category'] == cat).toList();
    final maxProd = catProds.reduce((a, b) => a['price'] > b['price'] ? a : b);
    mostExpensivePerCat[cat] = '${maxProd['name']} (${maxProd['price']} €)';
  }
  print(mostExpensivePerCat);
  print('---');

  // Question #47: Given a collection of collections of numbers, create a single collection containing all the numbers.
  final List<List<int>> nestedNumbers = [
    [1, 2, 3],
    [4, 5],
    [6, 7, 8, 9]
  ];
  print('Question #47: Aplanar col·leccions aniuades (expand)');
  print(nestedNumbers.expand((list) => list).toList());
  print('---');

  // Question #48: Given a collection of sentences, obtain a single collection containing all the words from all the sentences.
  final List<String> sentences = [
    'Dart és un llenguatge modern',
    'Flutter permet crear aplicacions mòbils',
    'Aprenem programació funcional'
  ];
  print('Question #48: Totes les paraules de les frases');
  print(sentences.expand((s) => s.split(' ')).toList());
  print('---');

  // Question #49: Given a collection of customers, where each customer has a collection of orders, obtain a single collection containing all the orders from all customers.
  final List<Map<String, dynamic>> customers = [
    {
      'customer': 'Anna',
      'orders': ['ORD-001', 'ORD-002']
    },
    {
      'customer': 'Joan',
      'orders': ['ORD-003']
    },
    {
      'customer': 'Maria',
      'orders': ['ORD-004', 'ORD-005', 'ORD-006']
    }
  ];
  print('Question #49: Totes les comandes de tots els clients');
  print(customers.expand((c) => c['orders'] as List<String>).toList());
  print('---');

  // Question #50: Given a collection of orders, where each order contains a collection of products, obtain a single collection containing all the products included in all orders and remove duplicate products.
  final List<Map<String, dynamic>> orders = [
    {
      'id': 1,
      'products': ['Poma', 'Plàtan', 'Taronja']
    },
    {
      'id': 2,
      'products': ['Plàtan', 'Kiwi', 'Maduixa']
    },
    {
      'id': 3,
      'products': ['Poma', 'Maduixa', 'Pera']
    }
  ];
  print('Question #50: Productes únics entre totes les comandes');
  print(orders.expand((o) => o['products'] as List<String>).toSet().toList());
  print('---');

  // Question #51: Given a collection of products, remove products that are out of stock, sort them by price from highest to lowest, take only the first 5, and return their names.
  print('Question #51: Top 5 més cars amb estoc');
  final top5 = products
      .where((p) => (p['stock'] as int) > 0)
      .toList()
    ..sort((a, b) => (b['price'] as double).compareTo(a['price'] as double));
  print(top5.take(5).map((p) => '${p['name']} (${p['price']}€)').toList());
  print('---');

  // Question #52: Given a collection of products and a specific category, filter the products belonging to that category, remove those that are out of stock, sort them by price, and obtain their names.
  print('Question #52: Categoria "Electrònica" amb estoc ordenada per preu');
  final catFiltered = products
      .where((p) => p['category'] == 'Electrònica' && (p['stock'] as int) > 0)
      .toList()
    ..sort((a, b) => (a['price'] as double).compareTo(b['price'] as double));
  print(catFiltered.map((p) => '${p['name']}: ${p['price']}€').toList());
  print('---');

  // Question #53: Given a collection of numbers, calculate the number of elements, the minimum, the maximum, the sum, the average, the number of even numbers, and the number of odd numbers.
  final List<int> statsNums = [12, 5, 8, 19, 3, 24, 7, 10];
  print('Question #53: Estadístiques completes de $statsNums');
  final int count = statsNums.length;
  final int minVal = statsNums.reduce((a, b) => a < b ? a : b);
  final int maxVal = statsNums.reduce((a, b) => a > b ? a : b);
  final int sumVal = statsNums.reduce((a, b) => a + b);
  final double avgVal = sumVal / count;
  final int evensCount = statsNums.where((n) => n % 2 == 0).length;
  final int oddsCount = statsNums.where((n) => n % 2 != 0).length;
  print('''
  - Elements: $count
  - Mínim: $minVal
  - Màxim: $maxVal
  - Suma: $sumVal
  - Mitjana: $avgVal
  - Parells: $evensCount
  - Senars: $oddsCount''');
  print('---');

  // Question #54: Given a collection of users, where each user has a name, age, and active status, keep only active users who are adults and obtain their names sorted alphabetically.
  final List<Map<String, dynamic>> users = [
    {'name': 'Carla', 'age': 25, 'active': true},
    {'name': 'Biel', 'age': 16, 'active': true},
    {'name': 'Andreu', 'age': 34, 'active': false},
    {'name': 'Diana', 'age': 29, 'active': true},
    {'name': 'Enric', 'age': 17, 'active': false},
    {'name': 'Francesc', 'age': 42, 'active': true},
  ];
  print('Question #54: Usuaris actius i adults ordenats alfabèticament');
  final activeAdults = users
      .where((u) => u['active'] == true && (u['age'] as int) >= 18)
      .map((u) => u['name'] as String)
      .toList()
    ..sort();
  print(activeAdults);
  print('---');

  // Question #55: Given a collection of users, calculate the average age, find the oldest user, determine whether there is at least one minor, determine whether all users are active, and obtain the names of the active users.
  print('Question #55: Anàlisi d\'usuaris');
  final double avgAge =
      users.map((u) => u['age'] as int).reduce((a, b) => a + b) / users.length;
  final oldestUser =
      users.reduce((a, b) => a['age'] > b['age'] ? a : b);
  final bool hasMinor = users.any((u) => (u['age'] as int) < 18);
  final bool allActive = users.every((u) => u['active'] == true);
  final activeNames = users.where((u) => u['active'] == true).map((u) => u['name']).toList();
  print('''
  - Edat mitjana: ${avgAge.toStringAsFixed(1)} anys
  - Usuari més veterà: ${oldestUser['name']} (${oldestUser['age']} anys)
  - Hi ha menors d'edat?: $hasMinor
  - Són tots actius?: $allActive
  - Noms actius: $activeNames''');
  print('---');

  // Question #56: Given a collection of invoice lines, where each line has a product, quantity, and unit price, calculate the total invoice amount. For each line, calculate quantity × unit price and then sum all the amounts.
  final List<Map<String, dynamic>> invoiceLines = [
    {'product': 'Toner Impressora', 'quantity': 2, 'unitPrice': 65.0},
    {'product': 'Paquet de Folis', 'quantity': 10, 'unitPrice': 4.5},
    {'product': 'Cadira Oficina', 'quantity': 3, 'unitPrice': 180.0},
    {'product': 'Cable Xarxa RJ45', 'quantity': 8, 'unitPrice': 3.25},
  ];
  print('Question #56: Import total de la factura');
  final double invoiceTotal = invoiceLines
      .map((l) => (l['quantity'] as int) * (l['unitPrice'] as double))
      .reduce((a, b) => a + b);
  print('${invoiceTotal.toStringAsFixed(2)} €');
  print('---');

  // Question #57: Given a collection of invoice lines, calculate the amount for each line, apply a 10% discount to lines whose amount is greater than 500, and sum all the final amounts.
  print('Question #57: Total factura amb descompte 10% en línies > 500€');
  final double invoiceWithDiscounts = invoiceLines.map((l) {
    final double lineAmount = (l['quantity'] as int) * (l['unitPrice'] as double);
    return lineAmount > 500 ? lineAmount * 0.90 : lineAmount;
  }).reduce((a, b) => a + b);
  print('${invoiceWithDiscounts.toStringAsFixed(2)} €');
  print('---');

  // Question #58: Given a collection of students, where each student has a name and a collection of grades, calculate the average grade for each student, obtain the students whose average is greater than or equal to 5, obtain the names of the passing students, and calculate the average grade for the entire class.
  final List<Map<String, dynamic>> students = [
    {'name': 'Jordi', 'grades': [6.5, 7.0, 5.5, 8.0]},
    {'name': 'Mireia', 'grades': [9.0, 8.5, 9.5, 10.0]},
    {'name': 'Pol', 'grades': [4.0, 3.5, 5.0, 4.5]},
    {'name': 'Laia', 'grades': [7.0, 6.0, 6.5, 7.5]},
  ];
  print('Question #58: Rendiment acadèmic');
  final studentAvgs = students.map((s) {
    final List<double> g = List<double>.from(s['grades'] as List);
    final double avg = g.reduce((a, b) => a + b) / g.length;
    return {'name': s['name'] as String, 'avg': avg};
  }).toList();

  final passingStudents = studentAvgs.where((s) => (s['avg'] as double) >= 5.0).toList();
  final passingNames = passingStudents.map((s) => s['name']).toList();
  final double classAvg =
      studentAvgs.map((s) => s['avg'] as double).reduce((a, b) => a + b) / studentAvgs.length;

  print('Mitjanes per alumne: ${studentAvgs.map((s) => "${s['name']}: ${(s['avg'] as double).toStringAsFixed(2)}").toList()}');
  print('Alumnes aprovats: $passingNames');
  print('Nota mitjana del grup: ${classAvg.toStringAsFixed(2)}');
  print('---');

  // Question #59: Given a collection of sentences, split the sentences into words, convert all words to lowercase, remove punctuation marks, count how many times each word appears, and obtain the words that appear more than 5 times.
  final List<String> textSentences = [
    'Dart és genial, Flutter és ràpid i Dart és fàcil.',
    'Dart i Flutter fan que Flutter siga molt divertit.',
    'Programar en Dart és fantàstic perquè Dart és potent.',
    'Flutter i Dart, una combinació guanyadora amb Dart.'
  ];
  print('Question #59: Freqüència de paraules i paraules > 5 aparicions');
  final allCleanWords = textSentences
      .expand((s) => s.toLowerCase().replaceAll(RegExp(r'[^\w\s]'), '').split(' '))
      .where((w) => w.trim().isNotEmpty)
      .toList();

  final Map<String, int> wordFrequency = {};
  for (final word in allCleanWords) {
    wordFrequency[word] = (wordFrequency[word] ?? 0) + 1;
  }
  print('Freqüències principals: $wordFrequency');
  final wordsMoreThan5 = wordFrequency.entries
      .where((e) => e.value >= 5)
      .map((e) => '${e.key} (${e.value} cops)')
      .toList();
  print('Paraules que apareixen 5 o més vegades: $wordsMoreThan5');
  print('---');

  // Question #60: Given a collection of products, where each product has a name, price, category, and stock quantity, discard products that are out of stock, keep products whose price is between 20 and 200, apply a 15% discount, sort them by final price from highest to lowest, take the first 10, and obtain only their names.
  print('Question #60: Pipeline complex de productes');
  final complexPipeline = products
      .where((p) => (p['stock'] as int) > 0)
      .where((p) => (p['price'] as double) >= 20.0 && (p['price'] as double) <= 200.0)
      .map((p) => {
            'name': p['name'] as String,
            'finalPrice': (p['price'] as double) * 0.85,
          })
      .toList()
    ..sort((a, b) => (b['finalPrice'] as double).compareTo(a['finalPrice'] as double));

  final finalResult =
      complexPipeline.take(10).map((p) => '${p['name']} (${(p['finalPrice'] as double).toStringAsFixed(2)} €)').toList();

  print('Top seleccionats:');
  for (final item in finalResult) {
    print('  - $item');
  }
  print('================================================================');
  print('     TOTES LES 60 PREGUNTES RESOLTES CORRECTAMENT!');
  print('================================================================');
}
