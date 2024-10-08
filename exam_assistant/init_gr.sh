#!/bin/bash
echo
echo

if [[ -e ".env" ]]
  then
    # loading script parameters from .env
    set -a            
    source .env
    set +a
else
    echo "No .env file with paramaters found. Exiting."
    exit 1
fi

echo
echo '2. Executing init_gr.py'
echo
docker exec -it streamlit bash -c "python init_gr.py"

sleep 5

