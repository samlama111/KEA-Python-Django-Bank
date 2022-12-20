# KEA-Python-Django-Bank

Final project of a banking system done in Django

## Prerequisites

- Python 3.9+, Django 4.0+

## Instructions

- install requirements in `requirements.txt`
    - to fix Chatterbot installation issues ([module time](https://stackoverflow.com/questions/66799322/chatterbot-attributeerror-module-time-has-no-attribute-clock), [module collections](https://stackoverflow.com/questions/72659999/chatterbot-module-error-attributeerror-module-collections-has-no-attribute)):
        - Open the file <Python-folder>\Lib\site-packages\sqlalchemy\util\compat.py Go to line 264 which states:
        ```
        if win32 or jython:
            time_func = time.clock
    
        else:
            time_func = time.time
        ```
        and change it to:
        ```
        if win32 or jython:
            #time_func = time.clock
            pass
        else:
            time_func = time.time
        ```
        - Open the file <Python-folder>\Lib\site-packages\yaml\constructor.py, go to line 126:
            - change `collections.Hashable` to `collections.abc.Hashable` (`if not isinstance(key, collections.abc.Hashable):`)
- download nltk data for the chatbot by running the nltk_download.py file and downloading all packages through the GUI presented.
Run `python nltk_download.py` and use the GUI to download all packages.
- set-up database & migrate using `python manage.py migrate`
- (optional) create super user using `python manage.py createsuperuser`
- populate the database using `python manage.py setup`
- create your own account or:
  - log-in as a customer using username: `user`, password: `test123`
  - as an employee using username: `employee`, password: `test123`

## Inter-bank transfer prerequisites

- Cron service running
  - implies Windows isn't supported, but can still execute transfers, but just manually, using `python manage.py {name_of_cron_task}`
- Cron scripts registered as tasks using `python manage.py installtasks`
- ATM transactions can be only iniated using the [API](http://localhost:8000/api/v1/transaction)
  - Make sure to use:
    - a UUID as `token`
    - select a correct Reservation bank account
- For a successful transfer, both servers need to have a local Bank account of each other (pointing to the correct URL)
  - Target customer account must exist
