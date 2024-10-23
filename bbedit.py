import re
import subprocess
import argparse

# Define the function to process the selected text
def open_bbedit_with_sftp(selected_text):
    # Use a regex to extract the IP and file path
    match = re.search(r'\[.*\(([\w\d\s\.]+)\)\s.*\]\s+(.*)', selected_text)

    if match:
        raw_captured = match.group(1)  # Captures 'QA2 10.150.2.19'

        # Apply a second regex to remove text parts that contain both letters and digits
        ip_address = re.sub(r'\b\w*[a-zA-Z]+\w*\b', '', raw_captured).strip()
        file_path = match.group(2)

        # Construct the BBEdit SFTP command
        sftp_url = f"sftp://{ip_address}/{file_path}"
        # bbedit_command = ["/usr/local/bin/bbedit", sftp_url]

        #####

        # Create a temporary SSH command with -o options to disable key checking
        ssh_command = f"ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {ip_address}"

        # Use subprocess to invoke bbedit with the SFTP URL
        bbedit_command = ["/usr/local/bin/bbedit", sftp_url]



        subprocess.run(bbedit_command)

        print(" ")

    else:
        print("Invalid selection. Could not parse IP and file path.")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Open a file in BBEdit via SFTP.")
    parser.add_argument('selected_text', nargs='?', default=None, help='The selected text to extract the IP and file path from')

    # Parse arguments
    args = parser.parse_args()
    # print(args)

    # Use the provided selected text if passed, otherwise fall back to hardcoded example
    if args.selected_text:
        selected_text = args.selected_text
    # else:
    #     # Fallback to hardcoded text if no argument is provided
    #     selected_text = "[root@lrs (QA2 10.150.2.19) ~]  cat versions_to_install_lrs_on_debian10.txt"

    # Clean up the selected text (remove 'cd', 'cat', and extra spaces)
        final = selected_text.replace('cd', '').replace('cat', '').strip()


        # Call the function with the processed text
        open_bbedit_with_sftp(final)
