from django.core.exceptions import ValidationError
from django.test import TestCase
from accounts.validators import validate_password_complexity

class TestPasswordValidator(TestCase):

    def test__valid_password__expect_success(self):
        try:
            validate_password_complexity("Valid123!")
        except ValidationError:
            self.fail("validate_password_complexity() raised ValidationError unexpectedly!")

    def test__password_too_short__expect_error(self):
        with self.assertRaisesMessage(ValidationError, "Password must be at least 8 characters long."):
            validate_password_complexity("Ab1!")

    def test__missing_uppercase__expect_error(self):
        with self.assertRaisesMessage(ValidationError, "Password must contain at least one uppercase letter."):
            validate_password_complexity("valid123!")

    def test__missing_lowercase__expect_error(self):
        with self.assertRaisesMessage(ValidationError, "Password must contain at least one lowercase letter."):
            validate_password_complexity("VALID123!")

    def test__missing_digit__expect_error(self):
        with self.assertRaisesMessage(ValidationError, "Password must contain at least one digit."):
            validate_password_complexity("ValidPass!")

    def test__missing_special_character__expect_error(self):
        with self.assertRaisesMessage(ValidationError, "Password must contain at least one special character."):
            validate_password_complexity("Valid1234")
