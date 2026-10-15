from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from templates.emails.confirm_email import HTML_CONTENT


def create_send_email(account, activation_link):
    name = create_name_from_email(account.username) or "Videoflix user"

    msg = EmailMultiAlternatives(
        subject="Confirm your email",
        body=create_text_content_email(name, activation_link),
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[account.email],
    )

    html_content = create_html_content_email(name, activation_link)

    msg.attach_alternative(html_content, "text/html")
    msg.send()


def create_name_from_email(username):
    username = username.split("@")[0]

    for char in [".", "!", "#", "$", "%", "&", "'", "*", "+", "-", "/", "=", "?", "^", "_", "`", "{", "|", "}", "~", ","]:
        username.replace(char, " ")
    username.strip()

    return username


def create_text_content_email(name, activation_link):
    text_content = (
        f"Dear {name} \n"
        "Thank you for registering with Videoflix. To complete your registration and verify your email address, please click the link below:\n\n"

        "Activate account\n"
        f"{activation_link}\n\n"

        "If you did not create an account with us, please disregard this email.\n\n"

        "Best regards,\n\n"

        "Your Videoflix Team."
    )

    return text_content


def create_html_content_email(name, activation_link):
    html_content = HTML_CONTENT.format(name=name, activation_link=activation_link)
    
    return html_content