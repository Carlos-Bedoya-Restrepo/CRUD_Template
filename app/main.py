from fastapi import FastAPI
from datetime import datetime
import zoneinfo
from models import Transaction, Invoice
from db import SessionDep,create_all_tables
from .routers import custormers



app=FastAPI(lifespan=create_all_tables)
app.include_router(custormers.router)

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






#Por ahora estos no estan muy elaborados
@app.post("/transactions")
async def create_transactions(transaction_data:Transaction):
    return transaction_data

@app.post("/invoices")
async def create_invoice(invoice_data:Invoice):
    return invoice_data