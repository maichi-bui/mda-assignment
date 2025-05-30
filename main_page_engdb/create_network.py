from pyvis.network import Network
from random import sample

LIMIT_NODE = 60

def create_project_network(project_id:str, org_df):

    net = Network(height='600px', width='100%', notebook=False, directed=False)
    net.barnes_hut(gravity=-5000, central_gravity=0.3, spring_length=95, spring_strength=0.02)

    net.set_options("""
            options = {
            "nodes": {
                "borderWidth": 2,
                "size": 16,
                "font": {
                "size": 14
                }
            },
            "edges": {
                "color": {
                "inherit": true
                },
                "smooth": false
            },
            "physics": {
                "barnesHut": {
                "gravitationalConstant": -30000,
                "centralGravity": 0.3,
                "springLength": 95,
                "springConstant": 0.02,
                "damping": 0.09,
                "avoidOverlap": 1
                },
                "minVelocity": 0.75
            }
            }
            """
        )
    # Define role-specific edge styles
    role_styles = {
        'coordinator': {'color': '#ff0000', 'width': 2, 'dashes': False, 'arrow': 'to'},
        'associatedPartner': {'color': '#0000ff', 'width': 2, 'dashes': [5,5], 'arrow': 'to'}
    }

    if project_id!=str(101096329): # only exception due to this project has no active coordinator
        coordinator_org = org_df.loc[(org_df['projectID'] == project_id)&(org_df['role']=='coordinator'),'organisationID'].values[0]
    else:
        coordinator_org = None

    partner_orgs = org_df.loc[(org_df['projectID'] == project_id)&(org_df['role']=='associatedPartner'),'organisationID'].tolist()

    # get projects that partner orgs are coordinators, limit by LIMIT_NODE
    if len(partner_orgs) > LIMIT_NODE:
        partner_orgs = sample(partner_orgs, LIMIT_NODE)
    neighbor_projects = org_df.loc[(org_df['organisationID'].isin(partner_orgs))&(org_df['role']=='coordinator'),'projectID'].tolist()

    # add projects that the above coordinator is partner
    neighbor_projects += org_df.loc[(org_df['organisationID']==coordinator_org)&(org_df['role']=='associatedPartner'),'projectID'].tolist()

    # get orgs that coordinates those neighbor_projects 
    if len(neighbor_projects) > LIMIT_NODE:
        neighbor_projects = sample(neighbor_projects, LIMIT_NODE)
    neighbor_orgs = org_df.loc[(org_df['projectID'].isin(neighbor_projects))&(org_df['role']=='coordinator'),'organisationID'].tolist()

    all_orgs = partner_orgs + neighbor_orgs
    if coordinator_org:
        all_orgs.append(coordinator_org)

    neighbor_projects.append(project_id)
    sub_df = org_df[
        org_df['projectID'].isin(neighbor_projects) &
        org_df['organisationID'].isin(all_orgs)][['organisationID','projectID','projectAcronym','name','role', 'country']]
    
    # Add edges between projects and organizations, limit to 20 edges
    for row in sub_df.to_dict('records'):
        pid = row['projectID']
        
        net.add_node(f"project_{pid}",
                    color='red' if pid == project_id else 'lightgray',
                    shape='star',
                    label = row['projectAcronym'],
                    size=20 if pid == project_id else 10)
        
        org_id = row['organisationID']
        role = row['role']
        name = row['name']
        country = row['country']
        
        net.add_node(f"org_{org_id}",
                    label=name,
                    title=f"{name} ({country})",
                    color='blue' if (org_id in partner_orgs or org_id == coordinator_org) else 'gray',
                    size=15 if (org_id in partner_orgs or org_id == coordinator_org) else 8)
        
        net.add_edge(f"project_{pid}", f"org_{org_id}",
                        color=role_styles[role]['color'],
                        width=role_styles[role]['width'],
                        dashes=role_styles[role]['dashes'],
                        arrow=role_styles[role]['arrow'])


    html_content = net.generate_html()
    
    return html_content



