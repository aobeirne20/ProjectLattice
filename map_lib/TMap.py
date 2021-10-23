class TMap:
    def __init__(self):
        self.line_list = []
        self.interchange_list = []
        self.feature_list = []

        self.secant_not_picked_dir = [0, 1, 2, 3, 4, 5, 6, 7]
        self.secant_picked_dir = []