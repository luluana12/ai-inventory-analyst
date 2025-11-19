import pandas as pd

def load_data():
    inventory = pd.read_csv("data/inventory_eov.csv")
    forecast = pd.read_csv("data/forecast_demand.csv")
    thresholds = pd.read_csv("data/unhealthy_thresholds.csv")
    return inventory, forecast, thresholds

def calculate_unhealthy_inventory(ship_name: str, as_of_date: str):
    inventory, forecast, thresholds = load_data()

    # Merge Data 
    df = inventory.merge(forecast, on = ["ship_name", "product_id"], how = "left")

    # Compute Weeks of Supply
    df["weeks_of_supply"] = df["on_hand_units"] / df["forecast_units"]

    # Merge thresholds
    df = df.merge(thresholds, on = "microcategory_name", how = "left")

    # Unhealthy if weeks_of_supply > threshold
    df["is_unhealthy"] = df["weeks_of_supply"] > df["max_weeks_of_supply"]

    # Filter by ship 
    df = df[df.ship_name == ship_name]

    # Return only unhealthy items
    return df[df.is_unhealthy]

    


    