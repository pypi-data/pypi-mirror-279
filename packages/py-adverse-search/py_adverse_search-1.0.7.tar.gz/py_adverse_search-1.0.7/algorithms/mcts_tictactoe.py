import math
import random

class Node:
    """
    Node class for Monte Carlo Tree Search (MCTS).
    """
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.score = 0

def mcts(game, c_choice, h_choice):
    """
    Monte Carlo Tree Search algorithm for Tic Tac Toe.
    """
    def select(node):
        """
        Select a child node for exploration.
        """
        if not node.children:
            return node

        selected_child = max(node.children, key=lambda child: uct(child))
        return select(selected_child)

    def expand(node):
        """
        Expand the tree by adding a new child node.
        """
        empty_cells = game.empty_cells(node.state)
        if empty_cells:
            selected_cell = random.choice(empty_cells)
            new_state = [row[:] for row in node.state]
            x, y = selected_cell
            new_state[x][y] = game.COMP if node.visits % 2 == 0 else game.HUMAN
            new_node = Node(new_state, parent=node)
            node.children.append(new_node)
            return new_node
        return None

    def simulate(state):
        """
        Simulate a game from the given state to the end.
        """
        while not game.game_over(state):
            empty_cells = game.empty_cells(state)
            if not empty_cells:
                return 0  # Draw
            random_cell = random.choice(empty_cells)
            x, y = random_cell
            state[x][y] = game.COMP if len(empty_cells) % 2 == 0 else game.HUMAN
        return game.evaluate(state)

    def backpropagate(node, score):
        """
        Backpropagate the result of a simulation through the tree.
        """
        while node is not None:
            node.visits += 1
            node.score += score
            node = node.parent

    def uct(node):
        """
        Upper Confidence Bound for Trees (UCT) formula.
        """
        if node.visits == 0:
            return math.inf
        return (node.score / node.visits) + math.sqrt(2 * math.log(node.parent.visits) / node.visits)

    root = Node(game.board)
    for _ in range(1000):
        selected_node = select(root)
        new_node = expand(selected_node)
        if new_node:
            simulation_result = simulate(new_node.state)
            backpropagate(new_node, simulation_result)

    best_child = max(root.children, key=lambda child: child.visits)
    return best_child.state

def mcts_ai_turn(game, c_choice, h_choice):
    """
    AI turn method using Monte Carlo Tree Search (MCTS).

    Parameters:
    - game: Instance of the TicTacToe game.
    - c_choice: Computer's choice, either 'X' or 'O'.
    - h_choice: Human's choice, either 'X' or 'O'.
    """
    next_state = mcts(game, c_choice, h_choice)
    for i in range(3):
        for j in range(3):
            if game.board[i][j] != next_state[i][j]:
                game.set_move(i, j, game.COMP)
                return
