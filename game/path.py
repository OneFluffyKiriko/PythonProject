from utils.settings import GRID_SIZE


def create_default_path(width, height, grid_size=GRID_SIZE):
    cols = (width + grid_size - 1) // grid_size
    rows = (height + grid_size - 1) // grid_size

    start_row = round(rows//4)
    end_row = min(rows - 1, start_row + max(2, rows // 2))
    turn_col = max(0, min(cols - 1, cols // 2))

    path_tiles = []

    for gx in range(0, turn_col + 1):
        path_tiles.append((gx, start_row))

    step = 1 if end_row >= start_row else -1

    for gy in range(start_row + step, end_row + step, step):
        path_tiles.append((turn_col, gy))

    for gx in range(turn_col + 1, cols):
        path_tiles.append((gx, end_row))

    return path_tiles
