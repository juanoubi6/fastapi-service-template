from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel

from app.models import Address, Task, User

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

    def from_model(address: Address) -> "AddressDTO":
        return AddressDTO(id=address.id, address_1=address.address_1)


class UserDTO(BaseModel):
    id: int
    name: str
    company: Optional[str]
    addresses: List[AddressDTO]

    async def from_model(user: User) -> "UserDTO":
        addresses = await user.awaitable_attrs.addresses

        return UserDTO(
            id=user.id,
            name=user.name,
            company=user.company,
            addresses=[AddressDTO.from_model(address) for address in addresses],
        )


class TaskDTO(BaseModel):
    id: int
    description: str

    async def from_model(task: Task) -> "TaskDTO":
        return TaskDTO(
            id=task.id,
            description=task.description,
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


class CreateTaskDTO(BaseModel):
    description: str
