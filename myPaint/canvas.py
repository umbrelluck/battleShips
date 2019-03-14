from rectangle import Rectangle


class Canvas:
    def __init__(self, width, height):
        """
        Initialize new canvas.
        :param width: canvas width.
        :param height: canvas height.
        """
        self.width = width
        self.height = height
        self.cells = [[None] * width for i in range(height)]

    def add_rectangle(self, corner, size, border='*', inside=' '):
        """
        Add rectangle to canvas.
        :param corner: corner coordinates.
        :param size: size of rectangle
        :param border: symbol that is used to display rectangle border.
        :param inside: symbol that is used to display rectangle border.
        :return: recatngle that has been added.
        """
        r = Rectangle(corner, size, border=border, inside=inside)
        for i in range(size[0]):
            for j in range(size[1]):
                coordinate = (corner[0] + i, corner[1] + j)
                if 0 <= coordinate[0] < self.height and 0 <= coordinate[1] < self.width:
                    if self.cells[coordinate[0]][coordinate[1]]:
                        self.cells[coordinate[0]][coordinate[1]].append(r)
                    else:
                        self.cells[coordinate[0]][coordinate[1]] = [r]
        return r

    def __str__(self):
        """
        View of canvas.
        :return: view of canvas.
        """
        s = ''
        for i in range(self.height):
            for j in range(self.width):
                cell = self.cells[i][j]
                if cell != None:
                    s += cell[-1].view((i, j))
                else:
                    s += ' '
            s += '\n'
        return s


if __name__ == '__main__':
    print('Example 1:')
    c = Canvas(20, 20)
    r1 = c.add_rectangle((1, 2), (10, 10))
    print(c)

    print('Example 2:')
    r1.border = '#'
    r1.inside = '%'
    print(c)

    print('Example 3:')
    r2 = c.add_rectangle((7, 7), (10, 10))
    print(c)
