"""Customers at Hackbright."""


class Customer(object):
    """Ubermelon customer."""

    def __init__(self, first_name,last_name,
                email,password):
        self.f_name = first_name
        self.l_name = last_name
        self.email = email
        self.password = password


    def __repr__(self):
        """Convenience method to show information about customer in console."""

        return "<Customer: {} {}; exemail:{}>".format(self.f_name, self.l_name, self.email)


def read_customer_txt_file(filepath):
    """Read in a filename and organize customers into Customer Objects"""
    customers = {}

    with open(filepath) as file:
        for line in file:
            (first_name,
            last_name,
            email,
            password) = line.strip().split("|")

    
            customers[email] = Customer(first_name,
                                        last_name, 
                                        email, 
                                        password)

    return customers

def get_by_email(email):
    """Return a customer object, given an email address."""
    
    return customers[email]


# Dictionary to hold customers organized by email.
#
# Format is {email: Customer object, ... }

customers = read_customer_txt_file("customers.txt")
