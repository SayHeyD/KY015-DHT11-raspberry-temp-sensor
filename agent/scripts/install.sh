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
  modelInfo=$(tr -d '\0' < /proc/device-tree/model)
  if [[ "$modelInfo" != "Raspberry "Pi* ]]; then
    logFatal "Can only be installed on a raspberry pi."
  fi

  logInfo "Installing on $modelInfo"
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

function installApp() {
  # Create application directory
  mkdir -p "$AppPath"

  # Install app files
  cp ./main.py "$AppPath/main.py"
  cp ./pyproject.toml "$AppPath/pyproject.toml"
  cp ./stubs/config.env "$AppPath/config.env"
  cp -R ./app "$AppPath/app"

  logInfo "Created application directory."

  logInfo "Creating python3 virtual environment"
  # Create virtual environment
  python3 -m venv "$AppPath/.venv"
  logInfo "Created python virtual environment."

  # Install dependencies
  source "$AppPath/.venv/bin/activate" && pip3 install .[full]
  logInfo "Installed dependencies"
}

function installService() {
  cp ./stubs/rtsa-agent.service /lib/systemd/system/rtsa-agent.service
  logInfo "Installed Service"
}

function configureApp() {
  logInfo "Setup initial config".
  nano "$AppPath/config.env"
  logInfo "Initial config"
}

function enableService() {
  systemctl daemon-reload
  systemctl enable rtsa-agent.service
}

# Preflight checks 📋
checkRoot
checkDevice
checkIfAlreadyInstalled

# Install and configuration 👩‍💻👨‍💻
installApp
installService
configureApp

# Enable Service 🔄
enableService