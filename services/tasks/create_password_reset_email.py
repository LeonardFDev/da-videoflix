"""create password reset email task"""

from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from templates.emails.password_reset_email import HTML_CONTENT


def password_reset_send_email(account, password_reset_link):
    """Create and send the reset password email."""

    msg = EmailMultiAlternatives(
        subject="Reset your Password",
        body=create_text_content_email(password_reset_link),
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[account.email],
    )

    html_content = create_html_content_email(password_reset_link)

    msg.attach_alternative(html_content, "text/html")
    msg.send()


def create_text_content_email(password_reset_link):
    """Creation of the text content of the email"""

    text_content = (
        "Hello,\n\n"

        "We recently received a request to reset your password. If you made this request, please click on the following link to reset your password:\n\n"

        "Reset password \n"
        f"{password_reset_link}\n\n"

        "Please note that for security reasons, this link is only valid for 24 hours.\n\n"

        "If you did not request a password reset, please ignore this email.\n\n"

        "Best regards,\n\n"

        "Your Videoflix team!"
    )

    return text_content


def create_html_content_email(password_reset_link):
    """Creation of the html content of the email"""

    html_content = HTML_CONTENT.format(password_reset_link=password_reset_link)
    
    return html_content