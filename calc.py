"""
calc.py — contains all math formulas for construction and household calculations.
"""

import math
from typing import Tuple

# Constants
BRICK_DIM_M = (0.19, 0.09, 0.09)  # m (length x width x height)
WASTAGE_FACTOR_BRICKS = 0.05  # 5%
MORTAR_FRACTION = 0.25  # mortar is ~25% of wall volume (practical assumption)
CEMENT_TO_SAND_RATIO = (1, 6)  # cement : sand
CEMENT_DENSITY_KG_PER_M3 = 1440.0  # approximate
CEMENT_BAG_KG = 50.0
M3_TO_CUBIC_FEET = 35.3146667
DEFAULT_PAINT_COVERAGE_SQFT_PER_LITER = 100.0  # as requested


def calculate_wall_volume(length_m: float, height_m: float, thickness_m: float) -> float:
    """
    Wall volume in cubic meters.
    """
    return length_m * height_m * thickness_m


def calculate_bricks(length_m: float, height_m: float, thickness_m: float,
                     brick_dims: Tuple[float, float, float] = BRICK_DIM_M,
                     wastage: float = WASTAGE_FACTOR_BRICKS) -> int:
    """
    Calculate bricks needed for the wall with wastage and round up.
    Returns integer count of bricks.
    """
    wall_vol = calculate_wall_volume(length_m, height_m, thickness_m)
    brick_vol = brick_dims[0] * brick_dims[1] * brick_dims[2]
    if brick_vol <= 0:
        raise ValueError("Invalid brick dimensions.")
    raw_count = wall_vol / brick_vol
    with_waste = raw_count * (1.0 + wastage)
    return math.ceil(with_waste)


def calculate_cement_and_sand(length_m: float, height_m: float, thickness_m: float,
                              mortar_fraction: float = MORTAR_FRACTION,
                              ratio: Tuple[int, int] = CEMENT_TO_SAND_RATIO,
                              cement_density=CEMENT_DENSITY_KG_PER_M3,
                              bag_weight=CEMENT_BAG_KG) -> Tuple[int, float]:
    """
    Calculate cement (in bags) and sand (in cubic feet) from wall dimensions.

    Returns:
      cement_bags (int), sand_cuft (float)
    """
    wall_vol_m3 = calculate_wall_volume(length_m, height_m, thickness_m)
    mortar_vol_m3 = wall_vol_m3 * mortar_fraction

    cement_parts, sand_parts = ratio
    total_parts = cement_parts + sand_parts
    if total_parts == 0:
        raise ValueError("Invalid mortar ratio.")

    cement_vol_m3 = mortar_vol_m3 * (cement_parts / total_parts)
    sand_vol_m3 = mortar_vol_m3 * (sand_parts / total_parts)

    # cement volume -> weight -> bags
    cement_weight_kg = cement_vol_m3 * cement_density
    cement_bags = math.ceil(cement_weight_kg / bag_weight)

    # sand in cubic feet
    sand_cuft = sand_vol_m3 * M3_TO_CUBIC_FEET

    return cement_bags, sand_cuft


def calculate_paint(length: float, width: float, height: float,
                    openings_area: float = 0.0, coats: int = 2,
                    coverage_sqft_per_liter: float = DEFAULT_PAINT_COVERAGE_SQFT_PER_LITER,
                    units: str = "ft") -> int:
    """
    Calculate paint liters required, rounded up using math.ceil.

    units: 'ft' (dimensions in feet, openings in sqft) or 'm' (dimensions in meters, openings in sqm).
    For 'm' we convert coverage to sqm per liter before computing.
    """
    if units == "ft":
        net_area_sqft = max(0.0, (2 * (length + width) * height) - openings_area)
        liters = (net_area_sqft / coverage_sqft_per_liter) * coats
        return math.ceil(max(0.0, liters))
    elif units == "m":
        # convert coverage from sqft/liter to sqm/liter
        sqm_per_liter = coverage_sqft_per_liter / 10.76391041671
        net_area_sqm = max(0.0, (2 * (length + width) * height) - openings_area)
        liters = (net_area_sqm / sqm_per_liter) * coats
        return math.ceil(max(0.0, liters))
    else:
        raise ValueError("units must be 'ft' or 'm'")


def calculate_flooring(floor_length: float, floor_width: float,
                       tile_length: float, tile_width: float,
                       units: str = "ft") -> int:
    """
    Calculate number of tiles needed (rounded up), adding 5% waste.
    units parameter is for clarity only; calculation expects consistent units.
    """
    floor_area = max(0.0, floor_length * floor_width)
    tile_area = tile_length * tile_width
    if tile_area <= 0:
        raise ValueError("Tile area must be > 0.")
    raw_tiles = floor_area / tile_area
    with_waste = raw_tiles * 1.05
    return math.ceil(with_waste)
