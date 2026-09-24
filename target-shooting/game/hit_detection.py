"""
hit_detection: figures out whether a click landed on a target.
"""


def check_hit(targets, click_pos):
    """
    Returns the target that was clicked, or None if the click missed
    every target.
    """
    for target in targets:
        rect = target.get_bounding_rect()
        if rect.collidepoint(click_pos):
            return target
    return None
