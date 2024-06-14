# shellsec/core.py

import base64
import sys
import re
import argparse

def encrypt_bash_script(input_file, output_file):
    # Read the Bash script
    with open(input_file, 'r') as file:
        script_content = file.read()

    # Encode the script content in Base64
    encoded_content = base64.b64encode(script_content.encode('utf-8')).decode('utf-8')

    # Create the obfuscated script
    obfuscated_script = f"""#!/bin/bash
source <(echo '{encoded_content}' | base64 --decode)
"""

    # Write the obfuscated script to the output file
    with open(output_file, 'w') as file:
        file.write(obfuscated_script)

def decrypt_bash_script(input_file, output_file):
    # Read the obfuscated Bash script
    with open(input_file, 'r') as file:
        obfuscated_content = file.read()

    # Extract the Base64 encoded part using regex
    match = re.search(r"echo '([^']+)' \| base64 --decode", obfuscated_content)

    if not match:
        print("Error: The input script does not match the expected obfuscation format.")
        sys.exit(1)

    encoded_content = match.group(1)

    # Decode the script content from Base64
    try:
        decoded_content = base64.b64decode(encoded_content).decode('utf-8')
    except (base64.binascii.Error, UnicodeDecodeError):
        print("Error: Failed to decode the Base64 content.")
        sys.exit(1)

    # Write the decoded script to the output file
    with open(output_file, 'w') as file:
        file.write(decoded_content)

def encrypt_script(input_script, output_script):
    encrypt_bash_script(input_script, output_script)

def decrypt_script(input_script, output_script):
    decrypt_bash_script(input_script, output_script)

def main():
    parser = argparse.ArgumentParser(description='Encrypt or decrypt Bash scripts.')
    parser.add_argument('--encrypt', help='Encrypt the Bash script', action='store_true')
    parser.add_argument('--decrypt', help='Decrypt the Bash script', action='store_true')
    parser.add_argument('input_script', help='Input script file')
    parser.add_argument('output_script', help='Output script file')

    args = parser.parse_args()

    if args.encrypt and args.decrypt:
        print("Error: Choose either --encrypt or --decrypt, not both.")
        sys.exit(1)
    elif args.encrypt:
        encrypt_bash_script(args.input_script, args.output_script)
        print(f"Encrypted script written to {args.output_script}")
    elif args.decrypt:
        decrypt_bash_script(args.input_script, args.output_script)
        print(f"Decrypted script written to {args.output_script}")
    else:
        print("Error: You must specify either --encrypt or --decrypt.")
        sys.exit(1)

if __name__ == "__main__":
    main()
