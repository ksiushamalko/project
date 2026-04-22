import sqlite3

class Recipe:
    def __init__(self, id, name, instructions):
        self._id = id          
        self._name = name      
        self._instructions = instructions 

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def instructions(self):
        return self._instructions

    def __str__(self):
        return f"{self._name}: {self._instructions}"


class DatabaseConnection:
    _instance = None
    _conn = None
    _cursor = None

    def __new__(cls, db_name='fridge.db'):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._conn = sqlite3.connect(db_name)
            cls._instance._conn.row_factory = sqlite3.Row
            cls._instance._cursor = cls._instance._conn.cursor()
        return cls._instance

    def get_connection(self):
        return self._conn

    def get_cursor(self):
        return self._cursor

    def close(self):
        if self._conn:
            self._conn.close()
            DatabaseConnection._instance = None


class Database:
    def __init__(self):
        self._db = DatabaseConnection()
        self._conn = self._db.get_connection()
        self._cursor = self._db.get_cursor()

    def find_recipes(self, user_products):
        if not user_products:
            return []
        
        user_products_lower = [p.lower().strip() for p in user_products]
        
        self._cursor.execute('SELECT id, name, instructions FROM recipes')
        all_recipes = self._cursor.fetchall()
        
        result = []
        for recipe in all_recipes:
            recipe_id = recipe['id']
            
            self._cursor.execute('''
                SELECT p.name 
                FROM recipe_products rp
                JOIN products p ON rp.product_id = p.id
                WHERE rp.recipe_id = ?
            ''', (recipe_id,))
            
            required_products = [row['name'].lower() for row in self._cursor.fetchall()]
            
            has_all = True
            for prod in required_products:
                if prod not in user_products_lower:
                    has_all = False
                    break
            
            if has_all:
                result.append(Recipe(recipe['id'], recipe['name'], recipe['instructions']))
        
        return result

    def get_all_products(self):
        self._cursor.execute('SELECT name FROM products ORDER BY name')
        return [row['name'] for row in self._cursor.fetchall()]

    def close(self):
        self._db.close()
