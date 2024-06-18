import os
import hashlib
import binascii
import uuid
from azure.storage.blob import BlobServiceClient
from io import BytesIO
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
import re
import docx
from openai import AzureOpenAI
import hashlib
 
# Azure Blob Storage connection string and container name
connection_string = "DefaultEndpointsProtocol=https;AccountName=rrfimainstorage;AccountKey=9h2WMr2hvNI1V8xixizn49neFq6/Oba61Z4e6L9YAuuRqrSXEsyEB2NuDhO2NXZaBec5VvH4O8D2+ASt1tyDqA==;EndpointSuffix=core.windows.net"
container_name = "rrfimaincon"
 
# Azure Cognitive Search configuration
search_service_name = "rrfimainsearch"
index_name = "rrfisearch"
api_key = "1LnrhfcdFVeuJ7jVOe2ElJi2uFib34RZhLWnig1nDiAzSeAIlOEO"
search_endpoint = 'https://rrfimainsearch.search.windows.net'
 
# Connect to Blob Storage
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)
 
# Connect to Azure Cognitive Search
search_client = SearchClient(endpoint=search_endpoint,
                             index_name=index_name,
                             credential=AzureKeyCredential(api_key))
 
# Area codes list
area_codes = ['NEA', 'CLA', 'YOR', 'GMC', 'EMD', 'LNA', 'WMD', 'EAN', 'HNL', 'THM', 'KSL', 'SSD', 'WSX', 'DCS']
 
# Function to extract postcodes using regular expression
def extract_postcodes(text):
    #postcode_regex = re.compile(r'\b[A-Za-z]{1,2}\d{1,2}[A-Za-z]?\s*\d[A-Za-z]{2}\b')
    postcode_regex = re.compile(r'^([A-Za-z]{1,2}\d[A-Za-z\d]?)[\s]?(\d[A-Za-z]{2})$')
    postcodes = set()
    for match in postcode_regex.finditer(text):
        postcodes.add(match.group())
    return ', '.join(postcodes)
 
# Helper function to get response from OpenAI
def get_openai_response(client, document_text, user_prompt, system_prompt):
    messages = [
        {"role": "system", "content": document_text},
        {"role": "user", "content": user_prompt},
        {"role": "system", "content": system_prompt}
    ]
    completion = client.chat.completions.create(
        model="gpt-35-turbo",  # model = "deployment_name"
        messages=messages,
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    return completion.choices[0].message.content.strip()
 
#Function to generate hash value of the file
def generate_file_hash(file_content):
    sha1 = hashlib.sha1()
    sha1.update(file_content)
    return sha1.hexdigest()
 
# Function to process a single Word document
def process_word_document(blob_client, area_name, full_file_path):
    try:
        # Download blob data
        blob_data = blob_client.download_blob()
        blob_content = blob_data.read()
 
        #Generate hash value for the file content
        file_hash = generate_file_hash(blob_content)
       
        # Initialize set to store unique postcodes found in the document
        unique_postcodes = set()
 
        # Handle Word files
        doc = docx.Document(BytesIO(blob_content))
        document_text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])  # Combine all paragraphs into a single text
 
        # Call OpenAI API to identify river names in the extracted text
        client = AzureOpenAI(
            azure_endpoint="https://rrfimainoai.openai.azure.com/",
            api_key="9c7a9a0b6b584e2c8701ae2fbb0ff6c2",
            api_version="2024-02-15-preview"
        )
 
        river_names_response = get_openai_response(
            client, document_text,
            "From the data provided, identify all England river names. \nReturn all values concatenated in a single string, comma separated. \nOnly return the values as your response",
            "You help process data in a pipeline. \nOnly return the values without any other response text"
        )
 
        # Call OpenAI API to identify location of incident in the extracted text
        location_response = get_openai_response(
            client, document_text,
            "From the data provided, identify all town names. \nOnly return the town names as your response",
            "You help process data in a pipeline. \nOnly return the values without any other response text"
        )
 
        # Call OpenAI API to identify security classification in the extracted text
        security_response = get_openai_response(
            client, document_text,
            "From the data you are given, identify if 'Official', 'Secret', 'Top Secret', 'Official Sensitive' is included within the data as text. If any of them are listed within the data, return the listed text.",
            "You help process data in a pipeline. \nOnly return the values without any other response text. \nOnly return the listed text that exist within the data and no other text"
        )
 
        # Call OpenAI API to identify catchment name in the extracted text
        catchment_response = get_openai_response(
            client, document_text,
            "From the given data identify all catchment names. \nReturn all catchment names concatenated in a single string comma separated. \nOnly return valid catchment names without any numerical values or special characters",
            "You help process data within a pipeline.\nOnly return the values without any other response text."
        )
 
        # Call OpenAI API to identify location in the extracted text for incident name
        incident_location_response = get_openai_response(
            client, blob_client.blob_name,
            "You are a helpful agent. Your task is to identify and extract UK locations as a substring from the given text. It is possible to have multiple locations within the URL text.",
            "You are an AI assistant that helps process data in a pipeline. Just return the values without any additional response text. Always return the last location name."
        )
 
        # Call OpenAI API to identify date in the extracted text for incident name
        incident_date_response = get_openai_response(
            client, blob_client.blob_name,
            "You are a helpful agent. Your task is to identify and extract date, month, year as a substring from the given text. It is possible to have multiple date, month within the URL text. Highest priority for a full date. If there is no full date, look for a month and year value to return.",
            "You are an AI assistant that helps process data in a pipeline. Just return the values without any additional response text. Always return the identified date in dd/mm/yyyy format. Only return one value based on prioritization. Higher priority value gets preference."
        )
 
        # Extract postcodes from the text
        postcodes = extract_postcodes(document_text)
        if postcodes:
            unique_postcodes.update(postcodes.split(', '))
 
        # Concatenate postcodes into a single string
        postcodes_str = ', '.join(unique_postcodes) if unique_postcodes else ''
 
        # Extracting event type for Incident Name:
        if 'storm' in blob_client.blob_name.lower() or 'flood' in blob_client.blob_name.lower():
            path_folders = blob_client.blob_name.split("/")
            for event in path_folders:
                if 'storm' in event.lower() or 'flood' in event.lower():
                    event_folder = event
                    break
        else:
            event_folder = ''
 
        # Logic to derive Incident_Name
        if 'EA-IMToolbox' in blob_client.blob_name:
            if 'Current Incidents' in blob_client.blob_name:
                path_folders = blob_client.blob_name.split("/")
                # Get the index of "Current Incidents" folder
                current_incidents_index = path_folders.index("Current Incidents")
                # The folder after "Current Incidents" is at index current_incidents_index + 1
                incident_name = path_folders[current_incidents_index + 1]
            elif 'Past Incidents' in blob_client.blob_name:
                path_folders = blob_client.blob_name.split("/")
                # Get the index of "Past Incidents" folder
                past_incidents_index = path_folders.index("Past Incidents")
                # The folder after "Past Incidents" is at index past_incidents_index + 1
                incident_name = path_folders[past_incidents_index + 1]
            else:
                area_name = area_name or ''
                event_folder = event_folder or ''
                incident_location_response = incident_location_response or ''
                incident_date_response = incident_date_response or ''
                if area_name == '':
                    incident_name = event_folder + '_' + incident_location_response + '_' + incident_date_response
                elif event_folder == '':
                    incident_name = area_name + '_' + incident_location_response + '_' + incident_date_response
                elif incident_location_response == '':
                    incident_name = area_name + '_' + event_folder + '_' + incident_date_response
                elif incident_date_response == '':
                    incident_name = area_name + '_' + event_folder + '_' + incident_location_response
                else:
                    incident_name = area_name + '_' + event_folder + '_' + incident_location_response + '_' + incident_date_response

        else:
            area_name = area_name or ''
            event_folder = event_folder or ''
            incident_location_response = incident_location_response or ''
            incident_date_response = incident_date_response or ''
            if area_name == '':
                incident_name = event_folder + '_' + incident_location_response + '_' + incident_date_response
            elif event_folder == '':
                incident_name = area_name + '_' + incident_location_response + '_' + incident_date_response
            elif incident_location_response == '':
                incident_name = area_name + '_' + event_folder + '_' + incident_date_response
            elif incident_date_response == '':
                incident_name = area_name + '_' + event_folder + '_' + incident_location_response
            else:
                incident_name = area_name + '_' + event_folder + '_' + incident_location_response + '_' + incident_date_response

        #Generating HASH value for identifying duplicate
        content_settings = blob_client.get_blob_properties().content_settings
        blobmd5 = bytearray(content_settings.content_md5)
        hex = binascii.hexlify(blobmd5).decode('utf-8')
        # Generate unique alphanumeric id
        unique_id = str(uuid.uuid4())
 
        # Create a document with area name, postcodes, incident name, river names, and location of incident
        document = {
            "Area_Name": area_name,
            "File_Name": os.path.basename(blob_client.blob_name),
            "File_Path": blob_client.blob_name,
            "Source_Path": blob_client.blob_name,
            "Item_Type": os.path.splitext(os.path.basename(blob_client.blob_name))[1] if '.' in blob_client.blob_name else '',
            "Postcode": postcodes_str,
            "Incident_Name": incident_name,
            "River_Name": river_names_response,
            "Location_of_Incident": location_response,
            "Security_Classification": security_response,
            "Catchment_Name": catchment_response,
            "Incident_Date_and_Time": incident_date_response,
            "Hash_Value": hex,
            "id": unique_id
        }
 
        # Upload document to Azure Cognitive Search
        search_client.upload_documents(documents=[document])
        print("Uploaded document to Azure Cognitive Search.")
    except Exception as e:
        print(f"An error occurred processing blob {blob_client.blob_name}: {str(e)}")
 
# Recursive function to iterate through blobs
def process_blobs(container_client, file_path=""):
    # Iterate over blobs in the current container
    for blob in container_client.list_blobs():
        # If blob is a directory, recursively process the directory
        if blob.name.endswith('/'):
            sub_folder_client = blob_service_client.get_container_client(container_name + '/' + blob.name)
            process_blobs(sub_folder_client, file_path=blob.name)
        else:
            area_name = ""
            for code in area_codes:
                if code in blob.name or code in file_path:
                    area_name = code
                    break
            if area_name != "" and blob.name.lower().endswith('.docx'):
                blob_client = container_client.get_blob_client(blob)
                process_word_document(blob_client, area_name, file_path)
            else:
                print(f"Skipping unsupported file format: {blob.name}")
 
# Start processing blobs in the root directory of the container
process_blobs(container_client)