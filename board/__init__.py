class Tile:
    """
    Base class for board tiles.
    """   
    def set_coords(self, coords):
        self.coords = tuple(coords)

    def get_coords(self):
        return self.coords

class Board:
    """
    The main class, for handling a game board.
    """

    def __init__(self, size=(20,20), tile_class=Tile):
        """
        The constructor for Board class.
  
        Parameters:
           size (tuple): Board's size.
           tile_class (class): Class to initialize the board's tiles. Defaults to standard Tile class. It's necessary for a custom class to inherit the Tile base class.   
        """
        self.board = []
        for j in range(size[1]):
            self.board.append([])
            for i in range(size[0]):
                tile = tile_class()
                tile.set_coords((i,j))
                self.board[-1].append(tile)

    def on_edge(self, *coords):
        """
        Checks which edge(s) the coords is on.

        Parameters: 
            *coords: The coordinate to check. May be a single tuple or two arguments representing it.

        Returns:
            str: Corresponding to which edge(s) the coords is on, by cardinal direction.
        """
        if len(coords)==1:
            coords=coords[0]

        if not self.is_coords_valid(coords):
            raise Exception

        direction = ""

        cx, cy = coords
        if cx == 0:
            direction += "n"
        elif cx == len(self.board)-1:
            direction += "s"

        if cy == 0:
            direction += "w"
        elif cy == len(self.board[0])-1:
            direction += "e"

        return direction

    def get(self):
        """
        Method to get the board's tile 2D list.
        """
        return self.board
    

    def get_tile(self, *coords, allow_negative=False):
        """
        Method to get a board's tile by it's coordinates

        Parameters: 
            *coords: The coordinate to check. May be a single tuple or two arguments representing it.
            allow_negative (bool): Whether negative coords should raie an error or not.

        Returns:
            Tile-based object: The corresponding tile.
        """
        if len(coords)==1:
            coords=coords[0]
        
        for num in coords:
            if num<0 and (not allow_negative):
                raise IndexError
        return self.board[coords[1]][coords[0]]

    def get_all_tiles(self):
        """
        Method to get all board tiles
        
        Returns: 
            set: A set containing all tiles
        """
        all_tiles = []
        for row in self.board:
            all_tiles += row
        return set(all_tiles)

    def is_coords_valid(self, *coords):
        """
        Method to check if a coordinate exists on the board

        Parameters: 
            *coords: The coordinate to check. May be a single tuple or two arguments representing it.

        Returns:
            bool: True if it's a valid coordinate, otherwise False.
        """

        if len(coords)==1:
            coords=coords[0]

        cx_valid = coords[0] in range(0, len(self.board))
        cy_valid = coords[1] in range(0, len(self.board[0]))
        return cx_valid and cy_valid
            

    def tiles_from_coords(self, coords_iterable):
        """
        Method to get tiles from coordinate tuples

        Parameters: 
            coords_iterable: Iterable object containing coordinate tuples

        Returns:
            set: A set containing tile objects
        """
        in_range = filter(self.is_coords_valid, coords_iterable)
        return set(map(self.get_tile, in_range))

    def filter_tiles(self, coords_pool=None, key_func=None):
        """
        Method to filter tiles

        Parameters: 
            coords_pool: Iterable containing coordinates from the tiles to be filtered. Defaults to None(meaning all board tiles)
            key_func: Function to filter the tiles

        Returns:
            set: A set containing the filtered tile objects
        """

        if coords_pool:
            in_range_tiles = self.tiles_from_coords(coords_pool)
        else:
            in_range_tiles = self.get_all_tiles()
        
        found = set()
        for tile in in_range_tiles:
            if not key_func or key_func(tile):
                found.add(tile)
        
        return found

    def move(self, attr_name, from_loc, to_loc):
        """
        Method to move an attribute from a tile to another.

        It does not delete any attributes, just replace their value to None if necesssary

        Parameters: 
            attr_name (str): Attribute's name
            from_loc (tuple or Tile object): Tile or coordinate where the attribute is originally located
            to_loc (tuple or Tile object): Tile or coordinate where the attribute is being moved to
        """
        if type(from_loc) is tuple: from_loc = self.get_tile(from_loc)
        if type(to_loc) is tuple: to_loc = self.get_tile(to_loc)

        attr_value = getattr(from_loc, attr_name)
        setattr(from_loc, attr_name, None)
        setattr(to_loc, attr_name, attr_value)

    def switch(self, attr_name, first_loc, second_loc):
        """
        Method to switch an attribute between tiles.

        It does not delete any attributes, just replace their value to None if necesssary

        Parameters: 
            attr_name (str): Attribute's name
            first_loc (tuple or Tile object): Tile or coordinate
            second_loc (tuple or Tile object): Tile or coordinate
        """
        if type(first_loc) is tuple: first_loc = self.get_tile(first_loc)
        if type(second_loc) is tuple: second_loc = self.get_tile(second_loc)

        attr_value1 = getattr(first_loc, attr_name)
        attr_value2 = getattr(second_loc, attr_name)
        setattr(first_loc, attr_name, attr_value2)
        setattr(second_loc, attr_name, attr_value1)




    @staticmethod
    def coords_pattern(center_coords, pattern="sqr", reach=1, exclude_center = False):
        """
        Static method to get coordinates based on patterns

        Parameters: 
            center_coords (tuple): Determines the center of the pool
            pattern (string): Determines the pool pattern. Defaults to sqr(square). Otherwise, the characters | - \\  / can be used accumulatively to create more complex patterns("|-" for a cross pattern, for example)
            reach (int): Determines for how many tiles the pattern will extend from the center.
            exclude_center (bool): Determines if the center will be excluded from the pool

        Returns:
            set: A set containing coord tuples

        """
        cx, cy = center_coords
        inrange_coords = set()
        top = cy - reach
        bottom = cy + reach
        left = cx - reach
        right = cx + reach

        if pattern == "sqr":
            for i in range(top, bottom+1):
                for j in range(left, right+1):
                    inrange_coords.add((i,j))

            if exclude_center: inrange_coords.remove(center_coords)
            return inrange_coords

        #type isnt square
        if '-' in pattern:
            for j in range(left, right+1):
                inrange_coords.add((j, cy))

        if '|' in pattern:
            for i in range(top, bottom+1):
                inrange_coords.add((cx, i))

        if '\\' in pattern:
            j_value = left
            for i in range(top, bottom+1):
                inrange_coords.add((i, j_value))
                j_value += 1

        if '/' in pattern:
            j_value = right
            for i in range(top, bottom+1):
                inrange_coords.add((i, j_value))
                j_value -= 1

        if exclude_center: inrange_coords.remove(center_coords)
        return inrange_coords
            


