from datetime import datetime, date
from decimal import Decimal
from typing import Dict, Any, List, Optional
from bson import ObjectId
from src.database.connection import DatabaseConnection


class Transaction:
    def __init__(
        self,
        product_id: ObjectId,
        product_name: str,
        quantity: int,
        total: Decimal,
        date: date,  # Bisa menerima datetime.date
        _id: Optional[ObjectId] = None,
        created_at: Optional[datetime] = None,
    ):
        self._id = _id or ObjectId()
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity
        self.total = total
        self.date = date
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "_id": self._id,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "quantity": self.quantity,
            "total": str(self.total),  # Konversi Decimal ke string
            "date": datetime.combine(
                self.date, datetime.min.time()
            ),  # Konversi date ke datetime
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Transaction":
        return cls(
            _id=data.get("_id"),
            product_id=data["product_id"],
            product_name=data["product_name"],
            quantity=data["quantity"],
            total=Decimal(str(data["total"])),
            date=data["date"].date(),  # Konversi datetime ke date
            created_at=data.get("created_at"),
        )


class TransactionManager:
    def __init__(self):
        self.db = DatabaseConnection.get_instance()
        self.collection = self.db.get_collection("transactions")

    def create_transaction(self, transaction: Transaction) -> bool:
        try:
            result = self.collection.insert_one(transaction.to_dict())
            return bool(result.inserted_id)
        except Exception as e:
            print(f"Error creating transaction: {e}")
            return False

    def update_transaction(self, transaction: Transaction) -> bool:
        try:
            result = self.collection.update_one(
                {"_id": transaction._id}, {"$set": transaction.to_dict()}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating transaction: {e}")
            return False

    def get_all_transactions(self) -> List[Transaction]:
        transactions = self.collection.find().sort("date", -1)
        return [Transaction.from_dict(t) for t in transactions]

    def get_transaction_by_id(self, transaction_id: ObjectId) -> Optional[Transaction]:
        transaction = self.collection.find_one({"_id": transaction_id})
        return Transaction.from_dict(transaction) if transaction else None

    def get_transactions_by_date_range(
        self, start_date: date, end_date: date
    ) -> List[Transaction]:
        try:
            # Konversi date ke datetime untuk query MongoDB
            start = datetime.combine(start_date, datetime.min.time())
            end = datetime.combine(end_date, datetime.max.time())

            transactions = self.collection.find(
                {"date": {"$gte": start, "$lte": end}}
            ).sort("date", -1)

            return [Transaction.from_dict(t) for t in transactions]
        except Exception as e:
            print(f"Error getting transactions: {e}")
            return []

    def delete_transaction(self, transaction_id: ObjectId) -> bool:
        result = self.collection.delete_one({"_id": transaction_id})
        return result.deleted_count > 0
