# This file experiements a weighted average center limne calculation

# Significance scalars to each frame
weights = [4,3,2,1]
straight_line = [(15,20), (15,20), (15,20), (15, 20)]
line_to_curve = [(15,20), (15,20), (25,25), (25, 35)]
end_curve = [(25, 35), (22, 32), (21, 30), (20, 30)]

def cal_center(line):
    sum_weighted_x = sum(l[0]* w for l, w in zip(line, weights))
    sum_weighted_y = sum(l[1]* w for l, w in zip(line, weights))
    avg_x = sum_weighted_x//sum(weights)
    avg_y = sum_weighted_y//sum(weights)
    return (avg_x, avg_y)

straight = cal_center(straight_line)
straight_to_curve = cal_center(line_to_curve)
curve_to_straight = cal_center(end_curve)

centers = {"Straight":straight, "Straight to curve" :straight_to_curve, "Curve to straight" :curve_to_straight}
for key, val in centers.items():
    print(f"{key}: {val}")
print("\n")


# Test the following from real-time camera feed
# get the tape first.
# re write the locations and test again.
lists_of_lines = [[(269, 113), (212, 48), (215, 52), (235, 41)],
[(246, 98), (273, 85), (200, 41), (268, 63)],
[(91, 51), (249, 47), (178, 44), (246, 54)],
[(91, 51), (249, 47), (178, 44), (246, 54)],
[(244, 96), (249, 36), (174, 41), (197, 51)],
[(191, 97), (290, 60), (197, 21), (213, 22)],
[(275, 101), (219, 71), (163, 47), (151, 48)],
[(223, 91), (264, 59), (175, 60), (152, 83)],
[(294, 94), (306, 46), (193, 31), (147, 88)],
[(249, 72), (218, 50), (251, 66), (207, 88)],
[(303, 104), (321, 32), (183, 43), (235, 71)],
[(304, 106), (322, 28), (162, 50), (196, 82)],
[(234, 56), (321, 26), (186, 13), (229, 78)],
[(225, 48), (315, 52), (150, 66), (218, 75)],
[(289, 95), (318, 64), (152, 70), (150, 55)],
[(234, 55), (302, 82), (161, 41), (238, 64)],
[(197, 78), (244, 94), (173, 66), (165, 52)],
[(190, 62), (336, 74), (173, 70), (163, 43)],
[(295, 61), (301, 75), (175, 70), (154, 40)],
[(250, 56), (194, 51), (168, 67), (186, 32)],
[(257, 62), (252, 60), (172, 73), (138, 44)]]


for l in lists_of_lines:
    center = cal_center(l)
    print(f"Actual X-axis={l[0][0]}, Averaged_x-axis={center[0]}")