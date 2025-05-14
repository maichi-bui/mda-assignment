from pyvis.network import Network
import pandas as pd
import os
import os
#os.chdir("C:/Users/lu/Desktop/KUL semester2/mda/EngineDashboard")

def create_project_network(project_id, org_df, output_folder='output/networks'):
    os.makedirs(output_folder, exist_ok=True)

    # 创建网络（取消force布局）
    net = Network(height='600px', width='100%', notebook=False, directed=False)

    # 开启物理引擎（只用简单 barnes_hut）
    net.barnes_hut(gravity=-5000, central_gravity=0.3, spring_length=95, spring_strength=0.02)

    # 设置网络选项
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

    # 当前项目的所有组织
    current_orgs = org_df[org_df['projectID'] == project_id]['organisationID'].unique().tolist()

    # 这些组织还参与了哪些项目（邻近项目）
    neighbor_projects = org_df[org_df['organisationID'].isin(current_orgs)]['projectID'].unique().tolist()

    # 邻近项目涉及的组织
    if len(neighbor_projects) < 3:
        neighbor_orgs = org_df[org_df['projectID'].isin(neighbor_projects)]['organisationID'].unique().tolist()
    else:
        neighbor_orgs = current_orgs
    # 子图数据（只保留相关组织和项目）
    sub_df = org_df[
        org_df['projectID'].isin(neighbor_projects) &
        org_df['organisationID'].isin(current_orgs)
    ][['projectID', 'organisationID']].drop_duplicates()

    # Add neighbor projects to the network
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

    # 生成HTML内容（改这里！自己生成，不用 net.save_graph）
    html_content = net.generate_html()

    # 保存HTML到指定文件
    network_html_path = os.path.join(output_folder, f"network_{project_id}.html")
    with open(network_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return network_html_path



