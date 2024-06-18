import logging

from django.core.management.base import (BaseCommand, CommandParser,
                                         CommandError)
from django.core.mail import EmailMessage
from botocore.exceptions import ClientError

logger = logging.getLogger('dict_config_logger')


def get_sender_email():
    """Getting sender email id"""

    sender_email_configuration = SenderEmailConfiguration.objects.first()
    if sender_email_configuration:
        sender = sender_email_configuration.sender_email_address
    else:
        sender = None
    return sender


def send_log_email(email_type):
    """ function to send emails of log file to personas"""

    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = email_type.sender

    # Replace recipient@example.com with a "To" address. If your account
    # is still in the sandbox, this address must be verified.
    RECIPIENT = list(email_type.recipients.values_list("email_address",
                                                       flat=True))

    # The subject line for the email.
    SUBJECT = email_type.subject

    # The HTML body of the email.
    BODY_HTML = email_type.template_type.template_body

    for each_recipient in RECIPIENT:
        try:
            # Provide the contents of the email.
            mail = EmailMessage(SUBJECT, BODY_HTML, SENDER,
                                [each_recipient])
            mail.content_subtype = "html"

            # mail.send()
        # Display an error if something goes wrong.
        except ClientError as e:
            logger.error(e.response['Error']['Message'])
            continue

    # body_data = EmailSerializer(email_type).data

    # body_data["template_inputs"] = template_inputs
    # body_data = json.dumps(body_data)

    # headers = {'Content-Type': 'application/json'}

    # jar = requests.cookies.RequestsCookieJar()
    # jar.set('__Host-p1ps-staging-authservice-session-id-cookie',
    #         'NlnUUosv8pQF85lKSwoFfVUjwbqy57Uskh1Mt9JJJ9pfwxqjk0h98tFooSfdvRvk',
    #         domain='p1ps-il2.staging.dso.mil', path='/')

    # P1_response = requests.post(url='https://p1ps-il2.staging.dso.mil/api/teams/IPKRGXU5RFEUNPJSNXWBGBSBNE/emails/edlm-status-update',
    #                             data=body_data, headers=headers,
    #                             auth=TokenAuth(), cookies=jar)

    # print(P1_response.text)


class Command(BaseCommand):
    """Django command to send an emails to the filer/personas, when the log
    warning/error occurred in the metadata EVTVL process."""

    def handle(self, *args, **options):
        """Email log notification is sent to filer/personas when warning/error
        occurred in EVTVL process"""
        send_log_email()
