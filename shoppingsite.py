"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken, Katie Byers.
"""
from flask_ngrok import run_with_ngrok
from flask import Flask,request,render_template, redirect, flash, session
import jinja2
import stripe
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, HiddenField, SelectField, SubmitField, PasswordField
from flask_wtf.file import FileField, FileAllowed

import melons

import customers

app = Flask(__name__)
run_with_ngrok(app)   #starts ngrok when the app is run

# A secret key is needed to use Flask sessioning features
app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.
app.jinja_env.undefined = jinja2.StrictUndefined

pub_key = 'pk_test_ehAVPFKRm6CKrzTW4F707sqF00zKTuDok9'
# This is a public key that one can obtain from the stripe website if you wish to carry on with any credit card transactions.


secret_key = 'sk_test_wawTZFb80biOYE4xP5OnpZke00WxjldcSP'
# This is a secret key that one can obtain from the stripe website if you wish to carry on with any credit card transactions.
stripe.api_key=secret_key
# The same secret key is then passed to the stripe to carry on the further processes.

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True

class Checkout(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    phone_number = StringField('Number')
    email = StringField('Email')
    address = StringField('Address')
    city = StringField('City')
    state = SelectField('State', choices=[('CA', 'Dublin'), ('CR', 'Cork'), ('GL', 'Galway')])
    country = SelectField('Country', choices=[('IR', 'Ireland'), ('UK', 'United Kingdom'), ('IN', 'India')])
    payment_type = SelectField('Payment Type', choices=[('CC', 'Credit Card'), ('DC', 'Debit Card')])


def handle_cart():
      if session['cart']:
        cart = session['cart']
        names_of_melons = []
        cart_total = 0
        for melon in cart:
            melon_object = melons.get_by_id(melon)
            quantity = cart[melon]
            melon_object.update_quantity_cost(quantity)

            names_of_melons.append(melon_object)
            cart_total += melon_object.total_cost

            return names_of_melons, cart_total


@app.route("/")
def index():
    """Return homepage."""
    session['session_id'] = "first"
    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()
    return render_template("all_melons.html",
                           melon_list=melon_list)


@app.route("/melon/<melon_id>")
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id)

    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def show_shopping_cart():
    """Display content of shopping cart."""

    # TODO: Display the contents of the shopping cart.

    # The logic here will be something like:
    #
    # - get the cart dictionary from the session
    # - create a list to hold melon objects and a variable to hold the total
    #   cost of the order
    # - loop over the cart dictionary, and for each melon id:
    #    - get the corresponding Melon object
    #    - compute the total cost for that type of melon
    #    - add this to the order total
    #    - add quantity and total cost as attributes on the Melon object
    #    - add the Melon object to the list created above
    # - pass the total order cost and the list of Melon objects to the template
    #
    # Make sure your function can also handle the case wherein no cart has
    # been added to the session
    if session['cart']:
        cart = session['cart']
        names_of_melons = []
        cart_total = 0
        for melon in cart:
            melon_object = melons.get_by_id(melon)
            quantity = cart[melon]
            melon_object.update_quantity_cost(quantity)

            names_of_melons.append(melon_object)
            cart_total += melon_object.total_cost

    else:
        flash("There are no items in your cart. Go find some melons.")

    
    return render_template("cart.html", melon_list = names_of_melons, cart_total=cart_total)


@app.route("/add_to_cart/<melon_id>")
def add_to_cart(melon_id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Melon successfully added to
    cart'."""

    # TODO: Finish shopping cart functionality

    # The logic here should be something like:
    #
    # - check if a "cart" exists in the session, and create one (an empty
    #   dictionary keyed to the string "cart") if not
    # - check if the desired melon id is the cart, and if not, put it in
    # - increment the count for that melon id by 1
    # - flash a success message
    # - redirect the user to the cart page
    
    #if 'cart' not in session keys, add it to sessions
    if 'cart' not in session:
        session['cart'] = {}

    if melon_id not in session['cart']:
        # add melon to cart dictionary and set quantity to 1
        session['cart'][melon_id] = 1
    else:
        # increase quantity by 1
        session['cart'][melon_id] += 1

    # get melon info for display
    melon = melons.get_by_id(melon_id)

    #flash message that a melon was added to the cart
    flash(f"You added one {melon.common_name} to your cart!")

    return redirect("/cart")

@app.route('/session-basic/set')
def set_session():
    session['session_id'] = "first"
    return redirect('/index')

@app.route('/session-basic/get')
def get_session():
    return session['session_id']



@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    # TODO: Need to implement this!

    # The logic here should be something like:
    #
    # - get user-provided name and password from request.form
    # - use customers.get_by_email() to retrieve corresponding Customer
    #   object (if any)
    # - if a Customer with that email was found, check the provided password
    #   against the stored one
    # - if they match, store the user's email in the session, flash a success
    #   message and redirect the user to the "/melons" route
    # - if they don't, flash a failure message and redirect back to "/login"
    # - do the same if a Customer with that email doesn't exist

    user_email = request.form.get('email')
    if customers.get_by_email(user_email):
        current_customer = customers.get_by_email(user_email)
        print(current_customer.email)
        if current_customer.password == request.form.get('password'):
            session['user'] = user_email
            flash("You've logged in successfully. Welcome to your Ubermelons account.")
            return redirect('/melons')
        else:
            flash('Incorrect Password. Please try again')
            return redirect('/melons')
    else:
        flash("no account with that email exists. please create one or try again")
        return redirect('/login')


@app.route("/checkout", methods=['GET', 'POST'])
def checkout():
    form = Checkout()
    names_of_melons, cart_total = handle_cart()
    if form.validate_on_submit():
        flash('Your order has been successfully submitted and payment is also done','success')        
        return redirect("/melons")
        
        
        customer = stripe.Customer.create(email=request.form['stripeEmail'], source=request.form['stripeToken'])
        print(request.form)
        names_of_melons, cart_total = handle_cart()
        charge = stripe.Charge.create(
            customer=customer.id,
            amount=cart_total,
            currency='usd',
            description='The Product'
        )
        flash('Your order has been successfully submitted and payment is also done','success')
        return redirect(url_for('index'))

    return render_template('checkout.html', form=form, grand_total=cart_total, quantity_total=cart_total, grand_total_plus_shipping=cart_total, pub_key=pub_key)

@app.route("/pay", methods=['POST'])
def pay():

    customer = stripe.Customer.create(email=request.form['stripeEmail'], source=request.form['stripeToken'])
    print(request.form)
    names_of_melons, cart_total = handle_cart()
    charge = stripe.Charge.create(
        customer=customer.id,
        amount=cart_total,
        currency='usd',
        description='The Product'
    )
    return 'successfully Done'


if __name__ == "__main__":
    app.run()
