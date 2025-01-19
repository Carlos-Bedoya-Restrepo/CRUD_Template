from fastapi import FastAPI
from datetime import datetime
import zoneinfo
from models import Customer,CustomerCreate, Transaction, Invoice



app=FastAPI()

@app.get("/")
async def root():
    return {"message":"hola mundo"}



country_timezone={
    "CO":"America/Bogota",
    "MX":"America/Mexico_City",
    "AR":"America/Argentina/Buenos_Aires",
    "BR":"America/Sao_Paulo",
    "PE":"America/Lima",
}


@app.get("/time/{iso_code}")
async def time(iso_code: str):
    iso=iso_code.upper()
    timezone_str=country_timezone.get(iso)
    tz=zoneinfo.ZoneInfo(timezone_str)
    return {"time":datetime.now(tz)}


#esto se supone que es nuestra base de datos, que es la lista de customers
db_customers:list[Customer]=[]


@app.post("/customers",response_model=Customer)
async def create_customer(customer_data:CustomerCreate):
    customer=Customer.model_validate(customer_data.model_dump())#esto almacena en un diccionario
    customer.id=len(db_customers)
    db_customers.append(customer)
    return customer


@app.get("/customers",response_model=list[Customer])
async def list_customer():
    return db_customers


@app.post("/transactions")
async def create_transactions(transaction_data:Transaction):
    return transaction_data

@app.post("/invoices")
async def create_invoice(invoice_data:Invoice):
    return invoice_data