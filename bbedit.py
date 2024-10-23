import re
import subprocess
import argparse

def open_bbedit_with_sftp(selected_text):
    match = re.search(r'\[.*\(([\w\s]*([\d\.]+))\)\s+(.*?)]\s+(.*)', selected_text)

    if match:
        # Step 1: Extract the raw IP part which may have alphanumeric text
        raw_captured = match.group(1).strip()  # Captures 'Qp7 10.150.2.19'

        # Step 2: Use regex to clean the alphanumeric text, leaving only the digits (IP address)
        ip_address = re.sub(r'\b\w*[a-zA-Z]+\w*\b', '', raw_captured).strip()  # Captures '10.150.2.19'
        # print("Captured IP Address:", ip_address)

        # Step 3: Extract the file path (e.g., '/usr/local/bin')
        file_path = match.group(3).strip().replace('~', '')
        # print("Captured File Path:", file_path)

        # Step 4: Extract the file name (e.g., 'restartPostfix.sh')
        file_name = match.group(4).strip()
        # print("Captured File Name:", file_name)
        if file_path:
            full_path = file_path + "/" + file_name
        else:
            full_path = file_name
        # print("Full Path:", full_path)

        sftp_url = f"sftp://{ip_address}/{full_path}"
        ssh_command = f"ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {ip_address}"

        bbedit_command = ["/usr/local/bin/bbedit", sftp_url]
        subprocess.run(bbedit_command)
        print(" ")

    else:
        print("Invalid selection. Could not parse IP and file path.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Open a file in BBEdit via SFTP.")
    parser.add_argument('selected_text', nargs='?', default=None, help='The selected text to extract the IP and file path from')
    args = parser.parse_args()

    if args.selected_text:
        selected_text = args.selected_text
        # print(selected_text)

        final = selected_text.replace('cd', '').replace('cat', '').replace('nano', '').replace('vi', '').replace('vim', '').strip()
        open_bbedit_with_sftp(final)
