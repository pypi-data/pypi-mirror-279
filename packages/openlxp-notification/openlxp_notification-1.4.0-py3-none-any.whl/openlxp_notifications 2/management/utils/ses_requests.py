import json
import logging

import requests

from requests.auth import AuthBase

from django.core.management.base import (BaseCommand, CommandParser,
                                         CommandError)
from django.core.mail import EmailMessage
from botocore.exceptions import ClientError

from openlxp_notifications.models import (email)

from openlxp_notifications.serializer import EmailSerializer

logger = logging.getLogger('dict_config_logger')

"""
    Requests set up to verify using AWS Simple Email Service (SES)

"""


def SendResponse(response):
    """Function to return response and error catches"""

    if response.status_code in [400, 401, 404, 500]:
        logger.error(response.json())
        return False
    elif response.status_code in [200, 201]:
        try:
            logger.info(response.json())
        except requests.RequestException:
            logger.warning(requests.RequestException)
        return True


"""
    Requests set up using AWS Simple Email Service (SES)

"""


def send_email(body_data, template_type):
    """Request to send email via P1PS"""

    # Check user Permissions to use team

    base_endpoint = get_SES_base_endpoint()
    # team_id = get_P1PS_team_ID()

    url = base_endpoint + "/api/teams/" + team_id + "/emails/" + template_type

    response = requests.post(url=url, headers=headers,
                             data=body_data, auth=TokenAuth(),
                             cookies=SetCookies())
    SendResponse(response)