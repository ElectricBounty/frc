import math

from Tools.scripts.pep384_macrocheck import report


def yes_no(question, error):
    """returns the string if it meets anything in available_choices"""
    while True:
        choice = input(question).lower()
        for item in ["yes","no"]:

            if choice == item:
                return item

            # check first num_letters of letters to see if they tried to write the answer
            elif choice == item[:1]:
                return item

        print(error)

def profit_goals(total_costs):
    """calculates profit goals"""

    error = "Please enter a number larger than zero"
    profit_type = "unknown"

    while True:
        # get user input
        response = input("What are your profit goals? (e.g $500 or %50): ")

        # check first character to see if we are using percentages or dollars
        if response[0] == "$":
            profit_type = "$"

            # get amount (everything after the $)
            amount = response[1:]

        elif response[-1] == "%":
            profit_type = "%"

            # get amount (everything after the $)
            amount = response[:-1]

        else:
            amount = response

        # have we actually entered something valid
        try:
            amount = float(amount)
            # number is a float large than zero
            if amount <= 0:
                print(error)
                continue
        except ValueError:
            print(amount)
            print(type(amount))
            print(error)
            continue

        if amount >= 100 and profit_type == "unknown":
            # ask if we want percentage
            want_dollars = yes_no(f"Did you mean ${amount:.2f} ({amount} dollars)?", "Please enter yes or no.")

            if want_dollars == "yes":
                profit_type = "$"
            else:
                profit_type = "%"
        elif amount < 100 and profit_type == "unknown":
            # ask if we want percentage
            want_percent = yes_no(f"Did you mean %{amount} ({amount} percent)?", "Please enter yes or no.")

            if want_percent == "yes":
                profit_type = "%"
            else:
                profit_type = "$"

        if profit_type == "$":
            return amount
        else:
            return amount / 100 * total_costs

def round_up(amount, round_val):
    """rounds up to nearest desired whole number"""
    return int(math.ceil(amount/round_val)) * round_val

# main routine starts here

# testing loop
while True:
    expenses = 200
    target = profit_goals(expenses)
    sales_target = target + expenses
    print(f"Profit Goal: ${target:.2f}")
    print(f"Sales Target: ${sales_target:.2f}")

    round_to = int(input("round to: "))

    selling_price =