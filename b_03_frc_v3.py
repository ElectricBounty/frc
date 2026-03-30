import pandas
import math # with cohen
from datetime import datetime
from tabulate import tabulate

output_array = []

def print_output_array(string):
    output_array.append(string)
    print(string)

def not_blank(question, error):
    """wrapper for input() that doesn't allow blank responses"""
    while True:
        response = input(question)
        if response != "":
            return response
        print(error)

def format_currency(x):
    return f"${x:.2f}"

def styled_statement(statement, decoration, multiplier):
    """Displays a statement with a certain number of decorations on each side"""
    return f"{decoration * multiplier} {statement} {decoration * multiplier}"

def num_check(question, num_type, error, exitcode=None):
    """only accept numbers within a certain range"""

    # define change_to variable as either the int function or the float function
    if num_type == "int":
        change_to = int
    else:
        change_to = float

    while True:
        try:
            # ask user for a number
            response = input(question)
            if response.lower() == exitcode:
                return exitcode

            # check if in range
            if 0 < change_to(response):
                return change_to(response)
            else: print(error)

        # checks that number is valid
        except ValueError:
            print(error)

def get_expenses(exp_type, amount):
    all_items = []
    all_amounts = []
    all_costs = []

    while True:
        # get item (string)
        expense_item = not_blank("Item: ", "Please enter a string")
        if len(all_items) > 0 and expense_item.lower() == "xxx":
            print(f"You entered {len(all_items)} item/s")
            break
        elif expense_item.lower() == "xxx":
            print("You must enter at least one item before you can exit the expenses.")
            continue

        expense_amount = 1
        if exp_type == "variable":
            # get amount of items
            expense_amount = num_check("# Bought: ", "int", "Must be an integer more than zero!","")

            # if they entered nothing then default to predefined amount
            if expense_amount == "":
                expense_amount = amount

        # get cost of items
        expense_cost = num_check("$ / item: ", "float", "Must be an integer more than zero!")

        # append everything to arrays
        all_items.append(expense_item)
        all_amounts.append(expense_amount)
        all_costs.append(expense_cost)

    # make panda
    expense_frame = pandas.DataFrame({
        "Item":     all_items,
        "Amount":   all_amounts,
        "$ / Item":     all_costs
    })

    # calc row cost
    # IF fixed variables we just cost = $/item
    if exp_type == "variable":
        expense_frame["Cost"] = expense_frame["Amount"] * expense_frame["$ / Item"]
    else:
        expense_frame["Cost"] = expense_frame["$ / Item"]

    subtotal = expense_frame["Cost"].sum()

    # formatting frame and making into tabulate string
    add_dollars = ["$ / Item", "Cost"]
    for var_item in add_dollars:
        expense_frame[var_item] = expense_frame[var_item].apply(format_currency)

    if exp_type == "variable":
        expense_string = tabulate(expense_frame, headers="keys", tablefmt="psql", showindex=False)
    else:
        expense_string = tabulate(expense_frame[["Item", "Cost"]], headers="keys", tablefmt="psql", showindex=False)

    # return all items and subtotal
    return expense_string, subtotal

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

# main routine

print(styled_statement("FUNDRAISING CALCULATOR", "*", 5))

# instructions
show_instructions = yes_no("Would you like to view the instructions? ", "Please enter yes or no.")

print()

# if the user wants to view instructions show them
if show_instructions == "yes":
    print(styled_statement("INSTRUCTIONS", "-", 3))
    print('''
This program will ask you for...
    - The name of the product you are selling
    - How many items you plan on selling
    - The costs for each component of the product
      (variable expenses)
    - Whether or not you have fixed expenses (If you have
      fixed expenses, it will ask you what they are).
    - How much money you want to make (ie: your profit goal)

It will also ask you how much the recommended sales piece should
be rounded to.

The program outputs an itemised list of the variable and fixed
expenses (which includes the subtotals for these expenses).

Finally it will tell you how much you should sell each item for
to reach your profit goal.

The data will also be written to a text file which has the
item name as your product and today's date.

''')

# get product name and amount
product_name = not_blank("Product Name: ", "Please enter a string")

product_amount = num_check("Amount being produced: ", "int","Please enter a whole quantity larger than zero")

print(f"You are making {product_amount} * {product_name}")
print()

# get variable expenses
print("Variable Expenses")
variable_expenses = get_expenses("variable", product_amount)
variable_df = variable_expenses[0]
variable_subtotal = variable_expenses[1]

print()

# ask if the user has fixed expenses
has_fixed = yes_no("Do you have fixed expenses? ", "Please enter yes or no.")

fixed_subtotal = 0

# get fixed expenses
if has_fixed == "yes":
    print("Fixed Expenses")
    fixed_expenses = get_expenses("fixed", product_amount)
    fixed_df = fixed_expenses[0]
    fixed_subtotal = fixed_expenses[1]

total_cost = variable_subtotal + fixed_subtotal

# get profit goals
profit_target = profit_goals(total_cost)
round_to = num_check("Round profit goals to nearest: $", "int", "Please enter a whole number larger than zero")

# use profit goals to get selling price to see how much each item needs to be sold for, and round up
selling_price = (total_cost + profit_target) / product_amount
suggested_price = round_up(selling_price, round_to)

# defining variables for printing in output

fancy_time = datetime.now().strftime("%d/%m/%Y %H:%M")

# print everything for our ticket and add to output array
print()
print_output_array(styled_statement(f"Fundraising Calculator ({product_name}, {fancy_time})", "*", 5))
print_output_array("")
print_output_array(f"Quantity being made: {product_amount}\n")
print_output_array(styled_statement("Variable Expenses", "=", 3))
print_output_array(variable_df)
print_output_array(f"Variable Expense Subtotal: {format_currency(variable_subtotal)}\n")

print_output_array(styled_statement("Fixed Expenses", "=", 3))
if has_fixed == "yes":
    print_output_array(fixed_df)
    print_output_array(f"Fixed Expense Subtotal: {format_currency(fixed_subtotal)}\n")
else:
    print_output_array("There were no fixed expenses provided.")


print_output_array(f"Total Expenses: {format_currency(total_cost)}\n")

print_output_array(styled_statement("Profit Goals", "=", 3))
print_output_array(f"Profit Target: {format_currency(profit_target)}\n")
print_output_array(f"Minimum Price per {product_name}:   ${format_currency(selling_price):.2f}")
print_output_array(f"Suggested Price per {product_name}: ${format_currency(suggested_price):.2f}")

# does the user want to save the output like mmf
want_txt = yes_no("Would you like to print the output of this program as a file?", "Please enter yes/no.")

if want_txt == "yes":
    # define filename
    formatted_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    write_to = "{}_{}_{}.txt".format("frc",product_name, formatted_time)

    text_file = open(write_to, "w+")

    # print to file
    for item in output_array:
        text_file.write(item)
        text_file.write("\n")


