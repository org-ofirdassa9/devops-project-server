from passlib.context import CryptContext
import re
from fastapi import HTTPException, status, Depends
import logging

logger = logging.getLogger(__name__)

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def validate_password(password: str):
    if len(password) < 8:
        logger.warning("Password should be at least 8 characters long.")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Password should be at least 8 characters long.")
    if not re.search("[a-z]", password):
        logger.warning("Password should include lowercase letters.")
        raise HTTPException(detail="Password should include lowercase letters.",
                            status_code=status.HTTP_400_BAD_REQUEST)
    if not re.search("[A-Z]", password):
        logger.warning("Password should include uppercase letters.")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Password should include uppercase letters.")
    if not re.search("[0-9]", password):
        logger.warning("Password should include digits")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password should include digits.")
    if not re.search("[#?!@$ %^&*-]", password):
        logger.warning("Password should include symbols.")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password should include symbols.")
    # Add more rules as per your requirement
    return True


def validate_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not re.fullmatch(regex, email):
        logger.warning("Invalid Email")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Email")
    return True
