MASS_PRODUCED = "Mass-Produced"
ARMORED = "Armored"
HIGH_TECH = "High-Tech"


def get_matching_tags(source_tags, target_tags):
    return set(source_tags).intersection(target_tags)
