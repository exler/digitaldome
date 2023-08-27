from digitaldome.common.tokens import JSONWebTokenGenerator
from users.models import User


class EmailVerificationTokenGenerator(JSONWebTokenGenerator):
    model = User
    obj_kwargs = ["email"]
    token_expiration = 60 * 60 * 24 * 3  # 3 days


class PasswordResetTokenGenerator(JSONWebTokenGenerator):
    model = User
    obj_kwargs = ["email"]
    token_expiration = 60 * 60 * 6  # 6 hours
