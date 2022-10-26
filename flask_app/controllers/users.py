from flask_app import app # Import the app

# Add bcrypt for hashing passwords when registering
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from flask import render_template, request, redirect, session, flash, json
from flask_app.models import user, expense # importing the model files here

# Starting with VISIBLE ROUTES

# Root route
@app.route("/")
def index_route():
    return render_template("register_login.html")
    #return render_template("login.html")

# Route to go to the dashboard when a new user registers or with an existing user
@app.route("/dashboard")
def go_to_dashboard():
    # checking if the user is already logged in by checking the session and doing this by creating a data dictionary with 
        # the id in session
    if "user_id" in session: # will only show the HTML page if the user is someone logged in
        data = {
            "id": session["user_id"]
        }
        # Getting the user info that's logged in and will show the HTML file
            # backslash \ allows a break in a line of code
        return render_template("user_dashboard.html", this_user = user.User.get_one_user_by_id(data),\
            # all_expenses = expense.Expense.get_all_expenses_with_users()) # get_all_expenses_with_users is coming from the model
            # need to only display the expense for the user logged in and NOT all expenses for all registered users so commenting out line above this
            all_expenses = expense.Expense.get_all_expenses_for_user(data)) #orig code # passing in data as a parameter because we need to join by the user logged into session
            #all_expenses = expense.Expense.get_total_by_category(data))
            
    else:
        return redirect("/") # if not in session then send user back to the root route

# route for the pie chart #!! testing only #
# @app.route("/dashboard/test")
# def dashboard():
#     needs_vs_wants = db.session.query(db.func.sum(expenses.price))
#     return render_template("user_dashboard.html")

# Route to go to the dashboard when a new user registers or with an existing user
@app.route("/details")
def go_to_details():
    # checking if the user is already logged in by checking the session and doing this by creating a data dictionary with 
        # the id in session
    if "user_id" in session: # will only show the HTML page if the user is someone logged in
        data = {
            "id": session["user_id"]
        }
        # Getting the user info that's logged in and will show the HTML file
            # backslash \ allows a break in a line of code
        return render_template("details.html", this_user = user.User.get_one_user_by_id(data),\
            # all_expenses = expense.Expense.get_all_expenses_with_users()) # get_all_expenses_with_users is coming from the model
            # need to only display the expense for the user logged in and NOT all expenses for all registered users so commenting out line above this
            all_expenses = expense.Expense.get_all_expenses_for_user(data)) # passing in data as a parameter because we need to join by the user logged into session
            
    else:
        return redirect("/") # if not in session then send user back to the root route


# INVISIBLE ROUTES
    # Registering a new user
    # logging in an existing user that's already in the database
    # logging out the user and clearing the session

# Registering a new user route
@app.route("/register_new", methods=["POST"])
def registering_new_user():
    # will need to perform validations on the form first before processing any of the info in the form fields
    # if the validation check fails, will send the user back to the root route
    if not user.User.validating_new_user(request.form): # referencing the method defined in the model file user and class User. this is also referencing the static method from the user model file
        return redirect("/")
    else: # Steps to take when the validation meets requirements and need to hash the password
        # creating a data dictionary to pass the data in from the form
        data = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "email": request.form["email"],
            "password": bcrypt.generate_password_hash(request.form["password"]), # hashing the password using bcrypt
            "birthdate": request.form["birthdate"],
        }
        # Then calling on the model to register the new user and placing the user id in a session so we will know this user is logged in when we do a check
        session["user_id"] = user.User.register_new_user(data) # the session variable is created in this line and you can name it what you want
        # redirect the user to the dashboard
        return redirect('/dashboard')

# Logging in an existing user
@app.route("/login_user", methods=["POST"])
def login_existing_user():
    # will need to perform validations on the form first before processing any of the info in the form fields
    # if the validation check fails, will send the user back to the root route
    if not user.User.validate_login_info(request.form):
        return redirect("/")
    else: 
        # get the user info from the database
        data = {
            "email": request.form["email"]
        }
        existing_user = user.User.get_one_user_by_email(data)
        #! Look more into this
        # print existing user
        # use the get expenses for one user
        # once I have the expenses then jsonify the data (flask jsonify)
        # save the user in session
        session["user_id"] = existing_user.id
        return redirect("/dashboard")


# Logging out the user and clearing the session
@app.route("/logout")
def logout_user():
    session.clear() # clears the session
    return redirect("/") # redirects or sends the user back to the root route with blank fields