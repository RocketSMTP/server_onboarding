#!/bin/bash

#!/bin/bash

# Function to install Python on Debian-based Linux
install_python_debian() {
    echo "Installing Python on Debian-based Linux..."
    sudo apt-get update -y
    sudo apt-get install python3 -y
    sudo apt-get install python3-pip -y
    echo "Python installed successfully on Debian-based Linux."
}

# Function to install Python on CentOS
install_python_centos() {
    echo "Installing Python on CentOS..."
    sudo yum update -y
    sudo yum install python3 -y
    echo "Python installed successfully on CentOS."
}

# Function to install Python on macOS
install_python_mac() {
    echo "Installing Python on macOS..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    brew install python
    echo "Python installed successfully on macOS."
}

# Function to install Python on Windows
install_python_windows() {
    echo "Installing Python on Windows..."
    powershell.exe -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"
    powershell.exe -Command "choco install python -y"
    echo "Python installed successfully on Windows."
}

# Detect the operating system
OS_TYPE=$(uname)

if [[ "$OS_TYPE" == "Linux" ]]; then
    # Check for CentOS or Debian-based system
    if [ -f /etc/centos-release ]; then
        install_python_centos
    elif [ -f /etc/debian_version ]; then
        install_python_debian
    else
        echo "Unsupported Linux distribution."
        exit 1
    fi
elif [[ "$OS_TYPE" == "Darwin" ]]; then
    install_python_mac
elif [[ "$OS_TYPE" == "MINGW64_NT"* || "$OS_TYPE" == "MSYS_NT"* || "$OS_TYPE" == "CYGWIN_NT"* ]]; then
    install_python_windows
else
    echo "Unsupported operating system: $OS_TYPE"
    exit 1
fi

# Create a virtual environment
python3 -m venv myenv

# Activate the virtual environment
source myenv/bin/activate

# Install necessary packages
pip install paramiko pandas

# Run your script
python automate_servers.py
