"""Login page of the application."""

import reflex as rx

from ..components import footer, navbar, player_shell


def privacy() -> rx.Component:
    """Privacy page of the application
    Returns:
        rx.Component: about page
    """
    return rx.container(
        rx.color_mode.button(position="bottom-left"),
        player_shell(
            rx.vstack(
                navbar(),
                rx.vstack(
                    rx.text("Privacy Policy", font_size="2xl", font_weight="bold"),
                    rx.text(
                        "Your privacy is important to us. This privacy policy explains how we collect, use, and protect your information when you use our application."
                    ),
                    rx.text("1. Information We Collect"),
                    rx.text(
                        "We may collect personal information such as your name, email address, and any other information you provide when you register for an account or use our services."
                    ),
                    rx.text("2. How We Use Your Information"),
                    rx.text(
                        "We may use your information to provide and improve our services, communicate with you, and personalize your experience."
                    ),
                    rx.text("3. Data Security"),
                    rx.text(
                        "We take data security seriously and implement reasonable measures to protect your information from unauthorized access, use, or disclosure."
                    ),
                    rx.text("4. Changes to This Privacy Policy"),
                    rx.text(
                        "We may update this privacy policy from time to time. We will notify you of any changes by posting the new privacy policy on our website."
                    ),
                    rx.text("5. Contact Us"),
                    rx.text(
                        "If you have any questions or concerns about this privacy policy, please contact us at ."
                    ),
                    rx.text("6. Your Consent"),
                    rx.text(
                        "By using our application, you consent to the collection and use of your information as described in this privacy policy."
                    ),
                    rx.text("7. Third-Party Services"),
                    rx.text(
                        "We may use third-party services to help us provide our services. These third-party services may have their own privacy policies, and we encourage you to review them."
                    ),
                    rx.text("8. Children's Privacy"),
                    rx.text(
                        "Our application is not intended for children under the age of 13. We do not knowingly collect personal information from children under 13. If we become aware that we have collected personal information from a child under 13, we will take steps to delete such information."
                    ),
                    rx.text("9. Governing Law"),
                    rx.text(
                        "This privacy policy shall be governed by and construed in accordance with the laws of [your jurisdiction]."
                    ),
                    rx.text("10. Limitation of Liability"),
                    rx.text(
                        "In no event shall we be liable for any direct, indirect, incidental, special, consequential or punitive damages arising out of or in connection with your use of our application or this privacy policy."
                    ),
                    rx.text("11. Disclaimer"),
                    rx.text(
                        "The information provided in this privacy policy is for general informational purposes only and should not be construed as legal advice. We make no representations or warranties of any kind, express or implied, about the completeness, accuracy, reliability, suitability or availability with respect to the information contained in this privacy policy."
                    ),
                    rx.text("12. Acceptance of Terms"),
                    rx.text(
                        "By using our application, you acknowledge that you have read and understood this privacy policy and agree to be bound by its terms."
                    ),
                ),
                footer(),
            )
        ),
    )
