from typing import List, Optional
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship

#####################################################################
class CustomerBase(SQLModel):
    name: str = Field(default=None)
    description: Optional[str] = Field(default=None)
    email: str = Field(default=None)
    age: int = Field(default=None)

class CustomerCreate(CustomerBase):  # Esto es porque cuando se crea a veces necesita parámetros de entrada como la contraseña
    pass

class CustomerUpdate(CustomerBase):  # Esto es porque cuando se crea a veces necesita parámetros de entrada como la contraseña
    pass

class Customer(CustomerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    transactions: List["Transaction"] = Relationship(back_populates="customer")  # Relación bidireccional

########################################################################

class TransactionBase(SQLModel):
    ammount: int = Field(default=None)
    description: str = Field(default=None)

class TransactionCreate(TransactionBase):
    customer_id: Optional[int] = Field(foreign_key="customer.id")


class Transaction(TransactionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: Optional[int] = Field(foreign_key="customer.id")
    customer: Optional["Customer"] = Relationship(back_populates="transactions")  # Relación bidireccional

########################################################################

class Invoice(BaseModel):
    id: int
    customer: Customer
    transactions: List[Transaction]
    total: int

    @property
    def ammount_total(self):
        return sum(transaction.ammount for transaction in self.transactions)
