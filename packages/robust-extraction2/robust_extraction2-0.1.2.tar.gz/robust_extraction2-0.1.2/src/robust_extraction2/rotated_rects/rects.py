from cv2.typing import RotatedRect

def verticalize(rect: RotatedRect) -> RotatedRect:
    """Rotates the `rect`  s.t. `|degrees| <= 45`
    - `rect = (x, y), (w, h), degrees`
    """
    (x, y), (w, h), degrees = rect
    if degrees < -45:
        return (x, y), (h, w), degrees+90
    elif degrees > 45:
        return (x, y), (h, w), degrees-90
    else:
        return rect