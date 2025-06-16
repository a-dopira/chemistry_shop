from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from djoser import utils


class EmailSender:

    def __init__(self, request=None, context=None):
        self.request = request
        self.context = context or {}

    def get_domain(self):
        if self.request:
            return self.request.get_host()
        return getattr(settings, "SITE_DOMAIN", "localhost:8000")

    def get_protocol(self):
        if self.request and self.request.is_secure():
            return "https"
        return "http"

    def get_site_name(self):
        return getattr(settings, "SITE_NAME", "The Hag's Cure")

    def send_html_email(self, to_emails, subject, html_template, text_content=None):
        try:
            context = self.get_context_data()

            html_content = render_to_string(html_template, context)

            email_message = EmailMultiAlternatives(
                subject=subject,
                body=text_content
                or "Пожалуйста, включите HTML для просмотра этого письма.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=to_emails,
            )

            email_message.attach_alternative(html_content, "text/html")

            result = email_message.send()
            return result

        except Exception as e:
            raise Exception(f"Error sending email: {e}")


class ActivationEmail(EmailSender):

    def get_context_data(self):
        user = self.context.get("user")

        if not user:
            raise ValueError("User is required for activation email")

        uid = utils.encode_uid(user.pk)
        token = default_token_generator.make_token(user)

        return {
            "user": user,
            "uid": uid,
            "token": token,
            "site_name": self.get_site_name(),
            "domain": self.get_domain(),
            "protocol": self.get_protocol(),
            "activation_url": f"{self.get_protocol()}://{self.get_domain()}/auth/activate/{uid}/{token}/",
        }

    def send(self, to_emails):
        subject = f"{self.get_site_name()} - Активация аккаунта"
        return self.send_html_email(
            to_emails=to_emails,
            subject=subject,
            html_template="userprofile/emails/activation.html",
            text_content="Активируйте ваш аккаунт, перейдя по ссылке в письме.",
        )


class ConfirmationEmail(EmailSender):

    def get_context_data(self):
        user = self.context.get("user")

        if not user:
            raise ValueError("User is required for confirmation email")

        return {
            "user": user,
            "site_name": self.get_site_name(),
            "domain": self.get_domain(),
            "protocol": self.get_protocol(),
        }

    def send(self, to_emails):
        subject = f"{self.get_site_name()} - Аккаунт активирован!"
        return self.send_html_email(
            to_emails=to_emails,
            subject=subject,
            html_template="userprofile/emails/confirmation.html",
            text_content="Ваш аккаунт успешно активирован!",
        )
