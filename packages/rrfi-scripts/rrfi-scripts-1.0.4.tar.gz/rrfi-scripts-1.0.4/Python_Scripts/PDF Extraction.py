import os
import pdfplumber
import io
import requests
import logging
import uuid
import re
from azure.storage.blob import BlobServiceClient
from openai import AzureOpenAI
import hashlib
 
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
 
def get_openai_client():
    try:
        client = AzureOpenAI(
            azure_endpoint="https://rrfimainoai.openai.azure.com/",
            api_key="9c7a9a0b6b584e2c8701ae2fbb0ff6c2",
            api_version="2024-02-15-preview"
        )
        return client
    except Exception as e:
        logger.error(f"Error creating OpenAI client: {e}")
        raise
 
def identify_data_in_text(extracted_text, prompt, sys_prompt):
    try:
        client = get_openai_client()
 
        messages = [
            {"role": "system", "content": extracted_text},
            {"role": "user", "content": prompt},
            {"role": "system", "content": sys_prompt}
        ]
 
        completion = client.chat.completions.create(
            model="gpt-35-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )
 
        response = completion.choices[0].message.content.strip()
        return response
    except Exception as e:
        logger.error(f"An error occurred while calling OpenAI API: {e}")
        return None
 
def identify_river_names_in_text(extracted_text):
    prompt = "From the data provided, identify all England river names. Return all values concatenated in a single string, comma separated."
    sys_prompt = "You help process data in a pipeline. \nOnly return the values without any other response text. If there are no values identified, return blank."
    return identify_data_in_text(extracted_text, prompt, sys_prompt)
 
def identify_location_of_incident_in_text(extracted_text):
    prompt = "From the data provided, identify all town names. Return all town names concatenated in a single string, comma separated."
    sys_prompt = "You help process data in a pipeline. \nOnly return the values without any other response text"
    return identify_data_in_text(extracted_text, prompt, sys_prompt)
 
def identify_catchment_names_in_text(extracted_text):
    prompt = "From the data provided, identify all catchment names. Return all catchment names concatenated in a single string, comma separated."
    sys_prompt = "You help process data in a pipeline. \nOnly return the values without any other response text"
    return identify_data_in_text(extracted_text, prompt, sys_prompt)
 
def identify_security_classification_in_text(extracted_text):
    prompt = "From the data you are given, identify if 'Official', 'Secret', 'Top Secret', 'Official Sensitive' is included within the data as text. If any of them are listed within the data, return the listed text."
    sys_prompt = "You help process data in a pipeline. \nOnly return the values without any other response text. \nOnly return the listed text that exist within the data and no other text"
    return identify_data_in_text(extracted_text, prompt, sys_prompt)
 
def extract_postcodes_from_text(extracted_text):
    #pattern = r'\b[A-Z]{1,2}\d{1,2} ?\d[A-Z]{2}\b'
    pattern = r'^([A-Za-z]{1,2}\d[A-Za-z\d]?)[\s]?(\d[A-Za-z]{2})$'
    postcodes = re.findall(pattern, extracted_text)
    if postcodes:
        return ', '.join(postcodes)
    return None
 
def get_area_name(blob_name, full_file_path):
    area_codes = ['NEA', 'CLA', 'YOR', 'GMC', 'EMD', 'LNA', 'WMD', 'EAN', 'HNL', 'THM', 'KSL', 'SSD', 'WSX', 'DCS']
    for code in area_codes:
        if code in blob_name or code in full_file_path:
            return code
    return None
 
def identify_date_from_file_path(file_path):
    try:
        client = get_openai_client()
 
        messages = [
            {"role": "system", "content": file_path},
            {"role": "user", "content": "You are a helpful agent. Your task is to identify and extract date, month, year as a substring from the given text. It is possible to have multiple date, month within the URL text. Highest priority for a full date. If there is no full date, look for a month and year value to return."},
            {"role": "system", "content": "You are an AI assistant that helps process data in a pipeline. Just return the values without any additional response text. Always return the identified date in dd/mm/yyyy format. Only return one value based on prioritization. Higher priority value gets preference."}
        ]
 
        completion = client.chat.completions.create(
            model="gpt-35-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=50,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )
 
        response = completion.choices[0].message.content.strip()
        return response
    except Exception as e:
        logger.error(f"An error occurred while calling OpenAI API for date identification: {e}")
        return "No date found"
 
def identify_location_from_file_path(file_path):
    try:
        client = get_openai_client()
 
        messages = [
            {"role": "system", "content": file_path},
            {"role": "user", "content": "You are a helpful agent. Your task is to identify and extract UK locations as a substring from the given text. It is possible to have multiple locations within the URL text."},
            {"role": "system", "content": "You are an AI assistant that helps process data in a pipeline. Just return the values without any additional response text. Always return the last location name."}
        ]
 
        completion = client.chat.completions.create(
            model="gpt-35-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=50,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )
 
        response = completion.choices[0].message.content.strip()
        return response
    except Exception as e:
        logger.error(f"An error occurred while calling OpenAI API for location identification: {e}")
        return "No location found"
 
def event(blob_name):
    event_folder = ''
    if 'storm' in blob_name.lower() or 'flood' in blob_name.lower():
        path_folders = blob_name.split("/")
        for event in path_folders:
            if 'storm' in event.lower() or 'flood' in event.lower():
                event_folder = event
                break
    return event_folder
 
def compute_hash(file_content):
    hash_object = hashlib.sha256()
    hash_object.update(file_content)
    return hash_object.hexdigest()
 
def process_pdf_files_from_blob_container(blob_service_client, container_name, directory_path=""):
    container_client = blob_service_client.get_container_client(container_name)
    blobs = container_client.list_blobs(name_starts_with=directory_path)
 
    for blob in blobs:
        # Check if the blob is a directory (folder)
        if blob.name.endswith('/'):
            process_pdf_files_from_blob_container(blob_service_client, container_name, directory_path=blob.name)
        elif blob.name.lower().endswith('.pdf'):
            process_pdf(blob_service_client, container_name, blob)
 
def process_pdf(blob_service_client, container_name, blob):
    try:
        # Download PDF file from Azure Blob storage
        container_client = blob_service_client.get_container_client(container_name)
        blob_data = container_client.download_blob(blob)
        pdf_bytes = blob_data.readall()
       
        #Compute hash value of the PDF file content
        hash_value = compute_hash(pdf_bytes)
       
        # Convert bytes to file-like object
        pdf_file_like = io.BytesIO(pdf_bytes)
 
        # Extract text from PDF
        extracted_text = ""
        with pdfplumber.open(pdf_file_like) as pdf:
            for page in pdf.pages:
                extracted_text += page.extract_text()
 
        # Call functions to identify various pieces of information
        identified_river_names = identify_river_names_in_text(extracted_text)
        identified_locations = identify_location_of_incident_in_text(extracted_text)
        identified_catchment = identify_catchment_names_in_text(extracted_text)
        identified_security = identify_security_classification_in_text(extracted_text)
        extracted_postcodes = extract_postcodes_from_text(extracted_text)
 
        # Get additional fields
        file_path = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{blob.name}"
        file_name = os.path.basename(blob.name)
        item_type = os.path.splitext(file_name)[1][1:]
        area_name = get_area_name(blob.name, file_path)
        incident_date_and_time = identify_date_from_file_path(file_path)
        location_from_path = identify_location_from_file_path(file_path)
        event_folder = event(blob.name)
 
        # Construct Incident_Name based on conditions
        if 'EA-IMToolbox' in file_path:
            if 'Current Incidents' in file_path:
                path_folders = file_path.split("/")
                current_incidents_index = path_folders.index("Current Incidents")
                incident_name = path_folders[current_incidents_index + 1]
            elif 'Past Incidents' in file_path:
                path_folders = file_path.split("/")
                past_incidents_index = path_folders.index("Past Incidents")
                incident_name = path_folders[past_incidents_index + 1]
            else:
                area_name = area_name or ''
                event_folder = event_folder or ''
                location_from_path = location_from_path or ''
                incident_date_and_time = incident_date_and_time or ''
                if area_name == '':
                    incident_name = f"{event_folder}_{location_from_path}_{incident_date_and_time}"
                elif event_folder == '':
                    incident_name = f"{area_name}_{location_from_path}_{incident_date_and_time}"
                elif location_from_path == '':
                    incident_name = f"{area_name}_{event_folder}_{incident_date_and_time}"
                elif incident_date_and_time == '':
                    incident_name = f"{area_name}_{event_folder}_{location_from_path}"
                else:
                    incident_name = f"{area_name}_{event_folder}_{location_from_path}_{incident_date_and_time}"
        else:
            area_name = area_name or ''
            event_folder = event_folder or ''
            location_from_path = location_from_path or ''
            incident_date_and_time = incident_date_and_time or ''
            if area_name == '':
                incident_name = f"{event_folder}_{location_from_path}_{incident_date_and_time}"
            elif event_folder == '':
                incident_name = f"{area_name}_{location_from_path}_{incident_date_and_time}"
            elif location_from_path == '':
                incident_name = f"{area_name}_{event_folder}_{incident_date_and_time}"
            elif incident_date_and_time == '':
                incident_name = f"{area_name}_{event_folder}_{location_from_path}"
            else:
                incident_name = f"{area_name}_{event_folder}_{location_from_path}_{incident_date_and_time}"
 
        # Send data to Azure Cognitive Search
        send_to_azure_cognitive_search(
            identified_river_names,
            extracted_postcodes,
            file_path,
            file_name,
            item_type,
            area_name,
            identified_locations,
            identified_catchment,
            identified_security,
            incident_date_and_time,
            incident_name,
            hash_value
        )
    except Exception as e:
        logger.error(f"Failed to process blob {blob.name}: {e}")
 
def send_to_azure_cognitive_search(identified_river_names, extracted_postcodes, file_path, file_name, item_type, area_name, identified_locations, identified_catchment, identified_security, incident_date_and_time, incident_name, hash_value):
        endpoint = "https://rrfimainsearch.search.windows.net"
        index_name = "rrfisearch"
        api_version = "2024-03-01-preview"
        api_key = "1LnrhfcdFVeuJ7jVOe2ElJi2uFib34RZhLWnig1nDiAzSeAIlOEO"
 
        headers = {
            "Content-Type": "application/json",
            "api-key": api_key
        }
 
        document_id = str(uuid.uuid4())
 
        documents = {
            "value": [
                {
                    "@search.action": "upload",
                    "id": document_id,
                    "River_Name": identified_river_names,
                    "Postcode": extracted_postcodes,
                    "File_Path": file_path,
                    "File_Name": file_name,
                    "Item_Type": item_type,
                    "Area_Name": area_name,
                    "Location_of_Incident": identified_locations,
                    "Catchment_Name": identified_catchment,
                    "Security_Classification": identified_security,
                    "Incident_Date_and_Time": incident_date_and_time,
                    "Incident_Name": incident_name,
                    "Hash_Value": hash_value
                }
            ]
        }
 
        url = f"{endpoint}/indexes/{index_name}/docs/index?api-version={api_version}"
        response = requests.post(url, json=documents, headers=headers)
 
        if response.status_code == 200:
            logger.info("Successfully sent to Azure Cognitive Search.")
        else:
            logger.error(f"Failed to send to Azure Cognitive Search. Status Code: {response.status_code}, Response: {response.json()}")
 
if __name__ == "__main__":
    azure_storage_connection_string = "DefaultEndpointsProtocol=https;AccountName=rrfimainstorage;AccountKey=9h2WMr2hvNI1V8xixizn49neFq6/Oba61Z4e6L9YAuuRqrSXEsyEB2NuDhO2NXZaBec5VvH4O8D2+ASt1tyDqA==;EndpointSuffix=core.windows.net"
    blob_service_client = BlobServiceClient.from_connection_string(azure_storage_connection_string)
    container_name = "rrfimaincon"
 
    process_pdf_files_from_blob_container(blob_service_client, container_name)