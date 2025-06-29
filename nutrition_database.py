"""
Base de données nutritionnelle complète pour améliorer la reconnaissance d'aliments
Valeurs pour 100g sauf indication contraire
"""

# Base de données nutritionnelle étendue
NUTRITION_DATABASE = {
    # === LÉGUMES ===
    'salade': {'cal': 15, 'prot': 1.4, 'fat': 0.2, 'carb': 2.9},
    'salade verte': {'cal': 15, 'prot': 1.4, 'fat': 0.2, 'carb': 2.9},
    'laitue': {'cal': 15, 'prot': 1.4, 'fat': 0.2, 'carb': 2.9},
    'roquette': {'cal': 25, 'prot': 2.6, 'fat': 0.7, 'carb': 3.7},
    'épinards': {'cal': 23, 'prot': 2.9, 'fat': 0.4, 'carb': 3.6},
    'epinards': {'cal': 23, 'prot': 2.9, 'fat': 0.4, 'carb': 3.6},
    'mâche': {'cal': 21, 'prot': 2, 'fat': 0.4, 'carb': 3.5},
    'mache': {'cal': 21, 'prot': 2, 'fat': 0.4, 'carb': 3.5},
    
    'tomate': {'cal': 18, 'prot': 0.9, 'fat': 0.2, 'carb': 3.9},
    'tomates': {'cal': 18, 'prot': 0.9, 'fat': 0.2, 'carb': 3.9},
    'tomates cerises': {'cal': 18, 'prot': 0.9, 'fat': 0.2, 'carb': 3.9},
    'tomate cerise': {'cal': 18, 'prot': 0.9, 'fat': 0.2, 'carb': 3.9},
    
    'concombre': {'cal': 16, 'prot': 0.7, 'fat': 0.1, 'carb': 3.6},
    'cornichon': {'cal': 16, 'prot': 0.7, 'fat': 0.1, 'carb': 3.6},
    'cornichons': {'cal': 16, 'prot': 0.7, 'fat': 0.1, 'carb': 3.6},
    
    'carotte': {'cal': 41, 'prot': 0.9, 'fat': 0.2, 'carb': 10},
    'carottes': {'cal': 41, 'prot': 0.9, 'fat': 0.2, 'carb': 10},
    'carottes râpées': {'cal': 41, 'prot': 0.9, 'fat': 0.2, 'carb': 10},
    'carotte rapee': {'cal': 41, 'prot': 0.9, 'fat': 0.2, 'carb': 10},
    
    'radis': {'cal': 16, 'prot': 0.7, 'fat': 0.1, 'carb': 3.4},
    'betterave': {'cal': 43, 'prot': 1.6, 'fat': 0.2, 'carb': 10},
    'betteraves': {'cal': 43, 'prot': 1.6, 'fat': 0.2, 'carb': 10},
    
    'poivron': {'cal': 31, 'prot': 1, 'fat': 0.3, 'carb': 6},
    'poivrons': {'cal': 31, 'prot': 1, 'fat': 0.3, 'carb': 6},
    'poivron rouge': {'cal': 31, 'prot': 1, 'fat': 0.3, 'carb': 6},
    'poivron vert': {'cal': 20, 'prot': 0.9, 'fat': 0.2, 'carb': 4.6},
    
    'courgette': {'cal': 17, 'prot': 1.2, 'fat': 0.3, 'carb': 3.1},
    'courgettes': {'cal': 17, 'prot': 1.2, 'fat': 0.3, 'carb': 3.1},
    'aubergine': {'cal': 25, 'prot': 1, 'fat': 0.2, 'carb': 6},
    'aubergines': {'cal': 25, 'prot': 1, 'fat': 0.2, 'carb': 6},
    
    'brocoli': {'cal': 34, 'prot': 2.8, 'fat': 0.4, 'carb': 7},
    'brocolis': {'cal': 34, 'prot': 2.8, 'fat': 0.4, 'carb': 7},
    'chou-fleur': {'cal': 25, 'prot': 1.9, 'fat': 0.3, 'carb': 5},
    'chou fleur': {'cal': 25, 'prot': 1.9, 'fat': 0.3, 'carb': 5},
    'chou': {'cal': 25, 'prot': 1.3, 'fat': 0.1, 'carb': 6},
    
    'champignon': {'cal': 22, 'prot': 3.1, 'fat': 0.3, 'carb': 3.3},
    'champignons': {'cal': 22, 'prot': 3.1, 'fat': 0.3, 'carb': 3.3},
    'champignons de paris': {'cal': 22, 'prot': 3.1, 'fat': 0.3, 'carb': 3.3},
    
    'oignon': {'cal': 40, 'prot': 1.1, 'fat': 0.1, 'carb': 9.3},
    'oignons': {'cal': 40, 'prot': 1.1, 'fat': 0.1, 'carb': 9.3},
    'échalote': {'cal': 72, 'prot': 2.5, 'fat': 0.1, 'carb': 17},
    'echalote': {'cal': 72, 'prot': 2.5, 'fat': 0.1, 'carb': 17},
    'ail': {'cal': 149, 'prot': 6.4, 'fat': 0.5, 'carb': 33},
    
    # === FRUITS ===
    'pomme': {'cal': 52, 'prot': 0.3, 'fat': 0.2, 'carb': 14},
    'pommes': {'cal': 52, 'prot': 0.3, 'fat': 0.2, 'carb': 14},
    'poire': {'cal': 57, 'prot': 0.4, 'fat': 0.1, 'carb': 15},
    'poires': {'cal': 57, 'prot': 0.4, 'fat': 0.1, 'carb': 15},
    
    'banane': {'cal': 89, 'prot': 1.1, 'fat': 0.3, 'carb': 23},
    'bananes': {'cal': 89, 'prot': 1.1, 'fat': 0.3, 'carb': 23},
    
    'orange': {'cal': 47, 'prot': 0.9, 'fat': 0.1, 'carb': 12},
    'oranges': {'cal': 47, 'prot': 0.9, 'fat': 0.1, 'carb': 12},
    'mandarine': {'cal': 53, 'prot': 0.8, 'fat': 0.3, 'carb': 13},
    'mandarines': {'cal': 53, 'prot': 0.8, 'fat': 0.3, 'carb': 13},
    'clémentine': {'cal': 47, 'prot': 0.9, 'fat': 0.2, 'carb': 12},
    'clementine': {'cal': 47, 'prot': 0.9, 'fat': 0.2, 'carb': 12},
    'citron': {'cal': 29, 'prot': 1.1, 'fat': 0.3, 'carb': 9},
    'citrons': {'cal': 29, 'prot': 1.1, 'fat': 0.3, 'carb': 9},
    
    'fraise': {'cal': 32, 'prot': 0.7, 'fat': 0.3, 'carb': 8},
    'fraises': {'cal': 32, 'prot': 0.7, 'fat': 0.3, 'carb': 8},
    'framboise': {'cal': 52, 'prot': 1.2, 'fat': 0.7, 'carb': 12},
    'framboises': {'cal': 52, 'prot': 1.2, 'fat': 0.7, 'carb': 12},
    'myrtille': {'cal': 57, 'prot': 0.7, 'fat': 0.3, 'carb': 14},
    'myrtilles': {'cal': 57, 'prot': 0.7, 'fat': 0.3, 'carb': 14},
    'mûre': {'cal': 43, 'prot': 1.4, 'fat': 0.5, 'carb': 10},
    'mures': {'cal': 43, 'prot': 1.4, 'fat': 0.5, 'carb': 10},
    
    'raisin': {'cal': 69, 'prot': 0.7, 'fat': 0.2, 'carb': 17},
    'raisins': {'cal': 69, 'prot': 0.7, 'fat': 0.2, 'carb': 17},
    'kiwi': {'cal': 61, 'prot': 1.1, 'fat': 0.5, 'carb': 15},
    'kiwis': {'cal': 61, 'prot': 1.1, 'fat': 0.5, 'carb': 15},
    
    'avocat': {'cal': 160, 'prot': 2, 'fat': 15, 'carb': 9},
    'avocats': {'cal': 160, 'prot': 2, 'fat': 15, 'carb': 9},
    
    'ananas': {'cal': 50, 'prot': 0.5, 'fat': 0.1, 'carb': 13},
    'mangue': {'cal': 60, 'prot': 0.8, 'fat': 0.4, 'carb': 15},
    'papaye': {'cal': 43, 'prot': 0.5, 'fat': 0.3, 'carb': 11},
    
    # === PROTÉINES ANIMALES ===
    'poulet': {'cal': 239, 'prot': 27, 'fat': 14, 'carb': 0},
    'blanc de poulet': {'cal': 165, 'prot': 31, 'fat': 3.6, 'carb': 0},
    'cuisse de poulet': {'cal': 250, 'prot': 26, 'fat': 15, 'carb': 0},
    'escalope de poulet': {'cal': 165, 'prot': 31, 'fat': 3.6, 'carb': 0},
    
    'bœuf': {'cal': 250, 'prot': 26, 'fat': 15, 'carb': 0},
    'boeuf': {'cal': 250, 'prot': 26, 'fat': 15, 'carb': 0},
    'steak': {'cal': 250, 'prot': 26, 'fat': 15, 'carb': 0},
    'steack': {'cal': 250, 'prot': 26, 'fat': 15, 'carb': 0},
    'bœuf haché': {'cal': 254, 'prot': 26, 'fat': 16, 'carb': 0},
    'boeuf hache': {'cal': 254, 'prot': 26, 'fat': 16, 'carb': 0},
    'steak haché': {'cal': 254, 'prot': 26, 'fat': 16, 'carb': 0},
    'steak hache': {'cal': 254, 'prot': 26, 'fat': 16, 'carb': 0},
    
    'porc': {'cal': 242, 'prot': 27, 'fat': 14, 'carb': 0},
    'côte de porc': {'cal': 242, 'prot': 27, 'fat': 14, 'carb': 0},
    'cote de porc': {'cal': 242, 'prot': 27, 'fat': 14, 'carb': 0},
    'jambon': {'cal': 145, 'prot': 21, 'fat': 6, 'carb': 1},
    'jambon blanc': {'cal': 145, 'prot': 21, 'fat': 6, 'carb': 1},
    'jambon de bayonne': {'cal': 268, 'prot': 30, 'fat': 15, 'carb': 0},
    'lardons': {'cal': 541, 'prot': 13, 'fat': 53, 'carb': 1},
    
    'agneau': {'cal': 294, 'prot': 25, 'fat': 21, 'carb': 0},
    'gigot d\'agneau': {'cal': 294, 'prot': 25, 'fat': 21, 'carb': 0},
    'côtelette d\'agneau': {'cal': 294, 'prot': 25, 'fat': 21, 'carb': 0},
    
    # Poissons
    'saumon': {'cal': 208, 'prot': 20, 'fat': 13, 'carb': 0},
    'saumon fumé': {'cal': 117, 'prot': 25, 'fat': 4.3, 'carb': 0},
    'saumon fume': {'cal': 117, 'prot': 25, 'fat': 4.3, 'carb': 0},
    'thon': {'cal': 144, 'prot': 30, 'fat': 1, 'carb': 0},
    'thon en boite': {'cal': 116, 'prot': 26, 'fat': 1, 'carb': 0},
    'thon en boîte': {'cal': 116, 'prot': 26, 'fat': 1, 'carb': 0},
    'sardine': {'cal': 208, 'prot': 25, 'fat': 11, 'carb': 0},
    'sardines': {'cal': 208, 'prot': 25, 'fat': 11, 'carb': 0},
    'maquereau': {'cal': 205, 'prot': 19, 'fat': 14, 'carb': 0},
    'cabillaud': {'cal': 82, 'prot': 18, 'fat': 0.7, 'carb': 0},
    'colin': {'cal': 82, 'prot': 18, 'fat': 0.7, 'carb': 0},
    'sole': {'cal': 86, 'prot': 17, 'fat': 1.3, 'carb': 0},
    'dorade': {'cal': 96, 'prot': 20, 'fat': 1.8, 'carb': 0},
    'bar': {'cal': 97, 'prot': 18, 'fat': 2.5, 'carb': 0},
    'truite': {'cal': 119, 'prot': 20, 'fat': 3, 'carb': 0},
    
    # Fruits de mer
    'crevette': {'cal': 106, 'prot': 20, 'fat': 1.7, 'carb': 1},
    'crevettes': {'cal': 106, 'prot': 20, 'fat': 1.7, 'carb': 1},
    'moule': {'cal': 86, 'prot': 12, 'fat': 2.2, 'carb': 7},
    'moules': {'cal': 86, 'prot': 12, 'fat': 2.2, 'carb': 7},
    'huître': {'cal': 68, 'prot': 9, 'fat': 1.3, 'carb': 4.9},
    'huitres': {'cal': 68, 'prot': 9, 'fat': 1.3, 'carb': 4.9},
    'huîtres': {'cal': 68, 'prot': 9, 'fat': 1.3, 'carb': 4.9},
    'crabe': {'cal': 87, 'prot': 18, 'fat': 1.1, 'carb': 0},
    'homard': {'cal': 89, 'prot': 19, 'fat': 0.9, 'carb': 0.5},
    
    # Œufs et produits laitiers
    'œuf': {'cal': 155, 'prot': 13, 'fat': 11, 'carb': 1.1},
    'oeuf': {'cal': 155, 'prot': 13, 'fat': 11, 'carb': 1.1},
    'oeufs': {'cal': 155, 'prot': 13, 'fat': 11, 'carb': 1.1},
    'œufs': {'cal': 155, 'prot': 13, 'fat': 11, 'carb': 1.1},
    'blanc d\'œuf': {'cal': 52, 'prot': 11, 'fat': 0.2, 'carb': 0.7},
    'blanc d\'oeuf': {'cal': 52, 'prot': 11, 'fat': 0.2, 'carb': 0.7},
    'jaune d\'œuf': {'cal': 322, 'prot': 16, 'fat': 27, 'carb': 3.6},
    'jaune d\'oeuf': {'cal': 322, 'prot': 16, 'fat': 27, 'carb': 3.6},
    
    'lait': {'cal': 42, 'prot': 3.4, 'fat': 1, 'carb': 5},
    'lait entier': {'cal': 61, 'prot': 3.2, 'fat': 3.2, 'carb': 4.8},
    'lait demi-écrémé': {'cal': 46, 'prot': 3.3, 'fat': 1.6, 'carb': 4.8},
    'lait demi-ecreme': {'cal': 46, 'prot': 3.3, 'fat': 1.6, 'carb': 4.8},
    'lait écrémé': {'cal': 34, 'prot': 3.4, 'fat': 0.1, 'carb': 4.9},
    'lait ecreme': {'cal': 34, 'prot': 3.4, 'fat': 0.1, 'carb': 4.9},
    
    'yaourt': {'cal': 59, 'prot': 3.5, 'fat': 3.3, 'carb': 4.6},
    'yaourt nature': {'cal': 59, 'prot': 3.5, 'fat': 3.3, 'carb': 4.6},
    'yaourt grec': {'cal': 59, 'prot': 10, 'fat': 0.4, 'carb': 4},
    'fromage blanc': {'cal': 75, 'prot': 8, 'fat': 3, 'carb': 4.5},
    'fromage blanc 0%': {'cal': 47, 'prot': 8, 'fat': 0.2, 'carb': 4.5},
    'skyr': {'cal': 57, 'prot': 11, 'fat': 0.2, 'carb': 4},
    
    # Fromages
    'fromage': {'cal': 402, 'prot': 25, 'fat': 33, 'carb': 1.3},
    'emmental': {'cal': 382, 'prot': 28, 'fat': 29, 'carb': 0.4},
    'gruyère': {'cal': 413, 'prot': 29, 'fat': 32, 'carb': 0.4},
    'gruyere': {'cal': 413, 'prot': 29, 'fat': 32, 'carb': 0.4},
    'comté': {'cal': 409, 'prot': 27, 'fat': 33, 'carb': 0.4},
    'comte': {'cal': 409, 'prot': 27, 'fat': 33, 'carb': 0.4},
    'camembert': {'cal': 299, 'prot': 20, 'fat': 24, 'carb': 0.5},
    'brie': {'cal': 334, 'prot': 21, 'fat': 27, 'carb': 0.5},
    'roquefort': {'cal': 369, 'prot': 22, 'fat': 31, 'carb': 2},
    'chèvre': {'cal': 364, 'prot': 22, 'fat': 30, 'carb': 2.5},
    'chevre': {'cal': 364, 'prot': 22, 'fat': 30, 'carb': 2.5},
    'mozzarella': {'cal': 280, 'prot': 18, 'fat': 22, 'carb': 2.2},
    'parmesan': {'cal': 431, 'prot': 38, 'fat': 29, 'carb': 4.1},
    'feta': {'cal': 264, 'prot': 14, 'fat': 21, 'carb': 4.1},
    
    # === FÉCULENTS ===
    'riz': {'cal': 130, 'prot': 2.7, 'fat': 0.3, 'carb': 28},
    'riz blanc': {'cal': 130, 'prot': 2.7, 'fat': 0.3, 'carb': 28},
    'riz complet': {'cal': 111, 'prot': 2.6, 'fat': 0.9, 'carb': 23},
    'riz basmati': {'cal': 130, 'prot': 2.7, 'fat': 0.3, 'carb': 28},
    'riz thai': {'cal': 130, 'prot': 2.7, 'fat': 0.3, 'carb': 28},
    'riz thaï': {'cal': 130, 'prot': 2.7, 'fat': 0.3, 'carb': 28},
    
    'pâtes': {'cal': 131, 'prot': 5, 'fat': 1.1, 'carb': 25},
    'pates': {'cal': 131, 'prot': 5, 'fat': 1.1, 'carb': 25},
    'spaghetti': {'cal': 131, 'prot': 5, 'fat': 1.1, 'carb': 25},
    'penne': {'cal': 131, 'prot': 5, 'fat': 1.1, 'carb': 25},
    'fusilli': {'cal': 131, 'prot': 5, 'fat': 1.1, 'carb': 25},
    'tagliatelle': {'cal': 131, 'prot': 5, 'fat': 1.1, 'carb': 25},
    'linguine': {'cal': 131, 'prot': 5, 'fat': 1.1, 'carb': 25},
    
    'pomme de terre': {'cal': 77, 'prot': 2, 'fat': 0.1, 'carb': 17},
    'pommes de terre': {'cal': 77, 'prot': 2, 'fat': 0.1, 'carb': 17},
    'patate': {'cal': 77, 'prot': 2, 'fat': 0.1, 'carb': 17},
    'patates': {'cal': 77, 'prot': 2, 'fat': 0.1, 'carb': 17},
    'patate douce': {'cal': 86, 'prot': 1.6, 'fat': 0.1, 'carb': 20},
    'patates douces': {'cal': 86, 'prot': 1.6, 'fat': 0.1, 'carb': 20},
    
    'pain': {'cal': 265, 'prot': 9, 'fat': 3.2, 'carb': 49},
    'pain blanc': {'cal': 265, 'prot': 9, 'fat': 3.2, 'carb': 49},
    'pain complet': {'cal': 247, 'prot': 13, 'fat': 4.2, 'carb': 41},
    'pain de mie': {'cal': 265, 'prot': 9, 'fat': 3.2, 'carb': 49},
    'baguette': {'cal': 265, 'prot': 9, 'fat': 3.2, 'carb': 49},
    'pain burger': {'cal': 265, 'prot': 9, 'fat': 3.2, 'carb': 49},
    'bun burger': {'cal': 265, 'prot': 9, 'fat': 3.2, 'carb': 49},
    'pain pita': {'cal': 275, 'prot': 9.1, 'fat': 1.2, 'carb': 55},
    'tortilla': {'cal': 304, 'prot': 8.2, 'fat': 7.7, 'carb': 49},
    
    'quinoa': {'cal': 120, 'prot': 4.4, 'fat': 1.9, 'carb': 22},
    'boulgour': {'cal': 83, 'prot': 3.1, 'fat': 0.2, 'carb': 19},
    'bulgur': {'cal': 83, 'prot': 3.1, 'fat': 0.2, 'carb': 19},
    'semoule': {'cal': 112, 'prot': 3.9, 'fat': 0.7, 'carb': 23},
    'couscous': {'cal': 112, 'prot': 3.9, 'fat': 0.7, 'carb': 23},
    
    # === LÉGUMINEUSES ===
    'lentilles': {'cal': 116, 'prot': 9, 'fat': 0.4, 'carb': 20},
    'lentilles vertes': {'cal': 116, 'prot': 9, 'fat': 0.4, 'carb': 20},
    'lentilles corail': {'cal': 116, 'prot': 9, 'fat': 0.4, 'carb': 20},
    'lentilles rouges': {'cal': 116, 'prot': 9, 'fat': 0.4, 'carb': 20},
    
    'haricots': {'cal': 127, 'prot': 8.7, 'fat': 0.5, 'carb': 23},
    'haricots rouges': {'cal': 127, 'prot': 8.7, 'fat': 0.5, 'carb': 23},
    'haricots blancs': {'cal': 139, 'prot': 9.7, 'fat': 0.5, 'carb': 25},
    'haricots noirs': {'cal': 132, 'prot': 8.9, 'fat': 0.5, 'carb': 24},
    'haricots verts': {'cal': 35, 'prot': 1.8, 'fat': 0.1, 'carb': 8},
    
    'pois chiches': {'cal': 164, 'prot': 8.9, 'fat': 2.6, 'carb': 27},
    'pois chiche': {'cal': 164, 'prot': 8.9, 'fat': 2.6, 'carb': 27},
    'houmous': {'cal': 166, 'prot': 8, 'fat': 10, 'carb': 14},
    'hummus': {'cal': 166, 'prot': 8, 'fat': 10, 'carb': 14},
    
    'petits pois': {'cal': 84, 'prot': 5.4, 'fat': 0.4, 'carb': 16},
    'pois cassés': {'cal': 118, 'prot': 8.3, 'fat': 0.8, 'carb': 21},
    'pois casses': {'cal': 118, 'prot': 8.3, 'fat': 0.8, 'carb': 21},
    
    # === CÉRÉALES ET GRAINES ===
    'flocons d\'avoine': {'cal': 389, 'prot': 16.9, 'fat': 6.9, 'carb': 66},
    'avoine': {'cal': 389, 'prot': 16.9, 'fat': 6.9, 'carb': 66},
    'muesli': {'cal': 367, 'prot': 10, 'fat': 6, 'carb': 66},
    'granola': {'cal': 471, 'prot': 10, 'fat': 20, 'carb': 65},
    
    # === OLÉAGINEUX ===
    'amandes': {'cal': 579, 'prot': 21, 'fat': 50, 'carb': 22},
    'amande': {'cal': 579, 'prot': 21, 'fat': 50, 'carb': 22},
    'noix': {'cal': 654, 'prot': 15, 'fat': 65, 'carb': 14},
    'noisettes': {'cal': 628, 'prot': 15, 'fat': 61, 'carb': 17},
    'noisette': {'cal': 628, 'prot': 15, 'fat': 61, 'carb': 17},
    'pistaches': {'cal': 560, 'prot': 20, 'fat': 45, 'carb': 28},
    'pistache': {'cal': 560, 'prot': 20, 'fat': 45, 'carb': 28},
    'cacahuètes': {'cal': 567, 'prot': 26, 'fat': 49, 'carb': 16},
    'cacahuetes': {'cal': 567, 'prot': 26, 'fat': 49, 'carb': 16},
    'arachides': {'cal': 567, 'prot': 26, 'fat': 49, 'carb': 16},
    
    # === GRAINES ===
    'graines de tournesol': {'cal': 584, 'prot': 21, 'fat': 51, 'carb': 20},
    'graines de courge': {'cal': 559, 'prot': 30, 'fat': 49, 'carb': 11},
    'graines de lin': {'cal': 534, 'prot': 18, 'fat': 42, 'carb': 29},
    'graines de chia': {'cal': 486, 'prot': 17, 'fat': 31, 'carb': 42},
    'graines de sésame': {'cal': 573, 'prot': 18, 'fat': 50, 'carb': 23},
    
    # === MATIÈRES GRASSES ===
    'huile d\'olive': {'cal': 884, 'prot': 0, 'fat': 100, 'carb': 0},
    'huile olive': {'cal': 884, 'prot': 0, 'fat': 100, 'carb': 0},
    'huile de tournesol': {'cal': 884, 'prot': 0, 'fat': 100, 'carb': 0},
    'huile de colza': {'cal': 884, 'prot': 0, 'fat': 100, 'carb': 0},
    'beurre': {'cal': 717, 'prot': 0.9, 'fat': 81, 'carb': 0.1},
    'margarine': {'cal': 717, 'prot': 0.2, 'fat': 80, 'carb': 0.4},
    
    # === CONDIMENTS ET SAUCES ===
    'sauce tomate': {'cal': 29, 'prot': 1.6, 'fat': 0.2, 'carb': 7},
    'ketchup': {'cal': 112, 'prot': 1.2, 'fat': 0.1, 'carb': 27},
    'mayonnaise': {'cal': 680, 'prot': 1.3, 'fat': 75, 'carb': 0.6},
    'moutarde': {'cal': 66, 'prot': 4.4, 'fat': 3.3, 'carb': 5.8},
    'vinaigre': {'cal': 18, 'prot': 0, 'fat': 0, 'carb': 0.04},
    'vinaigre balsamique': {'cal': 88, 'prot': 0.5, 'fat': 0, 'carb': 17},
    
    # === SUCRES ET ÉDULCORANTS ===
    'sucre': {'cal': 387, 'prot': 0, 'fat': 0, 'carb': 100},
    'miel': {'cal': 304, 'prot': 0.3, 'fat': 0, 'carb': 82},
    'sirop d\'érable': {'cal': 260, 'prot': 0, 'fat': 0.2, 'carb': 67},
    'confiture': {'cal': 278, 'prot': 0.4, 'fat': 0.1, 'carb': 69},
    
    # === BOISSONS ===
    'eau': {'cal': 0, 'prot': 0, 'fat': 0, 'carb': 0},
    'thé': {'cal': 1, 'prot': 0, 'fat': 0, 'carb': 0.3},
    'café': {'cal': 2, 'prot': 0.1, 'fat': 0, 'carb': 0.5},
    'jus d\'orange': {'cal': 45, 'prot': 0.7, 'fat': 0.2, 'carb': 10},
    'jus de pomme': {'cal': 46, 'prot': 0.1, 'fat': 0.1, 'carb': 11},
    'coca cola': {'cal': 42, 'prot': 0, 'fat': 0, 'carb': 10.6},
    'coca': {'cal': 42, 'prot': 0, 'fat': 0, 'carb': 10.6},
    
    # === SUPPLÉMENTS ===
    'whey': {'cal': 400, 'prot': 80, 'fat': 5, 'carb': 5},
    'protéine whey': {'cal': 400, 'prot': 80, 'fat': 5, 'carb': 5},
    'proteine whey': {'cal': 400, 'prot': 80, 'fat': 5, 'carb': 5},
    'créatine': {'cal': 0, 'prot': 0, 'fat': 0, 'carb': 0},
    'creatine': {'cal': 0, 'prot': 0, 'fat': 0, 'carb': 0},
}

# Synonymes et variantes pour améliorer la reconnaissance
FOOD_SYNONYMS = {
    'blanc de poulet': ['escalope de poulet', 'filet de poulet'],
    'bœuf': ['boeuf', 'viande de bœuf', 'viande de boeuf'],
    'œuf': ['oeuf'],
    'œufs': ['oeufs'],
    'pâtes': ['pates', 'pasta'],
    'pommes de terre': ['patates', 'pomme de terre'],
    'tomates cerises': ['tomate cerise', 'cherry tomatoes'],
    'salade verte': ['salade', 'laitue', 'mesclun'],
    'fromage blanc': ['faisselle'],
    'yaourt grec': ['yaourt à la grecque'],
}

def find_food_in_database(food_name):
    """
    Recherche intelligente d'un aliment dans la base de données
    Retourne les valeurs nutritionnelles pour 100g ou None si non trouvé
    """
    food_lower = food_name.lower().strip()
    
    # 1. Recherche exacte
    if food_lower in NUTRITION_DATABASE:
        return NUTRITION_DATABASE[food_lower]
    
    # 2. Recherche dans les synonymes
    for main_food, synonyms in FOOD_SYNONYMS.items():
        if food_lower in [s.lower() for s in synonyms]:
            return NUTRITION_DATABASE.get(main_food.lower())
    
    # 3. Recherche partielle (contient)
    for db_food, values in NUTRITION_DATABASE.items():
        if food_lower in db_food or db_food in food_lower:
            return values
    
    # 4. Recherche par mots-clés
    food_words = food_lower.split()
    for db_food, values in NUTRITION_DATABASE.items():
        db_words = db_food.split()
        if any(word in db_words for word in food_words):
            return values
    
    return None

def get_nutrition_for_ingredient(ingredient, grams):
    """
    Fonction améliorée pour obtenir les valeurs nutritionnelles
    Utilise la nouvelle base de données étendue
    """
    nutrition_data = find_food_in_database(ingredient)
    
    if nutrition_data:
        ratio = grams / 100.0
        return {
            'calories': nutrition_data['cal'] * ratio,
            'proteins': nutrition_data['prot'] * ratio,
            'fats': nutrition_data['fat'] * ratio,
            'carbs': nutrition_data['carb'] * ratio
        }
    
    # Valeur par défaut si aliment non trouvé (légume générique)
    print(f"⚠️ Aliment '{ingredient}' non trouvé dans la base, utilisation valeurs par défaut")
    return {
        'calories': 25 * grams / 100, 
        'proteins': 1.5 * grams / 100, 
        'fats': 0.3 * grams / 100, 
        'carbs': 5 * grams / 100
    }
