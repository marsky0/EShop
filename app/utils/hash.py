import bcrypt

def generate_hash(data: str) -> str:
    return bcrypt.hashpw(data.encode(), bcrypt.gensalt()).decode()

def validate_hash(data: str, hashed: str) -> bool:
    return bcrypt.checkpw(data.encode(), hashed.encode())
