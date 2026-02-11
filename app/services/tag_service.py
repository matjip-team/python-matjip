def infer_place_tags(place: dict):
    tags = []
    name = place.get("name", "")
    if "카페" in name:
        tags.append("감성")
    return tags
