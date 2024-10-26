from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

# Модель Wallet
class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, unique=True, index=True)
    balance_eth = Column(Float)  # Баланс в ETH
    total_balance_usd = Column(Float)  # Баланс в USD
    last_transaction = Column(DateTime)  # Дата последней транзакции
    first_transaction = Column(DateTime)  # Дата первой транзакции
    risk_score = Column(Float)  # Уровень риска

    # Связь с таблицей Transaction
    transactions = relationship("Transaction", back_populates="wallet")


# Модель Transaction
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    hash = Column(String, unique=True, index=True)
    status = Column(String)  # Статус транзакции
    block_chain = Column(String)  # Блокчейн (например, Ethereum)
    block_number = Column(String)  # Номер блока
    block_confirmations = Column(Integer)  # Количество подтверждений блока
    date = Column(DateTime)  # Дата транзакции
    from_address = Column(String)  # Отправитель
    to_address = Column(String)  # Получатель
    value_eth = Column(Float)  # Значение в ETH
    value_usd = Column(Float)  # Значение в USD
    gas_used = Column(Float)  # Количество использованного газа
    transaction_fee_eth = Column(Float)  # Комиссия за транзакцию в ETH
    transaction_fee_usd = Column(Float)  # Комиссия за транзакцию в USD
    wallet_id = Column(Integer, ForeignKey('wallets.id'))  # Внешний ключ на таблицу кошельков

    wallet = relationship("Wallet", back_populates="transactions")
