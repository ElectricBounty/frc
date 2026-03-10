from datetime import datetime
import pandas

# Functions begin here
def str_checker(question, available_choices, num_letters, error):
    """returns the string if it meets anything in available_choices"""
    while True:
        choice = input(question).lower()
        for item in available_choices:

            if choice == item:
                return item

            # check first num_letters of letters to see if they tried to write the answer
            elif choice == item[:num_letters]:
                return item

        print(error)

def not_blank(question, error):
    """wrapper for input() that doesn't allow blank responses"""
    while True:
        response = input(question)
        if response != "":
            return response
        print(error)

def int_check(question, error):
    """only accept integers"""

    while True:
        try:
            # ask user for a number
            response = input(question)

            return int(response)

        # checks that number is valid
        except ValueError:
            print(error)

def styled_statement(statement, decoration, multiplier):
    """Displays a statement with a certain number of decorations on each side"""
    return f"{decoration * multiplier} {statement} {decoration * multiplier}"

def format_currency(x):
    return f"${x:.2f}"

# MAIN ROUTINE BEGINS HERE

print(styled_statement("Fundraising Calculator", "*", 5))

# instructions
show_instructions = str_checker("Would you like to view the instructions? ", ["yes","no"],1,"Please enter yes or no.")

print()

# if the user wants to view instructions show them
if show_instructions == "yes":
    print(styled_statement("INSTRUCTIONS", "-", 3))
    print('''
Yup!!!!''')