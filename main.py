from collections import defaultdict

# Recipes: product -> raw material requirements
RECIPES = {
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
FOOD_PRIORITY = ["Bread", "Steak", "Cooked Fish"]
AMMO_PRIORITY = ["Heavy Ammo", "Medium Ammo", "Light Ammo"]
MONEY_PRIORITY = ["Steel", "Concrete"]

def count_needed(plan, product):
    """Count companies needed for product + missing raw materials."""
    needed = 1  # the product itself
    for req in RECIPES.get(product, {}):
        if plan[req] == 0:
            needed += 1
    return needed

def add_product(plan, product):
    """Add product and its missing raw materials to plan."""
    plan[product] += 1
    for req in RECIPES.get(product, {}):
        if plan[req] == 0:
            plan[req] += 1

# ---------------- DamageDealer ----------------
def optimize_damage(total_companies):
    plan = defaultdict(int)
    remaining = total_companies

    # 1. Food first
    for food in FOOD_PRIORITY:
        needed_food = count_needed(plan, food)
        if needed_food <= remaining:
            add_product(plan, food)
            remaining -= needed_food
            break  # only one food

    # 2. Ammo next
    for ammo in AMMO_PRIORITY:
        needed_ammo = count_needed(plan, ammo)
        if needed_ammo <= remaining:
            add_product(plan, ammo)
            remaining -= needed_ammo
            break  # only one ammo

    # 3. Boost
    needed_boost = count_needed(plan, "Pill")
    if needed_boost <= remaining:
        add_product(plan, "Pill")
        remaining -= needed_boost

    # 4. Money
    for money in MONEY_PRIORITY:
        needed_money = count_needed(plan, money)
        if needed_money <= remaining:
            add_product(plan, money)
            remaining -= needed_money
            break  # only one money

    return plan

# ---------------- Eco ----------------
def optimize_eco(total_companies):
    plan = defaultdict(int)
    remaining = total_companies

    for money in MONEY_PRIORITY:
        needed_money = count_needed(plan, money)
        if needed_money <= remaining:
            add_product(plan, money)
            remaining -= needed_money

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
