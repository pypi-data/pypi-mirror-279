#!/usr/bin/env bash

set -euo pipefail

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <version number>"
    exit 1
fi
APP_VERSION=$1

# Get the path of the directory where the script is located
BUILD_DIR=$(dirname "$(readlink -f "$0")")
APP_NAME="doris-sql-convertor-${APP_VERSION}-bin-x86"
HOME_DIR="${BUILD_DIR}/${APP_NAME}"

SPEC_FILE="${BUILD_DIR}/transform.spec"
DIST_PATH="${HOME_DIR}/bin/"
LOG_PATH="${HOME_DIR}/log"
LIB_PATH="${HOME_DIR}/lib"
CONF_PATH="${HOME_DIR}/conf"

# Clean up previous packaging files
rm -rf "${BUILD_DIR}/dist/${APP_NAME}"
rm -rf "${BUILD_DIR}/build/${APP_NAME}"
rm -rf "${BUILD_DIR}/${APP_NAME}"

# Check if pyinstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstaller is not installed, please install PyInstaller first."
    exit 1
fi

# Check python version
PYTHON_CMD=python3.9
PYTHON_PATH=`which ${PYTHON_CMD}`
version=$(${PYTHON_CMD} --version 2>&1 | awk '{print $2}')
major=$(echo $version | cut -d. -f1)
minor=$(echo $version | cut -d. -f2)
if [[ $major -lt 3 ]] || [[ $major -eq 3 && $minor -lt 7 ]]; then
    echo "Error: Python(${PYTHON_PATH}) version is less than 3.7: ${version}"
    exit 1
fi

echo "Python(${PYTHON_PATH}) version is $version, which is 3.7 or higher."

# Create output and log directories
mkdir -p "${DIST_PATH}"
mkdir -p "${LOG_PATH}"
mkdir -p "${LIB_PATH}"
mkdir -p "${CONF_PATH}"

# Check if the SPEC_FILE exists
if [ ! -f "$SPEC_FILE" ]; then
    echo "SPEC file does not exist: $SPEC_FILE"
    exit 1
fi

# Replace application name and dist_path in the .spec file using sed
sed -i "s/name='[^']*'/name='${APP_NAME}'/g" "$SPEC_FILE"

# Create and activate Python virtual environment
${PYTHON_CMD} -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
if [ ! -f "requirements.txt" ]; then
    echo "Dependencies file does not exist: requirements.txt"
    exit 1
fi
pip install -r requirements.txt
pip install ..


# Compile the project using PyInstaller
pyinstaller $SPEC_FILE --clean --noconfirm

# Check the result and copy it to the specified directory
if [ -f "./dist/${APP_NAME}" ]; then
    cp "./dist/${APP_NAME}" "${LIB_PATH}"
    cp "./bin/start.sh" "${DIST_PATH}"
    cp "./bin/stop.sh" "${DIST_PATH}"
    cp "../release-notes.md" "${HOME_DIR}"
    cp "./README.md" "${HOME_DIR}"
    cp "../LICENSE_SQLGLOT" "${HOME_DIR}"
    cp "../LICENSE" "${HOME_DIR}"
else
    echo "Compilation failed: ${APP_NAME} not found in '/dist/'"
    exit 1
fi

# Generate and write the configuration file
cat <<EOF >"${CONF_PATH}/config.conf"
# Default configurations
version=${APP_VERSION}
port=5001
EOF
cat <<EOF >"${CONF_PATH}/udf_functions.conf"
# Default configurations
[Functions]
extra=dept_privilege
EOF

# Package the doris-sql-convertor directory
tar -czvf "doris-sql-convertor-${APP_VERSION}-bin-x86.tar.gz" -C "$PWD" ${APP_NAME}/

echo -e "\e[32mCompiled successfully: doris-sql-convertor-${APP_VERSION}-bin-x86.tar.gz.\e[0m"

# When no TTY is available, don't output to console
have_tty=0
if [[ "`tty`" != "not a tty" ]]; then
    have_tty=1
fi

 # Only use colors if connected to a terminal
if [[ ${have_tty} -eq 1 ]]; then
  PRIMARY=$(printf '\033[38;5;082m')
  RED=$(printf '\033[31m')
  GREEN=$(printf '\033[32m')
  YELLOW=$(printf '\033[33m')
  BLUE=$(printf '\033[34m')
  BOLD=$(printf '\033[1m')
  RESET=$(printf '\033[0m')
else
  PRIMARY=""
  RED=""
  GREEN=""
  YELLOW=""
  BLUE=""
  BOLD=""
  RESET=""
fi
printf '\n'
printf '      %s       __________   __________________  ___      %s\n'          $PRIMARY $RESET
printf '      %s      / __/ __/ /  / __/ ___/_  __/ _ \/ _ )     %s\n'          $PRIMARY $RESET
printf '      %s     _\ \/ _// /__/ _// /__  / / / // / _  |     %s\n'          $PRIMARY $RESET
printf '      %s    /___/___/____/___/\___/ /_/ /____/____/      %s\n'          $PRIMARY $RESET
printf '      %s                                                 %s\n\n'        $PRIMARY $RESET
printf '      %s   Version:  1.0.5 %s\n'                                        $BLUE   $RESET
printf '      %s   WebSite:  https://selectdb.com%s\n'                          $BLUE   $RESET
printf '      %s   ──────── Doris SQL Convertor ô~ô!%s\n\n'    $PRIMARY  $RESET
