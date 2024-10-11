import random

# Updated list of bright and colorful colors in RGB format
colors = [
    '#ffb3b3', '#ffb3d9', '#ffb3ff', '#e0b3ff', '#c2b3ff', '#b3b3ff', '#b3c2ff', '#b3e0ff',
    '#b3ffff', '#b3ffe0', '#b3ffc2', '#b3ffb3', '#d9ffb3', '#ffffb3', '#ffe0b3', '#ffc2b3',
    '#ffcccc', '#ffccf2', '#e6ccff', '#ccccff', '#ccd9ff', '#ccf2ff', '#ccffff', '#ccffe6',
    '#ccffd9', '#ccffcc', '#e6ffcc', '#ffffcc', '#ffe6cc', '#ffd9cc', '#ff9999', '#ff99c2',
    '#ff99ff', '#cc99ff', '#9999ff', '#99b3ff', '#99ccff', '#99ffff', '#99ffcc', '#99ff99',
    '#c2ff99', '#ffff99', '#ffcc99', '#ffb399', '#ff8080', '#ff80bf', '#ff80ff', '#bf80ff',
    '#8080ff', '#80bfff', '#80ffff', '#80ffbf', '#80ff80', '#bfff80', '#ffff80', '#ffbf80',
    '#ff8080', '#ff80a0', '#ff80d4', '#d480ff', '#a080ff', '#80a0ff', '#80d4ff', '#80ffd4'
]

process_tids_colors = {}
used_colors = set()  # Set to keep track of used colors


def get_random_color() -> str:
    """Return a random color from the color list that has not been used."""
    available_colors = [color for color in colors if color not in used_colors]

    if available_colors:
        chosen_color = random.choice(available_colors)
        used_colors.add(chosen_color)  # Mark this color as used
        return chosen_color
    else:
        # Generate a new color if there are no available colors
        return generate_new_color()

MAX_COLOR_VALUE = 255
MIN_COLOR_VALUE = 0

def generate_new_color() -> str:

    # Randomly generate RGB values
    r = random.randint(MIN_COLOR_VALUE, MAX_COLOR_VALUE)
    g = random.randint(MIN_COLOR_VALUE, MAX_COLOR_VALUE)
    b = random.randint(MIN_COLOR_VALUE, MAX_COLOR_VALUE)
    return f'#{r:02x}{g:02x}{b:02x}'


def get_colors_by_tids(tids: list) -> list:
    result = []
    for tid in tids:
        if tid not in process_tids_colors:
            process_tids_colors[tid] = get_random_color()
        result.append(process_tids_colors[tid])
    return result

