import requests
import os
import argparse
import glob
import logging

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
            logging.error(f"An error occurred: {e}")
            return None

def send_files(bot_token, chat_id, directory_path=None, file=None, filetype=None):
    if directory_path is None:
        directory_path = os.getcwd()
    
    current_script = os.path.abspath(__file__)
    all_successful = True

    def should_exclude(file_path):
        return file_path == current_script or os.path.basename(file_path) == os.path.basename(current_script)

    if file:
        file_path = os.path.join(directory_path, file)
        if os.path.isfile(file_path) and not should_exclude(file_path):
            response = send_file(bot_token, chat_id, file_path)
            if response:
                logging.info("File sent successfully.")
            else:
                logging.error(f"Failed to send the file: {file_path}")
                all_successful = False
        else:
            logging.error(f"Error: File '{file}' does not exist or is the current script.")
            all_successful = False
    elif filetype:
        file_pattern = os.path.join(directory_path, filetype)
        files_matched = glob.glob(file_pattern)
        if not files_matched:
            logging.error(f"No files matching the pattern '{filetype}' found in '{directory_path}'.")
            all_successful = False
        for file_path in files_matched:
            if not should_exclude(file_path):
                response = send_file(bot_token, chat_id, file_path)
                if response:
                    logging.info("File sent successfully.")
                else:
                    logging.error(f"Failed to send the file: {file_path}")
                    all_successful = False
    else:
        for root, dirs, files in os.walk(directory_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                if not should_exclude(file_path):
                    response = send_file(bot_token, chat_id, file_path)
                    if response:
                        logging.info("File sent successfully.")
                    else:
                        logging.error(f"Failed to send the file: {file_path}")
                        all_successful = False

    return all_successful

def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    parser = argparse.ArgumentParser(description="Send files to a Telegram group.")
    parser.add_argument('--path', type=str, help="Path to the directory containing the files.")
    parser.add_argument('--file', type=str, help="Name of the file to send.")
    parser.add_argument('--filetype', type=str, help="File type pattern to send (e.g., '*.pdf' '*.png' '*.jpg').")
    parser.add_argument('--token', required=True, type=str, help="Telegram bot token.")
    parser.add_argument('--chat', required=True, type=str, help="Telegram chat ID or username.")
    args = parser.parse_args()

    success = send_files(args.token, args.chat, args.path, args.file, args.filetype)
    if success:
        logging.info("All files sent successfully.")
    else:
        logging.error("Failed to send some or all files.")

if __name__ == "__main__":
    main()
