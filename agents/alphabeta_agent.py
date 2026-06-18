# TODO: STUDENT IMPLEMENTATION

class AlphaBetaAgent:
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

        # If the game is finished, winning/losing must have very high importance.
        if game.game_over():
            if piece_score > 0:
                return 1000000
            elif piece_score < 0:
                return -1000000
            else:
                return 0

        # Mobility: having more legal moves is usually better in Othello.
        mobility_score = (
                len(game.get_valid_moves(player))
                - len(game.get_valid_moves(opponent))
        )

        # Corners are very valuable in Othello.
        # This works for different board sizes, not only 6x6.
        n = game.size
        corners = [
            (0, 0),
            (0, n - 1),
            (n - 1, 0),
            (n - 1, n - 1)
        ]

        my_corners = 0
        opponent_corners = 0

        for r, c in corners:
            if game.board[r][c] == player:
                my_corners += 1
            elif game.board[r][c] == opponent:
                opponent_corners += 1

        corner_score = my_corners - opponent_corners

        return piece_score + 5 * mobility_score + 25 * corner_score
        
    def _cell_weight(self, game, r, c, n, corners):
        if (r, c) in corners:
            return 50

        for cr, cc in corners:
            dr = abs(r - cr)
            dc = abs(c - cc)

            corner_occupied = (game.board[cr][cc] != 0)

            if dr == 1 and dc == 1:
                return 0 if corner_occupied else -25

            if (dr == 1 and dc == 0) or (dr == 0 and dc == 1):
                return 0 if corner_occupied else -15

        if r == 0 or r == n - 1 or c == 0 or c == n - 1:
            return 5

        return 0

    def alphabeta(self, game, depth, alpha, beta, maximizing, root_player):
        if depth == 0 or game.game_over():
            return self.evaluate(game, root_player), None

        current_player = root_player if maximizing else -root_player
        moves = game.get_valid_moves(current_player)

        if not moves:
            value, _ = self.alphabeta(
                game,
                depth - 1,
                alpha,
                beta,
                not maximizing,
                root_player,
            )
            return value, None

        if maximizing:
            best_value =float("-inf")
            best_move =moves[0]

            for move in moves:
                child =game.copy()
                child.make_move(current_player, *move)

                value, _ = self.alphabeta(
                    child,
                    depth - 1,
                    alpha,
                    beta,
                    False,          
                    root_player,
                )

                if value > best_value:
                    best_value =value
                    best_move =move

                alpha =max(alpha, best_value)
                if alpha >= beta:
                    break           

            return best_value, best_move

        else:
            best_value =float("inf")
            best_move =moves[0]

            for move in moves:
                child =game.copy()
                child.make_move(current_player, *move)

                value, _ = self.alphabeta(
                    child,
                    depth - 1,
                    alpha,
                    beta,
                    True,           
                    root_player,
                )

                if value < best_value:
                    best_value =value
                    best_move =move


                beta = min(beta, best_value)
                if alpha >= beta:
                    break           

            return best_value, best_move

    def choose_move(self, game, player):
        value, move = self.alphabeta(
            game, self.depth, float('-inf'), float('inf'), True, player
        )
        return move
