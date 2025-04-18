from pyvis.network import Network
import pandas as pd
import os

def create_project_network(project_id, org_df, output_folder='output/networks'):
    os.makedirs(output_folder, exist_ok=True)
    
    net = Network(height='600px', width='100%', notebook=False, directed=False)
    net.force_atlas_2based(gravity=-30, central_gravity=0.01, spring_length=100, spring_strength=0.05)

    # 当前项目的所有组织
    current_orgs = org_df[org_df['projectID'] == project_id]['organisationID'].unique()

    # 这些组织还参与了哪些项目（邻近项目）
    neighbor_projects = org_df[org_df['organisationID'].isin(current_orgs)]['projectID'].unique()

    # 邻近项目涉及的组织
    neighbor_orgs = org_df[org_df['projectID'].isin(neighbor_projects)]['organisationID'].unique()

    # 子图数据（只保留相关组织和项目）
    sub_df = org_df[
        org_df['projectID'].isin(neighbor_projects) &
        org_df['organisationID'].isin(neighbor_orgs)
    ]

    # 添加项目节点
    for pid in neighbor_projects:
        net.add_node(f"project_{pid}", 
                     label=f"Project {pid}", 
                     color='red' if pid == project_id else 'lightgray', 
                     shape='star', 
                     size=20 if pid == project_id else 10)

    # 添加组织节点
    for org_id in neighbor_orgs:
        org_rows = org_df[org_df['organisationID'] == org_id].iloc[0]
        name = org_rows['name']
        country = org_rows['country']
        color = 'blue' if org_id in current_orgs else 'gray'

        net.add_node(f"org_{org_id}", 
                     label=name, 
                     title=f"{name} ({country})", 
                     color=color,
                     size=15 if org_id in current_orgs else 8)

    # 添加边
    for _, row in sub_df.iterrows():
        net.add_edge(f"project_{row['projectID']}", f"org_{row['organisationID']}",
                     color='black' if row['projectID'] == project_id else '#cccccc')

    # 添加交互按钮
    net.show_buttons(filter_=['physics'])

    # 保存
    output_path = f"{output_folder}/network_{project_id}.html"
    net.save_graph(output_path)
    print(f"Network saved to: {output_path}")


