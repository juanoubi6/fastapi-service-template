from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict
from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

T = TypeVar('T')


class BaseDBModel(DeclarativeBase, AsyncAttrs):
    pass


class PagedResult(BaseModel, Generic[T]):
    total_records: int
    data: List[T]

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        populate_by_name=True
    )


class User(BaseDBModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str]
    company: Mapped[Optional[str]]

    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class Address(BaseDBModel):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    address_1: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(back_populates="addresses")


class AddressDTO(BaseModel):
    id: int
    address_1: str

    def from_address(address: Address) -> "AddressDTO":
        return AddressDTO(id=address.id, address_1=address.address_1)


class UserDTO(BaseModel):
    id: int
    name: str
    company: Optional[str]
    addresses: List[AddressDTO]

    def from_user(user: User) -> "UserDTO":
        return UserDTO(
            id=user.id,
            name=user.name,
            company=user.company,
            addresses=[AddressDTO.from_address(address) for address in user.addresses],
        )
