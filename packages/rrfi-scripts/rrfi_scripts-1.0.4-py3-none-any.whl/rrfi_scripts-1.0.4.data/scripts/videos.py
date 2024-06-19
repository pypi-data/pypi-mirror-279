import os
import uuid
import hashlib
from azure.storage.blob import BlobServiceClient, BlobPrefix
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI
 
# Azure Blob Storage connection string and container name
connection_string = "DefaultEndpointsProtocol=https;AccountName=rrfimainstorage;AccountKey=9h2WMr2hvNI1V8xixizn49neFq6/Oba61Z4e6L9YAuuRqrSXEsyEB2NuDhO2NXZaBec5VvH4O8D2+ASt1tyDqA==;EndpointSuffix=core.windows.net"
container_name = "rrfimaintestcon"
 
# Azure Cognitive Search details
search_service_name = "rrfimainsearch"
index_name = "rrfivideos"
api_key = "1LnrhfcdFVeuJ7jVOe2ElJi2uFib34RZhLWnig1nDiAzSeAIlOEO"
search_endpoint = f"https://{search_service_name}.search.windows.net/"
 
# Azure OpenAI details
openai_api_key = "9c7a9a0b6b584e2c8701ae2fbb0ff6c2"
openai_api_base = "https://rrfimainoai.openai.azure.com/"
openai_api_version = "2024-02-15-preview"
 
# Connect to Blob Storage
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)
 
# Connect to Azure Cognitive Search
search_client = SearchClient(endpoint=search_endpoint,
                             index_name=index_name,
                             credential=AzureKeyCredential(api_key))
 
# Set up OpenAI API client
client = AzureOpenAI(
    azure_endpoint=openai_api_base,
    api_key=openai_api_key,
    api_version=openai_api_version
)
 
# Area codes list
area_codes = ['NEA', 'CLA', 'YOR', 'GMC', 'EMD', 'LNA', 'WMD', 'EAN', 'HNL', 'THM', 'KSL', 'SSD', 'WSX', 'DCS']
 
# Helper function to get response from OpenAI
def get_openai_response(client, file_path, user_prompt, system_prompt):
    messages = [
        {"role": "system", "content": f"File path: {file_path}"},
        {"role": "user", "content": user_prompt},
        {"role": "system", "content": system_prompt}
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
    return completion.choices[0].message.content.strip()
 
# Function to generate hash value of the file
def generate_file_hash(blob_client):
    hasher = hashlib.sha256()
    downloader = blob_client.download_blob()
    for chunk in downloader.chunks():
        hasher.update(chunk)
    return hasher.hexdigest()
 
# Function to process a single video file
def process_video_file(blob_client, area_name, full_file_path):
    try:
        # Download blob data
        blob_data = blob_client.download_blob()
        blob_content = blob_data.readall()
 
        # Generate hash value for the file content
        file_hash = generate_file_hash(blob_client)
 
        # Extract metadata from the file path
        file_name = os.path.basename(blob_client.blob_name)
        unique_id = str(uuid.uuid4())
 
        # Call OpenAI API to identify location of incident in the file path
        location_response = get_openai_response(
            client, full_file_path,
            "You are a helpful agent. Your task is to identify and extract UK locations as a substring from the given text. It is possible to have multiple locations within the URL text.",
            "You are an AI assistant that helps process data in a pipeline. Just return the values without any additional response text. Always return the last location name."
        )
 
        # Call OpenAI API to identify date in the file path
        date_response = get_openai_response(
            client, full_file_path,
            "You are a helpful agent. Your task is to identify and extract date, month, year as a substring from the given text. It is possible to have multiple date, month within the URL text. Highest priority for a full date. If there is no full date, look for a month and year value to return.",
            "You are an AI assistant that helps process data in a pipeline. Just return the values without any additional response text. Always return the identified date in dd/mm/yyyy format. Only return one value based on prioritization. Higher priority value gets preference."
        )
 
        # Extracting event type for Incident Name:
        event_folder = ''
        if 'storm' in blob_client.blob_name.lower() or 'flood' in blob_client.blob_name.lower():
            path_folders = blob_client.blob_name.split("/")
            for event in path_folders:
                if 'storm' in event.lower() or 'flood' in event.lower():
                    event_folder = event
                    break
 
        # Logic to derive area_name
        for code in area_codes:
            if code in blob_client.blob_name.upper() or code in full_file_path.upper():
                area_name = code
                break
 
        # Logic to derive Incident_Name
        if 'EA-IMToolbox' in blob_client.blob_name:
            if 'Current Incidents' in blob_client.blob_name:
                path_folders = blob_client.blob_name.split("/")
                current_incidents_index = path_folders.index("Current Incidents")
                incident_name = path_folders[current_incidents_index + 1]
            elif 'Past Incidents' in blob_client.blob_name:
                path_folders = blob_client.blob_name.split("/")
                past_incidents_index = path_folders.index("Past Incidents")
                incident_name = path_folders[past_incidents_index + 1]
            else:
                area_name = area_name or ''
                event_folder = event_folder or ''
                location_response = location_response or ''
                date_response = date_response or ''
                if not area_name:
                    incident_name = f"{event_folder}_{location_response}_{date_response}"
                elif not event_folder:
                    incident_name = f"{area_name}_{location_response}_{date_response}"
                elif not location_response:
                    incident_name = f"{area_name}_{event_folder}_{date_response}"
                elif not date_response:
                    incident_name = f"{area_name}_{event_folder}_{location_response}"
                else:
                    incident_name = f"{area_name}_{event_folder}_{location_response}_{date_response}"
        else:
            area_name = area_name or ''
            event_folder = event_folder or ''
            location_response = location_response or ''
            date_response = date_response or ''
            if not area_name:
                incident_name = f"{event_folder}_{location_response}_{date_response}"
            elif not event_folder:
                incident_name = f"{area_name}_{location_response}_{date_response}"
            elif not location_response:
                incident_name = f"{area_name}_{event_folder}_{date_response}"
            elif not date_response:
                incident_name = f"{area_name}_{event_folder}_{location_response}"
            else:
                incident_name = f"{area_name}_{event_folder}_{location_response}_{date_response}"
 
        # Create a document with area name, incident name, and other details
        document = {
            "Area_Name": area_name,
            "File_Name": file_name,
            "File_Path": blob_client.blob_name,
            "Source_Path": blob_client.blob_name,
            "Item_Type": os.path.splitext(file_name)[1] if '.' in file_name else '',
            "Incident_Name": incident_name,
            #"Incident_Location": location_response,
            "Incident_Date_and_Time": date_response,
            "Hash_Value": file_hash,
            "id": unique_id
        }
 
        # Upload document to Azure Cognitive Search
        search_client.upload_documents(documents=[document])
        print(f"Uploaded document: {unique_id} - {file_name}")
    except Exception as e:
        print(f"An error occurred processing blob {blob_client.blob_name}: {str(e)}")
 
# Recursive function to iterate through blobs
def process_blobs(container_client, file_path=""):
    for blob in container_client.list_blobs(name_starts_with=file_path):
        if isinstance(blob, BlobPrefix):
            process_blobs(container_client, file_path=blob.name)
        else:
            area_name = ""
            for code in area_codes:
                if code in blob.name or code in file_path:
                    area_name = code
                    break
            if area_name != "" and (blob.name.lower().endswith('.mp4') or blob.name.lower().endswith('.avi')):
                blob_client = container_client.get_blob_client(blob)
                process_video_file(blob_client, area_name, blob.name)
            else:
                print(f"Skipping unsupported file format or missing area code: {blob.name}")
 
# Start processing blobs in the root directory of the container
process_blobs(container_client)