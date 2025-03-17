# Задача 1: Создайте экземпляр движка для подключения к SQLite базе данных в памяти.
# Задача 2: Создайте сессию для взаимодействия с базой данных, используя созданный движок.
# Задача 3: Определите модель продукта Product со следующими типами колонок:
# id: числовой идентификатор
# name: строка (макс. 100 символов)
# price: числовое значение с фиксированной точностью
# in_stock: логическое значение

# Задача 4: Определите связанную модель категории Category со следующими типами колонок:
# id: числовой идентификатор
# name: строка (макс. 100 символов)
# description: строка (макс. 255 символов)
# Задача 5: Установите связь между таблицами Product и Category с помощью колонки category_id.

from sqlalchemy import create_engine, Integer, String, ForeignKey, Numeric, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column, relationship
import logging
# Настройка базового логирования
# Взял пример с лекции ради интереса))
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('sqlalchemy.engine')
# Включение логирования SQL-запросов
logger.setLevel(logging.INFO)

URL = "sqlite:///:memory:"

engine = create_engine(URL, echo=True, echo_pool=True)

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int]=mapped_column(
        Integer,
        primary_key=True
    )
    name: Mapped[str]=mapped_column(
        String(100)
    )
    price: Mapped[Numeric]=mapped_column(
        Numeric(precision=6, scale=2)
    )
    in_stock: Mapped[bool]=mapped_column(
        Boolean
    )
    category_id: Mapped[int]=mapped_column(
        Integer,
        ForeignKey("categories.id")
    )

    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="products"
    )

class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    name: Mapped[str] = mapped_column(
        String(100)
    )
    description: Mapped[str] = mapped_column(
        String(255)
    )

    products: Mapped[list["Product"]] = relationship(
         "Product",
         back_populates="category"
    )

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

category1 = Category(id=1, name="Electronics", description="Gadgets and devices")
product1 = Product(id=1, name="Laptop", price=699.99, in_stock=True, category=category1)
product2 = Product(id=2, name="Phone", price=499.99, in_stock=False, category=category1)

session.add(category1)
session.add(product1)
session.add(product2)
session.commit()