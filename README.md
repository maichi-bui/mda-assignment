# [MDA assignment] Group 16 On-campus 

## Repository structure
    .
    ├── notebook                # POC code in Jupyter notebooks
    ├── horizon-dataset         # Data folders
    │   ├── clean_script.ipynb  # Script to clean raw files
    │   ├── clean-data/         # Folder including 6 cleaned data files
    │   ├── ...         
    ├── .gitignore              
    ├── app.py                  # Streamlit app
    ├── requirements.txt        # All packages required for scripts to run 
    ├── README.md               # Instructions to run script
    └── ...

## Streamlit blank app template
A simple Streamlit app template for you to modify!

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blank-app-template.streamlit.app/)

### How to run it on your own machine

1. Create virtual environment - Python 3.9
   
   ```
   $ python -m venv venv/
   $ source venv/bin/activate
   ```

2. Install the requirements

   
   ```
   $ curl -fsSL https://ollama.com/install.sh | sh
   $ pip install -r requirements.txt
   ```

3. Run the app

   ```
   $ python -m streamlit run app.py
   ```
