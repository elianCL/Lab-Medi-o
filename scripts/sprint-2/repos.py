import csv
import shutil
import subprocess
import zipfile
import os
from tqdm import tqdm
from git import Repo
import s2

CSV_FILE_PATH = './scripts/sprint-2/dataset/s2.csv'
CK_JAR_PATH = "../ck/target/ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar"
DATASET_PATH = "./scripts/sprint-2/dataset/"

# def compress_dataset(directory):
#     print("Compressing dataset...")
#     try:
#         with zipfile.ZipFile(os.path.join(directory, 'dataset-zip'), 'w') as zipf:
#             for root, _, files in os.walk(directory):
#                 for file in files:
#                     zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), directory))
#         print("Compression completed successfully!")
#     except Exception as e:
#         print(f"Error compressing dataset: {e}")

def get_repos(csv_file):
    s2.main()
    urls = []
    with open(csv_file, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            repo_url = row[0].split(',')[0]
            urls.append(repo_url)
            # print(repo_url)
    return urls

def download_repo(repo_url, target_dir):
    try:
        Repo.clone_from(repo_url, target_dir)
        print("Repository cloned successfully!")
    except Exception as e:
        print(f"Error cloning repository: {e}")

def analyze(repo_partial_url):
    dir_address = repo_partial_url.replace('/', '-')
    repo_url = "https://github.com/" + repo_partial_url
    download_repo(repo_url, dir_address)
    # target = DATASET_PATH + dir_address + "/aaa"
    target = DATASET_PATH + dir_address + "/"
    os.makedirs(target, exist_ok=True)
    try:
        subprocess.run(["java", "-jar", CK_JAR_PATH, target, "true", "0", "true", target + dir_address])
        print("Analysis completed successfully!")
        print(target)
    except Exception as e:
        print(f"Error analyzing repository: {e}")

    try:
        shutil.rmtree(dir_address)
        print("Repository directory deleted successfully!")
    except Exception as e:
        print(f"Error deleting repository directory: {e}")

urls = get_repos(CSV_FILE_PATH)

for x in tqdm(urls, desc="Processing repositories", unit="repo"):
    analyze(x)

# analyze('yangchong211/YCAppTool')

# compress_dataset(DATASET_PATH)
