import unittest
from board import Board

class BasicFunctionalities(unittest.TestCase):
    def test_create_board(self):
        board = Board((3,5))
        self.assertEqual((3,5), (len(board.board[0]), len(board.board)))

    def test_tile_coord(self):
        board = Board((5,5))
        tile = board.get_tile((2,3))

        self.assertEqual((2,3), tile.get_coords())

    def coords_validation(self, pos):
        board = Board((10,5))
        valid = True

        try:
            board.get_tile(pos)
        except IndexError:
            valid = False

        self.assertEqual(board.is_coords_valid(pos), valid)

    def test_coods_invalid_negative(self):
        self.coords_validation((-1, -1))

    def test_coods_invalid_negative2(self):
        self.coords_validation((-1, 1))

    def test_coods_valid(self):
        self.coords_validation((1, 2))

    def test_coods_validation_positive2(self):
        self.coords_validation((10, 5))


class GeneralTileSearching(unittest.TestCase):
    def test_single_attribute(self):
        board = Board((10,6))
        board.get_tile((0,2)).attribute = True
        board.get_tile((3,5)).attribute = True
        board.get_tile((2,5)).attribute = True
        board.get_tile((1,5)).attribute = False
        key_func = lambda tile : getattr(tile, 'attribute', False)
        tiles = board.filter_tiles(key_func=key_func)

        tiles_coords = set(tile.get_coords() for tile in tiles)

        self.assertEqual(tiles_coords, {(2,5), (3,5), (0,2)} )

    def test_multiple_attr(self):
        board = Board((10,6))
        board.get_tile((0,2)).attribute = True
        board.get_tile((3,5)).attribute = True
        board.get_tile((3,5)).attribute2 = "specific"
        board.get_tile((2,5)).attribute = True
        board.get_tile((1,5)).attribute = False
        key_func = lambda tile : \
            getattr(tile, 'attribute', False) \
            and getattr(tile, 'attribute2', False) == "specific"
        tiles = board.filter_tiles(key_func=key_func)
        tiles_coords = set(tile.get_coords() for tile in tiles)

        self.assertEqual(tiles_coords, {(3,5)} )

    def test_sqr_range(self):
        board = Board((10,10))
        coords_pattern = Board.coords_pattern((2,2), pattern="sqr", reach=1)
        tiles = board.filter_tiles(coords_pool = coords_pattern)
        tiles_coords = {tile.get_coords() for tile in tiles}

        self.assertEqual(
            tiles_coords, 
            {
                (1,1), (1,2), (1,3),
                (2,1), (2,2), (2,3),
                (3,1), (3,2), (3,3),
            }
            )

    def test_sqr_range_attributes(self):
        board = Board((10,10))
        board.get_tile((1,1)).attribute = True
        board.get_tile((1,2)).attribute = True
        board.get_tile((1,3)).attribute = True

        coords_pattern = Board.coords_pattern((2,2), pattern="sqr", reach=1)

        key_func = lambda tile : getattr(tile, 'attribute', False)
        tiles = board.filter_tiles(coords_pool = coords_pattern, key_func=key_func)

        tiles_coords = {tile.get_coords() for tile in tiles}


        self.assertEqual(
            tiles_coords, 
            {(1,1), (1,2), (1,3)}
            )

    def test_sqr_range_long_reach(self):
        board = Board((10,10))
        coords_pattern = Board.coords_pattern((2,2), pattern="sqr", reach=40)
        tiles = board.filter_tiles(coords_pool = coords_pattern)
        tiles_coords = {tile.get_coords() for tile in tiles}

        self.assertEqual(
            tiles_coords, 
            set(tile.get_coords() for tile in board.get_all_tiles())
            )

    def test_sqr_range_chopped(self):
        board = Board((10,10))
        coords_pattern = Board.coords_pattern((0,0), pattern="sqr", reach=1)
        tiles = board.filter_tiles(coords_pool = coords_pattern)
        tiles_coords = {tile.get_coords() for tile in tiles}

        self.assertEqual(
            tiles_coords, 
            {  
                (0,0), (0,1),
                (1,0), (1,1),
            }

            )

class RangeObjects(unittest.TestCase):
    def test_sqr(self):
        coords_pattern = Board.coords_pattern((2,2), pattern="sqr", reach=1, exclude_center=True)

        self.assertEqual(
            coords_pattern,
            {
                (1,1), (1,2), (1,3),
                (2,1),        (2,3),
                (3,1), (3,2), (3,3),
            }
        )

    def test_plus(self):
        coords_pattern = Board.coords_pattern((2,2), pattern="|-", reach=1)

        self.assertEqual(
            coords_pattern,
            {
                       (1,2), 
                (2,1), (2,2), (2,3),
                       (3,2), 
            }
        )

    def test_diagonal(self):
        coords_pattern = Board.coords_pattern((2,2), pattern="/", reach=1)

        self.assertEqual(
            coords_pattern,
            {
                              (1,3),
                       (2,2), 
                (3,1),        
            }
        )


    def test_diagonal_backslash(self):
        coords_pattern = Board.coords_pattern((2,2), pattern="\\", reach=1)

        self.assertEqual(
            coords_pattern,
            {
                (1,1),        
                       (2,2), 
                              (3,3),
            }
        )

    def test_column(self):
        coords_pattern = Board.coords_pattern((2,2), pattern="|", reach=1)

        self.assertEqual(
            coords_pattern,
            {
                (2,1),
                (2,2),
                (2,3),
            }
        )

    def test_line(self):
        coords_pattern = Board.coords_pattern((2,2), pattern="-", reach=1)

        self.assertEqual(
            coords_pattern,
            {
                (1,2), (2,2), (3,2),
            }
        )

class OnEdge(unittest.TestCase):
    def test_up(self):
        pos = (2,0)
        board = Board((10,9))

        self.assertEqual(board.on_edge(pos), 'n')

    def test_down(self):
        pos = (5,8)
        board = Board((10,9))

        self.assertEqual(board.on_edge(pos), 's')

    def test_right(self):
        pos = (9,5)
        board = Board((10,9))

        self.assertEqual(board.on_edge(pos), 'e')

    def test_left(self):
        pos = (0,5)
        board = Board((10,9))

        self.assertEqual(board.on_edge(pos), 'w')

    def test_double(self):
        pos = (9,0)
        board = Board((10,9))

        self.assertEqual(board.on_edge(pos), 'ne')

class Moving(unittest.TestCase):
    def test_move_to_empty_on_coords(self):
        board = Board((10,9))
        origin_tile = board.get_tile((3,3))
        origin_tile.attribute = True
        board.move("attribute", (3,3), (5,6))
        

        self.assertEqual(origin_tile.attribute, None)
        self.assertEqual(board.get_tile((5,6)).attribute, True)

    def test_move_to_empty_on_tiles(self):
        board = Board((10,9))
        origin_tile = board.get_tile((3,3))
        origin_tile.attribute = True
        board.move("attribute", origin_tile, (5,6))
        

        self.assertEqual(origin_tile.attribute, None)
        self.assertEqual(board.get_tile((5,6)).attribute, True)

    def test_switch(self):
        board = Board((10,9))
        from_tile = board.get_tile((3,3))
        from_tile.attribute = "a"

        to_tile = board.get_tile((5,5))
        to_tile.attribute = "b"

        board.switch("attribute", from_tile, to_tile)
        

        self.assertEqual(from_tile.attribute, "b")
        self.assertEqual(to_tile.attribute, "a")


if __name__ == '__main__':
    unittest.main()