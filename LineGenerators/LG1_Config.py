import style_data as sd

curve_scale = 50
curve_scale = curve_scale * sd.StyleDatabase.t_scale

exclusion_scale = 60
exclusion_scale = exclusion_scale * sd.StyleDatabase.t_scale

starting_exclusion_scale = 120
starting_exclusion_scale = starting_exclusion_scale * sd.StyleDatabase.t_scale



# Starting locations: To, and then from
slz = [[1/20, 1/4], [3/4, 19/20]]
angles = [0, 45, 90, 135, 180, 225, 270, 315]
P_chance_to_correct_random_continue = [0.3, 0.1, 0.6]
P_chance_to_random_continue = [0.2, 0.8]
P_curve_n90_n45_45_90_changes = [0.1, 0.4, 0.4, 0.1]
P_change_to_trend_by_amount_45_90 = [0.9, 0.1]
P_starting_on_trend = [0.6, 0.4]
P_sandwich_or_new = [0.1, 0.9]
line_length_size_divisors = [50, 10]
termination_score = 2000