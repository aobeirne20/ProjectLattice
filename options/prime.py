########################################################################################################
# PRIME OPTIONS ----------------------------------------------------------------------------------------
# LONDON -----------------------------------------------------------------------------------------------
########################################################################################################
options_file_name = "London"

# RIVER OPTIONS ----------------------------------------------------------------------------------------
b_river_ys = [0.6, 0.9]
lb_flat = [200, 1000]
lb_other = [200, 400]
p_river_change_n90_n45_45_90 = [0.35, 0.15, 0.15, 0.35]
cr_river = 30
river_inner_width = 26
river_outer_width = 30
river_label_font_size = 20

# SECANT OPTIONS ----------------------------------------------------------------------------------------
secant_starting_bounds_x = [0.35, 0.65]
secant_starting_bounds_y = [0.45, 0.55]

p_secant_pick_o_from_not_used_list = [0.8, 0.2]
p_secant_start_off_trend = [0.02, 0.08, 0.2, 0.4, 0.2, 0.08, 0.02]

b_secant_segment_length = [50, 1200]
secant_dist_params = [400, 350]

p_secant_on_trend_by = [0.05, 0.45, 0.45, 0.05]

p_secant_return_to_trend = [0.5, 0.5]
p_secant_off_trend_return_by = [0.05, 0.95]

cr_line = 18

single_line_width = 6
double_line_inner_width = 3


# TEXT OPTIONS -----------------------------------------------------------------------------------------
p_sub_name = 0.25

# IMAGE OPTIONS ----------------------------------------------------------------------------------------
s_antialiasing = 2
s_outputimage = 1

# PINATA OPTIONS ---------------------------------------------------------------------------------------
pinata_public_key = "314b41ace95e24c21572"
pinata_private_key = "e4a8b651968cf90767f5232eae853025009dc9a15512f6b53c499327df4c6e4d"
ipfs_directory_name = "RapidTopology_London"

# ------------------------------------------------------------------------------------------------------
# CALCULATED OPTIONS -----------------------------------------------------------------------------------
s_combined = s_outputimage * s_antialiasing
s = s_combined

lb_flat = [n * s for n in lb_flat]
lb_other = [n * s for n in lb_other]

cr_river *= s
river_inner_width *= s
river_outer_width *= s
river_label_font_size *= s

b_secant_segment_length = [n * s for n in b_secant_segment_length]

cr_line *= s

single_line_width *= s
double_line_inner_width *= s
