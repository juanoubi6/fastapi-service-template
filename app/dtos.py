from typing import Generic, List, Optional, TypeVar

from models import Address, User
from pydantic import BaseModel

T = TypeVar('T')


class Page(BaseModel, Generic[T]):
    page: int
    page_size: int
    total_records: int
    data: List[T]


class BasePaginationFilters(BaseModel):
    page: int = 1
    page_size: int = 10
    order_by: Optional[str] = None


class UserFiltersDTO(BasePaginationFilters):
    name: Optional[str] = None


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

    async def from_user(user: User) -> "UserDTO":
        addresses = await user.awaitable_attrs.addresses

        return UserDTO(
            id=user.id,
            name=user.name,
            company=user.company,
            addresses=[AddressDTO.from_address(address) for address in addresses],
        )


class CreateAddressDTO(BaseModel):
    address_1: str


class CreateUserDTO(BaseModel):
    name: str
    company: Optional[str] = None
    addresses: Optional[List[CreateAddressDTO]] = None


class UpdateUserDTO(BaseModel):
    name: Optional[str] = None
    company: Optional[str] = None
