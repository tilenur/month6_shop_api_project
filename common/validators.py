from rest_framework.exceptions import ValidationError
from datetime import date

class AgeValidator:
  def __call__(self, request):
    birthday = request.auth.get("birthday")

    if not birthday:
      raise ValidationError("Укажите дату рождения, чтобы создать продукт.")
    
    age = date.today().year - int(birthday.split("-")[0])

    if age < 18:
      raise ValidationError("Вам должно быть 18 лет, чтобы создать продукт.")