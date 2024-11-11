import paramiko
import pandas as pd

# Read the CSV file
servers = pd.read_csv('servers.csv')

# Function to execute commands on a remote server
def execute_commands(server_ip, username, password, domain_name):
    try:
        # Connect to the server
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server_ip, username=username, password=password)

        # Construct the bash script with DOMAIN_NAME
        bash_script_lines = [
            "#!/bin/bash",
            # Check if the URL is present before running sed command
            "if grep -q 'http://mirrors.linode.com' /etc/yum.repos.d/*.repo; then",
            "    sed -i 's|http://mirrors.linode.com|https://vault.centos.org|g' /etc/yum.repos.d/*.repo",
            "    echo 'URL found and replaced.'",
            "else",
            "    echo 'URL not found. No changes made.'",
            "fi",
            "sudo yum install expect -y",
            "cat << 'EOF' > change_root_password.exp",
            "#!/usr/bin/expect",
            'set new_password "ColdEmail2024"',
            "spawn sudo passwd root",
            'expect "Enter new UNIX password:"',
            'send "$new_password\\r"',
            'expect "Retype new UNIX password:"',
            'send "$new_password\\r"',
            "expect eof",
            "EOF",
            "chmod +x change_root_password.exp",
            "./change_root_password.exp",
            "sudo service sshd reload",
            f"hostname {domain_name}",
            "sudo yum update -y",
            "sudo yum install wget -y",
            "sudo wget -O install.sh http://www.aapanel.com/script/install_6.0_en.sh",
            "yes | sudo bash install.sh aapanel",
            "rm -rf install.sh",
            'iptables -A INPUT -m state --state NEW -m tcp -p tcp --dport 143 -j ACCEPT -m comment --comment "IMAP port"',
            'iptables -A INPUT -m state --state NEW -m tcp -p tcp --dport 2526 -j ACCEPT -m comment --comment "pmta port"',
            'iptables -A INPUT -m state --state NEW -m tcp -p tcp --dport 8085 -j ACCEPT -m comment --comment "pmtahttp port"',
            "sudo firewall-cmd --zone=public --add-port=2526/tcp --permanent",
            "sudo firewall-cmd --zone=public --add-port=143/tcp --permanent",
            "sudo firewall-cmd --zone=public --add-port=8085/tcp --permanent",
            "sudo firewall-cmd --reload",
            "sudo yum install perl -y",
            "sudo yum install gdb perl-Cwd perl-File-Temp perl-Getopt-Long perl-POSIX perl-Storable perl-Time-Local perl-strict perl-vars perl-warnings -y",
            "sudo wget -O install.sh https://raw.githubusercontent.com/chimajdev/rocket/main/install.sh",
            "yes | sudo bash install.sh",
            "sudo yum remove postfix3 -y",
            "sudo yum install postfix -y",
            "sudo systemctl enable postfix",
            "sudo systemctl start postfix",
            "sudo systemctl status postfix",
            "sudo service pmta restart"
        ]
        
        bash_script = "\n".join(bash_script_lines)

        # Write the bash script to a remote file
        sftp = ssh.open_sftp()
        script_file = sftp.file('setup.sh', 'w')
        script_file.write(bash_script)
        script_file.close()
        sftp.close()

        # Make the script executable and run it
        stdin, stdout, stderr = ssh.exec_command('chmod +x setup.sh && ./setup.sh')

        # Wait for the command to finish and capture the output
        stdout.channel.recv_exit_status()  # Ensure command execution is finished
        output = stdout.read().decode('utf-8')

        # Print the entire output for debugging purposes
        print("Full output from {}:\n{}".format(server_ip, output))

        # Extract relevant part of the output
        lines = output.splitlines()
        relevant_lines = []
        copy = False
        for line in lines:
            if "Congratulations! Installed successfully!" in line:
                copy = True
            if copy:
                relevant_lines.append(line)
            if "Warning" in line:
                break
        
        if not relevant_lines:
            relevant_output = "Lines Not Found, Please Check If You Installed aaPanel Already!"
        else:
            relevant_output = "\n".join(relevant_lines)

        # Save the output to a file
        with open('{}.txt'.format(server_ip), 'w') as f:
            f.write(relevant_output)

        print('Successfully executed on {}'.format(server_ip))

        # Close the SSH connection
        ssh.close()

    except Exception as e:
        print('Failed to execute on {}: {}'.format(server_ip, e))

# Iterate over each server and execute the script
for index, row in servers.iterrows():
    execute_commands(row['server_ip'], row['username'], row['password'], row['domain_name'])
