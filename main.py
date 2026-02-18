#!/usr/bin/env python3
"""
main.py — Entry point and main menu loop for Material Usage Calculator
"""

from datetime import datetime

import calc
import data
import check


def construction_flow():
    print("\n== Construction Materials (Bricks, Cement, Sand) ==")
    L = check.get_positive_float("Wall length (meters): ")
    H = check.get_positive_float("Wall height (meters): ")
    T = check.get_positive_float("Wall thickness (meters) (e.g. 0.10, 0.20): ")

    # Bricks
    bricks = calc.calculate_bricks(L, H, T)
    print(f"Bricks required (including 5% wastage): {bricks} bricks")

    # Cement & Sand
    cement_bags, sand_cuft = calc.calculate_cement_and_sand(L, H, T)
    print(f"Cement required (approx): {cement_bags} bags (50 kg each)")
    print(f"Sand required (approx): {sand_cuft:.3f} cubic feet")

    # Cost estimation and save
    if check.yes_no("Do you want to calculate cost for these materials?"):
        total_cost = 0.0

        if check.yes_no("Enter price for bricks?"):
            price_brick = check.get_positive_float("Price per brick (currency): ")
            cost = price_brick * bricks
            print(f"Bricks cost: {cost:.2f}")
            data.save_transaction(datetime.now().isoformat(), "Construction", "Bricks", f"{bricks}", f"{cost:.2f}")
            total_cost += cost

        if check.yes_no("Enter price per cement bag?"):
            price_bag = check.get_positive_float("Price per 50kg cement bag (currency): ")
            cost = price_bag * cement_bags
            print(f"Cement cost: {cost:.2f}")
            data.save_transaction(datetime.now().isoformat(), "Construction", "Cement (bags)", f"{cement_bags}", f"{cost:.2f}")
            total_cost += cost

        if check.yes_no("Enter price per cubic foot of sand?"):
            price_sand = check.get_positive_float("Price per cubic foot of sand (currency): ")
            cost = price_sand * sand_cuft
            print(f"Sand cost: {cost:.2f}")
            data.save_transaction(datetime.now().isoformat(), "Construction", "Sand (cuft)", f"{sand_cuft:.3f}", f"{cost:.2f}")
            total_cost += cost

        print(f"Total estimated cost: {total_cost:.2f}")


def household_flow():
    print("\n== Household / Renovation ==")
    while True:
        print("\n1. Paint\n2. Flooring\n3. Back")
        choice = input("Choose option [1-3]: ").strip()
        if choice == "1":
            paint_flow()
        elif choice == "2":
            flooring_flow()
        elif choice == "3":
            break
        else:
            print("Invalid choice; enter 1-3.")


def paint_flow():
    print("\n-- Paint Calculator --")
    unit = ""
    while unit not in ("ft", "m"):
        unit = input("Units? Enter 'ft' for feet or 'm' for meters (default ft): ").strip().lower() or "ft"
    if unit == "ft":
        L = check.get_positive_float("Room length (ft): ")
        W = check.get_positive_float("Room width (ft): ")
        H = check.get_positive_float("Room height (ft): ")
        openings = check.get_positive_float("Total openings area (sq ft, doors/windows) [0 if none]: ")
        coats = check.get_positive_int("Number of coats (default 2): ", default=2)
        liters = calc.calculate_paint(L, W, H, openings, coats, coverage_sqft_per_liter=100.0, units="ft")
        print(f"Paint required: {liters} liters (rounded up)")
        if check.yes_no("Do you want to calculate cost?"):
            price = check.get_positive_float("Price per liter (currency): ")
            cost = price * liters
            print(f"Estimated paint cost: {cost:.2f}")
            data.save_transaction(datetime.now().isoformat(), "Household", "Paint (liters)", f"{liters}", f"{cost:.2f}")
    else:
        L = check.get_positive_float("Room length (m): ")
        W = check.get_positive_float("Room width (m): ")
        H = check.get_positive_float("Room height (m): ")
        openings = check.get_positive_float("Total openings area (sq meters) [0 if none]: ")
        coats = check.get_positive_int("Number of coats (default 2): ", default=2)
        liters = calc.calculate_paint(L, W, H, openings, coats, coverage_sqft_per_liter=100.0, units="m")
        print(f"Paint required: {liters} liters (rounded up)")
        if check.yes_no("Do you want to calculate cost?"):
            price = check.get_positive_float("Price per liter (currency): ")
            cost = price * liters
            print(f"Estimated paint cost: {cost:.2f}")
            data.save_transaction(datetime.now().isoformat(), "Household", "Paint (liters)", f"{liters}", f"{cost:.2f}")


def flooring_flow():
    print("\n-- Flooring Calculator --")
    unit = ""
    while unit not in ("ft", "m"):
        unit = input("Units? Enter 'ft' for feet or 'm' for meters (default ft): ").strip().lower() or "ft"
    if unit == "ft":
        L = check.get_positive_float("Floor length (ft): ")
        W = check.get_positive_float("Floor width (ft): ")
        tile_str = input("Tile size (e.g. '2x2' for 2ft x 2ft): ").strip()
        try:
            tile_l, tile_w = check.parse_tile_size(tile_str)
        except ValueError as e:
            print("Error parsing tile size:", e)
            return
        tiles = calc.calculate_flooring(L, W, tile_l, tile_w, units="ft")
        print(f"Tiles required (including 5% wastage): {tiles}")
        if check.yes_no("Do you want to calculate cost?"):
            price = check.get_positive_float("Price per tile (currency): ")
            cost = price * tiles
            print(f"Estimated flooring cost: {cost:.2f}")
            data.save_transaction(datetime.now().isoformat(), "Household", "Tiles", f"{tiles}", f"{cost:.2f}")
    else:
        L = check.get_positive_float("Floor length (m): ")
        W = check.get_positive_float("Floor width (m): ")
        tile_str = input("Tile size (e.g. '0.6x0.6' for 0.6m x 0.6m): ").strip()
        try:
            tile_l, tile_w = check.parse_tile_size(tile_str)
        except ValueError as e:
            print("Error parsing tile size:", e)
            return
        tiles = calc.calculate_flooring(L, W, tile_l, tile_w, units="m")
        print(f"Tiles required (including 5% wastage): {tiles}")
        if check.yes_no("Do you want to calculate cost?"):
            price = check.get_positive_float("Price per tile (currency): ")
            cost = price * tiles
            print(f"Estimated flooring cost: {cost:.2f}")
            data.save_transaction(datetime.now().isoformat(), "Household", "Tiles", f"{tiles}", f"{cost:.2f}")


def view_history_flow():
    print("\n== Transaction History ==")
    data.view_history()


def clear_history_flow():
    print("\n== Clear Transaction History ==")
    if check.yes_no("Are you sure you want to delete all previous transactions?"):
        data.clear_history()
        print("All transactions have been cleared.")
    else:
        print("Clear history cancelled.")


def main():
    print("Welcome — Material Usage Calculator (College Project)")
    while True:
        print("\nMain Menu:")
        print("1. Construction Materials (Bricks, Cement, Sand)")
        print("2. Household Renovation (Paint, Flooring)")
        print("3. View Transaction History")
        print("4. Clear All Previous Transactions")
        print("5. Exit")
        choice = input("Select [1-5]: ").strip()
        if choice == "1":
            construction_flow()
        elif choice == "2":
            household_flow()
        elif choice == "3":
            view_history_flow()
        elif choice == "4":
            clear_history_flow()
        elif choice == "5":
            print("Exiting. Goodbye.")
            break
        else:
            print("Invalid option. Please enter 1-5.")


if __name__ == "__main__":
    main()
