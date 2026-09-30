"""
hit_detection: figures out whether a click landed on a target.
"""


def check_hit(targets, click_pos):
    """
    Returns the target that was clicked, or None if the click missed
    every target.

    Uses a true circular hit test: a click counts as a hit only if it
    lands inside the target's actual visible circle, i.e. the distance
    from the click to the target's center is <= the target's radius.
    Squared distance is used to avoid an unnecessary sqrt.
    """
    click_x, click_y = click_pos
    for target in targets:
        dx = click_x - target.x
        dy = click_y - target.y
        distance_sq = dx * dx + dy * dy
        if distance_sq <= target.radius * target.radius:
            return target
    return None
