import pandas

from datetime import datetime
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

def int_check_low(question, low, error, exitcode=None):
    """only accept numbers within a certain range"""

    while True:
        try:
            # ask user for a number
            response = input(question)
            if response.lower() == exitcode:
                return exitcode

            # check if in range
            if low <= int(response):
                return int(response)
            else: print(error)

        # checks that number is valid
        except ValueError:
            print(error)

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
        print(len(all_items))
        if len(all_items) > 0 and expense_item.lower() == "xxx":
            print(f"You entered {len(all_items)} item/s")
            break
        elif expense_item.lower() == "xxx":
            print("You must enter at least one item before you can exit the expenses.")
            continue

        # get amount of items
        expense_amount = num_check("# Bought: ", "int", "Must be an integer more than zero!","xxx")

        # get cost of items
        expense_cost = num_check("$ / item: ", "float", "Must be an integer more than zero!", "xxx")

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


    # return all items and subtotal
    subtotal = expense_frame["Cost"].sum()

    return expense_frame, subtotal

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

product_amount = int_check_low("Amount being produced: ", 0,"Please enter a valid integer")

print(f"You are making {product_amount} {product_name}s")
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

add_dollars = ["$ / Item", "Cost"]
for var_item in add_dollars:
    variable_df[var_item] = variable_df[var_item].apply(format_currency)
    if has_fixed == "y":
        fixed_df[var_item] = fixed_df[var_item].apply(format_currency)

total_cost = variable_subtotal + fixed_subtotal

# defining variables for printing in output

fancy_time = datetime.now().strftime("%d/%m/%Y %H:%M\n")

# print everything for our ticket and add to output array
print()
print_output_array(styled_statement(f"Fundraising Calculator ({product_name}, {fancy_time})", "*", 5))
print_output_array("\n")
print_output_array(f"Quantity being made: {product_amount}\n")
print_output_array(styled_statement("Variable Expenses", "=", 3))
print_output_array(variable_df.to_string(index=False))
print_output_array(f"Variable Expense Subtotal: {format_currency(variable_subtotal)}\n")

print_output_array(styled_statement("Fixed Expenses", "=", 3))
if has_fixed == "y":
    print_output_array(fixed_df.to_string(index=False))
    print_output_array(f"Fixed Expense Subtotal: {format_currency(fixed_subtotal)}\n")


print_output_array(f"Total Expenses: {format_currency(total_cost)}")

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


