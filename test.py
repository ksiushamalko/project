from database import Database

def main():
    _db = Database() 

    print("TEST 1: Connection")
    try:
        products = _db.get_all_products()
        print(f"OK. Found {len(products)} products.")
    except Exception as e:
        print(f"Error: {e}")
        return

    print("\nTEST 2: Search for omlet")
    user_products = ['яйца', 'молоко', 'соль']
    recipes = _db.find_recipes(user_products)
    if recipes:
        print(f"Found {len(recipes)} recipe(s):")
        for r in recipes:
            print(f"  - {r.name}")
    else:
        print("No recipes. Order pizza?")

    print("\nTEST 3: Search with more products")
    user_products = ['яйца', 'молоко', 'соль', 'хлеб', 'сыр', 'масло сливочное']
    recipes = _db.find_recipes(user_products)
    if recipes:
        print(f"Found {len(recipes)} recipe(s):")
        for r in recipes:
            print(f"  - {r.name}")
    else:
        print("No recipes. Order pizza?")

    print("\nTEST 4: Empty fridge")
    recipes = _db.find_recipes([])
    if recipes:
        print(f"Found {len(recipes)} recipes (should be 0)")
    else:
        print("No recipes. Order pizza?")

    print("\nTEST 5: Missing ingredients")
    user_products = ['молоко', 'соль']
    recipes = _db.find_recipes(user_products)
    if recipes:
        print(f"Found {len(recipes)} recipes (should be 0)")
    else:
        print("No recipes. Order pizza?")

    print("\nTEST 6: Case insensitivity")
    user_products = ['ЯЙЦА', 'Молоко', 'СОЛЬ']
    recipes = _db.find_recipes(user_products)
    if recipes:
        print(f"Found {len(recipes)} recipe(s):")
        for r in recipes:
            print(f"  - {r.name}")
    else:
        print("No recipes. Order pizza?")

    _db.close()
    print("\nAll tests finished.")

if __name__ == '__main__':
    main()
