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

        # If the game is finished, winning/losing must have very high importance.
        if game.game_over():
            return 1000 * piece_score

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

    def minimax(self, game, depth, maximizing, root_player):
        """
        Minimax search.

        Parameters:
        - game: current Othello state
        - depth: remaining search depth
        - maximizing: True if it is root_player's turn, False if opponent's turn
        - root_player: the player for whom we are choosing the best move

        Returns:
        - (best_value, best_move)
        """

        # Terminal condition:
        # Stop searching if depth limit is reached or the game is over.
        if depth == 0 or game.game_over():
            return self.evaluate(game, root_player), None

        # Determine whose turn it is at this level of the tree.
        if maximizing:
            current_player = root_player
        else:
            current_player = -root_player

        moves = game.get_valid_moves(current_player)

        # Othello rule:
        # If current player has no legal move, the turn passes to the opponent.
        if not moves:
            value, _ = self.minimax(
                game,
                depth - 1,
                not maximizing,
                root_player
            )
            return value, None

        if maximizing:
            best_value = float("-inf")
            best_move = moves[0]

            for move in moves:
                # Create a child state without changing the original game.
                child = game.copy()
                child.make_move(current_player, *move)

                value, _ = self.minimax(
                    child,
                    depth - 1,
                    False,
                    root_player
                )

                if value > best_value:
                    best_value = value
                    best_move = move

            return best_value, best_move

        else:
            best_value = float("inf")
            best_move = moves[0]

            for move in moves:
                # Create a child state without changing the original game.
                child = game.copy()
                child.make_move(current_player, *move)

                value, _ = self.minimax(
                    child,
                    depth - 1,
                    True,
                    root_player
                )

                if value < best_value:
                    best_value = value
                    best_move = move

            return best_value, best_move

    def choose_move(self, game, player):
        """
        Select the best legal move for the given player.
        """
        moves = game.get_valid_moves(player)

        if not moves:
            return None

        value, move = self.minimax(
            game,
            self.depth,
            True,
            player
        )

        return move