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

