from inventory_core.metrics import calculate_unhealthy_inventory


def tool_get_unhealthy_items(ship_name: str, as_of_date: str, top_k: int = 10):
    """
    A tool the AI agent can call to retrieve unhealthy inventroy items for a specific ship
    """
    df = calculate_unhealthy_inventory(ship_name, as_of_date)
    return df.head(top_k).to_dict(orient="records")

    
