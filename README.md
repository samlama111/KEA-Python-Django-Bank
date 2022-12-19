# KEA-Python-Django-Bank
Final project of a banking system done in Django

## Inter-bank prerequisites:
- Cron service running
  - implies Windows isn't supported, but can still execute transfers, but just manually, using `python manage.py {name_of_cron_task}` 
- Cron scripts registered as tasks using `python manage.py installtasks`
- ATM transactions can be only iniated using the [API](http://localhost:8000/api/v1/transaction)
  - Make sure to use:
    - a UUID as `token`
    - select a correct Reservation bank account    
- For a successful transfer, both servers need to have a local Bank account of each other (pointing to the correct URL)
  - Target customer account must exist 
