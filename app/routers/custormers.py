from fastapi import HTTPException,status,APIRouter
from db import SessionDep
from models import Customer,CustomerCreate,CustomerUpdate,Plan,CustomerPlan
from sqlmodel import select 

router=APIRouter()

@router.post("/customers",response_model=Customer,tags=['customers'])  #session es una clase que pérmite hacer querys
async def create_customer(customer_data:CustomerCreate,session:SessionDep): 
    customer=Customer.model_validate(customer_data.model_dump())#esto almacena en un diccionario
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@router.get("/customers/{customer_id}",response_model=Customer,tags=['customers'])
async def read_customer(customer_id:int,session:SessionDep):
    customer_db=session.get(Customer,customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Customer doesn't exist")
    return customer_db

@router.patch("/customers/{customer_id}",response_model=Customer,status_code=status.HTTP_201_CREATED,tags=['customers'])
async def read_customer(customer_id:int,customer_data: CustomerUpdate,session:SessionDep):
    customer_db=session.get(Customer,customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Customer doesn't exist")
    
    customer_data_dict=customer_data.model_dump(exclude_unset=True)
    customer_db.sqlmodel_update(customer_data_dict)
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db

@router.delete("/customers/{customer_id}",tags=['customers'])
async def read_customer(customer_id:int,session:SessionDep):
    customer_db=session.get(Customer,customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Customer doesn't exist")
    session.delete(customer_db)
    session.commit()
    return {"detail":"ok"}

@router.get("/customers",response_model=list[Customer],tags=['customers'])
async def list_customer(session:SessionDep):
    return session.exec(select(Customer)).all()


@router.post("/customers/{customer_id}/plans/{plan_id}",tags=['customers'])
async def subscribe_customer_to_plan(customer_id:int,plan_id:int,session:SessionDep):
    customer_db=session.get(Customer,customer_id)
    plan_db=session.get(Plan,plan_id)
    if not customer_db or not plan_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="The customer or plan doesn't exist")
    customer_plan_db = CustomerPlan(plan_id=plan_db.id,customer_id=customer_db.id)
    session.add(customer_plan_db)
    session.commit()
    session.refresh(customer_plan_db)
    return customer_plan_db


@router.get("/customers/{customer_id}/plans",tags=['customers'])
async def get_customer_to_plan(customer_id:int,session:SessionDep):
    customer_db=session.get(Customer,customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="The customer doesn't exist")

    return customer_db.plans
