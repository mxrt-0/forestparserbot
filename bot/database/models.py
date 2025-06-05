from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, Integer, Boolean, String, Text

from bot.database.utils import KleinanzeigenOneUtilities

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    refferer_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    current_balance: Mapped[int] = mapped_column(Integer, default=0)
    total_balance: Mapped[int] = mapped_column(Integer, default=0)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)


class KleinanzeigenOneData(Base):
    __tablename__ = "kleinanzeigenOne"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    url: Mapped[str] = mapped_column(String, nullable=False)
    views: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[str] = mapped_column(String, nullable=False)
    scraped_at: Mapped[str] = mapped_column(String, nullable=False)


class KleinanzeigenOnePreferences(Base):
    __tablename__ = "kleinanzeigenOnePreferences"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    subcategories: Mapped[str] = mapped_column(
        Text, default=KleinanzeigenOneUtilities.concatenate_subcategories()
    )
    banwords: Mapped[str] = mapped_column(
        Text, default=KleinanzeigenOneUtilities.concatenate_subcategories()
    )
    view_range: Mapped[str] = mapped_column(String)
    price_range: Mapped[str] = mapped_column(String)
