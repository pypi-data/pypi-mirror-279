import requests
import os
import argparse
import glob

def calculate_timeout(file_size):
    base_timeout = 10
    timeout_per_mb = 2
    file_size_mb = file_size / (1024 * 1024)
    return base_timeout + (timeout_per_mb * file_size_mb)

def send_file(bot_token, chat_id, file_path):
    url = f'https://api.telegram.org/bot{bot_token}/sendDocument'
    file_size = os.path.getsize(file_path)
    timeout = calculate_timeout(file_size)
    
    with open(file_path, 'rb') as file:
        files = {'document': file}
        data = {'chat_id': chat_id}
        try:
            response = requests.post(url, data=data, files=files, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

def send_files(bot_token, chat_id, directory_path, file=None, filetype=None):
    if file:
        if os.path.isfile(os.path.join(directory_path, file)):
            file_path = os.path.join(directory_path, file)
            print(f"Sending file: {file_path}")
            response = send_file(bot_token, chat_id, file_path)
            if response:
                print(response)
            else:
                print(f"Failed to send the file: {file_path}")
        else:
            print(f"Error: File '{file}' does not exist.")
    elif filetype:
        file_pattern = os.path.join(directory_path, filetype)
        for file_path in glob.glob(file_pattern):
            print(f"Sending file: {file_path}")
            response = send_file(bot_token, chat_id, file_path)
            if response:
                print(response)
            else:
                print(f"Failed to send the file: {file_path}")
    else:
        for root, dirs, files in os.walk(directory_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                print(f"Sending file: {file_path}")
                response = send_file(bot_token, chat_id, file_path)
                if response:
                    print(response)
                else:
                    print(f"Failed to send the file: {file_path}")

def main():
    parser = argparse.ArgumentParser(description="Send files to a Telegram group.")
    parser.add_argument('--path', type=str, help="Path to the directory containing the files.")
    parser.add_argument('--file', type=str, help="Name of the file to send.")
    parser.add_argument('--filetype', type=str, help="File type pattern to send (e.g., '*.pdf' '*.png' '*.jpg').")
    parser.add_argument('--token', required=True, type=str, help="Telegram bot token.")
    parser.add_argument('--chat', required=True, type=str, help="Telegram chat ID or username.")
    args = parser.parse_args()

    directory_path = args.path if args.path else os.getcwd()
    send_files(args.token, args.chat, directory_path, args.file, args.filetype)

if __name__ == "__main__":
    main()
