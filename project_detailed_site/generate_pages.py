import pandas as pd
import os
from jinja2 import Environment, FileSystemLoader
from create_network import create_project_network

# read CSV files
project_df = pd.read_csv('data/project.csv', sep=',')
org_df = pd.read_csv('data/organization.csv', sep=',')

# create output directories
os.makedirs('output/networks', exist_ok=True)

# initialize Jinja2 environment
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('project_template.html')

# run through each project and generate HTML pages
for project_id, group in org_df.groupby('projectID'):
    # gain project information
    project_info = project_df[project_df['id'] == project_id].iloc[0].to_dict()

    # gain organization information
    orgs = group[['organisationID', 'name', 'country', 'city', 'role', 'ecContribution']].to_dict(orient='records')

    # generate network graph
    create_project_network(project_id, org_df)
    network_path = f"networks/network_{project_id}.html"

    # render HTML page
    rendered_html = template.render(project=project_info, organization=orgs, network_path=network_path)

    with open(f'output/project_{project_id}.html', 'w', encoding="utf-8") as f:
        f.write(rendered_html)
