#!/bin/sh

echo "${RTE} Runtime Environment - Running entrypoint."

if [ "$RTE" = "dev" ]; then

    python manage.py makemigrations --merge
    python manage.py migrate --noinput
    python manage.py runserver "$APP_IP_SCOPE":8000

elif [ "$RTE" = "test" ]; then

    echo "This is test."

elif [ "$RTE" = "prod" ]; then

    python manage.py check --deploy #checks whether project is ready for production, i.e. are you running debug mode, https, set-up, etc.
    python manage.py collectstatic --noinput #puts static subfolders together into a single one
    gunicorn dj_deploy.asgi:application -b 0.0.0.0:8080 -k uvicorn.workers.UvicornWorker # needs to be 0.0.0.0, as 127.0.0.1 won't work, as nginx doesn't know localhost 

fi
