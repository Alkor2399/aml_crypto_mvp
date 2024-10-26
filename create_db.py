from app.database import engine, Base
from app.models import Wallet, Transaction

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Таблицы созданы")
