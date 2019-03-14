class Rectangle:
    def __init__(self, corner, size, border='*', inside=' '):
        """
        Initialize new rectangle.
        :param corner: corner coordinates.
        :param size: size of rectangle
        :param border: symbol that is used to display rectangle border.
        :param inside: symbol that is used to display rectangle border.
        """
        self._corner = corner
        self._size = size
        self.border = border
        self.inside = inside

    def view(self, coordinate):
        """
        Display view of rectangle by coordinate.
        :param coordinate: coordinate of cell.
        :return: view of rectangle by coordinate.
        """
        if coordinate[0] == self._corner[0] or coordinate[1] == self._corner[1] or \
           coordinate[0] == self._corner[0] + self._size[0] - 1 or coordinate[1] == self._corner[1] + self._size[1] - 1:
            return self.border
        else:
            return self.inside

