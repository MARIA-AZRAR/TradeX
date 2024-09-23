from django.core.management.base import BaseCommand, CommandError

from apps.trading.models import Transaction
from apps.trading.services import handle_transaction_status
from apps.users.models import Account


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('transaction_id', type=int, nargs='?')
        parser.add_argument('status', type=str, choices=[choice[0] for choice in Transaction.StatusTypes.choices])
        
    def handle(self, *args, **options):
        transaction_id = options.get('transaction_id', None)
        new_status = options['status']
        
        if transaction_id:
            try:  
                tran_object = Transaction.objects.get(id=transaction_id)
                update_transaction(self, tran_object, new_status)
            except Transaction.DoesNotExist:
                raise CommandError(f"No transactions against id: {transaction_id}")
        else:
            tran_objects = Transaction.objects.filter(status=Transaction.StatusTypes.PENDING).order_by('created_at')
            
            for tran_object in tran_objects:
                update_transaction(self, tran_object, new_status)
            
def update_transaction(self, tran_object, new_status):
    if tran_object.status == Transaction.StatusTypes.PENDING:
        try:
            account = Account.objects.get(user=tran_object.user)
            # Process the transaction
            response = handle_transaction_status(tran_object, new_status, account)
            
            if "error" in response:
                self.stdout.write(self.style.ERROR(f"Transaction {tran_object.id} failed: {response['error']}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Transaction {tran_object.id} success: {response['success']}"))
        except Account.DoesNotExist:
            # Set the transaction status to FAILED
            tran_object.status = Transaction.StatusTypes.FAILED
            tran_object.save()
            self.stdout.write(self.style.ERROR(f"Transaction {tran_object.id} failed: No account number against User"))
 