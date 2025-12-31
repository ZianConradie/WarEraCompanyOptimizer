from collections import defaultdict
from main import optimize_eco, optimize_damage, PRODUCT_RECIPES

def test_eco_mode():
    """Test eco mode with various company counts."""
    print("=" * 50)
    print("TESTING ECO MODE")
    print("=" * 50)
    
    # Test 1: 8 companies - should get 2 of each
    print("\nTest 1: 8 companies")
    plan = optimize_eco(8)
    assert plan["Steel"] == 2, f"Expected 2 Steel, got {plan['Steel']}"
    assert plan["Iron"] == 2, f"Expected 2 Iron, got {plan['Iron']}"
    assert plan["Concrete"] == 2, f"Expected 2 Concrete, got {plan['Concrete']}"
    assert plan["Limestone"] == 2, f"Expected 2 Limestone, got {plan['Limestone']}"
    assert sum(plan.values()) == 8, f"Expected 8 total, got {sum(plan.values())}"
    print("✓ Result:", dict(plan))
    
    # Test 2: 4 companies - should get 1 of each
    print("\nTest 2: 4 companies")
    plan = optimize_eco(4)
    assert plan["Steel"] == 1
    assert plan["Iron"] == 1
    assert plan["Concrete"] == 1
    assert plan["Limestone"] == 1
    assert sum(plan.values()) == 4
    print("✓ Result:", dict(plan))
    
    # Test 3: 10 companies - should get 2 of each + 1 Steel + 1 Iron
    print("\nTest 3: 10 companies")
    plan = optimize_eco(10)
    assert plan["Steel"] == 3
    assert plan["Iron"] == 3
    assert plan["Concrete"] == 2
    assert plan["Limestone"] == 2
    assert sum(plan.values()) == 10
    print("✓ Result:", dict(plan))
    
    # Test 4: 3 companies - should get 1 Steel + 1 Iron (can't afford Concrete+Limestone)
    print("\nTest 4: 3 companies (odd number)")
    plan = optimize_eco(3)
    assert plan["Steel"] == 1
    assert plan["Iron"] == 1
    assert sum(plan.values()) == 2  # Only uses 2 companies
    print("✓ Result:", dict(plan))
    
    # Test 5: 0 companies
    print("\nTest 5: 0 companies")
    plan = optimize_eco(0)
    assert sum(plan.values()) == 0
    print("✓ Result: Empty plan")
    
    print("\n✓ All eco mode tests passed!\n")


def test_damage_mode():
    """Test damage mode with various company counts."""
    print("=" * 50)
    print("TESTING DAMAGE MODE")
    print("=" * 50)
    
    # Test 1: 2 companies - just food
    print("\nTest 1: 2 companies (only food)")
    plan = optimize_damage(2)
    assert plan["Bread"] == 1
    assert plan["Grain"] == 1
    assert sum(plan.values()) == 2
    print("✓ Result:", dict(plan))
    
    # Test 2: 4 companies - food + ammo
    print("\nTest 2: 4 companies (food + ammo)")
    plan = optimize_damage(4)
    assert plan["Bread"] == 1
    assert plan["Grain"] == 1
    assert plan["Heavy Ammo"] == 1
    assert plan["Lead"] == 1
    assert sum(plan.values()) == 4
    print("✓ Result:", dict(plan))
    
    # Test 3: 6 companies - food + ammo + boost
    print("\nTest 3: 6 companies (food + ammo + boost)")
    plan = optimize_damage(6)
    assert plan["Bread"] == 1
    assert plan["Heavy Ammo"] == 1
    assert plan["Pill"] == 1
    assert sum(plan.values()) == 6
    print("✓ Result:", dict(plan))
    
    # Test 4: 10 companies - food + ammo + boost + money
    print("\nTest 4: 10 companies (full loadout + money)")
    plan = optimize_damage(10)
    assert plan["Bread"] == 1
    assert plan["Grain"] == 1
    assert plan["Heavy Ammo"] == 1
    assert plan["Lead"] == 1
    assert plan["Pill"] == 1
    assert plan["Mysterious Plant"] == 1
    # Remaining 4 companies should go to money products
    assert sum(plan.values()) == 10
    money_companies = plan["Steel"] + plan["Iron"] + plan["Concrete"] + plan["Limestone"]
    assert money_companies == 4
    print("✓ Result:", dict(plan))
    
    # Test 5: 1 company - not enough for anything
    print("\nTest 5: 1 company (insufficient)")
    plan = optimize_damage(1)
    assert sum(plan.values()) == 0  # Can't build anything
    print("✓ Result: Empty plan")
    
    print("\n✓ All damage mode tests passed!\n")


def test_recipe_costs():
    """Verify recipe costs are calculated correctly."""
    print("=" * 50)
    print("TESTING RECIPE COSTS")
    print("=" * 50)
    
    expected_costs = {
        "Light Ammo": 2,  # Lead + Light Ammo
        "Heavy Ammo": 2,  # Lead + Heavy Ammo
        "Medium Ammo": 3,  # Lead + Steel + Medium Ammo
        "Bread": 2,  # Grain + Bread
        "Steak": 2,  # Livestock + Steak
        "Cooked Fish": 2,  # Fish + Cooked Fish
        "Pill": 2,  # Mysterious Plant + Pill
        "Steel": 2,  # Iron + Steel
        "Concrete": 2,  # Limestone + Concrete
    }
    
    for product, expected_cost in expected_costs.items():
        actual_cost = 1 + sum(PRODUCT_RECIPES.get(product, {}).values())
        assert actual_cost == expected_cost, f"{product}: expected {expected_cost}, got {actual_cost}"
        print(f"✓ {product}: {actual_cost} companies")
    
    print("\n✓ All recipe cost tests passed!\n")


def run_all_tests():
    """Run all test suites."""
    try:
        test_recipe_costs()
        test_eco_mode()
        test_damage_mode()
        print("=" * 50)
        print("ALL TESTS PASSED! ✓")
        print("=" * 50)
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        raise


if __name__ == "__main__":
    run_all_tests()