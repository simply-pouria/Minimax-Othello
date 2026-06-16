# TODO: STUDENT IMPLEMENTATION

class MinimaxAgent:
    def __init__(self, depth=4):
        self.depth = depth

    def evaluate(self, game, player):
        """
        positive = good for player
        negative = good for opponent
        """
        opponent = -player

        black_score, white_score = game.score()
        if player == 1:
            piece_score = black_score - white_score
        else:
            piece_score = white_score - black_score

        # winning/losing should matter a lot I think?
        if game.game_over():
            return 1000 * piece_score

        # more options
        mobility_score = len(game.get_valid_moves(player)) - len(game.get_valid_moves(opponent))

        # corners are very valuable in Othello, I have lost too many times because of this...
        n = game.size
        corners = [(0, 0), (0, n - 1), (n - 1, 0), (n - 1, n - 1)]

        my_corners = 0
        opponent_corners = 0

        for r, c in corners:
            if game.board[r][c] == player:
                my_corners += 1
            elif game.board[r][c] == opponent:
                opponent_corners += 1

        corner_score = my_corners - opponent_corners

        return piece_score + 5 * mobility_score + 25 * corner_score

    def minimax(self, game, depth, maximizing, root_player):
        raise NotImplementedError

    def choose_move(self, game, player):
        value, move = self.minimax(game, self.depth, True, player)
        return move
