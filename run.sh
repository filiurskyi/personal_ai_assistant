#!/bin/bash

# Fetch latest repo
git pull

# Specify the path to your virtual environment
venv_path="/home/anjey_mail/personal_ai_assistant/.venv"

# Activate the virtual environment
source "${venv_path}/bin/activate"

# Find the PID of the running "python3 main.py" process
pidtg=$(ps x | grep "python3 main.py" | grep -v grep | awk '{print $1}')

if [ -z "$pidtg" ]; then
    echo "No process found."
else
    echo "Found process with PID: $pidtg"
    # Kill the process
    kill -9 "$pidtg"
fi

# Remove nohup.out file
if [ -f "nohup.out" ]; then
    rm "nohup.out"
    echo "nohup.out removed."
fi


# Find the PID of the running "python3 -m uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8000" process
piduv=$(ps x | grep "python3 -m uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8000" | grep -v grep | awk '{print $1}')

if [ -z "$piduv" ]; then
    echo "No process found."
else
    echo "Found process with PID: $piduv"
    # Kill the process
    kill -9 "$piduv"
fi


# Find the PID of the running "ngrok http 8000 --log=stdout" process
pidng=$(ps x | grep "ngrok http 8000 --log=stdout" | grep -v grep | awk '{print $1}')

if [ -z "$pidng" ]; then
    echo "No process found."
else
    echo "Found process with PID: $pidng"
    # Kill the process
    kill -9 "$pidng"
fi


# Perform a git pull to update the code
git pull --all

# Make alembic migrations
alembic upgrade head

# Start "nohup python3 main.py &"
nohup python3 main.py &

# Deactivate the virtual environment (optional)
deactivate


# ngrok up
ngrok http 8000 --log=stdout >/dev/null &


sleep 5


PUBLIC_URL=$(curl -sS http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url')
echo $PUBLIC_URL