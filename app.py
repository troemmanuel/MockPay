import json
import os
import logging
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field, validator
from enum import Enum
import uuid
import random
import httpx
import asyncio
from typing import Dict
import re

app = FastAPI()

# Fichiers
TRANSACTION_FILE = "transactions.json"
ERROR_LOG_FILE = "webhook_errors.log"

# Setup du logging
logging.basicConfig(
    filename=ERROR_LOG_FILE,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# Enums
class PaymentMethod(str, Enum):
    debit_card = "debit_card".upper()
    mobile_money = "mobile_money".upper()


# Spécifique à chaque méthode
class DebitCardData(BaseModel):
    card_number: str
    expiry_date: str
    cvv: str

    @validator("card_number")
    def validate_card_number(cls, v):
        # Simple regex to check if the card number is valid (16 digits)
        if not re.match(r"^\d{16}$", v):
            raise ValueError("Card number must be a 16-digit number.")

        # Additional Luhn algorithm validation could be added here if required
        return v

    @validator("cvv")
    def validate_cvv(cls, v):
        # CVV must be exactly 3 digits
        if not re.match(r"^\d{3}$", v):
            raise ValueError("CVV must be a 3-digit number.")
        return v

    @validator("expiry_date")
    def validate_expiry_date(cls, v):
        # Expiry date should follow the format MM/YY
        if not re.match(r"^(0[1-9]|1[0-2])\/\d{2}$", v):
            raise ValueError("Expiry date must be in the format MM/YY.")
        return v


class MobileMoneyData(BaseModel):
    phone_number: str
    provider: str


# Requête de paiement
class PaymentRequest(BaseModel):
    amount: float = Field(..., gt=0)
    currency: str = "XOF"
    method: PaymentMethod
    customer_id: str
    webhook_url: str
    external_reference: str
    payment_data: Dict

    @validator("payment_data")
    def validate_payment_data(cls, v, values):
        method = values.get("method")
        if method == PaymentMethod.debit_card:
            DebitCardData(**v)
        elif method == PaymentMethod.mobile_money:
            MobileMoneyData(**v)
        return v


class PaymentResponse(BaseModel):
    external_reference: str
    status: str = "processing"


class WebhookNotification(BaseModel):
    transaction_id: str
    status: str
    amount: float
    currency: str
    method: PaymentMethod
    customer_id: str
    external_reference: str


# Chargement du fichier JSON
def load_transactions():
    if os.path.exists(TRANSACTION_FILE):
        with open(TRANSACTION_FILE, "r") as f:
            return json.load(f)
    return {}


# Sauvegarde du fichier JSON
def save_transactions(data):
    with open(TRANSACTION_FILE, "w") as f:
        json.dump(data, f, indent=2)


# Initialisation
transactions_db = load_transactions()


@app.post("/pay", response_model=PaymentResponse)
async def initiate_payment(request: PaymentRequest, background_tasks: BackgroundTasks):
    transaction_id = str(uuid.uuid4())

    if any(tx["external_reference"] == request.external_reference for tx in transactions_db.values()):
        raise HTTPException(status_code=400, detail="external_reference already used")

    transaction_data = {
        "status": "processing",
        "amount": request.amount,
        "currency": request.currency,
        "method": request.method,
        "customer_id": request.customer_id,
        "webhook_url": request.webhook_url,
        "external_reference": request.external_reference,
        "payment_data": request.payment_data
    }

    transactions_db[transaction_id] = transaction_data
    save_transactions(transactions_db)

    background_tasks.add_task(process_payment, transaction_id)

    return PaymentResponse(external_reference=request.external_reference)


async def process_payment(transaction_id: str):
    await asyncio.sleep(2)

    transaction = transactions_db.get(transaction_id)
    if not transaction:
        return

    status = "success" if random.random() < 0.8 else "failed"
    transaction["status"] = status

    notification = WebhookNotification(
        transaction_id=transaction_id,
        status=status,
        amount=transaction["amount"],
        currency=transaction["currency"],
        method=transaction["method"],
        customer_id=transaction["customer_id"],
        external_reference=transaction["external_reference"]
    )

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(transaction["webhook_url"], json=notification.dict())
            if response.status_code != 200:
                raise httpx.HTTPStatusError(f"Unexpected status code {response.status_code}", request=response.request,
                                            response=response)
    except Exception as e:
        error_message = f"[Webhook Error] Impossible d'envoyer la notification à {transaction['webhook_url']}. Erreur : {e}"
        print(error_message)
        logging.error(error_message)  # Log error in the file
        transaction["status"] = "webhook_failed"

    save_transactions(transactions_db)


@app.get("/webhook-errors")
async def get_webhook_errors():
    # Lire les erreurs du fichier de log
    if os.path.exists(ERROR_LOG_FILE):
        with open(ERROR_LOG_FILE, "r") as file:
            errors = file.readlines()
        return {"errors": errors}
    return {"errors": []}
