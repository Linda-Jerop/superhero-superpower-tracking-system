from flask_mail import Message
from app import mail
from flask import current_app

def send_hero_power_email(hero_name, power_name, recipient_email):
    """Send email notification when a hero gains a new power"""
    try:
        subject = f"🦸 {hero_name} has acquired a new power!"
        body = f"""
Hello,

Great news! {hero_name} has just acquired a new superpower: {power_name}.

This hero is now even more powerful and ready to save the day!

Best regards,
Superheroes API Team
        """
        
        msg = Message(
            subject=subject,
            recipients=[recipient_email],
            body=body
        )
        
        mail.send(msg)
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to send email: {str(e)}")
        return False
