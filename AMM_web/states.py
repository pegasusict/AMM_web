"""Container of all the state information for the app.
This file contains the state classes for the app. Each state class
is a subclass of the `State` class from the `reflex` module.
The state classes are used to manage the state of the app and
to handle the interactions between the app and the user.
"""

import reflex as rx


class State(rx.State):
    """The base app state."""


class ContactState(State):
    """The state for the contact page."""

    name: str = ""
    email: str = ""
    message: str = ""
    submitted: bool = False

    def submit(self):
        """Submit the contact form."""
        self.submitted = True
        # Here you would typically send the data to a server or an email service
        # For this example, we'll just print it to the console
        print(f"Name: {self.name}, Email: {self.email}, Message: {self.message}")


class SignupState(State):
    """The state for the signup page."""

    name: str = ""
    email: str = ""
    password: str = ""
    confirm_password: str = ""
    signed_up: bool = False

    def signup(self):
        """Sign up the user."""
        self.signed_up = True
        # Here you would typically save the user data to a database
        # For this example, we'll just print it to the console
        print(f"Signed up with email: {self.email}")
