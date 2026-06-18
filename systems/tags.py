MASS_PRODUCED = "Mass-Produced"
ARMORED = "Armored"
HIGH_TECH = "High-Tech"
# Tags for the tag damage system. Used for the tag damage modifiers by both turrets and enemies.

def get_matching_tags(source_tags, target_tags):
    return set(source_tags).intersection(target_tags)
