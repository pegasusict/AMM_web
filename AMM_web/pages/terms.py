"""Terms page of the application."""

import reflex as rx
from page_base import page_base


@page_base
def terms() -> rx.Component:
    """Terms and Conditions page of the application
    Returns:
        rx.Component: terms page
    """
    return rx.container(
        rx.text("Terms and Conditions", font_size="2xl", font_weight="bold"),
        rx.text("Welcome to our application. By using our application, you agree to comply with and be bound by the following terms and conditions."),
        rx.text("1. Acceptance of Terms"),
        rx.text("By accessing or using our application, you agree to be bound by these terms and conditions and our privacy policy."),
        rx.text("2. Changes to Terms"),
        rx.text("We may update these terms from time to time. We will notify you of any changes by posting the new terms on our website."),
        rx.text("3. User Accounts"),
        rx.text("""You may need to create an account to access certain features of our application. 
                You are responsible for maintaining the confidentiality of your account information."""),
        rx.text("4. User Conduct"),
        rx.text("You agree to use our application only for lawful purposes and in accordance with these terms."),
        rx.text("5. Intellectual Property"),
        rx.text("All content and materials on our application are protected by copyright, trademark, and other intellectual property laws."),
        rx.text("6. Limitation of Liability"),
        rx.text("""In no event shall we be liable for any direct, indirect, incidental, special, consequential or punitive damages arising
            out of or in connection with your use of our application."""),
        rx.text("7. Governing Law"),
        rx.text("These terms shall be governed by and construed in accordance with the laws of [your jurisdiction]."),
        rx.text("8. Contact Us"),
        rx.text("If you have any questions or concerns about these terms, please contact us at ."),
        rx.text("9. Disclaimer"),
        rx.text("""The information provided in our application is for general informational purposes only and should not be construed as legal advice.
                We make no representations or warranties of any kind, express or implied, about the completeness, accuracy, reliability, suitability or
                availability with respect to the information contained in our application."""),
        rx.text("10. Acceptance of Terms"),
        rx.text("By using our application, you acknowledge that you have read and understood these terms and agree to be bound by them."),
        rx.text("11. Third-Party Services"),
        rx.text("""We may use third-party services to help us provide our services. These third-party services may have their own terms and conditions, 
                and we encourage you to review them."""),
        rx.text("12. User-Generated Content"),
        rx.text("""You are solely responsible for any content you post or submit to our application. We reserve the right to remove any content that 
                violates these terms or is otherwise objectionable."""),
        rx.text("13. Indemnification"),
        rx.text("""You agree to indemnify and hold us harmless from any claims, damages, losses, liabilities, costs, or expenses arising out of your use 
                of our application or violation of these terms."""),
        rx.text("14. Termination"),
        rx.text("""We reserve the right to terminate or suspend your access to our application at any time, without notice, for conduct that we believe 
                violates these terms or is harmful to other users of our application."""),
        rx.text("15. Severability"),
        rx.text("If any provision of these terms is found to be invalid or unenforceable, the remaining provisions shall remain in full force and effect."),
        rx.text("16. Waiver"),
        rx.text("No waiver of any term or condition of these terms shall be deemed a further or continuing waiver of such term or any other term."),
        rx.text("17. Entire Agreement"),
        rx.text("""These terms constitute the entire agreement between you and us regarding your use of our application and supersede any prior 
                agreements or understandings."""),
    )
