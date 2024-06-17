import re
import json
import logging
import sys
import os
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from configparser import ConfigParser
from typing import Optional, List, Tuple

# Configure logging
logging.basicConfig(filename='process_gemini_conversation.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

CONFIG_FILE = 'config.ini'
SCOPES = ['https://www.googleapis.com/auth/drive']

def process_contents_to_ipynb(input_strings, queries, output_filename, documents):
    cells = []
    title = "MULTI-TURN" if len(input_strings) > 1 else "SINGLE-TURN"
    cells.append({"cell_type": "markdown", "metadata": {}, "source": [title + '\n']})

    for idx, (input_string, query) in enumerate(zip(input_strings, queries)):
        turn_number = idx + 1
        turn_markdown = f"Turn {turn_number}\n\nQuery {turn_number}: {query}\n\n"
        query_data_markdown = ""
        for i, link in enumerate(documents):
            query_data_markdown += f"Data {i+1}: {link}\n" if len(documents) > 1 else f"Data: {link}\n"

        cells.append({"cell_type": "markdown", "metadata": {}, "source": [turn_markdown + query_data_markdown]})

        cleaned_content = re.sub(r'```text\?code_stdout.*?\n.*?\n```', '', input_string, flags=re.DOTALL)
        cleaned_content = re.sub(r'```text\?code_stderr.*?\n.*?\n```', '', cleaned_content, flags=re.DOTALL)
        code_blocks = re.findall(r'```python\?code.*?\n(.*?)\n```', cleaned_content, flags=re.DOTALL)
        cleaned_content = re.sub(r'```python\?code.*?\n', 'CODE_BLOCK_START\n', cleaned_content)
        cleaned_content = re.sub(r'\n```', '\nCODE_BLOCK_END', cleaned_content)
        split_content = cleaned_content.split('\n')
        code_block_index = 0
        inside_code_block = False
        markdown_content = ""
        for line in split_content:
            if line == "CODE_BLOCK_START":
                if markdown_content.strip():
                    cells.append({
                        "cell_type": "markdown",
                        "metadata": {},
                        "source": [line + '\n' for line in markdown_content.strip().split('\n')]
                    })
                    markdown_content = ""
                inside_code_block = True
                code_content = ""
            elif line == "CODE_BLOCK_END":
                inside_code_block = False
                if code_block_index < len(code_blocks):
                    code_content = code_blocks[code_block_index]
                    cells.append({
                        "cell_type": "code",
                        "execution_count": None,
                        "metadata": {},
                        "outputs": [],
                        "source": [line + '\n' for line in code_content.strip().split('\n')]
                    })
                    code_block_index += 1
            else:
                if inside_code_block:
                    code_content += line + "\n"
                else:
                    markdown_content += line + "\n"

        if markdown_content.strip():
            cells.append({
                "cell_type": "markdown",
                "metadata": {},
                "source": [line + '\n' for line in markdown_content.strip().split('\n')]
            })

    notebook_content = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.8.5",
                "mimetype": "text/x-python",
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "pygments_lexer": "ipython3",
                "nbconvert_exporter": "python",
                "file_extension": ".py"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

    try:
        with open(output_filename, 'w', encoding='utf-8') as file:
            json.dump(notebook_content, file, ensure_ascii=False, indent=2)
        logging.info(f"Notebook '{output_filename}' has been created successfully.")
    except IOError as e:
        logging.error(f"Error writing notebook file: {e}")
        sys.exit(1)

def count_code_errors(input_strings):
    error_types = [
        'AttributeError', 'ValueError', 'ModuleNotFoundError',
        'FileNotFoundError', 'KeyError', 'TypeError',
        'NameError', 'SyntaxError', 'CouldNotFindError'
    ]

    total_error_counts = {error: 0 for error in error_types}
    turn_error_counts = []

    for idx, input_string in enumerate(input_strings):
        error_counts = {error: 0 for error in error_types}
        tracebacks = re.findall(r'Traceback \(most recent call last\):.*?(?=\n\n|\Z)', input_string, re.DOTALL)

        for traceback in tracebacks:
            for error in error_types:
                if f"{error}:" in traceback:
                    error_counts[error] += 1
                    total_error_counts[error] += 1

        turn_error_counts.append((f"Turn {idx + 1}", error_counts))

    error_title = "Error Counts Across {} Turn{}".format(len(input_strings), "s" if len(input_strings) > 1 else "")
    error_table = pd.DataFrame(
        {error: [turn_error_counts[i][1][error] for i in range(len(input_strings))] for error in error_types},
        index=[f"Turn {i+1}" for i in range(len(input_strings))]
    ).T
    error_table_md = error_table.to_markdown(index=True, numalign="left", stralign="left")

    print(f"\n{error_title}")
    print("-" * len(error_title))
    print(error_table_md)

    if all(count == 0 for count in total_error_counts.values()):
        summary = "\nNo errors found across all turns.\n"
    else:
        summary = "\nSummary of Total Error Counts\n" + "-" * 30 + "\n"
        summary += "\n".join([f"- {error}: {count}" for error, count in total_error_counts.items() if count > 0])

    print(summary)

    return total_error_counts

def get_persisted_raters_id():
    return get_persisted_value('RatersID')

def save_raters_id(raters_id):
    save_persisted_value('RatersID', raters_id)

def get_input(prompt):
    user_input = input(prompt).strip()
    if user_input.lower() == 'exit':
        logging.info("Process exited by user.")
        raise SystemExit(0)
    return user_input

def get_drive_credentials_path() -> str:
    """Get the Google Drive credentials path, either from the config file or user input."""
    credentials_path = get_persisted_value('DriveCredentialsPath')
    if not credentials_path:
        credentials_path = get_valid_input("Enter the path to your Google Drive API credentials file (or type 'exit' to quit): ", os.path.exists, "Invalid path. Please enter a valid file path.")
        save_persisted_value('DriveCredentialsPath', credentials_path)
    return credentials_path

def upload_folder_to_drive(folder_path: str, raters_id: str, credentials_path: str) -> None:
    """Upload the specified folder to Google Drive."""
    try:
        credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
        drive_service = build('drive', 'v3', credentials=credentials)
        logging.info("Successfully authenticated with Google Drive.")

        # Check if the rater's folder exists on Google Drive
        raters_folder_name = f"rater_{raters_id}"
        raters_folder_id = get_drive_folder_id(drive_service, raters_folder_name)

        if not raters_folder_id:
            raters_folder_id = create_drive_folder(drive_service, raters_folder_name)

        # Log the rater's folder ID
        logging.info(f"Rater's folder ID for '{raters_folder_name}': {raters_folder_id}")

        # Create the subfolder (ID_{row_id}) in the rater's folder
        folder_name = os.path.basename(folder_path)
        logging.info(f"Uploading folder '{folder_name}' to Google Drive under folder ID '{raters_folder_id}'...")

        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [raters_folder_id]
        }
        folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
        folder_id = folder.get('id')
        logging.info(f"Created folder '{folder_name}' on Google Drive with ID: {folder_id}")

        for root, _, files in os.walk(folder_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                logging.info(f"Uploading file '{file_path}' to Google Drive...")
                file_metadata = {
                    'name': file_name,
                    'parents': [folder_id]
                }
                media = MediaFileUpload(file_path, mimetype='application/octet-stream', resumable=True)
                drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
                logging.info(f"Uploaded file '{file_name}' to Google Drive.")

        logging.info(f"Uploaded folder '{folder_name}' to Google Drive successfully!")

    except Exception as e:
        logging.error(f"An error occurred while uploading the folder to Google Drive: {e}")

def create_drive_folder(drive_service, folder_name: str, parent_id: Optional[str] = None) -> str:
    """Create a new folder on Google Drive and return its ID."""
    try:
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        if parent_id:
            folder_metadata['parents'] = [parent_id]

        folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
        logging.info(f"Folder '{folder_name}' created on Google Drive with ID: {folder.get('id')}")
        return folder.get('id')
    except Exception as e:
        logging.error(f"An error occurred while creating the folder on Google Drive: {e}")
        raise

def get_drive_folder_id(drive_service, folder_name: str) -> Optional[str]:
    """Get the Google Drive folder ID if it exists, otherwise return None."""
    try:
        query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
        results = drive_service.files().list(q=query, fields="files(id, name)").execute()
        items = results.get('files', [])
        if items:
            logging.info(f"Found existing folder '{folder_name}' on Google Drive.")
            return items[0]['id']
        else:
            logging.info(f"Folder '{folder_name}' does not exist on Google Drive.")
            return None
    except Exception as e:
        logging.error(f"An error occurred while checking for the folder on Google Drive: {e}")
        return None

def extract_queries_from_json(json_file: str, num_turns: int) -> Tuple[List[str], bool]:
    """Extract queries from a JSON file and check if the number of queries matches the number of turns."""
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            row_id = list(data.keys())[0]
            queries = data[row_id]['queries']
            matches = len(queries) == num_turns
            if not matches:
                logging.error(f"Number of queries in JSON ({len(queries)}) does not match the number of turns ({num_turns}).")
            return queries, matches
    except IOError as e:
        logging.error(f"Error reading JSON file: {e}")
        sys.exit(1)
    except (json.JSONDecodeError, KeyError) as e:
        logging.error(f"Error parsing JSON file: {e}")
        sys.exit(1)

def update_json_with_input_strings(json_file: str, row_id: str, input_strings: List[str]) -> None:
    """Update the JSON file with input strings."""
    try:
        if os.path.exists(json_file):
            with open(json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
        else:
            data = {}

        if row_id in data:
            data[row_id]['input_strings'] = input_strings
        else:
            data[row_id] = {"queries": [], "input_strings": input_strings}

        with open(json_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        logging.info(f"JSON file '{json_file}' updated successfully.")
    except IOError as e:
        logging.error(f"Error updating JSON file: {e}")
        sys.exit(1)
    except (json.JSONDecodeError, KeyError) as e:
        logging.error(f"Error parsing JSON file: {e}")
        sys.exit(1)

def check_and_update_json_files(input_strings: List[str], row_id: str) -> None:
    """Check JSON files in the comp_ana_json folder and update them if the number of queries matches the number of turns."""
    comp_ana_json_folder = 'comp_ana_json'
    json_file_path = os.path.join(comp_ana_json_folder, f"user_queries_{row_id}.json")
    
    if not os.path.exists(json_file_path):
        logging.error(f"JSON file for row ID {row_id} does not exist in {comp_ana_json_folder}.")
        return

    _, matches = extract_queries_from_json(json_file_path, len(input_strings))
    if matches:
        update_json_with_input_strings(json_file_path, row_id, input_strings)
    else:
        logging.error(f"Number of queries does not match the number of turns for row ID {row_id}. No update performed.")

def process_gemini_conversation(input_strings):
    try:
        raters_id = get_persisted_raters_id()
        if raters_id:
            while True:
                use_stored_id = get_input(f"Continue with stored rater's ID '{raters_id}'? (yes/no or type 'exit' to quit): ").strip().lower()
                if use_stored_id in {'yes', 'no'}:
                    break
                else:
                    logging.error("Please enter 'yes' or 'no'.")
            if use_stored_id == 'no':
                raters_id = None

        while not raters_id:
            rater_id = get_input("Enter the rater's ID (numbers only or type 'exit' to quit): ")
            if rater_id.isdigit():
                save_raters_id(rater_id)
                raters_id = rater_id
            else:
                logging.error("Invalid rater's ID. Please enter numbers only.")

        while True:
            row_id = get_input("Enter the row ID (numbers only or type 'exit' to quit): ")
            if row_id.isdigit():
                break
            else:
                logging.error("Invalid row ID. Please enter numbers only.")

        num_turns = len(input_strings)
        logging.info(f"Number of conversation turns is {num_turns} based on input strings.")

        while True:
            try:
                num_documents = int(get_input("Enter the number of documents used (or type 'exit' to quit): "))
                if num_documents > 0:
                    break
                else:
                    logging.error("Number of documents must be a positive integer.")
            except ValueError:
                logging.error("Invalid input. Please enter a positive integer.")

        documents = []
        for i in range(num_documents):
            while True:
                document_link = get_input(f"Enter link for Document {i+1} (must be a valid Google Drive link or type 'exit' to quit): ")
                if re.match(r'^https://drive\.google\.com/file/d/[\w-]+/view\?usp=sharing$', document_link):
                    documents.append(document_link)
                    break
                else:
                    logging.error("Invalid document link. Please enter a valid Google Drive URL in the format 'https://drive.google.com/file/d/{file_id}/view?usp=sharing'.")

        # Check and update JSON files in comp_ana_json folder
        check_and_update_json_files(input_strings, row_id)

        json_file_path = os.path.join('comp_ana_json', f"user_queries_{row_id}.json")
        queries, matches = extract_queries_from_json(json_file_path, num_turns)

        if not matches:
            logging.error("Number of queries does not match the number of turns. Exiting.")
            sys.exit(1)

        folder_path = f"ID_{row_id}"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        output_file = os.path.join(folder_path, f"Gemini_rater_{raters_id}_ID_{row_id}.ipynb")
        process_contents_to_ipynb(input_strings, queries, output_file, documents)

        logging.info("\n")
        count_code_errors(input_strings)

        while True:
            upload_to_drive_prompt = get_input("Do you want to upload the folder to Google Drive now? (yes/no or type 'exit' to quit): ").strip().lower()
            if upload_to_drive_prompt in {'yes', 'no'}:
                break
            else:
                logging.error("Please enter 'yes' or 'no'.")

        if upload_to_drive_prompt == 'yes':
            drive_credentials_path = get_drive_credentials_path()
            upload_folder_to_drive(folder_path, raters_id, drive_credentials_path)

    except SystemExit:
        print("You have exited the process. You can start again later if you wish.")

def get_persisted_value(key: str) -> Optional[str]:
    """Retrieve a value from the config file."""
    if not os.path.exists(CONFIG_FILE):
        return None
    config = ConfigParser()
    config.read(CONFIG_FILE)
    return config.get('DEFAULT', key, fallback=None)

def save_persisted_value(key: str, value: str) -> None:
    """Save a value to the config file."""
    config = ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
    config['DEFAULT'][key] = value
    try:
        with open(CONFIG_FILE, 'w') as configfile:
            config.write(configfile)
        logging.info(f"{key} saved to config file.")
    except IOError as e:
        logging.error(f"Error saving {key}: {e}")

def get_valid_input(prompt: str, validation_fn: callable, error_message: str) -> str:
    """Get valid input from the user with validation."""
    while True:
        user_input = get_input(prompt)
        if validation_fn(user_input):
            return user_input
        else:
            logging.error(error_message)