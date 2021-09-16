


class GraphMain:
    def __init__(self, square_dim):
        sd = square_dim
        random.seed()

        self.vertex_list = []
        self.edge_list = []

        x = random.randint(sd*0.25, sd-sd*0.25)
        y = random.randint(sd*0.25, sd-sd*0.25)
        origin = Vertex(x, y, "Interchange", "Paddington")

        self.vertex_list.append(origin)


class Vertex:
    def __init__(self, locx, locy, renderName, name):
        self.position = (locx, locy)
        self.renderName = renderName
        self.connections = []
        self.nameTag = name

class Generator:
    def __init__(self):
        lineID = 0
        lineGen = []
        origin_line_num = np.random.choice([2, 3, 4, 5], p=[0.6, 0.3, 0.08, 0.02])
        for n in range(1, origin_line_num):
            lineGen.append(LineGenerator(lineID))
            lineID += 1


class LineGenerator:
    def __init__(self, ID):
        self.cscore = 100
        self.cscore -= 5

        self.prime_direction = np.random.choice([0, 1, 2, 3, 4, 5, 6, 7])
        #N=0, NE=1, E=2, SE=3, S=4, SW=5, W=6, NW=7



