def sortpts_clockwise(coords):
    by_x = sorted(coords, key=lambda c: c[0])

    left_side = [by_x[0], by_x[1]]
    top_left = max(left_side, key=lambda c: c[1])
    bottom_left = min(left_side, key=lambda c: c[1])

    right_side = [by_x[2], by_x[3]]
    top_right = max(right_side, key=lambda c: c[1])
    bottom_right = min(right_side, key=lambda c: c[1])

    return [top_left, top_right, bottom_right, bottom_left]
