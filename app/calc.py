from decimal import Decimal
import math
from .models import Receipt, Item
from datetime import date, time

class CalculatePoints:
    def __init__(self, logger):
        self.logger = logger
    
    def calculate_total_points(self, receipt: Receipt) -> int:
        total = Decimal(receipt.total)
        items = receipt.items
        points = 0 
        
        points+=self.points_for_retailer(receipt.retailer)
        points+=self.points_for_round_total(total)
        points+=self.points_for_mulitple_of_twenty_five(total)
        points+=self.points_for_pair_items(len(items))
        points+=self.points_for_item_description(items)
        points+=self.points_for_odd_day(receipt.purchaseDate)
        points+=self.points_for_afternoon(receipt.purchaseTime)
        
        self.logger.info(f"Total points for receipt {receipt.retailer} is {points}")
        return points
        
    def points_for_retailer(self,retailer_name) -> int:
        points = 0
        for char in retailer_name:
            if(char.isalnum()):
                points+=1
        return points

    def points_for_round_total(self,total: Decimal) -> int:
        if total == total.to_integral_value(): return 50
        else: return 0

    def points_for_mulitple_of_twenty_five(self, total: Decimal) -> int:
        if(total*100)%25==0: return 25
        else: return 0
    
    def points_for_pair_items(self, item_count: int) -> int:
        return ((item_count)//2)*5
    
    def points_for_item_description(self, items: list[Item]) -> int:
        total = 0
        for item in items:
            description = item.shortDescription.strip()
            if(len(description)%3 == 0):
                price = Decimal(item.price)
                points = math.ceil(price * Decimal('0.2'))
                total+=points
        return total

    def points_for_odd_day(self, purchase_date: date) -> int:
        if purchase_date.day%2!=0: return 6
        else: return 0
    
    def points_for_afternoon(self, purchase_time: time) -> int:
        if(purchase_time.hour>=14 and purchase_time.hour<16): return 10
        else: return 0

    