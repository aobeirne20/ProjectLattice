########################################################################################################
# PRIME OPTIONS ----------------------------------------------------------------------------------------
# LONDON -----------------------------------------------------------------------------------------------
########################################################################################################
options_file_name = "London"

# RIVER OPTIONS ----------------------------------------------------------------------------------------
b_river_ys = [0.6, 0.9]
lb_flat = [200, 1000]
lb_other = [200, 400]
v_river_change, p_river_change = [-2, -1, 1, 2], [0.35, 0.15, 0.15, 0.35]
cr_river = 30
river_inner_width = 26
river_outer_width = 30
river_label_font_size = 20

# SECANT OPTIONS ----------------------------------------------------------------------------------------
secant_starting_bounds_x = [0.30, 0.70]
secant_starting_bounds_y = [0.45, 0.55]

v_secant_pick_o_from_not_used_list, p_secant_pick_o_from_not_used_list = [True, False], [0.8, 0.2]
v_secant_start_off_trend, p_secant_start_off_trend = [-2, -1, 0, 1, 2], [0.05, 0.2, 0.5, 0.2, 0.05]

b_secant_segment_length = [50, 1200]
std_secant_segment_length = [400, 350]

v_secant_on_trend_diverge_by, p_secant_on_trend_diverge_by = [-2, -1, 1, 2], [0.02, 0.48, 0.48, 0.02]

p_secant_return_to_trend_off_by_1 = [0.6, 0.4]
p_secant_return_to_trend_off_by_2 = [0.8, 0.2]
p_secant_return_to_trend_off_by_3 = [1, 0]

p_secant_off_trend_return_by = [0.04, 0.96]

cr_line = 18

single_line_width = 6
double_line_inner_width = 3
station_tick_width = 4

map_border_buffer = 200

# STATION OPTIONS --------------------------------------------------------------------------------------
tick_length = 8

# INTERCHANGE OPTIONS ----------------------------------------------------------------------------------
interchange_render_outer_radius = 9
interchange_render_inner_radius = 6

# TEXT OPTIONS -----------------------------------------------------------------------------------------
p_sub_name = 0.25

# IMAGE OPTIONS ----------------------------------------------------------------------------------------
s_antialiasing = 1
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
station_tick_width *= s

tick_length *= s

interchange_render_outer_radius *= s
interchange_render_inner_radius *= s

map_border_buffer *= s
