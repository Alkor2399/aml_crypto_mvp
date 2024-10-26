import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import SessionLocal
from app.moralis_service import MoralisService
from app.wallet_service import WalletService



def main():
    if len(sys.argv) < 3:
        print("Использование: python run_analysis.py <moralis_api_key> <wallet_address1> [<wallet_address2> ...]")
        return

    api_key = sys.argv[1]
    addresses = sys.argv[2:]

    db_session = SessionLocal()
    moralis_service = MoralisService(api_key)
    wallet_service = WalletService(moralis_service, db_session)

    for address in addresses:
        print(f"Обработка кошелька: {address}")
        wallet_service.save_wallet_and_transactions(address)

    print("Анализ завершен. Данные сохранены в базе данных.")

if __name__ == "__main__":
    main()
