import re
import subprocess
import argparse

def open_bbedit_with_sftp(selected_text):
    match = re.search(r'\[.*\(([\w\d\s\.]+)\)\s.*\]\s+(.*)', selected_text)

    if match:
        raw_captured = match.group(1)
        ip_address = re.sub(r'\b\w*[a-zA-Z]+\w*\b', '', raw_captured).strip()
        file_path = match.group(2)

        sftp_url = f"sftp://{ip_address}/{file_path}"
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

        final = selected_text.replace('cd', '').replace('cat', '').replace('nano', '').replace('vi', '').replace('vim', '').strip()
        open_bbedit_with_sftp(final)
