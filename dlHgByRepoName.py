
import os
import requests
from tqdm import tqdm
from huggingface_hub import list_repo_files

# 询问用户存储库用户名和模型名
repo_user = input("Enter the repository user name: ")
model_name = input("Which model do you want to download? ")

# 存储库名称
repo_name = f"{repo_user}/{model_name}"

# 获取存储库中的所有文件
repo_files = list_repo_files(repo_name)

# 检查是否获取到了文件
if not repo_files:
    print(f"No files found in the repository {repo_name}.")
else:
    # 创建一个目录来存储下载的文件
    os.makedirs(repo_name, exist_ok=True)

    # 遍历每个文件并下载
    for file_path in tqdm(repo_files, desc="Downloading files"):
        # 构造下载URL
        download_url = f"https://huggingface.co/{repo_name}/resolve/main/{file_path}"
        
        # 发送GET请求以下载文件
        response = requests.get(download_url, stream=True)
        
        # 处理请求错误
        if response.status_code != 200:
            print(f"Error downloading {file_path}: {response.status_code}")
            continue
        
        # 构造本地文件路径
        local_path = os.path.join(repo_name, file_path)
        
        # 创建必要的目录
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        # 下载文件
        with open(local_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    file.write(chunk)
        
        # 输出下载进度
        print(f"Downloaded {file_path}")
