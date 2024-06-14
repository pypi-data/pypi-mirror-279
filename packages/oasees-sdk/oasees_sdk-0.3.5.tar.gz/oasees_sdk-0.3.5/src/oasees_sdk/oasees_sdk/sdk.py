import sys
from web3 import Web3
from dotenv import load_dotenv
import ipfshttpclient
import json
import requests
import yaml
import os
import json
import subprocess
import shutil
import zipfile



from kubernetes import client, config
from kubernetes.client import ApiException
from .deploy_pipeline import create_job, create_load_job
from .cluster_ipfs_upload import assets_to_ipfs
from .training_workload import deploy_workload

template = {
    "cells": [
        {
            "cell_type": "markdown",
            "id": "0e70ec26",
            "metadata": {},
            "source": [
                "## Imports"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "id": "5605ba05",
            "metadata": {},
            "outputs": [],
            "source": [
                "from oasees_loggers import setup_logger"
            ]
        },
        {
            "cell_type": "markdown",
            "id": "f66d45a6",
            "metadata": {},
            "source": [
                "## Load Data"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "id": "3eeedb6c",
            "metadata": {},
            "outputs": [],
            "source": []
        },
        {
            "cell_type": "markdown",
            "id": "615b19a0",
            "metadata": {},
            "source": [
                "## Model Definition"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "id": "3eeedb6c",
            "metadata": {},
            "outputs": [],
            "source": []
        },
        {
            "cell_type": "markdown",
            "id": "615b19a0",
            "metadata": {},
            "source": [
                "## Model Parameters As Functions"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "id": "7d1e1722",
            "metadata": {},
            "outputs": [],
            "source": []
        },
        {
            "cell_type": "markdown",
            "id": "003262e7",
            "metadata": {},
            "source": [
                "## Training Model And Export"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "id": "2da0e77d",
            "metadata": {},
            "outputs": [],
            "source": [
                "training_logger = setup_logger('training_logger', 'assets/training_output.log')\n",
                "#Make sure to export the model to assets/model.pth"
            ]
        },
        {
            "cell_type": "markdown",
            "id": "36907aba",
            "metadata": {},
            "source": [
                "## Testing Model"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "id": "fad80187",
            "metadata": {},
            "outputs": [],
            "source": [
                "testing_logger = setup_logger('testing_logger', 'assets/testing_output.log')"
            ]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3 (ipykernel)",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.10.12"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

logger_template = '''import logging

def setup_logger(name, log_file, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    file_handler = logging.FileHandler(log_file)
    console_handler = logging.StreamHandler()

    file_handler.setLevel(level)
    console_handler.setLevel(level)

    formatter = logging.Formatter('%(asctime)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
'''


load_dotenv()
__IPFS_HOST = os.getenv('IPFS_HOST')
__BLOCK_CHAIN_IP = os.getenv('BLOCK_CHAIN_IP')
__ACCOUNT_ADDRESS = os.getenv('ACCOUNT_ADDRESS')

if(__ACCOUNT_ADDRESS):
    __ACCOUNT_ADDRESS = Web3.to_checksum_address(str(__ACCOUNT_ADDRESS))


###### INITIALIZE THE CONNECTIONS TO THE SERVICES AND CONTRACTS INVOLVED ######

__web3 = Web3(Web3.HTTPProvider(f"http://{__BLOCK_CHAIN_IP}:8545"))                    # BLOCKCHAIN
__response = requests.get(f'http://{__IPFS_HOST}:6001/ipfs_portal_contracts')
__data = __response.json()
__ipfs_json = __data['portal_contracts']


__nft_abi = __ipfs_json['nft_abi']             
__nft_address = __ipfs_json['nft_address']
__marketplace_abi = __ipfs_json['marketplace_abi']
__marketplace_address = __ipfs_json['marketplace_address']


__nft = __web3.eth.contract(address=__nft_address, abi=__nft_abi)                           # NFT contract
__marketplace = __web3.eth.contract(address=__marketplace_address, 
                                    abi=__marketplace_abi)                            # Marketplace contract





def __getPurchases():
    if (__ACCOUNT_ADDRESS):

        client = ipfshttpclient.connect(f"/ip4/{__IPFS_HOST}/tcp/5001")                       # IPFS

        results = __marketplace.caller({'from': __ACCOUNT_ADDRESS}).getMyNfts()
        purchases=[]

        for r in results:
            token_id = r[1]
            content_hash = __nft.functions.tokenURI(token_id).call()
            metadata_hash = r[5]

            

            metadata = client.cat(metadata_hash)
            metadata = metadata.decode("UTF-8")
            metadata = json.loads(json.loads(metadata))

            purchases.append({'contentURI': content_hash, 'title':metadata['title']})

        client.close()

        return purchases


def __getDevices():
    results = __marketplace.caller({'from': __ACCOUNT_ADDRESS}).getMyDevices()
    devices = []

    client = ipfshttpclient.connect(f"/ip4/{__IPFS_HOST}/tcp/5001")  

    for r in results:
        token_id = r[1]
        content_hash = __nft.functions.tokenURI(token_id).call()

        content = client.cat(content_hash)
        content = content.decode("UTF-8")
        content = json.loads(content)
        
        devices.append({'name': content['name'], 'endpoint':content['device_endpoint'][7:]})
    
    client.close()
    
    return devices

def __clusterJoined():
    results = __marketplace.caller({'from':__ACCOUNT_ADDRESS}).getJoinedDaos()
    clusterJoined = False

    client = ipfshttpclient.connect(f"/ip4/{__IPFS_HOST}/tcp/5001")  
    for r in results:
        if(r[6]):
            clusterJoined = True
            break

    client.close()

    return clusterJoined


def __get_config():
    results = __marketplace.caller({'from':__ACCOUNT_ADDRESS}).getJoinedDaos()

    client = ipfshttpclient.connect(f"/ip4/{__IPFS_HOST}/tcp/5001") 
    for r in results:
        if(r[6]):
            token_id = r[5]
            content_hash = __nft.functions.tokenURI(token_id).call()

            content = client.cat(content_hash)
            content = content.decode("UTF-8")
            config = yaml.safe_load(content)

    with open('config', 'w') as f:
        yaml.safe_dump(config,f)

    client.close()


def my_algorithms():
    '''Returns a list with all the algorithms purchased from your account
        on the OASEES Marketplace.''' 

    purchases = __getPurchases()


    print("\nOwned algorithms")
    print("---------------------------------")
    i=1
    if(purchases):
        for purchase in purchases:
            print(str(i) + ") " + purchase['title'])
            i+=1
    
    else:
        print("You have not bought any items from the marketplace yet.")



def my_devices():
    '''Returns a list with all the devices purchased / uploaded from your account
        on the OASEES Marketplace.''' 

    devices = __getDevices()

    print("\nOwned devices")
    print("---------------------------------")
    i=1
    if(devices):
        for device in devices:
            print(str(i) + ") " + device['name'] + " | " + device['endpoint'])
            i+=1
    
    else:
        print("You have not bought any devices from the marketplace yet.")




def deploy_algorithm(algorithm_title:str):
    '''Deploys a purchased algorithm on all your connected devices.

        - algorithm_title: Needs to be provided in "string" form.
    
        e.g. algorithm.py -> deploy_algorithm("algorithm.py")
    '''

    

    purchases = __getPurchases()
    daos = __getDevices()
    found = False
    for purchase in purchases:
        if found:
            break

        if(purchase['title']==algorithm_title):
            found = True
            ipfs_cid = purchase['contentURI']

            if(__clusterJoined()):
                __get_config()

                with open('config', 'r') as f:
                    kube_config = yaml.safe_load(f)

                master_ip = kube_config['clusters'][0]['cluster']['server']
                master_ip = master_ip.split(':')


                ipfs_api_url = "http://{}:5001".format(__IPFS_HOST)
                app_name = algorithm_title
                print(app_name.split(".")[0])
                config.load_kube_config("./config")
                # config.load_kube_config()
                batch_v1 = client.BatchV1Api()
                resp = create_load_job(ipfs_api_url,batch_v1,ipfs_cid, app_name)
                print(resp)


            else:
                print("You aren't a member of any cluster at the moment.")

            
            

    if not found:
        print("The file you requested was not found in your purchases.")



# def deploy_local_file(path:str):
#     '''Deploys the file found in the specified path on all your connected devices.
    
#         - path: -> Needs to be provided in "string" form.
#                 -> Is equal to the filename when the file is located in
#                    the Jupyter Notebook's directory.
    
#         e.g. algorithm.py -> deploy_local_file("algorithm.py")
#     '''

#     devices = __getDevices()
#     file = open(path,"rb")

#     for device in devices:
#         __response= requests.post("http://{}/deploy_file".format(device['endpoint']), files={'file': file})                 
#         print(__response.text)
    
#     file.close()


def build_image(image_folder_path):

    '''Deploys a job on the Kubernetes cluster associated with your blockchain
    account, which builds a container image out of your specified folder.
    The image will then be stored on your master node, and will be available
    for deployment on any of the cluster's nodes specified in your manifest file. 
    
        - image_folder_path: Needs to be providerd in "string" form.

    e.g. DApp_Image_Folder -> build_image("DApp_Image_Folder")

    '''

    __get_config()

    with open('config', 'r') as f:
        kube_config = yaml.safe_load(f)

    master_ip = kube_config['clusters'][0]['cluster']['server']
    master_ip = master_ip.split(':')

    ipfs_api_url = "http://{}:31005".format(master_ip[1][2:])
    directory_path = image_folder_path
    ipfs_cid = assets_to_ipfs(ipfs_api_url, directory_path)
    print(ipfs_cid)
    app_name = directory_path.split('/')[-1].lower()
    print(app_name)
    config.load_kube_config("./config")
    # config.load_kube_config()
    batch_v1 = client.BatchV1Api()
    resp = create_job(batch_v1,ipfs_cid, app_name)
    print(resp)


def deploy_manifest(manifest_file_path):
    '''Deploys all the objects included in your specified manifest file, on the
    Kubernetes cluster associated with your blockchain account.

    - manifest_file_path: Needs to be providerd in "string" form.

    e.g. manifest.yaml -> build_image("manifest.yaml")'''

    __get_config()

    # Load kube config
    config.load_kube_config("./config")

    api_instance = client.CustomObjectsApi()

    try:
        # Read manifest file
        with open(manifest_file_path, 'r') as f:
            manifest_documents = yaml.safe_load_all(f)

            # Iterate over each document and deploy it
            for manifest in manifest_documents:
                try:
                    if manifest['kind'] == 'Service':
                        # Deploy Service
                        api_response = client.CoreV1Api().create_namespaced_service(
                            namespace="default",
                            body=manifest
                        )
                    elif manifest['kind'] == 'Ingress':
                        # Deploy Ingress
                        api_response = client.NetworkingV1Api().create_namespaced_ingress(
                            namespace="default",
                            body=manifest
                        )
                    else:
                        # Deploy other resources
                        api_response = api_instance.create_namespaced_custom_object(
                            group=manifest['apiVersion'].split('/')[0],
                            version=manifest['apiVersion'].split('/')[1],
                            namespace="default",
                            plural=manifest['kind'].lower() + 's',  # Convert resource kind to plural form
                            body=manifest
                        )
                    print("Manifest deployed successfully!")
                except Exception as e:
                    print(f"Error deploying manifest: {e}")
                    print("Problematic manifest:")
                    print(yaml.dump(manifest))  # Print the problematic manifest
    except Exception as e:
        print(f"Error reading manifest file: {e}")



def create_ml_pipeline(filename):
    # Create the directory if it doesn't exist
    if os.path.exists(filename):
        print(f"The ML pipeline '{filename}' already exists")
        return

    os.makedirs(filename, exist_ok=True)
    os.makedirs("{}/assets".format(filename), exist_ok=True)

    # Create the .ipynb file inside the directory
    filepath = os.path.join(filename, filename + ".ipynb")
    with open(filepath, 'w') as f:
        json.dump(template, f, indent=4)  # Use json.dump() for proper JSON formatting
    
    # Create the oasees_loggers.py file inside the directory
    logger_filepath = os.path.join(filename, 'oasees_loggers.py')
    with open(logger_filepath, 'w') as f:
        f.write(logger_template)

    print(f"Oasees ML Template '{filename}' created.")

def convert_to_pipeline(filename):
    notebook_path = os.path.join(filename, f"{filename}.ipynb")
    assets_folder = os.path.join(filename, "assets")
    exported_file_path = os.path.join(filename, "exported.py")
    requirements_file = os.path.join(filename, "requirements.txt")

    if not os.path.isfile(notebook_path):
        raise FileNotFoundError(f"Notebook {notebook_path} not found.")
    

    if os.path.isfile(requirements_file):
        os.remove(requirements_file)

    original_cwd = os.getcwd()
    os.chdir(filename)
    
    try:
        command = ["soorgeon", "refactor", f"{filename}.ipynb"]
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print(f"ML pipeline '{filename}' created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running soorgeon refactor: {e.stderr}")
        raise
    finally:
        os.chdir(original_cwd)

    shutil.copy(exported_file_path, os.path.join(assets_folder, "exported.py"))


    if os.path.isfile(requirements_file):
        with open(requirements_file, 'r') as rf:
            lines = rf.readlines()
        with open(requirements_file, 'w') as nf:
            for line in lines:
                if 'ploomber' not in line.lower():
                    nf.write(line)

    shutil.copy(requirements_file, os.path.join(assets_folder, "requirements.txt"))


    try:
        shutil.make_archive(filename, 'zip', original_cwd, filename)
    except Exception as e:
        print(f"Error creating zip archive: {e}")
        raise


def deploy_training_workload(filename,node_name):
    __get_config()

    with open('config', 'r') as f:
        kube_config = yaml.safe_load(f)

    master_ip = kube_config['clusters'][0]['cluster']['server']
    master_ip = master_ip.split(':')

    ipfs_api_url = "http://{}:31005/api/v0/add".format(master_ip[1][2:])

    deploy_workload(filename,ipfs_api_url,node_name)


def download_trained_model(filename):
    __get_config()

    with open('config', 'r') as f:
        kube_config = yaml.safe_load(f)

    master_ip = kube_config['clusters'][0]['cluster']['server']
    master_ip = master_ip.split(':')
    master_ip = master_ip[1][2:]

    output_file = f"assets-{filename}.zip"

    url = "http://{}/training-pod-{}/download_assets".format(master_ip,filename.replace("_","-").lower())

    # Perform the GET request to download the file
    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()  # Check if the request was successful
            with open(output_file, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
        print(f"File downloaded successfully and saved as {output_file}")
    except requests.exceptions.RequestException as e:
        print(f"Training is still in progress.")
        return

    try:
        with zipfile.ZipFile(output_file, 'r') as zip_ref:
            # Extract all the contents into the specified directory
            extract_dir = f"assets-{filename}"
            os.makedirs(extract_dir, exist_ok=True)
            zip_ref.extractall(extract_dir)
    except zipfile.BadZipFile as e:
        print(f"Error unzipping the file: {e}")

    # Optionally, remove the downloaded zip file if you don't need it anymore
    if os.path.exists(output_file):
        os.remove(output_file)
        print(f"Downloaded zip file {output_file} has been removed.")

    namespace_name = "{}".format(filename.replace("_","-").lower())
    print(namespace_name)

    config.load_kube_config("./config")
    v1 = client.CoreV1Api()
    # Delete the namespace
    try:
        api_response = v1.delete_namespace(namespace_name)
        print(f"Namespace {namespace_name} deleted successfully.")
    except ApiException as e:
        print(f"Exception when deleting namespace: {e}")

def instructions():
    
    # \033[1m{deploy_algorithm.__name__}\033[0m(algorithm_title: str) \t \t
    #     {deploy_algorithm.__doc__}


    # \033[1m{deploy_local_file.__name__}\033[0m(path: str) \t   \t
    #     {deploy_local_file.__doc__}

    text = (f'''
    \033[1m{my_algorithms.__name__}\033[0m() \t\t
        {my_algorithms.__doc__}


    \033[1m{my_devices.__name__}\033[0m() \t   \t
        {my_devices.__doc__}
    
        
    \033[1m{build_image.__name__}\033[0m() \t  \t
        {build_image.__doc__}

        
    \033[1m{deploy_manifest.__name__}\033[0m() \t      \t
        {deploy_manifest.__doc__}

        
    \033[1m{instructions.__name__}\033[0m() \t \t
        Reprints the above documentation.
        ''')
    
    __print_msg_box(text,title="\033[1mOASEES SDK methods\033[0m \t \t")

 
def __print_msg_box(msg, indent=1, width=None, title=None):
    """Print message-box with optional title."""
    lines = msg.split('\n')
    space = " " * indent
    if not width:
        width = max(map(len, lines))
    box = f'╔{"═" * (width + indent * 2)}╗\n'  # upper_border
    if title:
        box += f'║{space}{title:<{width}}{space}║\n'  # title
        box += f'║{space}{"-" * len(title):<{width}}{space}║\n'  # underscore
    box += ''.join([f'║{space}{line:<{width}}{space}║\n' for line in lines])
    box += f'╚{"═" * (width + indent * 2)}╝'  # lower_border
    print(box)

instructions()