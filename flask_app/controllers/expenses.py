from flask_app import app # Import the app
# Add bcrypt for hashing passwords when registering
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from flask import render_template, request, redirect, session, flash
from flask_app.models import user, expense # importing the model files here

# Visible routes
@app.route("/new")
def new_expense():
    # doing a check to see if user is not logged in and sending them to the login page if they're not
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": session["user_id"],
    }
    return render_template("add_expense.html", this_user = user.User.get_one_user_by_id(data)) # going to the html page and also creating a new variable to hold the current user that's logged in


@app.route("/edit/<int:id>")
def edit_expense(id): # need to remember to use id as a parameter since using a path variable within the route
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": id,
    }
    return render_template("edit_expense.html", this_expense = expense.Expense.get_one_expense_with_user(data))


@app.route("/show/<int:id>")
def view_expense_info(id):
    # #doing a check to see if someone is not logged in and sending them to the login/reg page if they're not
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": id
    }
    return render_template("view_expense.html", this_expense = expense.Expense.get_one_expense_with_user(data))


# Invisible Routes

@app.route("/add_to_db", methods=["POST"])
def add_expense_to_db():
    # doing a check to see if user is not logged in and sending them to the login page if they're not
    if "user_id" not in session:
        return redirect("/")
    # doing validation checks on form input before processing the info
    if not expense.Expense.validate_expense(request.form): # referencing the static method here
        return redirect("/new") # redirecting back to entering new expense html
    else:
        # adding the expense to the database using the model
        data = {
            "date": request.form["date"],
            "item": request.form["item"],
            "description": request.form["description"],
            "price": request.form["price"],
            "category": request.form["category"],
            "comments": request.form["comments"],
            "user_id": session["user_id"],  # placing the current user_id in session in the user_id attribute
        }
        expense.Expense.add_expense(data) # calling the class method created in the model file
        # redirect to the dashboard
        return redirect("/dashboard")


@app.route("/edit_in_db/<int:id>", methods=["POST"])
def edit_expense_in_db(id):
    #doing a check to see if someone is not logged in and sending them to the login/reg page if they're not
    if "user_id" not in session:
        return redirect("/")
    # doing validation checks on form input before processing the info
    if not expense.Expense.validate_expense(request.form):
        return redirect(f"/edit/{id}") # using f-string here
    else:
        # edit expense in the db through the model
        data = {
            "date": request.form["date"],
            "item": request.form["item"],
            "description": request.form["description"],
            "price": request.form["price"],
            #"category": request.form["category"],
            "comments": request.form["comments"],
            "id": id  # this is the id of the expense and remember to NOT include the user id
        }
        expense.Expense.edit_expense(data)
        # redirecting to new route
        return redirect("/details")


@app.route("/delete/<int:id>")
def delete_expense(id):
    # Doing a check to see if someone is not logged in and sending them to the login/reg page if they're not
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": id
    }
    expense.Expense.delete_expense(data)
    return redirect("/dashboard")