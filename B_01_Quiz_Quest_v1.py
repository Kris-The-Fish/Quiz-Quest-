
import random

def yes_no(question):

    """Checks user response to a questin is yes / no (y/), returns 'yes' or 'no' """

    while True:

        response = input(question).lower()

        # check the user says yes / no / Y / n
        if response == "yes" or response == "y":
           return "yes"
        elif response == "no" or response == "n":
            return "no"
        else:
            print("please enter yes / no")

def difficulty(question):

    """Checks user response to a questin is yes / no (y/), returns 'yes' or 'no' """

    while True:

        response = input(question).lower()

        # check the user says yes / no / Y / n
        if response == "easy" or response == "e":
           return "easy"
        elif response == "medium" or response == "m":
            return "medium"
        elif response == "hard" or response == "h":
            return "hard"
        elif response == "costume" or response == "c":
            return "costume"
        else:
            print("please enter easy / medium / hard / costume")

def int_check(question, low=None, high=None, exit_code=None):

    # if any integer is allowed...
    if low is None and high is None:
        error = "Please enter an number!"

    while True:
        response = input(question).lower()

        # check for infinite mode / exit mode
        if exit_code is not None and response == exit_code:
            return response

        try:
            response = int(response)

            return response


        except ValueError:
            print(error)

def string_checker(question, valid_ans=('yes', 'no')):

    error = f"Please enter a valid option from the following list: {valid_ans}"

    while True:

        # Get user response and make sure it's lowercase
        user_response = input(question).lower()

        for item in valid_ans:
            # check if the user response in a word in the list
            if item == user_response:
                return item

            # check if the user response is the same as
            # the first letter of an item in the list
            elif user_response == item[0]:
                return item

        # print error if user does not enter something that is valid
        print(error)
        print()

def instructions():
    """prints instructions"""

    print("""
                * WELCOME! here are the * 
                **** Instructions ****
------------------------------------------------------------------------
  You'll be ask questions a series of multiple different math questions.
------------------------------------------------------------------------
- Choose how many rounds you would like, or press <enter> for infinity. 
- Choose the difficulty or just use the default difficulty (medium).   
- Try to answer the questions the best you can!
- You can exit the game by entering <xxx>.
- at the end you'll be able to see your history, if you want.
------------------------------------------------------------------------
                🍀🍀🍀 Good Luck 🍀🍀🍀
    """)

def generate_addition(low, high):
    answer = random.randint(low, high)
    num1 = random.randint(low, answer)
    num2 = answer - num1
    return num1, num2, answer, "+"

def generate_subtraction(low, high):
    answer = random.randint(low, high)
    num1 = random.randint(answer, high)
    num2 = num1 - answer
    return num1, num2, answer, "-"

def generate_multiplication(low, high):
    for _ in range(1000):
        i = random.randint(low, high)
        answer = random.randint(low, high)

        factors = [(i, answer * i) for i in range(low, high + 1)
                   if answer * i == 0 and low <= answer * i <= high]

        if answer or i == 0:
            continue

        if factors:
            num1, num2 = random.choice(factors)
            return num1, num2, answer, "x"
    # fallback
    return generate_addition(low, high)

def generate_division(low, high):
    for _ in range(1000):
        divisor = random.randint(low, high)
        if divisor == 0:
            continue
        answer: int = random.randint(low, high)
        dividend = answer * divisor
        if low <= dividend <= high:
            return dividend, divisor, answer, "/"
    # fallback
    return generate_addition(low, high)

# Main routine
print()
print(" === Quiz Quest === ")
print()

# ask the user if they want instructions (check they say yes / no)
want_instructions = yes_no("Do you want to see the instructions? ")

# Display the instructions if the user wants to see them...
if want_instructions == "yes":
    instructions()

mode = "regular"
rounds_played = 0
end_game = "no"
feedback = ""
rounds_lost = 0
guesses_allowed = 1
question_history = set()

game_history = []
all_scores = []

# ask user for number of rounds / infinite mode
num_rounds = int_check("Rounds <enter for infinite>: ",
                       low=1, exit_code="")

if num_rounds == "":
    mode = "infinite"
    num_rounds = 1

# ask user if they want to customise the number range
default_params = yes_no("Do you want to use the default game difficulty? ")
if default_params == "yes":
    low_num = 0
    high_num = 100

# allow user to choose difficulty
else:

    difficult = difficulty(
        "what difficulty would you like? (Easy, Medium, Hard) or type <costume> for costume parameter ")

    if difficult == "easy":
        low_num = 1
        high_num = 10

    elif difficult == "medium":
        low_num = 1
        high_num = 100

    elif difficult == "hard":
        low_num = 1
        high_num = 1000

    else:

        print("""
                    ⚠️⚠️⚠️ WARNING ⚠️⚠️⚠️

            <0> does not work ! do NOT enter <0> ! 
            However negative numbers do work. 
            (also make sure you're using full numbers) 

        """)
        low_num = int_check("Low Number? ")
        high_num = int_check("High Number? ", low=low_num + 1)

# Game loop starts
while rounds_played < num_rounds:

    rounds_played += 1
    print(f"\n💿💿💿 Question {rounds_played} / {num_rounds} {'(Infinite Mode)' if mode == 'infinite' else''} 💿💿💿 ")

    guesses_used = 0
    already_guessed = []

    # pick question at random
    while True:
        operation = random.choice(["+", "-", "x", "/"])
        if operation == "+":
            num1, num2, answer, op = generate_addition(low_num, high_num)
        elif operation == "-":
            num1, num2, answer, op = generate_subtraction(low_num, high_num)
        elif operation == "x":
            num1, num2, answer, op = generate_multiplication(low_num, high_num)
        else:
            num1, num2, answer, op = generate_division(low_num, high_num)

        question = f"{num1} {op} {num2}"
        if question not in question_history:
            question_history.add(question)
            break

    user_answer = int_check(f"{question} = ", exit_code= "xxx")

    # if user has entered exit code, end game!!
    if user_answer == "xxx":
        rounds_played -= 1
        end_game = "yes"
        break

    # if user answered right or wrong, print the right response
    if user_answer == answer:
        feedback = "✅✅✅ correct! Good Job! You got it! ✅✅✅"

    else:
        feedback = f"❌❌❌ WRONG! The answer is [{answer}], you silly! You'll get it eventually (maybe). ❌❌❌"
        rounds_lost += 1

    print(feedback)

    if mode == "infinite":
        num_rounds += 1

    if end_game == "yes":
        break

    rounds_won = rounds_played - rounds_lost
    percent_won = rounds_won / rounds_played * 100
    percent_lost = rounds_lost / rounds_played * 100

    # history
    history_feedback = (
        f"Question {rounds_played}: {num1} {op} {num2} = {answer} | {feedback} "
        f" won: {percent_won:.2f}% | Lost: {percent_lost:.2f}%"
    )
    game_history.append(history_feedback)

# print history if the user wants it
if rounds_played > 0:
    # calculate statistics
    rounds_won = rounds_played - rounds_lost
    percent_won = rounds_won / rounds_played * 100
    percent_lost = rounds_lost / rounds_played * 100



    # output game statistics
    print()
    print("📊📊📊Game Statistics📊📊📊")
    print(f"👍Won: {percent_won: .2f}% \t "
          f"😢Lost: {percent_lost:.2f}% \t ")

    # Ask user if they want to see their game history output if it requested
    see_history = string_checker("\nDo you want to see your Game History? ")
    if see_history == "yes":
        for item in game_history:
            print()
            print(item)
if rounds_played == 0:
    percent_won = percent_lost = 0
    print()
    print("NO history available! Try actually playing the game. ")

print()
print("!!! Thanks for playing !!!")


