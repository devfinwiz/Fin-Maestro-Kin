#!/bin/bash

# Function to stop Redis gracefully
stop_redis() {
    echo "Stopping Redis gracefully..."
    redis-cli shutdown
}

# Trap SIGTERM signal and call the stop_redis function
trap 'stop_redis' SIGTERM

# Keep the script running in the background
while true; do
    sleep 1
done
