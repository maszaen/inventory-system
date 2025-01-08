from decimal import Decimal
from typing import Dict, Any, List, Optional
from datetime import datetime
from bson import ObjectId
from src.database.connection import DatabaseConnection


class Product:
    def __init__(
        self,
        name: str,
        price: Decimal,
        capital: Decimal,
        stock: int,
        _id: Optional[ObjectId] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self._id = _id or ObjectId()
        self.name = name
        self.price = price
        self.capital = capital
        self.stock = stock
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Product":
        return cls(
            _id=data.get("_id"),
            name=data["name"],
            price=Decimal(str(data["price"])),
            capital=Decimal(str(data["capital"])),
            stock=data["stock"],
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "_id": self._id,
            "name": self.name,
            "price": str(self.price),
            "capital": str(self.capital),
            "stock": self.stock,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class ProductManager:
    def __init__(self):
        self.db = DatabaseConnection.get_instance()
        self.collection = self.db.get_collection("products")

    def create_product(self, product: Product) -> ObjectId:
        result = self.collection.insert_one(product.to_dict())
        return result.inserted_id

    def get_all_products(self) -> List[Product]:
        products = self.collection.find()
        return [Product.from_dict(p) for p in products]

    def get_product_by_id(self, product_id: ObjectId) -> Optional[Product]:
        product = self.collection.find_one({"_id": product_id})
        return Product.from_dict(product) if product else None

    def update_product(self, product: Product) -> bool:
        try:
            result = self.collection.update_one(
                {"_id": product._id},
                {
                    "$set": {
                        "name": product.name,
                        "price": str(product.price),
                        "capital": str(product.capital),
                        "stock": product.stock,
                        "updated_at": datetime.utcnow(),
                    }
                },
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating product: {e}")
            return False

    def delete_product(self, product_id: ObjectId) -> bool:
        result = self.collection.delete_one({"_id": product_id})
        return result.deleted_count > 0
