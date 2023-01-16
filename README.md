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

- Cron service running (if you want the transfer process to not be manual)
  - this implies the features isn't supported on Windows
  - transfers can be execuated manually, using `python manage.py {name_of_cron_task}`
  - on WSL remember to start `cron` by running `sudo service cron start`
- Cron scripts registered as tasks using `python manage.py installtasks`
- Transactions can be iniated from your particular account, to any external bank selected from a drop-down
- For a successful transfer, both servers need to have a local reservation Bank account of each other (pointing to the correct URL)
  - and the receiving, Target customer account must exist
