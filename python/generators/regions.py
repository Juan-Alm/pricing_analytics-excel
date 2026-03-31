# regions.py

from config import NUM_REGIONS


def generate_regions():
    """
    Generate region data for New Zealand.

    Columns:
    - region_id
    - country
    - region
    - city
    - market_type (developed / emerging)

    Returns:
        List[dict]
    """

    regions = [
        ("Auckland", "Auckland", "developed"),
        ("Wellington", "Wellington", "developed"),
        ("Canterbury", "Christchurch", "developed"),
        ("Waikato", "Hamilton", "developed"),
        ("Bay of Plenty", "Tauranga", "developed"),
        ("Otago", "Dunedin", "developed"),
        ("Manawatu-Whanganui", "Palmerston North", "developed"),
        ("Hawke's Bay", "Napier-Hastings", "developed"),
        ("Taranaki", "New Plymouth", "developed"),
        ("Tasman", "Richmond", "emerging"),
        ("West Coast", "Greymouth", "emerging"),
        ("Southland", "Invercargill", "emerging"),
        ("Nelson", "Nelson", "emerging"),
        ("Marlborough", "Blenheim", "emerging"),
        ("Northland", "Whangarei", "emerging"),
        ("Gisborne", "Gisborne", "emerging"),
    ]

    if len(regions) != NUM_REGIONS:
        raise ValueError(f"Expected {NUM_REGIONS} regions, but got {len(regions)}")

    output = []

    for i, (region, city, market_type) in enumerate(regions, start=1):
        row = {
            "region_id": f"R{i:03d}",
            "country": "New Zealand",
            "region": region,
            "city": city,
            "market_type": market_type
        }
        output.append(row)

    return output


if __name__ == "__main__":
    data = generate_regions()
    for row in data:
        print(row)