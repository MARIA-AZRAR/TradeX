from django.db import transaction
from apps.trading.helpers import convert_currency
from .models import Transaction, Portfolio


def handle_transaction(user, stock, account, quantity, transaction_type):
    """handle the operation of stock buying and selling """
    
    # convert stock currency according to user account currency
    price = convert_currency(stock.current_price, stock.currency, account.currency)
    total_amount = price * quantity
    
    with transaction.atomic():
        if transaction_type == Transaction.TransactionTypes.BUY:
            if stock.volume < quantity:
                raise ValueError("Stock doesn't have this much shares")
            if account.balance < total_amount:
                raise ValueError("Insufficient balance")
            
            portfolio = Portfolio.objects.get(stock=stock, user=user)
            
            if portfolio:
                portfolio.quantity += quantity
            else:
                portfolio = Portfolio(user=user, stock=stock, quantity=quantity, purchase_price=stock.current_price)
                
            account.balance = float(account.balance) - total_amount
            account.save()
            
            portfolio.save()
            
            Transaction.objects.create(
                user = user,
                stock = stock,
                quantity = quantity,
                price_at_transaction = stock.current_price,
                transaction_type = transaction_type,
                status = Transaction.StatusTypes.COMPLETED
            )
            
        else:
            try:
                portfolio = Portfolio.objects.get(stock=stock, user=user)
                # Now check if the user owns enough shares
                if portfolio.quantity < quantity:
                    raise ValueError("You don't own enough shares of this stock.")
            except Portfolio.DoesNotExist:
                raise ValueError("You don't own any shares of this stock.")
            
            Transaction.objects.create(
                    user = user,
                    stock = stock,
                    quantity = quantity,
                    price_at_transaction = stock.current_price,
                    transaction_type = transaction_type,
                    status = Transaction.StatusTypes.PENDING
                )
                
def handle_transaction_status(data, status, account):
    
    with transaction.atomic():
        if status == Transaction.StatusTypes.COMPLETED:
            price = convert_currency(data.price_at_transaction, data.stock.currency, account.currency)
            total_amount = price * data.quantity
            
            try:
                portfolio = Portfolio.objects.get(stock=data.stock, user=data.user)
                # Now check if the user owns enough shares
                if portfolio.quantity < data.quantity:
                    raise ValueError("You don't own enough shares of this stock.")
            except Portfolio.DoesNotExist:
                raise ValueError("You don't own any shares of this stock.")

            portfolio.quantity -= data.quantity

            #  if sold all the shares 
            if portfolio.quantity == data.quantity:
                portfolio.delete()
            else:
                portfolio.save()
                
            account.balance = float(account.balance) + total_amount
            account.save()
        
        # in case of completed or failed update the status
        data.status = status
        data.save()
            
            
            
# Check stock exists or not

    # User wants to buy a Stock

        # Check User balance (Convert the Currency)
        # Check if portfolio already has a stock (Buy at once ) minus the balance from account and increase quantity
            # otherwise create portfolio
        # Do a Transaction Entry

    # User wants to sell a stock
        #  Check if Portfolio has that Stock
        # Check if user owns the quantity
        # make the transaction and status pending
        # Once Admin approves the transaction (decrease the quantity and increase user account balance)
        
        
# if all shares given should i remove the stock from portfolio
# didn't check if stock had that much quantity