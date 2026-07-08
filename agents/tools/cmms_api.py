# agents/tools/cmms_api.py

def check_warehouse_inventory(part_name: str) -> dict:
    """
    Queries the CMMS/Maximo inventory system for specific spare parts availability.
    """
    # Simulated database lookup
    inventory_db = {
        "V-102": {"available": True, "warehouse_zone": "Zone 4", "aisle": 12, "shelf": "B", "stock_count": 3},
        "GASKET-NBR": {"available": True, "warehouse_zone": "Zone 2", "aisle": 5, "shelf": "A", "stock_count": 42}
    }
    
    part_key = "V-102" if "V-102" in part_name.upper() else "GASKET-NBR"
    part_info = inventory_db.get(part_key, {"available": False, "stock_count": 0})
    
    return {
        "query_success": True,
        "part_found": part_info["available"],
        "details": part_info
    }