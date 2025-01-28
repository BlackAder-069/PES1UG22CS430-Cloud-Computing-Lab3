import json
from typing import List, Optional
import products
from cart import dao
from products import Product

# Cache for storing product lookups
_product_cache = {}

class Cart:
    def __init__(self, id: int, username: str, contents: List[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data: dict) -> 'Cart':
        return Cart(data['id'], data['username'], data['contents'], data['cost'])

def get_cart(username: str) -> List[Product]:
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []
    
    # Use list comprehension for better performance
    items = [
        item 
        for detail in cart_details
        for item in eval(detail['contents'])
    ]
    
    # Use cached product lookups
    return [
        _product_cache.setdefault(item, products.get_product(item))
        for item in items
    ]

def add_to_cart(username: str, product_id: int) -> None:
    # Cache the product for future lookups
    if product_id not in _product_cache:
        _product_cache[product_id] = products.get_product(product_id)
    dao.add_to_cart(username, product_id)

def remove_from_cart(username: str, product_id: int):
    dao.remove_from_cart(username, product_id)

def delete_cart(username: str):
    dao.delete_cart(username)


