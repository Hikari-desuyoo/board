from board import Board, Tile

class TicTile(Tile):
    def __init__(self):
        self.player = None

    def set_player(self, player):
        if self.player:
            raise Exception
        self.player = player

    def __repr__(self):
        return self.player if self.player else " "


class Game:
    def __init__(self):
        self.board = Board(size = (3,3), tile_class = TicTile)
        self.turn = True
        self.players = {False:"X", True:"O"}
        self.last_played = None

    def view(self):
        display_string = ""
        for row in self.board.get():
            display_string += str(row)
            display_string += "\n"

        return display_string

    def get_player(self):
        return self.players[self.turn]

    def pass_turn(self):
        self.turn = not self.turn

    def check_draw(self):
        is_tile_filled = lambda tile: tile.player
        filled_tiles = self.board.filter_tiles(key_func = is_tile_filled)
        
        if len(filled_tiles) == 9:
            return True
        return False


    def request_move_from_user(self):
        valid_answer = False
        while not valid_answer:
            print(self.view())
            coords = input(f"[{self.get_player()}] Coordinates separated by space:")
            try:
                coords = coords.split(' ')
                coords = map(int, coords)
                coords = tuple(coords)
                if len(coords)>2: raise Exception
                tile = self.board.get_tile(coords)
                tile.set_player(self.get_player())
                self.last_played = tile
                valid_answer = True
            except:
                print("Invalid move.")

    def check_win(self):
        current_player = self.get_player()
        get_player_tiles = lambda tile: tile.player == "O"

        patterns_to_check = "|-"

        #diagonals (only check if necessary)
        edge = self.board.on_edge(self.last_played.get_coords())
        if edge in ["nw", "se"]: 
            patterns_to_check += "\\"
        elif edge in ["sw", "ne"]: 
            patterns_to_check += "/"


        for pattern in patterns_to_check:
            coords_pool = Board.coords_pattern(self.last_played.get_coords(), pattern=pattern, reach=3)
            player_tiles = self.board.filter_tiles(
                coords_pool = coords_pool, key_func = get_player_tiles
                )

            if len(player_tiles) == 3:
                return True


    def run(self):
        while True:
            self.request_move_from_user()
            if self.check_win():
                print(f"{self.get_player()} wins!")
                return
            if self.check_draw():
                print(f"Draw")
                return
            self.pass_turn()
        


if __name__ == '__main__':
    while True:
        game = Game()
        game.run()