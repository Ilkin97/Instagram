#!/usr/bin/bash

echo "Making migrations"

python manage.py makemigrations

if [ $? -ne 0 ]; then
    echo "Error making migrations"
    exit 1
fi

echo "Migrations made"