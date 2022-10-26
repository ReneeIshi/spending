from sqlite3 import connect
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re # the regex module

# create a regular expression object that we'll use later for validations
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# For bcrypt
from flask_app import app # importing the app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# Link models as needed in projects by importing them
from flask_app.models import user

class Expense:
    database_name = "spending_schema" # class variable holding the schema
    def __init__(self, data): # data is a dictionary representing a recrod which is also a row from the database
        self.id = data["id"] # need to be sure that the names match the columns in the database
        self.date = data["date"]
        self.item = data["item"]
        self.description = data["description"]
        self.price = data["price"]
        self.category = data["category"]
        self.comments = data["comments"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user = None # creating placeholder to hold a single user since an expense can only have 1 user. You can pick any name here and user was picked


    # Class method to add expenses to the database
    @classmethod
    def add_expense(cls, data):
        query = "INSERT INTO expenses (date, item, description, price, category, comments, user_id) VALUES (%(date)s, %(item)s, %(description)s, %(price)s, %(category)s, %(comments)s, %(user_id)s);"
        return connectToMySQL(cls.database_name).query_db(query, data)


    # Get all expenses with the users who added it
    @classmethod
    def get_all_expenses_with_users(cls):
        query = "SELECT * FROM expenses JOIN users ON expenses.user_id = users.id;"
        output = connectToMySQL(cls.database_name).query_db(query)
        print(output)
        if len(output) == 0:
            return []
        else:
            all_expenses_list = [] # will store all expenses
            # Loop through each expense from the query by going through each dictionary
            for current_expense_dict in output:
                # Create an expense or class instance
                expense_inst = cls(current_expense_dict)
                # Get the info about the user who is spending and place it in another dictionary because of how the attributes/variables need to match and they don't when you add a join to a table with the same attribute/variable names
                another_user_dict = {
                    "id": current_expense_dict["users.id"],
                    "first_name": current_expense_dict["first_name"],
                    "last_name": current_expense_dict["last_name"],
                    "birthdate": current_expense_dict["birthdate"],
                    "email": current_expense_dict["email"],
                    "password": current_expense_dict["password"],
                    "created_at": current_expense_dict["users.created_at"],
                    "updated_at": current_expense_dict["users.updated_at"]
                }
                # Create the user class instance
                user_inst = user.User(another_user_dict)
                # Link this user to the expense
                expense_inst.user = user_inst
                # Add the expense to the list called all_expenses_list
                all_expenses_list.append(expense_inst)
            return all_expenses_list


    # Get all expenses for the user who is logged in
    @classmethod
    def get_all_expenses_for_user(cls, data):
        query =  "SELECT * FROM expenses JOIN users ON expenses.user_id = users.id WHERE users.id = %(id)s"
        output = connectToMySQL(cls.database_name).query_db(query, data)
        print(output)
        if len(output) == 0:
            return []
        else:
            all_expenses_list = [] # will store all expenses here
            # Loop through each expense from the query by going through each dictionary
            for current_expense_dict in output:
                # Create an expense or class instance
                expense_inst = cls(current_expense_dict)
                # Get the info about the user who is spending and place it in another dictionary because of how the attributes/variables need to match and they don't when you add a join to a table with the same attribute/variable names
                another_user_dict = {
                    "id": current_expense_dict["users.id"],
                    "first_name": current_expense_dict["first_name"],
                    "last_name": current_expense_dict["last_name"],
                    "birthdate": current_expense_dict["birthdate"],
                    "email": current_expense_dict["email"],
                    "password": current_expense_dict["password"],
                    "created_at": current_expense_dict["users.created_at"],
                    "updated_at": current_expense_dict["users.updated_at"]
                }
                # Create the user class instance
                user_inst = user.User(another_user_dict)
                # Link this user to the expense
                expense_inst.user = user_inst
                # Add the expense to the list called all_expenses_list
                all_expenses_list.append(expense_inst)
            return all_expenses_list


    # Creating class to get the sum of price and group by category to use for the chart
    #!! testing only
    # @ classmethod
    # def get_total_by_category(cls, data):
    #     query = "SELECT category, SUM(price) as total FROM expenses WHERE user_id = %(id)s GROUP BY category;"
    #     output = connectToMySQL(cls.database_name).query_db(query, data)
    #     print(output)
    #     if len(output) == 0:
    #         return []
    #     else:
    #         all_expenses_list = [] # will store all expenses here
    #         # Loop through each expense from the query by going through each dictionary
    #         for current_expense_dict in output:
    #             # Create an expense or class instance
    #             expense_inst = cls(current_expense_dict)
    #             # Get the info about the user who is spending and place it in another dictionary because of how the attributes/variables need to match and they don't when you add a join to a table with the same attribute/variable names
    #             another_user_dict = {
    #                 "id": current_expense_dict["users.id"],
    #                 "first_name": current_expense_dict["first_name"],
    #                 "last_name": current_expense_dict["last_name"],
    #                 "birthdate": current_expense_dict["birthdate"],
    #                 "email": current_expense_dict["email"],
    #                 "password": current_expense_dict["password"],
    #                 "created_at": current_expense_dict["users.created_at"],
    #                 "updated_at": current_expense_dict["users.updated_at"]
    #             }
    #             # Create the user class instance
    #             user_inst = user.User(another_user_dict)
    #             # Link this user to the expense
    #             expense_inst.user = user_inst
    #             # Add the expense to the list called all_expenses_list
    #             all_expenses_list.append(expense_inst)
    #         return all_expenses_list

    # Get one expense with info on user who added it
    @classmethod
    def get_one_expense_with_user(cls, data):
        query = "SELECT * FROM expenses JOIN users ON expenses.user_id = users.id WHERE expenses.id = %(id)s;"
        output = connectToMySQL(cls.database_name).query_db(query, data)
        print(output)
        if len(output) == 0:
            return []
        else:
            # create a class instance of the expense
            expense_inst = cls(output[0])
            # Get the user info on who added the expense and will place it in another new dictionary
            another_user_expense_dict = {
                "id": output[0]["users.id"],
                "first_name": output[0]["first_name"],
                "last_name": output[0]["last_name"],
                "birthdate": output[0]["birthdate"],
                "email": output[0]["email"],
                "password": output[0]["password"],
                "created_at": output[0]["created_at"],
                "updated_at": output[0]["updated_at"]
            }
            # Create the class instance of User
            user_inst = user.User(another_user_expense_dict)
            # Linking user to the expense
            expense_inst.user = user_inst
            return expense_inst

    # Edit expense info
    @classmethod
    def edit_expense(cls, data):
        query = "UPDATE expenses SET date = %(date)s, item = %(item)s, description = %(description)s, price = %(price)s, comments = %(comments)s WHERE id = %(id)s;"
        return connectToMySQL(cls.database_name).query_db(query, data)


    # Delete expense info
    @classmethod
    def delete_expense(cls, data):
        query = "DELETE FROM expenses WHERE id = %(id)s;"
        return connectToMySQL(cls.database_name).query_db(query, data)


    # Validations are done here
    @staticmethod
    def validate_expense(expense_info):
        is_valid = True
        print(expense_info) # printing to terminal to see output
        # checking length of the name
        # if int(expense_info['price']) < 1:
        #     is_valid = False
        #     flash("Price must be greater than 0", "expense")
        if expense_info["date"] == '':
            is_valid = False
            flash("Purchase date is a required field", "expense")

        if expense_info["item"] == '':
            is_valid = False
            flash("Item is a required field", "expense")
        if expense_info["description"] == '':
            is_valid = False
            flash("Description is a required field", "expense")
        # if expense_info["category"] == '':
        #     is_valid = False
        #     flash("Category is a required field", "expense")
        return is_valid