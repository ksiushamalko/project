from tkinter import *
from database import Database

root = Tk()
root.geometry("700x600")
root.title("Холодильник - Поиск рецептов")

db = Database()

def search_recipes():
    products_input = entry.get()
    
    if not products_input.strip():
        label_result.config(text="Введите хотя бы один продукт")
        return
    
    products_list = [p.strip() for p in products_input.split(',')]
    user_products_lower = set(p.lower().strip() for p in products_list)
    
    text_result.delete(1.0, END)
    
    recipes = db.find_recipes(products_list)
    
    if recipes:
        text_result.insert(END, "МОЖНО ПРИГОТОВИТЬ:\n\n")
        for r in recipes:
            text_result.insert(END, f"  {r.name}\n")
            text_result.insert(END, f"  {r.instructions}\n\n")
        label_result.config(text="")
        return
    
    text_result.insert(END, "Рецептов не найдено.\n\n")
    
    db.cursor.execute('SELECT id, name, instructions FROM recipes')
    all_recipes = db.cursor.fetchall()
    
    best_recipe = None
    best_match_count = 0
    best_missing = []
    
    for recipe in all_recipes:
        recipe_id = recipe['id']
        
        db.cursor.execute('''
            SELECT p.name 
            FROM recipe_products rp
            JOIN products p ON rp.product_id = p.id
            WHERE rp.recipe_id = ?
        ''', (recipe_id,))
        required = [row['name'].lower() for row in db.cursor.fetchall()]
        required_products = set(required)
        
        have_products = user_products_lower & required_products
        match_count = len(have_products)
        
        if match_count > best_match_count:
            best_match_count = match_count
            best_recipe = recipe
            best_missing = list(required_products - user_products_lower)
    
    if best_recipe and best_match_count > 0:
        text_result.insert(END, f"Ближайший рецепт: {best_recipe['name']}\n")
        text_result.insert(END, f"  {best_recipe['instructions']}\n\n")
        text_result.insert(END, f"У вас есть: {best_match_count} из {best_match_count + len(best_missing)} продуктов\n")
        
        if best_missing:
            text_result.insert(END, f"Не хватает: {', '.join(best_missing)}\n\n")
        
        if len(best_missing) <= 2:
            label_result.config(text="Сходите в магазин за этими продуктами!")
        else:
            label_result.config(text="Лучше закажите пиццу! Доставка: https://dodopizza.ru")
    else:
        label_result.config(text="У вас нет продуктов ни для одного рецепта. Закажите пиццу!")

def clear_all():
    entry.delete(0, END)
    text_result.delete(1.0, END)
    label_result.config(text="")

def on_closing():
    db.close()
    root.destroy()

label_title = Label(
    root,
    text="Что у вас есть в холодильнике?",
    font=("Arial", 16, "bold")
)

label_instruction = Label(
    root,
    text="Введите продукты через запятую (например: яйца, молоко, соль)",
    font=("Arial", 10)
)

entry = Entry(
    root,
    width=50,
    font=("Arial", 12)
)

button_search = Button(
    root,
    text="Найти рецепты",
    command=search_recipes,
    bg="lightblue",
    font=("Arial", 12)
)

button_clear = Button(
    root,
    text="Очистить",
    command=clear_all,
    bg="lightgray",
    font=("Arial", 12)
)

text_result = Text(
    root,
    width=80,
    height=22,
    font=("Arial", 10),
    wrap=WORD
)

label_result = Label(
    root,
    text="",
    font=("Arial", 12),
    fg="#4682B4",
    bg = "#ADD8E6"
)

label_title.place(x=160, y=10, width=400, height=30)
label_instruction.place(x=150, y=50, width=400, height=20)
entry.place(x=150, y=80, width=400, height=30)
button_search.place(x=200, y=120, width=150, height=35)
button_clear.place(x=370, y=120, width=120, height=35)
text_result.place(x=50, y=170, width=600, height=300)

label_result.place(x=50, y=480, width=600, height=40)

root.mainloop()