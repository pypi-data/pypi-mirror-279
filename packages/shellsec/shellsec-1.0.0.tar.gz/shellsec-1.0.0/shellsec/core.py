# shellsec/core.py

import base64
import sys
import re

# Copyright (c) 2024 Your Name
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

def encrypt_bash_script(input_file, output_file):
    with open(input_file, 'r') as file:
        script_content = file.read()

    encoded_content = base64.b64encode(script_content.encode('utf-8')).decode('utf-8')

    obfuscated_script = f"""#!/bin/bash
source <(echo '{encoded_content}' | base64 --decode)
"""

    with open(output_file, 'w') as file:
        file.write(obfuscated_script)

def decrypt_bash_script(input_file, output_file):
    with open(input_file, 'r') as file:
        obfuscated_content = file.read()

    match = re.search(r"echo '([^']+)' \| base64 --decode", obfuscated_content)

    if not match:
        print("Error: The input script does not match the expected obfuscation format.")
        sys.exit(1)

    encoded_content = match.group(1)

    try:
        decoded_content = base64.b64decode(encoded_content).decode('utf-8')
    except (base64.binascii.Error, UnicodeDecodeError):
        print("Error: Failed to decode the Base64 content.")
        sys.exit(1)

    with open(output_file, 'w') as file:
        file.write(decoded_content)

def encrypt_script(input_script, output_script):
    try:
        encrypt_bash_script(input_script, output_script)
        return True  # Encryption successful
    except Exception as e:
        print(f"Error: {e}")
        return False  # Encryption failed

def decrypt_script(input_script, output_script):
    try:
        decrypt_bash_script(input_script, output_script)
        return True  # Decryption successful
    except Exception as e:
        print(f"Error: {e}")
        return False  # Decryption failed

def main():
    if len(sys.argv) < 4:
        print("Usage: python core.py [--encrypt|--decrypt] input_script output_script")
        sys.exit(1)

    action = sys.argv[1]
    input_script = sys.argv[2]
    output_script = sys.argv[3]

    if action == '--encrypt':
        if encrypt_script(input_script, output_script):
            print("Installed")
        else:
            print("Not installed")
    elif action == '--decrypt':
        if decrypt_script(input_script, output_script):
            print("Installed")
        else:
            print("Not installed")
    else:
        print("Invalid action. Use --encrypt or --decrypt.")
        sys.exit(1)

if __name__ == "__main__":
    main()
