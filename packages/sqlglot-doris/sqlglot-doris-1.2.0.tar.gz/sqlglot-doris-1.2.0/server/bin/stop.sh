#!/bin/bash

# Get the path of the directory where this script is located
BIN_DIR=$(dirname "$(readlink -f "$0")")
# Get the parent directory of the script
APP_DIR=$(dirname "$BIN_DIR")
# Define the path of the configuration file
CONFIG_FILE="${APP_DIR}/conf/config.conf"
# Define the path of the log file
LOG_FILE="${APP_DIR}/log/nohup.out"

# Read the version and port information from the configuration file
if [ -f "$CONFIG_FILE" ]; then
    source $CONFIG_FILE
else
    echo "Configuration file not found: $CONFIG_FILE"
    exit 1
fi

# Combine the application name with the information from the configuration file
APP_NAME="doris-sql-convertor-$version-bin-x86"

# Output the start information to the log and console
echo "$(date) - Stopping $APP_NAME" | tee -a $LOG_FILE

# Find process IDs that contain the application name
PIDS=$(pgrep -f "$APP_NAME")

# If processes were found, confirm them further by port number
if [ ! -z "$PIDS" ]; then
  echo -e "\e[33mFound application(s) with name $APP_NAME.\e[0m" | tee -a $LOG_FILE
  for PID in $PIDS
  do
    # Check if any process is listening on the specified port using lsof
    if lsof -i TCP:$port -t | grep -q "$PID"; then
      echo -e "\e[31mStopping application with PID $PID on port $port.\e[0m" | tee -a $LOG_FILE
      kill -15 $PID
      sleep 2  # Delay for 2 seconds to provide a buffer for the application

      # Check if the application has stopped
      if kill -0 $PID 2>/dev/null; then
        echo -e "\e[31mFailed to stop process with PID $PID. Trying to kill it forcefully with SIGKILL.\e[0m" | tee -a $LOG_FILE
        kill -9 $PID
      fi

      # Final check to see if the process still exists
      if kill -0 $PID 2>/dev/null; then
        echo -e "\e[31mFailed to terminate process with PID $PID.\e[0m" | tee -a $LOG_FILE
      else
        echo -e "\e[32mSuccessfully terminated process with PID $PID.\e[0m" | tee -a $LOG_FILE
      fi
    else
      echo -e "\e[33mProcess $PID is not listening on port $port, skipping.\e[0m" | tee -a $LOG_FILE
    fi
  done
else
  echo -e "\e[32mNo running application(s) found with name $APP_NAME.\e[0m" | tee -a $LOG_FILE
fi
