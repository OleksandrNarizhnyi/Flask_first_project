from sqlalchemy import create_engine, Integer, String, ForeignKey, Numeric, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column, relationship

URL = "sqlite:///my_hw_4_database.db"

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
# 1. Наполнение данными
# Добавьте в базу данных категории и продукты.
# with Session() as session:
#
#     category1 = Category(id=1, name="Electronics", description="Gadgets and devices.")
#     category2 = Category(id=2, name="Books", description="Printed books and e-books.")
#     category3 = Category(id=3, name="Clothing", description="Clothing for men and women.")
#
#     product1 = Product(id=1, name="Smartphone", price=299.99, in_stock=True, category=category1)
#     product2 = Product(id=2, name="Laptop", price=499.99, in_stock=True, category=category1)
#     product3 = Product(id=3, name="Sci-Fi Novel", price=15.99, in_stock=True, category=category2)
#     product4 = Product(id=4, name="Jeans", price=40.50, in_stock=True, category=category3)
#     product5 = Product(id=5, name="T-Shirt", price=20.00, in_stock=True, category=category3)
#
#     session.add_all([
#                 category1, category2, category3,
#                 product1, product2, product3, product4, product5
#             ])
#     session.commit()
#     print("Database populated successfully!")
#====================================================================================================
# 2. Извлеките все записи из таблицы categories. Для каждой категории извлеките и выведите все связанные с
# ней продукты, включая их названия и цены.
# with Session() as session:
#     all_from_category = session.query(Category).all()
#
#     for cat in all_from_category:
#         print(f"Категория: {cat.name}, Описание: {cat.description}")
#         for product in cat.products:
#             print(f" Product name: {product.name}, price: {product.price}, available: {product.in_stock}")
#===========================================================================================================
# 3. Обновление данных
# with Session() as session:
#     update_first_in_product = session.query(Product).filter().first()
#     if update_first_in_product:
#         update_first_in_product.price = 349.99
#         session.commit()
#=================================================================================================================
# 4. Агрегация и группировка
# Используя агрегирующие функции и группировку, подсчитайте общее количество продуктов в каждой
# категории.
with Session() as session:
    from sqlalchemy import func
    count_prod_in_category = session.query(
        Category.name,
        func.count(Product.id).label("count_prod")
    ).join(Product).group_by(Category.id).all()

    for count in count_prod_in_category:
        print(f"Category: {count.name} - count of product: {count.count_prod}")