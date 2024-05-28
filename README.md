# Server Onboarding Automation Script

This repository contains a Python script designed to automate the onboarding process for servers. The script uses SSH to connect to each server, execute a series of commands, and capture relevant output.

## Prerequisites

- Python 3.x
- `paramiko` library
- `pandas` library
- SSH access to the target servers

## Setup

1. **Clone the repository**:
   ```sh
   git clone https://github.com/yourusername/yourrepository.git
   cd yourrepository

2. **Create a virtual environment (optional but recommended)**:
   ```sh
   python3 -m venv venv
   source venv/bin/activate

3. **Install the required Python packages**:
   ```sh
   pip install paramiko pandas

4. **Prepare the servers.csv file**:
   Create a servers.csv file in the root directory of the repository with the following format:
   ```csv
   server_ip,username,password,domain_name
   192.168.1.1,user1,pass1,example.com
   192.168.1.2,user2,pass2,example.org

## Usage

1. **Ensure your local changes are committed**:
   Before running the script, make sure all your changes are committed to your local repository.
   ```sh
   git add .
   git commit -m "Your commit message"

2. **Run the script**:
   ```sh
   chmod +x python_setup.sh
   ./python_setup.sh
   python automate_servers.py

3. **Check the output**:
   The script will create a .txt file for each server, named after the server's IP address. These files will contain the output of the executed commands.



