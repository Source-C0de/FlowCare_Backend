
def generate_branch_public_id(city: str, number: int) -> str:

    city_slug = city.lower().replace(" ", "_")
    return f"br_{city_slug}_{number}"