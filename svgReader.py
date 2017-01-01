from xml.dom import minidom
from svg.path import parse_path

class svg_reader(object):

    def __init__(self):
        self.svg_data = None  # All data from the svg file when loaded
        self.getSvg()
        self.points = []
        self.getPoints()

    def getSvg(self):
        xmldoc = minidom.parse('C:\\Users\\fsr19\\Desktop\\Soccerball.svg')
        svg = xmldoc.getElementsByTagName("svg")[0]
        g = svg.getElementsByTagName("g")[0]
        self.svg_data = [path.getAttribute('d') for path in g.getElementsByTagName("path")]

    def getPoints(self):
        for path_string in self.svg_data:
            path_data = parse_path(path_string)
            for x in [j / 1000 for j in range(0, 1000)]:
                '#Send x and y separate'
                point = path_data.point(x)
                x = int(float(str(point).split('+')[0].replace('(', '')))
                y = int(float(str(point).split('+')[1].replace(')', '').replace('j', '')))
                if (x, y) not in self.points:
                    self.points.append((x, y))
