import sqlite3

def create_database():
    conn = sqlite3.connect('fridge.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        instructions TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS recipe_products (
        recipe_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        amount TEXT,
        PRIMARY KEY (recipe_id, product_id),
        FOREIGN KEY (recipe_id) REFERENCES recipes (id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
    )
    ''')

    products = [
        'яйца', 'молоко', 'мука', 'сахар', 'соль',
        'масло сливочное', 'хлеб', 'сыр', 'колбаса',
        'картошка', 'лук', 'помидоры', 'огурцы',
        'рис', 'гречка', 'курица', 'чеснок'
    ]
    for p in products:
        cursor.execute('INSERT OR IGNORE INTO products (name) VALUES (?)', (p,))

    recipes = [
        ('Омлет', 'Взбить яйца с молоком и солью. Пожарить на сковороде 5 минут.'),
        ('Бутерброд с сыром', 'Положить сыр на хлеб. Разогреть в микроволновке 30 секунд.'),
        ('Гречка с маслом', 'Сварить гречку. Добавить сливочное масло.'),
        ('Яичница', 'Разбить яйца на сковороду. Жарить до готовности. Посолить.'),
        ('Салат из огурцов и помидоров', 'Нарезать огурцы и помидоры. Посолить. Заправить маслом.'),
        ('Курица с чесноком', 'Натереть курицу чесноком и солью. Запечь 40 минут.'),
        ('Картошка жареная', 'Нарезать картошку и лук. Обжарить на масле.'),
        ('Сладкий бутерброд', 'Намазать хлеб маслом, посыпать сахаром.')
    ]
    for name, instr in recipes:
        cursor.execute('INSERT OR IGNORE INTO recipes (name, instructions) VALUES (?, ?)', (name, instr))

    cursor.execute('SELECT id, name FROM products')
    product_ids = {name: id for id, name in cursor.fetchall()}

    cursor.execute('SELECT id, name FROM recipes')
    recipe_ids = {name: id for id, name in cursor.fetchall()}

    links = [
        (recipe_ids['Омлет'], product_ids['яйца'], '2 шт'),
        (recipe_ids['Омлет'], product_ids['молоко'], '50 мл'),
        (recipe_ids['Омлет'], product_ids['соль'], 'щепотка'),
        (recipe_ids['Бутерброд с сыром'], product_ids['хлеб'], '2 куска'),
        (recipe_ids['Бутерброд с сыром'], product_ids['сыр'], '50 г'),
        (recipe_ids['Гречка с маслом'], product_ids['гречка'], '1 стакан'),
        (recipe_ids['Гречка с маслом'], product_ids['масло сливочное'], '20 г'),
        (recipe_ids['Яичница'], product_ids['яйца'], '2 шт'),
        (recipe_ids['Яичница'], product_ids['соль'], 'щепотка'),
        (recipe_ids['Салат из огурцов и помидоров'], product_ids['огурцы'], '2 шт'),
        (recipe_ids['Салат из огурцов и помидоров'], product_ids['помидоры'], '2 шт'),
        (recipe_ids['Салат из огурцов и помидоров'], product_ids['соль'], 'по вкусу'),
        (recipe_ids['Салат из огурцов и помидоров'], product_ids['масло сливочное'], '1 ст.л'),
        (recipe_ids['Курица с чесноком'], product_ids['курица'], '1 шт'),
        (recipe_ids['Курица с чесноком'], product_ids['чеснок'], '3 зубчика'),
        (recipe_ids['Курица с чесноком'], product_ids['соль'], 'по вкусу'),
        (recipe_ids['Картошка жареная'], product_ids['картошка'], '4 шт'),
        (recipe_ids['Картошка жареная'], product_ids['лук'], '1 шт'),
        (recipe_ids['Картошка жареная'], product_ids['масло сливочное'], '2 ст.л'),
        (recipe_ids['Сладкий бутерброд'], product_ids['хлеб'], '1 кусок'),
        (recipe_ids['Сладкий бутерброд'], product_ids['масло сливочное'], '10 г'),
        (recipe_ids['Сладкий бутерброд'], product_ids['сахар'], '1 ч.л'),
    ]
    for recipe_id, product_id, amount in links:
        cursor.execute('INSERT OR IGNORE INTO recipe_products (recipe_id, product_id, amount) VALUES (?, ?, ?)',
                       (recipe_id, product_id, amount))

    conn.commit()
    conn.close()
    print("Database 'fridge.db' created and filled.")

if __name__ == '__main__':
    create_database()