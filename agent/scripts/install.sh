#!/usr/bin/env bash

# Paths for files
AppPath="/opt/rtsa"
SystemdServicePath="/lib/systemd/system/rtsa-agent.service"
ServiceUserName="rtsa"

# Functions for logging
function log() {
  timestamp=$(date -u +"%Y-%m-%d %T")
  echo "[$timestamp] $1"
}

function logInfo() {
  log "INFO - $1 ✅" > /dev/stdout
}

function logError() {
  log "ERROR - $1 ❌" > /dev/stderr
}

function logFatal() {
  log "FATAL - $1 ❌" > /dev/stderr
  exit 1
}

function checkRoot() {
  if [[ $EUID -ne 0 ]]; then
     logFatal "This script must be run as root."
  fi

  logInfo "Running as root"
}

# Check if device is a raspberry
function checkDevice() {
  modelInfo=$(cat /proc/device-tree/model)
  if [ "$modelInfo" != "Raspberry Pi*" ]; then
    logFatal "Can only be installed on a raspberry pi."
  fi

  logInfo "Installing on $modelInfo"
}

# Check if required packages are install
function checkPackages() {
  pythonVersion="$(python3 --version)"
  if [ "$pythonVersion" != "Python 3.11*" ]; then
    logFatal "Python version 3.11 or newer must be installed!"
  fi
}

# Check if the agent has already been installed
function checkIfAlreadyInstalled() {

  # Check if app files already exist
  if [ -d "$AppPath" ]; then
    logFatal "Application files at $AppPath already exists. If you want to reinstall remove them manually."
  fi

  # Check if systemd service file already exists
  if [ -f "$SystemdServicePath" ]; then
    logFatal "SystemdServicePath service file at $SystemdServicePath already exists. If you want to reinstall remove it manually."
  fi

  logInfo "No previous installation found"
}

function createUserAndGroup() {
  # Create group if it doesn't exist
  if [ $(getent group "$ServiceUserName") ]; then
    logInfo "Group '$ServiceUserName' already exists."
  else
    groupadd "$ServiceUserName"
    logInfo "Created group '$ServiceUserName'"
  fi

  # Create user if it doesn't exist
  if id "$ServiceUserName" >/dev/null 2>&1; then
    logInfo "User '$ServiceUserName' found."
  else
    useradd -s "/usr/bin/bash" -a -G "$ServiceUserName" "$ServiceUserName"
    logInfo "Created user '$ServiceUserName'"
  fi
}

function installApp() {
  # Create application directory
  mkdir -p "$AppPath"

  # Install app files
  cp ../main.py "$AppPath/main.py"
  cp ../requirements.txt "$AppPath/requirements.txt"
  cp ../stubs/config.env "$AppPath/config.env"

  logInfo "Created application directory."

  # Create virtual environment
  python3 -m venv "$AppPath/.venv"
  logInfo "Created python virtual environment."

  # Install dependencies
  source "$AppPath/.venv/bin/activate" && pip3 install -r requirements.txt
  logInfo "Installed dependencies"

  # Set file permissions
  chgrp -R "$ServiceUserName" "$AppPath"
  chmod g+rwx "$AppPath"
}

function installService() {
  cp ../stubs/rtsa-agent.service /lib/systemd/system/rtsa-agent.service
}

function configureApp() {
  logInfo "Setup initial config".
  vi "$AppPath/config.env"
  logInfo "Initial config"
}

function enableService() {
  systemctl daemon-reload
  systemctl enable rsta-agent.service
}

# Preflight checks 📋
checkRoot
checkDevice
checkIfAlreadyInstalled

# Install and configuration 👩‍💻👨‍💻
createUserAndGroup
installApp
installService
configureApp

# Enable Service 🔄
enableService