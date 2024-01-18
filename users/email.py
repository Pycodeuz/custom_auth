from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task()
def send_email(user_info, verification_code):
    try:
        send_mail(
            'Verification Code',
            f'Your verification code is: {verification_code}',
            settings.EMAIL_HOST_USER,
            [user_info],
            fail_silently=False,
        )
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

        # Print the status code if available
        if hasattr(e, 'code'):
            print(f"Status Code: {e.code}")

# @shared_task()
# def send_verification_email(user_id):
#     user = User.objects.get(pk=user_id)
#
#     # Generate verification code
#     verification_code = ''.join([str(randint(100000, 999999))])
#
#     # Save verification code to Redis cache with an expiration time (e.g., 5 minutes)
#     cache_key = f'verification_code_{user_id}'
#     cache.set(cache_key, verification_code, timeout=300)
#
#     # Send email asynchronously
#     send_email.delay(user.email, verification_code)
