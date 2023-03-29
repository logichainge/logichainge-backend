
#!/bin/bash
if [ "$1" == "" ] 
then
echo "No message provided"
else
alembic revision --autogenerate -m "$1"
fi

alembic upgrade heads
