import math

def calculate_score(state):
  # Calculates the score of the game given the final state and the winner.
    return 2*state['red'] + 3*state['blue']   #2 points each for red marble remaining & 3 points each for blue marble remaining


# returns the new game state that results from applying that move to the original state.
def apply_move(state, move):
    color, amount = move # which marble,amount(1)
    new_state = state.copy() #This function creates a copy of the original state using the copy() method, so that the original state is not modified
    new_state[color] -= amount  #It subtracts the amount of marbles moved by the player (specified by 'amount'(1)) from the corresponding color (specified by 'color') in the state
    return new_state #new state after applying the move.

def game_over(state):
    return state['red'] == 0 or state['blue'] == 0 # the code is checking if either the red or blue pile is empty, which indicates the game has ended.

def get_possible_moves(state):
  # In this game, there are only two possible moves: removing a marble from the red pile or removing a marble from the blue pile
    if state['red'] > 0:
        yield ('red', 1) # which marble,amount
    if state['blue'] > 0:
        yield ('blue', 1)

#Our Max player is computer(First player)
def red_blue_nim(state, alpha, beta, max_player='Computer'):
    if game_over(state):
# function returns negative infinity if the computer is the maximum player, otherwise it returns positive infinity. None, indicating that no move is available when the game is over.
        return -math.inf if max_player else math.inf, None

# If the game is not over, the function proceeds with initializing the best_move variable to None, which will be updated later to hold the best move found by the function.
    best_move = None
    
    # we start a loop over all the possible moves that can be made from the current state
    for move in get_possible_moves(state):
        new_state = apply_move(state, move)
        # recursively calls the minimax function with the new state, swapping the max_player parameter to get the score for the opposing playe
        eval, _ = red_blue_nim(new_state, alpha, beta, not max_player)  #We store the returned score in the eval variable.
      
        if max_player: #if the current player is the max player
            if eval > alpha:# we check if the returned eval score is greater than the current alpha value.
                alpha = eval # If it is, we update the alpha value to the eval score
                best_move = move #and set the best_move variable to the current move being considered
                 
        else: #if the current player is the min player
            if eval < beta: # we check if the returned eval score is less than the current beta value.
                beta = eval # If it is, we update the beta value to the eval score
                best_move = move #and set the best_move variable to the current move being considered.

        if beta <= alpha:
            break #since we have found the optimal move for the current player.
    
    if max_player: #If the current player is the max player,
        return alpha, best_move # we return alpha and the best_move
    else:
        return beta, best_move #if the current player is the min player, we return beta and the best_move.
    

# This is a function that allows a human player to play against the computer in a game of Red-Blue Nim.
def play_game():
  # Initialize the game state
    state = {'red': 5, 'blue': 6}
    print("Starting state:", state)

    while not game_over(state):
        _, computer_move = red_blue_nim(state, -math.inf, math.inf, True) #Computer is the max player here
        print("Computer's move:", computer_move)
        state = apply_move(state, computer_move) #after the move is made
        print("Current state:", state) #print the state after the move is applied
        
        if game_over(state):
            break #if the game is over then exit.
        
        valid_human_move = False #
        while not valid_human_move:
            human_move_color = input("Which pile do you want to take a marble from? (red or blue)") #ask the human player to make a move
            #exception handling if the human player enter anything wrong
            if human_move_color not in state:
                print("Invalid input, please try again.")
                continue
            valid_human_move = True
            
        state = apply_move(state, (human_move_color, 1)) #apply the human player move to the current state
        print("Current state:", state)

    score = calculate_score(state)
    if score > 0:
        print("Human wins with a score of", -score)
    elif score < 0:
        print("Computer wins with a score of", score)
    else:
        print("It's a tie!")

play_game()