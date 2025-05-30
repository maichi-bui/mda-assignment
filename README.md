# [MDA assignment] Group 16 On-campus 
## Dataset
**The CORDIS Horizon Europe Dataset (2021–2027)**
- €95.5 billion in EU funding for research & innovation
- Covers over 15,000+ projects across science & technology
- Open-access, publicly available [data source](https://data.europa.eu/data/datasets/cordis-eu-research-projects-under-horizon-europe-2021-2027?locale=en)

![Horizon EU](https://github.com/user-attachments/assets/dd62a134-ddb4-48af-b581-77b4c6a8695a)


## Repository structure
    .
    ├── .streamlit              # Streamlit configure folder
    │   ├── secrets.toml        # Credentials to run the app, structured as `secret_example.toml`    
    ├── analysis-results        # Aggregated data folders
    ├── chatbot                 
    │   ├── pdfs_to_supabase.py # Function to downdload pdfs file then send embedding to Supabase
    ├── horizon-dataset         # Raw and cleaned data folders    
    ├── main_page_engdb         # Streamlit sub-pages and utilities functions
    │   ├── create_network.py   # Function to create network visualization
    │   ├── dashboard.py        # Dashboard page
    │   ├── indexer.py          # Create indices for search engine
    │   ├── introduction.py     # Introduction page
    │   ├── rag_app.py          # Function for chatbot
    │   ├── search_engine.py    # Search page and Individual project page
    │   ├── searcher.py         # Search function
    ├── notebook                # POC code in Jupyter notebooks
    ├── .dockerignore              
    ├── .gitignore              
    ├── app.py                  # Streamlit main app
    ├── app.yaml                # GAE deployment configation
    ├── Dockerfile              
    ├── README.md               # Instructions to run script
    ├── requirements.txt        # All packages required for scripts to run 
    └── ...

## How to run it on your own machine

1. Create virtual environment - Python 3.9 and install requirements
   
   ```
   $ python -m venv venv/
   $ source venv/bin/activate
   $ pip install -r requirements.txt
   ```

2. Create `.streamlit/secrets.toml` as example `secret_example.toml`

3. Run the app

   ```
   $ python main_page_engdb/indexer.py
   $ streamlit run app.py
   ```

## How to Deploy on Google App Engine

1. Install Google Cloud SDK and authorize: 
   [Instructions](https://cloud.google.com/sdk/docs/install-sdk)

2. Deploy on Google App Engine via this command: `gcloud app deploy`
