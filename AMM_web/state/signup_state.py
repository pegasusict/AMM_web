from AMM_web.state.base_state import BaseState

class SignupState(BaseState):
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
