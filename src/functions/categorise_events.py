# Fuction to categorise events

def categorise_event(name):
    name_lower = name.lower()
    if "networking" in name_lower:
        return "Networking"
    elif "workshop" in name_lower or "technical" in name_lower:
        return "Workshop"
    else:
        return "Fun/Social"

