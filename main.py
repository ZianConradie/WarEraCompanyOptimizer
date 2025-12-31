from collections import defaultdict

# Recipes: product -> raw material requirements
PRODUCT_RECIPES = {
    # Ammo
    "Light Ammo": {"Lead": 1},
    "Medium Ammo": {"Lead": 1, "Steel": 1},
    "Heavy Ammo": {"Lead": 1},
    # Food
    "Bread": {"Grain": 1},
    "Steak": {"Livestock": 1},
    "Cooked Fish": {"Fish": 1},
    # Boost
    "Pill": {"Mysterious Plant": 1},
    # Money / Infrastructure
    "Steel": {"Iron": 1},
    "Concrete": {"Limestone": 1},
}

# Priority orders
FOOD_PRIORITY_PRODUCTS = ["Bread", "Steak", "Cooked Fish"]
AMMO_PRIORITY_PRODUCTS = ["Heavy Ammo", "Medium Ammo", "Light Ammo"]
MONEY_PRIORITY_PRODUCTS = ["Steel", "Concrete"]


def count_required_companies(plan, product):
    """Count companies needed to ADD ONE MORE of product + its missing raw materials."""
    needed = 1  # the product itself
    for ingredient, amount in PRODUCT_RECIPES.get(product, {}).items():
        if plan[ingredient] == 0:
            needed += amount
    return needed


def add_product(plan, product):
    """Add ONE unit of product and its missing raw materials to plan."""
    plan[product] += 1
    for req, amount in PRODUCT_RECIPES.get(product, {}).items():
        if plan[req] == 0:
            plan[req] += amount


def add_product_with_materials(plan, product):
    """Add ONE unit of product AND ONE unit of each required raw material."""
    plan[product] += 1
    for req, amount in PRODUCT_RECIPES.get(product, {}).items():
        plan[req] += amount


# ---------------- DamageDealer ----------------
def optimize_damage(total_companies):
    plan = defaultdict(int)
    remaining_companies = total_companies

    # 1. Food first
    for food in FOOD_PRIORITY_PRODUCTS:
        required_food_companies = count_required_companies(plan, food)
        if required_food_companies <= remaining_companies:
            add_product(plan, food)
            remaining_companies -= required_food_companies
            break  # only one food

    # 2. Ammo next
    for ammo in AMMO_PRIORITY_PRODUCTS:
        required_ammo_companies = count_required_companies(plan, ammo)
        if required_ammo_companies <= remaining_companies:
            add_product(plan, ammo)
            remaining_companies -= required_ammo_companies
            break  # only one ammo

    # 3. Boost
    needed_boost_companies = count_required_companies(plan, "Pill")
    if needed_boost_companies <= remaining_companies:
        add_product(plan, "Pill")
        remaining_companies -= needed_boost_companies

    # 4. Money - keep adding until we run out of companies
    while remaining_companies > 0:
        added = False
        for product in MONEY_PRIORITY_PRODUCTS:
            # Cost is always 2: 1 for product + 1 for raw material
            cost = 2
            if cost <= remaining_companies:
                add_product_with_materials(plan, product)
                remaining_companies -= cost
                added = True
                break
        if not added:
            break

    return plan


# ---------------- Eco ----------------
def optimize_eco(total_companies):
    plan = defaultdict(int)
    remaining_companies = total_companies

    product_index = 0
    while remaining_companies > 0:
        cost = 2
        if cost <= remaining_companies:
            product = MONEY_PRIORITY_PRODUCTS[product_index]
            add_product_with_materials(plan, product)
            remaining_companies -= cost
            # Alternate between products
            product_index = (product_index + 1) % len(MONEY_PRIORITY_PRODUCTS)
        else:
            break

    return plan


# ---------------- Display ----------------
def display(plan):
    print("\n=== WarEra Company Setup ===\n")
    total = 0
    for item, count in sorted(plan.items()):
        print(f"{item}: {count}")
        total += count
    print(f"\nTotal companies used: {total}\n")


# ---------------- Main ----------------
def main():
    mode = input("Mode (eco/damage): ").strip().lower()
    companies = int(input("Number of companies: "))

    if mode == "damage":
        plan = optimize_damage(companies)
    elif mode == "eco":
        plan = optimize_eco(companies)
    else:
        print("Unknown mode.")
        return

    display(plan)


if __name__ == "__main__":
    main()