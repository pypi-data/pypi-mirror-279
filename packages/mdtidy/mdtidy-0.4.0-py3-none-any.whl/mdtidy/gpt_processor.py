import re
import os
import logging
import sys
import requests
from bs4 import BeautifulSoup
import json
from typing import List, Tuple, Optional, Dict
from configparser import ConfigParser
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Configure logging
logging.basicConfig(filename='process_gpt_conversation.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

CONFIG_FILE = 'config.ini'
SCOPES = ['https://www.googleapis.com/auth/drive']

def fetch_conversation_data(url: str) -> List[Tuple[str, str]]:
    """Fetch and parse conversation data from the given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        logging.info("Successfully fetched data from URL.")
    except requests.RequestException as e:
        logging.error(f"Error fetching data from URL: {e}")
        sys.exit(1)

    soup = BeautifulSoup(response.content, 'html.parser')
    script_tag = soup.find('script', id='__NEXT_DATA__')
    if not script_tag:
        logging.error("No conversation data found at the URL.")
        sys.exit(1)

    data_json = script_tag.string
    data = json.loads(data_json)
    return parse_conversation_data(data)

def parse_conversation_data(data: dict) -> List[Tuple[str, str]]:
    """Parse the conversation data JSON into a list of tuples."""
    conversation = []

    for message_id, message_data in data['props']['pageProps']['serverResponse']['data']['mapping'].items():
        if 'message' not in message_data:
            continue
        message = message_data['message']
        author_role = message['author']['role']
        if author_role.lower() == 'system':
            continue
        content_type = message['content'].get('content_type', 'text')
        content = extract_content(message, content_type, author_role)
        if content:
            conversation.append((author_role, content))

    logging.info("Successfully parsed conversation data.")
    return conversation[::-1]

def extract_content(message: dict, content_type: str, author_role: str) -> Optional[str]:
    """Extract content based on the author role and content type."""
    if author_role.lower() == 'user':
        return " ".join(part if isinstance(part, str) else part.get('text', '') for part in message['content']['parts'])
    elif author_role.lower() == 'assistant':
        if content_type == 'text':
            return " ".join(part if isinstance(part, str) else part.get('text', '') for part in message['content']['parts'])
        elif content_type == 'code':
            return f"```python\n{message['content'].get('text', '')}\n```"
        elif content_type == 'image':
            return "[Image content not displayable]"
    return None

def create_gpt_colab_notebook(conversations: List[Tuple[str, str]], output_filename: str, documents: List[str], folder_path: str) -> None:
    """Create a Google Colab notebook from the conversation data."""
    cells = generate_notebook_cells(conversations, documents)
    notebook_content = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.8.5", "mimetype": "text/x-python", "codemirror_mode": {"name": "ipython", "version": 3}, "pygments_lexer": "ipython3", "nbconvert_exporter": "python", "file_extension": ".py"}
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    output_filepath = os.path.join(folder_path, output_filename)
    write_notebook_to_file(output_filepath, notebook_content)

def generate_notebook_cells(conversations: List[Tuple[str, str]], documents: List[str]) -> List[dict]:
    """Generate the cells for the Google Colab notebook."""
    cells = []
    num_queries = sum(1 for role, _ in conversations if role == 'user')
    title = "MULTI-TURN" if num_queries > 1 else "SINGLE-TURN"
    cells.append({"cell_type": "markdown", "metadata": {}, "source": [f"{title}\n"]})
    turn_number = 0
    for role, content in conversations:
        if role == 'user':
            turn_number += 1
            query_header = f"Turn {turn_number}\n\nQuery {turn_number}:\n{content}\n\n"
            for idx, link in enumerate(documents, start=1):
                query_header += f"Data {idx}: {link}\n" if len(documents) > 1 else f"Data: {link}\n"
            cells.append({"cell_type": "markdown", "metadata": {}, "source": [query_header]})
        elif role == 'assistant':
            if content.startswith('```python'):
                cells.append({"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": [content.replace('```python\n', '').replace('\n```', '')]})
            else:
                cells.append({"cell_type": "markdown", "metadata": {}, "source": [content + "\n"]})
    return cells

def write_notebook_to_file(filename: str, content: dict) -> None:
    """Write the notebook content to a file."""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(content, file, ensure_ascii=False, indent=2)
        logging.info(f"Notebook '{filename}' has been created successfully.")
    except IOError as e:
        logging.error(f"Error writing notebook file: {e}")
        sys.exit(1)

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

def is_valid_conversation_url(url: str) -> bool:
    """Check if the conversation URL is valid."""
    regex = re.compile(r'^https://chatgpt\.com/share/[0-9a-fA-F-]{36}$')
    return re.match(regex, url) is not None

def is_valid_document_url(url: str) -> bool:
    """Check if the document URL is a valid Google Drive link."""
    google_drive_pattern = re.compile(
        r'^https://drive\.google\.com/file/d/[\w-]+/view\?usp=sharing$'
    )
    return bool(google_drive_pattern.match(url))

def get_input(prompt: str) -> str:
    """Get user input with a prompt."""
    user_input = input(prompt).strip()
    if user_input.lower() == 'exit':
        logging.info("Process exited by user.")
        raise SystemExit(0)
    return user_input

def process_gpt_conversation() -> None:
    """Main process for handling GPT conversation."""
    try:
        conversation_url = get_valid_input("Enter the conversation URL (or type 'exit' to quit): ", is_valid_conversation_url, "Invalid URL. Please enter a valid URL in the format 'https://chatgpt.com/share/{UUID}'.")
        raters_id = get_raters_id()
        row_id = get_valid_input("Enter the row ID (numbers only or type 'exit' to quit): ", str.isdigit, "Invalid row ID. Please enter numbers only.")
        num_documents = get_valid_input("Enter the number of documents used (or type 'exit' to quit): ", lambda x: x.isdigit() and int(x) > 0, "Number of documents must be a positive integer.")
        num_documents = int(num_documents)
        documents = [get_valid_input(f"Enter link for Document {i+1} (must be a valid Google Drive link or type 'exit' to quit): ", is_valid_document_url, "Invalid document link. Please enter a valid Google Drive URL starting with 'https://drive.google.com/file/d/....'") for i in range(num_documents)]

        folder_path = f"ID_{row_id}"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        output_file = f"GPT_rater_{raters_id}_ID_{row_id}.ipynb"
        logging.info("Fetching conversation data...")
        conversation_data = fetch_conversation_data(conversation_url)

        logging.info("Creating Google Colab notebook...")
        create_gpt_colab_notebook(conversation_data, output_file, documents, folder_path)

        logging.info("Extracting user queries and document links...")
        extract_user_queries(conversation_data, row_id, documents)

        upload_to_drive_prompt = get_input("Do you want to upload the folder to Google Drive now? (yes/no or type 'exit' to quit): ").strip().lower()
        if upload_to_drive_prompt == 'yes':
            drive_credentials_path = get_drive_credentials_path()
            upload_folder_to_drive(folder_path, raters_id, drive_credentials_path)

    except SystemExit:
        print("You have exited the process. You can start again later if you wish.")

def get_valid_input(prompt: str, validation_fn: callable, error_message: str) -> str:
    """Get valid input from the user with validation."""
    while True:
        user_input = get_input(prompt)
        if validation_fn(user_input):
            return user_input
        else:
            logging.error(error_message)

def get_raters_id() -> str:
    """Get the rater's ID, either from the config file or user input."""
    raters_id = get_persisted_value('RatersID')
    if raters_id:
        use_stored_id = get_valid_input(f"Continue with stored rater's ID '{raters_id}'? (yes/no or type 'exit' to quit): ", lambda x: x.lower() in {'yes', 'no'}, "Please enter 'yes' or 'no'.")
        if use_stored_id.lower() == 'no':
            raters_id = get_valid_input("Enter the new rater's ID (numbers only or type 'exit' to quit): ", str.isdigit, "Invalid rater's ID. Please enter numbers only.")
            save_persisted_value('RatersID', raters_id)
    else:
        raters_id = get_valid_input("Enter the rater's ID (numbers only or type 'exit' to quit): ", str.isdigit, "Invalid rater's ID. Please enter numbers only.")
        save_persisted_value('RatersID', raters_id)
    return raters_id

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

        # Upload the entire folder to Google Drive under the rater's folder
        folder_id = create_drive_folder(drive_service, os.path.basename(folder_path), parents=[raters_folder_id])
        for root, _, files in os.walk(folder_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                logging.info(f"Uploading file '{file_path}' to Google Drive under '{raters_folder_name}' folder...")
                file_id = upload_file_to_drive(drive_service, folder_id, file_path)
                logging.info(f"Uploaded file ID: {file_id}")

    except Exception as e:
        logging.error(f"An error occurred while uploading the folder to Google Drive: {e}")

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

def create_drive_folder(drive_service, folder_name: str, parents: Optional[List[str]] = None) -> str:
    """Create a new folder on Google Drive and return its ID."""
    try:
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': parents or []
        }
        folder = drive_service.files().create(body=file_metadata, fields='id').execute()
        logging.info(f"Folder '{folder_name}' created on Google Drive.")
        return folder.get('id')
    except Exception as e:
        logging.error(f"An error occurred while creating the folder on Google Drive: {e}")
        raise

def upload_file_to_drive(drive_service, folder_id: str, file_path: str) -> str:
    """Upload a file to a specified folder on Google Drive."""
    try:
        file_metadata = {
            'name': os.path.basename(file_path),
            'parents': [folder_id]
        }
        media = MediaFileUpload(file_path, mimetype='application/json', resumable=True)
        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        logging.info(f"File '{file_path}' uploaded to Google Drive.")
        return file.get('id')
    except Exception as e:
        logging.error(f"An error occurred while uploading the file to Google Drive: {e}")
        return ""

def extract_user_queries(conversation_data: List[Tuple[str, str]], row_id: str, documents: List[str]) -> None:
    """Extract user queries and document links from the conversation data and save them to a JSON file."""
    queries = [content for role, content in conversation_data if role == 'user']
    queries_dict = {row_id: {'queries': queries, 'documents': documents}}
    json_filename = f"user_queries_{row_id}.json"
    json_folder_path = os.path.join("comp_ana_json", json_filename)
    
    try:
        if not os.path.exists("comp_ana_json"):
            os.makedirs("comp_ana_json")
        
        with open(json_folder_path, 'w', encoding='utf-8') as json_file:
            json.dump(queries_dict, json_file, ensure_ascii=False, indent=2)
        logging.info(f"User queries and document links extracted and saved to '{json_folder_path}'")
    except IOError as e:
        logging.error(f"Error writing JSON file: {e}")