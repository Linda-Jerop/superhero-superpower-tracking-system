from flask_mail import Message
from app import mail
from flask import current_app

def send_hero_assignment_email(hero_name, power_name, recipient_email):
    """Send email when a hero is assigned a new power"""
    try:
        msg = Message(
            subject=f"New Power Assignment: {hero_name}",
            recipients=[recipient_email],
            body=f"""
Hello,

Congratulations! {hero_name} has been assigned a new power: {power_name}.

This is an exciting development in the superhero universe.

Best regards,
The Superheroes API Team
            """
        )
        mail.send(msg)
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to send email: {str(e)}")
        return False

def send_power_update_email(power_name, recipient_email):
    """Send email when a power is updated"""
    try:
        msg = Message(
            subject=f"Power Updated: {power_name}",
            recipients=[recipient_email],
            body=f"""
Hello,

The power '{power_name}' has been updated with new information.

Please check the system for details.

Best regards,
The Superheroes API Team
            """
        )
        mail.send(msg)
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to send email: {str(e)}")
        return False
