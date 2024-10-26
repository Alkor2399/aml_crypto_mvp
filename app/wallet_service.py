from app.models import Wallet, Transaction
from datetime import datetime

class WalletService:
    def __init__(self, moralis_service, db_session):
        self.moralis_service = moralis_service
        self.db_session = db_session

    def save_wallet_and_transactions(self, address):
        # Получаем данные о кошельке
        wallet_data = self.moralis_service.get_wallet_info(address)
        transactions_data = self.moralis_service.get_wallet_transactions(address)

        # Проверяем, есть ли кошелек в БД
        wallet = self.db_session.query(Wallet).filter_by(address=address).first()
        if not wallet:
            wallet = Wallet(address=address)
            self.db_session.add(wallet)
            self.db_session.commit()
            self.db_session.refresh(wallet)

        # Обновляем данные о балансе кошелька
        if 'balance' in wallet_data:
            wallet.balance_eth = float(wallet_data['balance']) / 1e18  # Преобразуем из wei в ETH
        else:
            print(f"Ошибка: Не удалось получить баланс для кошелька {address}")

        # Проверяем, есть ли транзакции
        if transactions_data and len(transactions_data) > 0:
            # Обновляем данные о первой транзакции
            first_tx = transactions_data[-1]  # Самая первая транзакция в конце списка
            if 'block_timestamp' in first_tx:
                wallet.first_transaction = datetime.fromtimestamp(int(first_tx['block_timestamp']))
            else:
                print(f"Ошибка: Первая транзакция для кошелька {address} не содержит 'block_timestamp'")

            # Обновляем данные о последней транзакции
            last_tx = transactions_data[0]  # Последняя транзакция в начале списка
            if 'block_timestamp' in last_tx:
                wallet.last_transaction = datetime.fromtimestamp(int(last_tx['block_timestamp']))
            else:
                print(f"Ошибка: Последняя транзакция для кошелька {address} не содержит 'block_timestamp'")

            # Сохраняем транзакции
            for tx in transactions_data:
                existing_tx = self.db_session.query(Transaction).filter_by(hash=tx['hash']).first()
                if not existing_tx:
                    try:
                        transaction = Transaction(
                            hash=tx['hash'],
                            status=tx.get('receipt_status'),
                            block_chain='Ethereum',  # Пока только Ethereum
                            block_number=tx.get('block_number'),
                            block_confirmations=tx.get('confirmations'),
                            date=datetime.fromtimestamp(int(tx['block_timestamp'])) if 'block_timestamp' in tx else None,
                            from_address=tx.get('from_address'),
                            to_address=tx.get('to_address'),
                            value_eth=float(tx['value']) / 1e18 if 'value' in tx else None,
                            value_usd=self.convert_eth_to_usd(float(tx['value']) / 1e18) if 'value' in tx else None,
                            gas_used=float(tx['gas_used']) if 'gas_used' in tx else None,
                            transaction_fee_eth=(float(tx['gas_price']) * float(tx['gas_used']) / 1e18) if 'gas_price' in tx and 'gas_used' in tx else None,
                            transaction_fee_usd=self.convert_eth_to_usd(float(tx['gas_price']) * float(tx['gas_used']) / 1e18) if 'gas_price' in tx and 'gas_used' in tx else None,
                            wallet_id=wallet.id
                        )
                        self.db_session.add(transaction)
                    except Exception as e:
                        print(f"Ошибка при сохранении транзакции {tx['hash']}: {e}")
        else:
            print(f"Транзакции для кошелька {address} не найдены или отсутствуют.")

        # Сохраняем изменения в кошельке
        self.db_session.commit()

    def convert_eth_to_usd(self, eth_value):
        # Пример конвертации ETH в USD, замените на актуальный курс
        usd_value = eth_value * 3000  # Замените на реальный курс или API для получения актуального курса
        return usd_value
