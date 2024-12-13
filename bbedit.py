#!/usr/bin/python3

import re
import subprocess
import argparse


def check_host_key(ip_address):
    """
    Check if the SSH connection succeeds or fails due to a host key issue.
    """
    ssh_check_command = [
        "ssh",
        "-o", "BatchMode=yes",
        "-o", "StrictHostKeyChecking=no",
        "-o", "UserKnownHostsFile=/dev/null",
        ip_address, "exit"
    ]
    try:
        # Run the SSH command to test the connection
        subprocess.run(ssh_check_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError as e:
        # If the error indicates a host key issue
        if "Host key verification failed" in e.stderr.decode():
            print(f"Host key verification failed for {ip_address}. Please check your SSH settings.")
        else:
            print(f"SSH connection to {ip_address} failed: {e.stderr.decode()}")
        return False


def open_bbedit_with_sftp(selected_text):
    # Regex to capture the parts needed from the selected text
    match = re.search(r'\[.*\(([\w\s]*([\d\.]+))\)\s+(.*?)]\s+(.*)', selected_text)

    if match:
        # Step 1: Extract the raw IP part which may have alphanumeric text
        raw_captured = match.group(1).strip()  # Captures 'Qp7 10.150.2.19'

        # Step 2: Use regex to clean the alphanumeric text, leaving only the digits (IP address)
        ip_address = re.sub(r'\b\w*[a-zA-Z]+\w*\b', '', raw_captured).strip()  # Captures '10.150.2.19'

        # Validate IP address format
        if not re.match(r'^\d{1,3}(\.\d{1,3}){3}$', ip_address):
            print(f"Invalid IP address format: {ip_address}")
            return

        # Check host key and return if it fails
        if not check_host_key(ip_address):
            return

        # Step 3: Extract the file path (e.g., '/usr/local/bin')
        file_path = match.group(3).strip()

        # Normalize the file path by handling '~/' and standalone '~'
        if file_path.startswith('~/'):
            file_path = file_path.replace('~/', '/root/')
        elif file_path == '~':
            file_path = ''

        # Step 4: Extract the file name (e.g., 'restartPostfix.sh')
        file_name = match.group(4).strip()

        # Build the full path
        if file_path:
            full_path = file_path + "/" + file_name
        else:
            full_path = file_name

        # Build the SFTP URL
        sftp_url = f"sftp://{ip_address}/{full_path}"

        # Execute the BBEdit command with the SFTP URL
        bbedit_command = ["/usr/local/bin/bbedit", sftp_url]

        try:
            subprocess.run(bbedit_command, check=True)
            print(" ")
        except subprocess.CalledProcessError as e:
            print(f"Failed to open BBEdit: {e}")

    else:
        print("Invalid selection. Could not parse IP and file path.")


if __name__ == "__main__":
    # Argument parser to pass selected text
    parser = argparse.ArgumentParser(description="Open a file in BBEdit via SFTP.")
    parser.add_argument('selected_text', nargs='?', default=None,
                        help='The selected text to extract the IP and file path from')
    args = parser.parse_args()

    if args.selected_text:
        selected_text = args.selected_text

        # Cleaning up unwanted commands from the selected text
        final = re.sub(r'\b(cat|nano|sudo)\b', '', selected_text).strip()

        # Call the function with cleaned-up selected text
        open_bbedit_with_sftp(final)