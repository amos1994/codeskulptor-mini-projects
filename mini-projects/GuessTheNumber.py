__author__ = 'sachin'

#All the imports for the program
import simplegui
import random
import math



# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console


# initialize global variables used in your code
__running_codeskulptor__ = True

#Store the total number of guesses
game_max_guesses = -1

#The current guess of the player
#A zero value indicates start of a new game.
game_current_guess = 0

#Store the low and high end of the game
game_low_end = -1
game_high_end = -1


#Number to store the secret number
game_secret_number = -1


# define event handlers for control panel
def range100():
    #Start a new game
    start_game(0, 100)
    return

def range1000():
    # button that changes range to range [0,1000) and restarts the game
    start_game(0, 1000)
    return

def convert_to_integer(input_value):

    choice = str.strip(input_value)
    if str.isdigit(choice):
        return (True, int(choice))
    else:
        return(False, 0)


def get_input(guess):
    # main game logic goes here

    global game_current_guess


    #Process the input to get a valid input
    (valid_input, input_number) = convert_to_integer(guess)


    print "Guess was [" + guess + "]"

    if valid_input:
        #Update the current guess index
        game_current_guess += 1

    #Display the number of guesses available.
    remaining_guesses = game_max_guesses - game_current_guess
    print "Number of remaining guesses is", remaining_guesses

    if not valid_input:
        print "*** Error: Invalid input. Try again :)"
        print ""
        return


    #Valid input and correct guess
    if input_number == game_secret_number: #Correct guess
        print "Correct!\n"
        start_game(game_low_end, game_high_end)
        return


    #Check if reached the end.
    if remaining_guesses == 0:
        print "You ran out of guesses. The number was", game_secret_number, "\n"
        start_game(game_low_end, game_high_end)
        return
    elif input_number < game_secret_number:
        print "Higher!\n"
    else:
        print "Lower!\n"

    return


# main game logic goes here
def start_game(low_end, high_end):

    #List of all the global variables set by this function.
    global game_low_end
    global game_high_end
    global game_current_guess
    global game_max_guesses
    global game_secret_number

    #Generate the secret number.
    game_secret_number = random.randrange(low_end, high_end)

    #Store the low and high end in the global variables
    game_low_end = low_end
    game_high_end = high_end

    #Generate the number of guesses allowed for this range.
    total_reach = high_end - low_end + 1

    #Get the log for this range in base 2
    reach_log = math.log(total_reach, 2)

    #The number of choices is such that 2 * guesses >= total_reach
    game_max_guesses = int(math.ceil(reach_log))

    #Reset the current guess to zero.
    #The game could be written using a single variable and
    #decrementing it to zero. However I wanted to keep track
    #of values for a guess for enhancements
    game_current_guess = 0


    #Display banner message for new game.
    print "New game. Range is from", game_low_end, "to", game_high_end
    print "Number of remaining guesses is", game_max_guesses
    print ""
    return



# create frame
frame = simplegui.create_frame("Guess the number", 200, 200, 300)


# register event handlers for control elements
range100_button  = frame.add_button("Range is [0, 100)", range100)
range1000_button = frame.add_button("Range is [0, 1000)", range1000)

input_value = frame.add_input("Enter a guess", get_input, 100)


if __name__ == '__main__': #Condition will be true when code is run in CodeSkulptor

    #Start the frame
    frame.start()

    #Start default game.
    range100()


# always remember to check your completed program against the grading rubric

#The following piece of code is test runner code. It should be ignored by the reviewers.
def __test__100_001():
    print "Test Range 100 - Invalid inputs or over the range"

    #Initialize the game
    range100()

    get_input("2001")
    get_input("Low End2")
    get_input("High End3")
    get_input("300")
    get_input("A345")
    get_input("+456")
    get_input("Last Chance")
    return


def __test__100_002():
    print "Test Range 100 - Valid Inputs to guess the number\n"

    #Initialize the game
    range100()

    get_input("50")
    get_input("50")
    get_input("50")
    get_input("50")
    get_input("50")
    get_input("50")
    get_input("50")

    return


def __test__get_input():
    #get_input("200.0")
    get_input("Low End")
    get_input("High End")
    get_input("300")

#The pretest module is loaded in the test runner
if __name__ != '__main__':
    __running_codeskulptor__ = False
    import pretest
    pretest.pretest(__name__, True)


