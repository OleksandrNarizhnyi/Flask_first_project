# Разработать систему регистрации пользователя,
# используя Pydantic для валидации входных данных, обработки вложенных структур и сериализации.
# Система должна обрабатывать данные в формате JSON.
#
# Задачи:
# Создать классы моделей данных с помощью Pydantic для пользователя и его адреса.
# Реализовать функцию, которая принимает JSON строку, десериализует её в объекты Pydantic, валидирует данные,
# и в случае успеха сериализует объект обратно в JSON и возвращает его.
# Добавить кастомный валидатор для проверки соответствия возраста и статуса занятости пользователя.
# Написать несколько примеров JSON строк для проверки различных сценариев валидации: успешные регистрации и случаи,
# когда валидация не проходит (например возраст не соответствует статусу занятости).
#
# Модели:
# Address: Должен содержать следующие поля:
# city: строка, минимум 2 символа.
# street: строка, минимум 3 символа.
# house_number: число, должно быть положительным.
#
# User: Должен содержать следующие поля:
# name: строка, должна быть только из букв, минимум 2 символа.
# age: число, должно быть между 0 и 120.
# email: строка, должна соответствовать формату email.
# is_employed: булево значение, статус занятости пользователя.
# address: вложенная модель адреса.
#
# Валидация:
# Проверка, что если пользователь указывает, что он занят (is_employed = true), его возраст должен быть от 18 до 65 лет.

from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator, ValidationError
from typing import Any

class Address(BaseModel):
    city: str = Field(min_length=2)
    street: str = Field(min_length=3)
    house_number: int = Field(gt=0)


class User(BaseModel):
    name: str = Field(min_length=2)
    age: int = Field(
        gt=0,
        lt=120
    )
    email: EmailStr
    is_employed: bool
    address: Address

    class Config:
        str_strip_whitespace = True
        validate_assignment = True


    @model_validator(mode='before')
    @classmethod
    def check_is_employed(cls, data: dict[str, Any]) -> dict[str, Any]:
        is_employed = data.get('is_employed')
        age = data.get('age')
        if is_employed and (age < 18 or age >= 65):
            raise ValueError("Возраст рабочего должен быть в диапазоне от 18 до 65 лет.")
        return data


json_data = [
    """{
    "name": "John Doe",
    "age": 70,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
        }
    }""",
    """"{
    "name": "Alice Smith",
    "age": 34,
    "email": "alice.smith@gmail.com",
    "is_employed": true,
    "address": {
        "city": "Los Angeles",
        "street": "Sunset Boulevard",
        "house_number": 456
        }
    }""",
    """{
    "name": "Bob Johnson",
    "age": 25,
    "email": "bob.johnson@yahoo.com",
    "is_employed": false,
    "address": {
        "city": "Chicago",
        "street": "Michigan Avenue",
        "house_number": 789
        }
    }""",
    """{
    "name": "Maria Garcia",
    "age": 52,
    "email": "maria.garcia@outlook.com",
    "is_employed": true,
    "address": {
        "city": "Miami",
        "street": "Ocean Drive",
        "house_number": 10
        }
    }""",
    """{
    "name": "Emma Brown",
    "age": 17,
    "email": "emma.brown@protonmail.com",
    "is_employed": true,
    "address": {
        "city": "Seattle",
        "street": "Pine Street",
        "house_number": 305
        }
    }"""
]

for obj in json_data:
     try:
         user = User.model_validate_json(obj)
         print(user.model_dump_json())
     except ValidationError as err:
         print(err)