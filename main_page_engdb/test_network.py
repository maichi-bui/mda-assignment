import pandas as pd
from create_network import create_project_network
import os
#os.chdir("C:/Users/lu/Desktop/KUL semester2/mda/EngineDashboard")

# 读取组织数据
org_df = pd.read_csv('organization.csv')  # 路径根据你的实际文件来改

# 随机选择 5 个不同的 projectID
sample_projects = org_df['projectID'].drop_duplicates().sample(5, random_state=42).tolist()

print(f"Testing projects: {sample_projects}")

# 逐个生成网络图
for pid in sample_projects:
    output_path = create_project_network(pid, org_df)
    if output_path:
        print(f"✅ Successfully generated: {output_path}")
    else:
        print(f"❌ Failed to generate for projectID: {pid}")
