# from django.core.exceptions import ValidationError 

from django.contrib.auth import get_user_model


User = get_user_model()


class MyCustomPasswordValidator:
    def validate(self, password: str, user: User | None = None):    #type: ignore
        # raise ValidationError("My custom Error")
        return