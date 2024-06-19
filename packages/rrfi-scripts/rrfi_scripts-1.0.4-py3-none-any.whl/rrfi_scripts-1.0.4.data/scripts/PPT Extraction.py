import os
import comtypes.client
import tempfile
import requests
import json
import uuid
import re
from azure.storage.blob import BlobServiceClient
from openai import AzureOpenAI
import hashlib
 
# Define function to extract text from PowerPoint files
def extract_text_from_ppt_from_blob(container_client, blob, file_name):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(container_client.download_blob(blob).readall())
        temp_file_path = temp_file.name
 
    powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
    powerpoint.Visible = True
    presentation = powerpoint.Presentations.Open(temp_file_path)
    text = []
    try:
        for slide in presentation.Slides:
            for shape in slide.Shapes:
                if shape.HasTextFrame:
                    text.append(shape.TextFrame.TextRange.Text)
    finally:
        presentation.Close()
        powerpoint.Quit()
        os.remove(temp_file_path)  # Clean up temp file
 
    # Combine text from all slides into a single string
    text = '\n'.join(text)
 
    # Extract postcode using regex
    #postcode_pattern = re.compile(r'^([A-Za-z]{2}\d{1,2}[A-Za-z]?)[\s]+([\d][A-Za-z]{2})$', re.MULTILINE)
    postcode_pattern=re.compile(r'^([A-Za-z]{1,2}\d[A-Za-z\d]?)[\s]?(\d[A-Za-z]{2})$', re.MULTILINE)
    match = postcode_pattern.search(text)
    postcode = None
    if match:
        postcode = f"{match.group(1)} {match.group(2)}"
 
    return text, postcode
 
# Define function to send data to Azure Cognitive Search
def send_to_azure_search(id, rivername, filename, file_path, item_type, postcode, location_of_incident, catchment_name, security_classification, area_name, incident_date, IncName, hash_value):
    # Azure Cognitive Search endpoint and API version
    search_endpoint = "https://rrfimainsearch.search.windows.net/"
    api_version = "2024-03-01-preview"
 
    # Azure Cognitive Search index name
    index_name = "rrfitesting_v1"
 
    # API key for authentication
    api_key = "1LnrhfcdFVeuJ7jVOe2ElJi2uFib34RZhLWnig1nDiAzSeAIlOEO"
 
    # Endpoint for adding documents to the index
    index_url = f"{search_endpoint}indexes/{index_name}/docs/index?api-version={api_version}"
 
    # Document to be added to the index
    document = {
        "value": [
            {
                "@search.action": "upload",
                "id": id,
                "River_Name": rivername,
                "File_Name": filename,
                "File_Path": file_path,
                "Item_Type": item_type,
                "Postcode": postcode,
                "Location_of_Incident": location_of_incident,
                "Catchment_Name": catchment_name,
                "Security_Classification": security_classification,
                "Area_Name": area_name,
                "Incident_Date_and_Time": incident_date,
                "Incident_Name": IncName,
                "Hash_Value": hash_value
            }
        ]
    }
 
    # Convert document to JSON format
    document_json = json.dumps(document)
 
    # Headers for the HTTP request
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }
 
    # Send HTTP POST request to add document to the index
    response = requests.post(index_url, headers=headers, data=document_json)
 
    # Check if the request was successful
    if response.status_code == 201:
        print("Document added to Azure Cognitive Search index successfully.")
    else:
        print(f"Error: Failed to add document to Azure Cognitive Search index. Status code: {response.status_code}")
        print(response.text)
 
# Define function to process PowerPoint files from Azure Blob container
def process_ppt_files_from_blob_container(blob_service_client, container_name, directory_path=""):
    container_client = blob_service_client.get_container_client(container_name)
    blob_list = container_client.list_blobs(name_starts_with=directory_path)
 
    for blob in blob_list:
        if blob.name.endswith('/'):
            process_ppt_files_from_blob_container(blob_service_client, container_name, blob.name)
        elif blob.name.lower().endswith(('.ppt', '.pptx')):
            # Extract text and postcode from PowerPoint file
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(container_client.download_blob(blob).readall())
                temp_file_path = temp_file.name            
           
            try:
                extracted_text, postcode = extract_text_from_ppt_from_blob(container_client, blob, blob.name)
            except Exception as e:
                print(f"Failed to extract text from {blob.name}: {e}")
                continue
           
            # Determine Are_Name
            area_name = ''
           
            area_codes = ['NEA', 'CLA', 'YOR', 'GMC', 'EMD', 'LNA', 'WMD', 'EAN', 'HNL', 'THM', 'KSL', 'SSD', 'WSX', 'DCS']
            for code in area_codes:
                if code in blob.name:
                    area_name = code
                    break
           
            #Extracting event type for Incident Name:
                if 'storm' in blob.name.lower() or 'flood' in blob.name.lower():                  
                        path_folders = blob.name.split("/")
                        for event in path_folders:
                            if 'storm' in event.lower() or 'flood' in event.lower():
                                event_folder = event
                                break
                else:
                        event_folder=''
 
            # Use Azure OpenAI to determine river names from extracted text
            client = AzureOpenAI(
                azure_endpoint="https://rrfimainoai.openai.azure.com/",
                api_key="9c7a9a0b6b584e2c8701ae2fbb0ff6c2",
                api_version="2024-02-15-preview"
            )
 
            # Call OpenAI to extract location for incident name
            message_text_incident_location = [
                {"role": "system", "content": blob.name},
                {"role": "system", "content": "You are an AI assistant that helps process data in a pipeline. Just return the values without any additional response text. Always return the last location name, even if it is followed by special characters and other text."},    
                {"role": "user", "content": "You are a helpful agent. Your task is to identify and extract UK location name as a substring from the given text. It is possible to have multiple location names within the URL text."}
            ]
 
            try:
                completion_incident_location = client.chat.completions.create(
                    model="gpt-35-turbo",
                    messages=message_text_incident_location,
                    temperature=0.7,
                    max_tokens=800,
                    top_p=0.95,
                    frequency_penalty=0,
                    presence_penalty=0,
                    stop=None
                )
                incident_location = completion_incident_location.choices[0].message.content
            except Exception as e:
                print(f"Failed to get incident location for {blob.name}: {e}")
                incident_location = ""
           
            # Call OpenAI to extract date for incident name
            message_text_incident_date = [
                {"role": "system", "content": blob.name},
                {"role": "system", "content": "You are an AI assistant that helps process data in a pipeline. Just return the values without any additional response text. Always return the identified date in dd/mm/yyyy format. Only return one value based on prioritization. Higher priority value gets preference."},    
                {"role": "user", "content": "You are a helpful agent. Your task is to identify and extract date, month, year as a substring from the given text. It is possible to have multiple date, month within the URL text. Highest priority for a full date. If there is no full date, look for a month and year value to return."},
            ]
 
            try:
                completion_incident_date = client.chat.completions.create(
                    model="gpt-35-turbo",
                    messages=message_text_incident_date,
                    temperature=0.2,
                    max_tokens=800,
                    top_p=0.95,
                    frequency_penalty=0,
                    presence_penalty=0,
                    stop=None
                )
                incident_date = completion_incident_date.choices[0].message.content
            except Exception as e:
                print(f"Failed to get incident date for {blob.name}: {e}")
                incident_date = ""
           
            # Call OpenAI to extract river names
            message_text_river = [
                {"role": "system", "content": extracted_text},
                {"role": "user", "content": "From the data provided, identify all England river names. \nReturn all river names concatenated in a single string, comma separated."},
                {"role": "system", "content": "You help process data in a pipeline. \nOnly return the values without any other response text. If values can't be identified, return blank."}
            ]
 
            try:
                completion_river = client.chat.completions.create(
                    model="gpt-35-turbo",
                    messages=message_text_river,
                    temperature=0.7,
                    max_tokens=800,
                    top_p=0.95,
                    frequency_penalty=0,
                    presence_penalty=0,
                    stop=None
                )
                rivername = completion_river.choices[0].message.content
            except Exception as e:
                print(f"Failed to get river names for {blob.name}: {e}")
                rivername = ""
 
            # Call OpenAI to extract location of incident
            message_text_location = [
                {"role": "system", "content": extracted_text},
                {"role": "user", "content": "From the data provided, identify all town names. \nReturn all town names concatenated in a single string, comma separated."},
                {"role": "system", "content": "You help process data in a pipeline. \nOnly return the values without any other response text"}
            ]
 
            try:
                completion_location = client.chat.completions.create(
                    model="gpt-35-turbo",
                    messages=message_text_location,
                    temperature=0.7,
                    max_tokens=800,
                    top_p=0.95,
                    frequency_penalty=0,
                    presence_penalty=0,
                    stop=None
                )
                location_of_incident = completion_location.choices[0].message.content
            except Exception as e:
                print(f"Failed to get location of incident for {blob.name}: {e}")
                location_of_incident = ""
 
            # Call OpenAI to extract catchment_name
            message_text_catchment = [
                {"role": "system", "content": extracted_text},
                {"role": "user", "content": "From the data provided, identify all catchment names. \nReturn all catchment names concatenated in a single string, comma separated."},
                {"role": "system", "content": "You help process data in a pipeline. \nOnly return the values without any other response text"}
            ]
 
            try:
                completion_catchment = client.chat.completions.create(
                    model="gpt-35-turbo",
                    messages=message_text_catchment,
                    temperature=0.7,
                    max_tokens=800,
                    top_p=0.95,
                    frequency_penalty=0,
                    presence_penalty=0,
                    stop=None
                )
                catchment_name = completion_catchment.choices[0].message.content
            except Exception as e:
                print(f"Failed to get catchment names for {blob.name}: {e}")
                catchment_name = ""
 
            # Call OpenAI to extract security classification
            message_text_security = [
                {"role": "system", "content": extracted_text},
                {"role": "user", "content": "From the data you are given, identify if any of the following text is included within the data. 'Official', 'Secret', 'Top Secret', 'Official Sensitive'. If any of them are listed within the data, return the text."},
                {"role": "system", "content": "You help process data in a pipeline. \nOnly return the values without any other response text. Do not add any of these four texts if they are not found within the data provided"}
            ]
 
            try:
                completion_security = client.chat.completions.create(
                    model="gpt-35-turbo",
                    messages=message_text_security,
                    temperature=0.7,
                    max_tokens=800,
                    top_p=0.95,
                    frequency_penalty=0,
                    presence_penalty=0,
                    stop=None
                )
                security_classification = completion_security.choices[0].message.content
            except Exception as e:
                print(f"Failed to get security classification for {blob.name}: {e}")
                security_classification = ""
 
            #Generate Incident Name
            if 'EA-IMToolbox' in blob.name:
                if 'Current Incidents' in blob.name:
                    path_folders = blob.name.split("/")
                    current_incidents_index = path_folders.index("Current Incidents")
                    IncName = path_folders[current_incidents_index + 1]
                elif 'Past Incidents' in blob.name:
                    path_folders = blob.name.split("/")
                    current_incidents_index = path_folders.index("Past Incidents")
                    IncName = path_folders[current_incidents_index + 1]
                else:
                    area_name = area_name or ''
                    event_folder = event_folder or ''
                    incident_location = incident_location or ''
                    incident_date = incident_date or ''
                    if area_name=='':
                        IncName=event_folder+'_'+incident_location+'_'+incident_date
                    elif event_folder=='':
                        IncName=area_name+'_'+incident_location+'_'+incident_date
                    elif incident_location=='':
                        IncName=area_name+'_'+event_folder+'_'+incident_date
                    elif incident_date=='':
                        IncName=area_name+'_'+event_folder+'_'+incident_location
                    else:
                        IncName=area_name+'_'+event_folder+'_'+incident_location+'_'+incident_date
            else:
                area_name = area_name or ''
                event_folder = event_folder or ''
                incident_location = incident_location or ''
                incident_date = incident_date or ''
                #IncName = f"{area_name}_{location}_{event_folder}_{incident_datetime}"
                if area_name=='':
                    IncName=event_folder+'_'+incident_location+'_'+incident_date
                elif event_folder=='':
                    IncName=area_name+'_'+incident_location+'_'+incident_date
                elif incident_location=='':
                    IncName=area_name+'_'+event_folder+'_'+incident_date
                elif incident_date=='':
                    IncName=area_name+'_'+event_folder+'_'+incident_location
                else:
                    IncName=area_name+'_'+event_folder+'_'+incident_location+'_'+incident_date
 
            # Generate UUID for document
            doc_id = str(uuid.uuid4())
 
            # Calculate hash value for the file
            with open(temp_file_path, "rb") as f:
                hash_value = hashlib.sha256(f.read()).hexdigest()
            # Add the document to Azure Cognitive Search
            send_to_azure_search(doc_id, rivername, os.path.basename(blob.name), blob.name,
                                 os.path.splitext(blob.name)[1][1:], postcode, location_of_incident, catchment_name, security_classification, area_name, incident_date, IncName, hash_value)
 
# Initialize Azure Blob service client
blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=rrfimainstorage;AccountKey=9h2WMr2hvNI1V8xixizn49neFq6/Oba61Z4e6L9YAuuRqrSXEsyEB2NuDhO2NXZaBec5VvH4O8D2+ASt1tyDqA==;EndpointSuffix=core.windows.net")
 
# Process PowerPoint files from Azure Blob container
process_ppt_files_from_blob_container(blob_service_client, "rrfimaintestcon")