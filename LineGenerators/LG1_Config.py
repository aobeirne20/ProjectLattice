import style_data as sd

curve_scale = 50
curve_scale = curve_scale * sd.StyleDatabase.t_scale

exclusion_scale = 60
exclusion_scale = exclusion_scale * sd.StyleDatabase.t_scale

starting_exclusion_scale = 80
starting_exclusion_scale = starting_exclusion_scale * sd.StyleDatabase.t_scale

parallel_exclusion_scale = 80
parallel_exclusion_scale = parallel_exclusion_scale * sd.StyleDatabase.t_scale

interchange_exclusion_scale = 50
interchange_exclusion_scale = interchange_exclusion_scale * sd.StyleDatabase.t_scale

termination_score = 10000
low_termination_score = 2000

# Starting locations: To, and then from
# outer_rect = [[0.05, 0.95], [0.05, 0.95]]
# inner_rect = [[0.2, 0.8], [0.2, 0.8]]
# zone_rects =[[[0, 0], [1/3, 0.5]],
#             [[1/3, 0], [2/3, 0.5]],
#             [[2/3, 0], [1, 0.5]],
#             [[0, 0.5], [1/3, 1]],
#             [[1/3, 0.5], [2/3, 1]],
#             [[2/3, 0.5], [1, 1]]]

x_box = [40/100, 60/100]
y_box = [45/100, 55/100]

angles = [0, 45, 90, 135, 180, 225, 270, 315]

P_chance_to_start_n45_on_45 = [0.1, 0.8, 0.1]

P_chance_of_branch_reverse_continue_choices = [[0.01, 0.01, 0.98], [0, 0, 1], [0.08, 0.01, 0.91]]
P_branch_type_choice = [0.3, 0.5, 0.2]

P_chance_to_start_at_interchange_or_new = [0.2, 0.8]

P_branch_trend_change = [0.15, 0.3, 0.1, 0.3, 0.15]
branch_t_f = 4

P_seg_onto_seg = [0.95, 0.05]
P_curve_onto_seg = [0.7, 0.3]

tscore = [1, 6]

branch_codes = [{"trend_change": -90, "angle_changes": [-90, -45], "angle_changes_P": [0.1, 0.9]},
                {"trend_change": -45, "angle_changes": [-90, -45], "angle_changes_P": [0.1, 0.9]},
                {"trend_change": 0, "angle_changes": [-90, -45, 45, 90], "angle_changes_P": [0.05, 0.45, 0.45, 0.05]},
                {"trend_change": 45, "angle_changes": [90, 45], "angle_changes_P": [0.1, 0.9]},
                {"trend_change": 90, "angle_changes": [90, 45], "angle_changes_P": [0.1, 0.9]}]

P_chance_to_correct_random_continue = [0.8, 0.1, 0.1]
P_chance_to_random_continue = [0.4, 0.6]
P_curve_n90_n45_45_90_changes = [0.05, 0.45, 0.45, 0.05]
P_change_to_trend_by_amount_45_90 = [0.95, 0.05]

P_sandwich_or_new = [0.1, 0.9]

line_length_size_divisors = [60, 5]

termination_randomness = [1, 5]

boundaries = [0.05, 0.95]

#P_starting_zones = [0.2, 0.3, 0.2, 0.1, 0.1, 0.1]
#P_trend_chance = [[0.1, 0.8, 0.1], [0.1, 0.8, 0.1], [0.1, 0.8, 0.1], [0.1, 0.8, 0.1], [0.1, 0.8, 0.1], [0.1, 0.8, 0.1]]
#P_angle_chance = [[0.3, 0.4, 0.3], [0.3, 0.4, 0.3], [0.3, 0.4, 0.3], [0.3, 0.4, 0.3], [0.3, 0.4, 0.3], [0.3, 0.4, 0.3]]

