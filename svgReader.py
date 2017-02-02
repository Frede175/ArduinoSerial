from xml.dom import minidom
from svg.path import parse_path
from multiprocessing.dummy import Pool as ThreadPool
import concurrent.futures

class svg_reader(object):

    def __init__(self, path):
        self.svg_data = None  # All data from the svg file when loaded
        self.getSvg(path)
        self.points = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as exec:
            future_points = {exec.submit(self.getPoints, path_string): path_string for path_string in self.svg_data}

            for future in concurrent.futures.as_completed(future_points):
                points = future_points[future]
                try:
                    data = future.result()
                except Exception as exc:
                    print('%r generated an exception: %s' % (points, exc))
                else:
                    self.points.extend(data)

    def getSvg(self, path):
        xmldoc = minidom.parse(path)
        svg = xmldoc.getElementsByTagName("svg")[0]
        g = svg.getElementsByTagName("g")[0]
        self.svg_data = [path.getAttribute('d') for path in g.getElementsByTagName("path")]


    @staticmethod
    def getPoints(path_string):
        print("getPoints")
        points = []
        path_data = parse_path(path_string)
        for x in [j / 1000 for j in range(0, 1000)]:
            point = path_data.point(x)

            p = (int(point.real), int(point.imag))
            if p not in points:
                points.append(p)

        return points