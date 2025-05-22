#!/usr/bin/bash

echo "Migrating"

python manage.py migrate

if [ $? -ne 0 ]; then
    echo "Error migrating"
    exit 1
fi

echo "Migrated"