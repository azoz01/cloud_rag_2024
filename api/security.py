from fastapi import HTTPException


def verify_credential(token):
    if token != "walaszekgrubasiekiedynowybomba":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True
