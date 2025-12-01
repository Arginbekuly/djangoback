#Python modules
import re

#Django modules
from django.core.exceptions import ValidationError

_RESTRICTED_DOMAINS= (
    "mail.ru",
)

def validatate_email_domain(value: str) -> None:
    """
    Validate that the email address belongs to a specific domain.
    """
    domain: str = value.split('@')[-1]
    if domain in _RESTRICTED_DOMAINS:
        raise ValidationError(
            message = f'Registrstion using "{domain}" is not allowed.',
            code = "invalid domain",

        )


def validate_email_payload_not_in_fullname(value: str,full_name:str) -> None:
    """
    Validate that the email address doesnt contain the full name.
    """
    email_payload: str = value.split('@')[0]
    if email_payload.lower() in full_name.lower:
        raise ValidationError(
            {
                "email": "Email address payload should not be part of the full name.",
                "full_name": "Full name should not contain email address payload.", 
            },
                code = "invalid_email_full_name_relation",
        )
    

def validate_phone(value: str, phone:str) -> None:
    """ 
    Validate phone number!!!
    """
    phone_number: str = value.strip()
    pattern = r'^\d{11}$'
    if not re.match(pattern, phone_number):
        raise ValidationError(
            {
            "phone": "The phone number must be 11 digits",
            },
            code = "invalid_phone_format"
        )    
