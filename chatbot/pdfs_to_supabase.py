import os
import warnings
import re
import string
import time
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PDFPlumberLoader
from google import genai
from google.genai import types
from supabase import create_client, Client

warnings.filterwarnings('ignore')
load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai_client = genai.Client(api_key=GEMINI_API_KEY)
pdfs_directory = '/Users/maichi/KULeuven/mda/mda-assignment/chatbot/pdfs'

def clean_text(raw_text):
    # Remove escape sequences and non-printable characters
    cleaned = raw_text.encode('utf-8', 'ignore').decode('unicode_escape')
    
    # Keep printable characters only
    cleaned = ''.join(ch for ch in cleaned if ch in string.printable)
    
    # Optionally remove extra whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()

    return cleaned

def load_pdf(file_path):
    loader = PDFPlumberLoader(file_path)
    documents = loader.load()
    return documents

def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )
    chunks = text_splitter.split_documents(documents)
    temp = ' '
    all_content = []
    for chunk in chunks:
        content = clean_text(chunk.page_content) + temp
        if len(content) < 1000:
            print('content too short')
            temp = content
            continue
        else:
            all_content.append(content)
            temp = ' '
    return all_content

def get_embedding(text):
    response = genai_client.models.embed_content(
        model="text-embedding-004",
        contents=text,
        config=types.EmbedContentConfig(output_dimensionality=768)
        
    )
    return response.embeddings[0].values
            
def send_supabase(chunks, project_id, deliverable_id):
    if len(chunks) > 150:
        print("Documents too long, number of chunks: ", len(chunks))
        return deliverable_id
    if deliverable_id =='190109269_4_DELIVHORIZON':
        chunks = chunks[39:]
    for chunk in chunks:
        if chunk:
            embedding = get_embedding(chunk)
            supabase.table("horizon_deliverables").insert({
                "project_id": project_id,
                "deliverable_id":deliverable_id,
                "content": chunk,
                "embedding": embedding
            }).execute()
            print("Data sent to Supabase successfully : {}".format(deliverable_id))


if __name__ == '__main__':
    deliverables = pd.read_csv("deliverables_supabse.csv") # 8897 pdf files
    sent_deliverables = set(pd.read_csv("sent_items.csv").deliverable_id).union(set(pd.read_csv("removed_deliver.csv").deliverable_id))
    

    deliverables = deliverables[~deliverables.id.isin(sent_deliverables)] # this is the test record
    print("Number of deliverables: ", len(deliverables))
    # deliverables = deliverables.sort_values('contentUpdateDate').groupby('projectID').tail(10)
    deliverables = deliverables.to_dict(orient='records')
    service = Service("/usr/local/bin/chromedriver")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Optional: run headless
    prefs = {"download.default_directory" : pdfs_directory}
    chrome_options.add_experimental_option("prefs", prefs)

    for item in tqdm(deliverables):
        if os.path.exists('pdfs/Attachment_0.pdf'):
            os.remove("pdfs/Attachment_0.pdf")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("start download for: ", item['id'])
        deliverable_id = item['id']
        project_id = item['projectID']
        description = item['description']
        url = item['url']

        driver.get(url)
            
        time.sleep(10)  # Wait for download
        
        if not os.path.exists('pdfs/Attachment_0.pdf'):
            if sum([fname.endswith('.crdownload') for fname in os.listdir('pdfs')]) == 0:
                print("link died: ", url)
                pd.DataFrame([{'deliverable_id': deliverable_id, 'count': 0}]).to_csv("sent_items.csv", mode='a', header=False, index=False)
                continue
            else:
                time.sleep(10)
                if not os.path.exists('pdfs/Attachment_0.pdf'):
                    print("link take too long to download: ", url)
                    pd.DataFrame([{'deliverable_id': deliverable_id, 'count': 0}]).to_csv("sent_items.csv", mode='a', header=False, index=False)
                    continue
            continue  
                    
    
        print("Download should be complete. Check your files.")
        # Closing the tab 
        driver.close() 
        documents = load_pdf("pdfs/Attachment_0.pdf")
        chunked_texts = split_text(documents)
        
        check_document = send_supabase(chunked_texts, project_id, deliverable_id)
        if check_document:
            pd.DataFrame([{'deliverable_id': deliverable_id, 'count': len(chunked_texts)}]).to_csv("removed_deliver.csv", mode='a', header=False, index=False)    
        
        pd.DataFrame([{'deliverable_id': deliverable_id, 'count': len(chunked_texts)}]).to_csv("sent_items.csv", mode='a', header=False, index=False)
        