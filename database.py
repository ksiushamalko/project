import sqlite3

class Recipe:
    def __init__(self, id, name, instructions):
        self.id = id
        self.name = name
        self.instructions = instructions

    def __str__(self):
        return f"{self.name}: {self.instructions}"

class Database:
    def __init__(self, db_name='fridge.db'):
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def find_recipes(self, user_products):
        if not user_products:
            return []
        
        user_products_lower = [p.lower().strip() for p in user_products]
        
        self.cursor.execute('SELECT id, name, instructions FROM recipes')
        all_recipes = self.cursor.fetchall()
        
        result = []
        for recipe in all_recipes:
            recipe_id = recipe['id']
            
            self.cursor.execute('''
                SELECT p.name 
                FROM recipe_products rp
                JOIN products p ON rp.product_id = p.id
                WHERE rp.recipe_id = ?
            ''', (recipe_id,))
            
            required_products = [row['name'].lower() for row in self.cursor.fetchall()]
            
            has_all = True
            for prod in required_products:
                if prod not in user_products_lower:
                    has_all = False
                    break
            
            if has_all:
                result.append(Recipe(recipe['id'], recipe['name'], recipe['instructions']))
        
        return result

    def get_all_products(self):
        self.cursor.execute('SELECT name FROM products ORDER BY name')
        return [row['name'] for row in self.cursor.fetchall()]

    def close(self):
        self.conn.close()