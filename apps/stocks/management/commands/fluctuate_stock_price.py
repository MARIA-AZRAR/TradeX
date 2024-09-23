from decimal import Decimal
import numpy as np
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from apps.stocks.models import Stock, PriceChangeLog
from apps.watchlist.models import Watchlist

class Command(BaseCommand):
    def add_arguments(self, parser) -> None:
        parser.add_argument("id", type=int, help="id of a stock", nargs='?')
        parser.add_argument("percentage", type=float, help="based on percentage it is identified how much price will fluctuate")
    
      
    def handle(self, *args, **options):
        stock_id = options.get('id', None)
        percentage = options.get('percentage') / 100
        
        if stock_id:
            try:
                stock = Stock.active_objects.get(id=stock_id)
                perform_fluctuation(self, stock, percentage)
            except Stock.DoesNotExist:
                raise CommandError(f"No Stock exists with id {stock_id}")
        
        else:
            stocks = Stock.active_objects.all()
            for stock in stocks:
                perform_fluctuation(self, stock, percentage)
        

@transaction.atomic
def perform_fluctuation(self, stock, percentage):
    fluctuate = np.random.normal(0, percentage)
    old_price = stock.current_price
    new_price = max(stock.current_price * Decimal(1+ fluctuate) , 0) # avoid negative value 
    
    price_change_log = PriceChangeLog (
        stock = stock,
        old_price = stock.current_price,
        new_price = new_price
    )
    
    stock.current_price = new_price
    stock.save() 
    
    price_change_log.save()
    
    check_alert_price(stock, old_price)
    
    self.stdout.write(self.style.SUCCESS(f'{stock.company_name} new price: {stock.current_price:.2f}'))
    

def check_alert_price(stock, old_price):
    watchlists = Watchlist.objects.filter(stock=stock)
    
    for watchlist in watchlists:
        if send_alert(watchlist.alert_price, old_price, stock.current_price):
            print('--------- price alert ------------') 
        
        
def send_alert(alert_price, old_price, new_price):
    if old_price > alert_price: 
        # send alert when price decrease
        return new_price <= alert_price
    else:
        # send alert when price increases
        return new_price >= alert_price