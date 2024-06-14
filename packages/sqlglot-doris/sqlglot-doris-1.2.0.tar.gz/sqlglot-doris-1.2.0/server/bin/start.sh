#!/bin/bash

# Define the directory of the application and the path of the configuration file, adjust according to actual situation
# Get the path of the directory where this script is located
BIN_DIR=$(dirname "$(readlink -f "$0")")

# Get the directory of the script
APP_DIR=$(dirname "$BIN_DIR")
LOG_PATH="${APP_DIR}/log/"
CONFIG_FILE="${APP_DIR}/conf/config.conf"


# Read the version and port number of the application
if [ -f "$CONFIG_FILE" ]; then
    source $CONFIG_FILE
else
    echo "Configuration file not found: $CONFIG_FILE"
    exit 1
fi

# Define the full path of the application executable
APP_EXECUTABLE="${APP_DIR}/lib/doris-sql-convertor-$version-bin-x86"

# Check if the executable exists
if [ ! -f "$APP_EXECUTABLE" ]; then
    echo "Executable not found: $APP_EXECUTABLE"
    exit 1
fi

# Start the application
nohup $APP_EXECUTABLE run --host=0.0.0.0 --port=$port > "${LOG_PATH}/nohup.out" 2>&1 &

echo -e "\e[32mdoris-sql-convertor started on port $port with version $version.\e[0m"
