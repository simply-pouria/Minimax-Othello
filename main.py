"""
University: University of Isfahan
Faculty: Mathematics and Statistics
Department: Computer Science
Course: Artificial Intelligence
Professor: Dr. Faria Nasiri Mofakham
TAs: MehrAzin Marzough, Mohammad Karimi, Anahita Honarmandian
Project: Adversarial Search in Othello (Minimax and Alpha-Beta Pruning)
"""

from agents.random_agent import RandomAgent
from agents.greedy_agent import GreedyAgent
from agents.minimax_agent import MinimaxAgent
from agents.alphabeta_agent import AlphaBetaAgent
from tournament import play_game

print("Minimax vs Random:", play_game(MinimaxAgent(depth=3), RandomAgent()))
print("AlphaBeta vs Random:", play_game(AlphaBetaAgent(depth=3), RandomAgent()))
print("Minimax vs Greedy:", play_game(MinimaxAgent(depth=3), GreedyAgent()))
print("AlphaBeta vs Greedy:", play_game(AlphaBetaAgent(depth=3), GreedyAgent()))
