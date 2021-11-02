#!/bin/bash

# must match the name of the service for the database in
# the docker-compose.yml file
DATABASE_SERVICE=postgres
COUNTER=0
EXIT_CODE=1
SECONDS_BEFORE_TIMEOUT=59

# check to see if script is running in docker
if [ -f /.dockerenv ]; then

    # spin until database is ready
    while [ $EXIT_CODE -ne 0 ]
    do
      pg_isready -h $DATABASE_SERVICE
      EXIT_CODE=$?
      COUNTER=`expr $COUNTER + 1`

      sleep 1

      # Check for time out
      if [ $COUNTER -ge $SECONDS_BEFORE_TIMEOUT ]; then
        echo "Timed Out - Database not Found"
        exit 1
      fi

    done
fi

pytest