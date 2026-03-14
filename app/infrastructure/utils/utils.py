
def generate_branch_public_id(city: str, number: int) -> str:

    city_slug = city.lower().replace(" ", "_")
    return f"br_{city_slug}_{number}"


def generate_service_type_public_id(branch_id: str, number: int) -> str:
    return f"svc_{branch_id.split('_')[1][:3]}_{number}"


def generate_slot_public_id(branch_id: str, number: int) -> str:
    return f"slot_{branch_id.split('_')[1][:3]}_{number}"

    