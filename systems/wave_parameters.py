#Functions as a list of all incoming waves, in order. Waves can be added or adjusted as needed.
WAVES = [
    {
        "spawn_delay": 45,
        "enemies": [
            {"type": "basic", "count": 5}
        ]
    },
    {
        "spawn_delay": 40,
        "enemies": [
            {"type": "basic", "count": 6},
            {"type": "fast", "count": 3}
        ]
    },
    {
        "spawn_delay": 35,
        "enemies": [
            {"type": "fast", "count": 6},
            {"type": "basic", "count": 6},
            {"type": "tank", "count": 1}
        ]
    },
    {
        "spawn_delay": 30,
        "enemies": [
            {"type": "basic", "count": 8},
            {"type": "tank", "count": 2},
            {"type": "fast", "count": 8}
        ]
    }
]
