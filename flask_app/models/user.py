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
from flask_app.models import expense


class User:
    database_name = "spending_schema" # creating a class variable which stores the schema name
    def __init__(self, data): # data is a dictionary representing a record which is also a row in the database
        self.id = data["id"] 
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.birthdate = data["birthdate"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.expenses = [] # creating a list since users can have multiple expenses and this is also linking to the expenses class
    # MAKE SURE the @classmethods are indented under class User so that it knows that it's part of the class
    # Creating a class method to register a new user
    @classmethod
    def register_new_user(cls, data): # need to remember to pass in the data dictionary here by adding data as a parameter
        query = "INSERT INTO users (first_name, last_name, birthdate, email, password) VALUES (%(first_name)s, %(last_name)s, %(birthdate)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.database_name).query_db(query, data)

    # Creating class method to get a user's id for one user
    @classmethod
    def get_one_user_by_id(cls, data):
        query = "SELECT * FROM USERS WHERE id = %(id)s;"
        output = connectToMySQL(cls.database_name).query_db(query, data)
        print(output)
        if len(output) == 0: # doing a check just in case there is nothing to return
            return None
        else: 
            return cls(output[0])

    # Creating class method to get user's email for one user
    @ classmethod
    def get_one_user_by_email(cls, data): # need to pass in a data dictionary in the parameter
        query = "SELECT * FROM users WHERE email = %(email)s;"
        output = connectToMySQL(cls.database_name).query_db(query, data)
        print(output) # printing to terminal to see the data output
        if len(output) == 0: # adding in a check if there's nothing returned
            return None
        else:
            return cls(output[0])

    # Creating class to get the sum of price and group by category
    #!! testing only
    # @ classmethod
    # def get_total_by_category(cls, data):
    #     query = "SELECT category, SUM(price) as total FROM expenses WHERE user_id = %(id)s GROUP BY category;"
    #     output = connectToMySQL(cls.database_name).query_db(query, data)
    #     print(output)
    #     return cls(output[0])


    # Validation checks using static methods
    @staticmethod
    def validating_new_user(form_info):
        is_valid = True # setting to True from the start
        # Checking each field and processing each field individually
        if len(form_info["first_name"]) < 3:
            is_valid = False
            flash("First name must be at least 3 characters.", "register") # setting a flask category here so the correct flash messages will show
        if len(form_info["last_name"]) < 3:
            is_valid = False
            flash("Last name must be at least 3 characters.","register")
        if not EMAIL_REGEX.match(form_info["email"]):
            is_valid = False
            flash("Email address is not in the correct format.", "register")
        if len(form_info["password"]) < 8:
            is_valid = False
            flash("Password must be at least 8 characters long.", "register")
        # if not form_info["password"] == form_info["confirm_password"]:
        #     is_valid = False
        #     flash("Your passwords do not match.", "register")
        return is_valid

    @staticmethod
    def validate_login_info(form_info):
        is_valid = True # setting to True from the start
        # Checking to see if the user has an email in the database to determine if it's an existing user
        data = {
            "email": form_info["email"] # getting the email info from the form
        }
        user_exists_or_not = User.get_one_user_by_email(data) # creating variable to hold info from the class method defined in the User class
        if not user_exists_or_not:
            flash("Invalid login provided.", "login") # adding in a flash by category "login"
            return False # stop the validation checks here and do not proceed because we only want to check the password if the user has a matching email
        if not bcrypt.check_password_hash(user_exists_or_not.password, form_info["password"]):
            flash("Invalid login provided", "login")
            is_valid = False
        return is_valid