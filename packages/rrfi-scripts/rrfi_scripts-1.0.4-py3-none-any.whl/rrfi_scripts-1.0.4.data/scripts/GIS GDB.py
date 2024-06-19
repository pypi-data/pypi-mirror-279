import logging
import os
import hashlib
import binascii
from datetime import datetime
import uuid
from PIL import Image
from exif import Image as ExifImage
import ezdxf
from azure.storage.blob import BlobServiceClient
from azure.search.documents import SearchClient
from azure.core.exceptions import HttpResponseError, ResourceNotFoundError
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
global IncName
filename='Na'

 
# Azure OpenAI configuration
openai_endpoint = "https://rrfimainoai.openai.azure.com/"
openai_api_key = "9c7a9a0b6b584e2c8701ae2fbb0ff6c2"
 
# Connect to Azure OpenAI
openai_client = AzureOpenAI(
    azure_endpoint=openai_endpoint,
    api_key=openai_api_key,
    api_version="2024-02-15-preview"
)

class AzureMetadataExtractor:
    def __init__(self, connection_string, container_name, search_service_name, index_name, search_api_key):
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        self.container_name = container_name
        self.search_client = SearchClient(
            endpoint=f"https://{search_service_name}.search.windows.net/",
            index_name=index_name,
            credential=AzureKeyCredential(search_api_key)
        )
 
    def extract_metadata_and_send_to_search(self, blob_client):
        blob_url = blob_client.url
        blob_name = blob_client.blob_name
        sas_token = "sp=r&st=2024-05-01T00:21:52Z&se=2024-05-01T08:21:52Z&sv=2022-11-02&sr=c&sig=AtMqLobgDKZ5WwlCFijX2YWnGUDFNiFsekY8zNZIIgo%3D"
        # Format file path with SAS token appended
        sas_token_param = f"&{sas_token}" if sas_token else ""  # Check if SAS token exists
        full_file_path = blob_name
        _, file_extension = os.path.splitext(blob_name)
        area_codes = ['NEA', 'CLA', 'YOR', 'GMC', 'EMD', 'LNA', 'WMD', 'EAN', 'HNL', 'THM', 'KSL', 'SSD', 'WSX', 'DCS']
        for code in area_codes:
            if code in blob_name or code in full_file_path:
                area_name = code
                break
        parent_folder = None
        if 'Sample Data (CLA)' in full_file_path:
            parent_folder = 'Sample Data (CLA)'
        elif 'Sample Data (THM)' in full_file_path:
            parent_folder = 'Sample Data (THM)'
        elif 'Sample Data (WMD)' in full_file_path:
            parent_folder = 'Sample Data (WMD)'
        if parent_folder:
            source_path_index = full_file_path.find(parent_folder) + len(parent_folder) + 1
            source_path = full_file_path[source_path_index:]
        else:
            source_path = full_file_path      
 
        if ".gdb" in full_file_path:                      
                    global metadata
                    global filename  
 
                    pwd=os.path.split(os.path.split(full_file_path)[0])[1]
                     # Extract location from the file path for Incident Name
                    location_completion = openai_client.chat.completions.create(
                        model="gpt-35-turbo",
                        messages=[
                            {"role": "system", "content": blob_name},
                            {"role": "system", "content": "You are an AI assistant that helps process data in a pipeline. Just return the values without any additional response text. Always return the last location name."},    
                            {"role": "user", "content": "You are a helpful agent. Your task is to identify and extract UK location names as a substring from the given text. It is possible to have multiple location names within the URL text."}
                        ],
                        temperature=0.7,
                        max_tokens=50,
                        top_p=0.95,
                        frequency_penalty=0,
                        presence_penalty=0,
                        stop=None
                    )
                
                    location = location_completion.choices[0].message.content
                    # Call OpenAI GPT-3.5 model to generate Incident_Date_and_Time
                    Incident_Datetime_completion = openai_client.chat.completions.create(
                        model="gpt-35-turbo",  # model = "deployment_name"
                        messages=[
                            {"role": "system", "content": blob_name},
                            {"role": "system", "content": "You are an AI assistant that helps process data in a pipeline. Just return the values without any additional response text. Always return the identified date in dd/mm/yyyy format. Only return one value based on prioritization. Higher priority value gets preference."},    
                            {"role": "user", "content": "You are a helpful agent. Your task is to identify and extract date, month, year as a substring from the given text. It is possible to have multiple date, month within the URL text. Highest priority for a full date. If there is no full date, look for a month and year value to return."}
                        ],
                        temperature=0.7,
                        max_tokens=800,
                        top_p=0.95,
                        frequency_penalty=0,
                        presence_penalty=0,
                        stop=None
                    )
        
                    # Extract Incident date and time from OpenAI output
                    incident_datetime = Incident_Datetime_completion.choices[0].message.content
 


                    #Extracting event type for Incident Name:
                    if 'storm' in blob_name.lower() or 'flood' in blob_name.lower():                  
                            path_folders = blob_name.split("/")
                            for event in path_folders:
                                if 'storm' in event.lower() or 'flood' in event.lower():
                                    event_folder = event
                                    break
                    else:
                            event_folder=''
                                                
                    # Extract the Area_Name from blob name
                    area_name = None
                    for code in area_codes:
                        if code in blob_name.upper():
                            area_name = code
                            break
 
                     # Construct Incident_Name based on conditions
                    if 'EA-IMToolbox' in blob_name:
                        if 'Current Incidents' in blob_name:
                            path_folders = blob_name.split("/")
                            current_incidents_index = path_folders.index("Current Incidents")
                            IncName = path_folders[current_incidents_index + 1]
                        elif 'Past Incidents' in blob_name:
                            path_folders = blob_name.split("/")
                            current_incidents_index = path_folders.index("Past Incidents")
                            IncName = path_folders[current_incidents_index + 1]
                        else:
                            area_name = area_name or ''
                            event_folder = event_folder or ''
                            location = location or ''
                            incident_datetime = incident_datetime or ''
                            if area_name=='':
                                IncName=event_folder+'_'+location+'_'+incident_datetime
                            elif event_folder=='':
                                IncName=area_name+'_'+location+'_'+incident_datetime
                            elif location=='':
                                IncName=area_name+'_'+event_folder+'_'+incident_datetime
                            elif incident_datetime=='':
                                IncName=area_name+'_'+event_folder+'_'+location
                            else:
                                IncName=area_name+'_'+event_folder+'_'+location+'_'+incident_datetime
                    else:
                        area_name = area_name or ''
                        event_folder = event_folder or ''
                        location = location or ''
                        incident_datetime = incident_datetime or ''
                        #IncName = f"{area_name}_{location}_{event_folder}_{incident_datetime}"
                        if area_name=='':
                            IncName=event_folder+'_'+location+'_'+incident_datetime
                        elif event_folder=='':
                            IncName=area_name+'_'+location+'_'+incident_datetime
                        elif location=='':
                            IncName=area_name+'_'+event_folder+'_'+incident_datetime
                        elif incident_datetime=='':
                            IncName=area_name+'_'+event_folder+'_'+location
                        else:
                            IncName=area_name+'_'+event_folder+'_'+location+'_'+incident_datetime
                    try:
                    # blob_properties = blob_client.get_blob_properties()
                        #blob_data = blob_client.download_blob()
                        self.search_client.upload_documents([metadata])
                        logger.info(f"Metadata uploaded for {blob_name}")
                    except Exception as e:
                        logger.error(f"Error processing {blob_name}: {str(e)}")
                        print(f"Error processing {blob_name}: {str(e)}")
                    if filename!=pwd:
                            file_id = str(uuid.uuid4())
                            # Get folder path by removing last segment (i.e., the filename) from the full file path
                            folder_path = os.path.dirname(full_file_path)
                            # Append SAS token to folder path
                            #folder_path_with_sas = f'{folder_path}?{sas_token_param[1:]}'
                            folder_path1=os.path.dirname(full_file_path)  
                            source_path=os.path.dirname(source_path)  
                            filename=os.path.split(os.path.split(full_file_path)[0])[1]
                            #Generating HASH value for identifying duplicate
                            content_settings = blob_client.get_blob_properties().content_settings
                            blobmd5 = bytearray(content_settings.content_md5)
                            hex = binascii.hexlify(blobmd5).decode('utf-8')

                            metadata = {
                                'id': file_id,
                                'Area_Name': area_name,
                                'Location_of_Incident': '',
                                'Incident_Name': IncName,
                                'Incident_Date_and_Time': '',
                                'Source_Type': '',
                                'Source_Name': '',
                                'TA_Code': '',
                                'TA_Name': '',
                                'Property_Protected': '',
                                'Property_Type': '',
                                'Security_Classification': '',
                                'Latitude': None,
                                'Longitude': None,
                                'Altitude': None,
                                'Catchment_Name': '',
                                'Postcode': '',
                                'National_Grid': '',
                                'Data_Type': '',
                                'River_Name': '',
                                'File_Name': filename,
                                'File_Path': folder_path,
                                'Flood_Outline': '',
                                'Rolling_Brief': '',
                                'Item_Type': '.gdb',
                                'Geo_Tag': '',
                                'Source_Path': source_path,
                                'Hash_value': hex                    
                            }
 
 
    def process_blob_container(self, container_client):
        for blob in container_client.list_blobs():
            if blob.name.endswith('/'):
                sub_folder_client = container_client.get_blob_client(blob.name)
                self.process_blob_container(sub_folder_client)
            else:
                try:
                    blob_client = container_client.get_blob_client(blob.name)                    
                    self.extract_metadata_and_send_to_search(blob_client)
                except (HttpResponseError, ResourceNotFoundError) as e:
                    logger.error(f"Error accessing {blob.name}: {str(e)}")
                    print(f"Error accessing {blob.name}: {str(e)}")
 
if __name__ == "__main__":
    connection_string = 'DefaultEndpointsProtocol=https;AccountName=rrfimainstorage;AccountKey=9h2WMr2hvNI1V8xixizn49neFq6/Oba61Z4e6L9YAuuRqrSXEsyEB2NuDhO2NXZaBec5VvH4O8D2+ASt1tyDqA==;EndpointSuffix=core.windows.net'
    container_name = 'rrfimaincon'
    search_service_name = 'rrfimainsearch'
    index_name = 'rrfisearch_v2'
    search_api_key = '1LnrhfcdFVeuJ7jVOe2ElJi2uFib34RZhLWnig1nDiAzSeAIlOEO'
 
    metadata_extractor = AzureMetadataExtractor(connection_string, container_name, search_service_name, index_name, search_api_key)
    container_client = metadata_extractor.blob_service_client.get_container_client(container_name)
    metadata_extractor.process_blob_container(container_client)