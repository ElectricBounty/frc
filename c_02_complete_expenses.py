from itertools import product

import pandas

from TCCOM2.mmf.b_01_mmf import add_dollars


def not_blank(question, error):
    """wrapper for input() that doesn't allow blank responses"""
    while True:
        response = input(question)
        if response != "":
            return response
        print(error)

def format_currency(x):
    return f"${x:.2f}"

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


# main routine

while True:
    print("what are we cookin")
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

    # get fixed expenses
    print("Fixed Expenses")
    fixed_expenses = get_expenses("fixed", product_amount)
    fixed_df = fixed_expenses[0]
    fixed_subtotal = fixed_expenses[1]

    add_dollars = ["$ / Item", ""]
    for var_item in add_dollars:
        variable_df[var_item] = variable_df[var_item].apply(format_currency)
        fixed_df[var_item] = fixed_df[var_item].apply(format_currency)

    # print everything
    print(variable_df.to_string(index=False))
    print(format_currency(variable_subtotal))

    print(fixed_df.to_string(index=False))
    print(format_currency(fixed_subtotal))

