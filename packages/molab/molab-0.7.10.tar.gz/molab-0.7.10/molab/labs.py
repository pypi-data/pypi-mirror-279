import json, urllib3, requests, pkgutil, time, boto3
from concurrent.futures import as_completed, ThreadPoolExecutor
from requests_futures.sessions import FuturesSession
from loguru import logger
from .tools import get_class_lab_instance_type, get_class_layout_id, get_morpheus_terraform_plan_id, get_instance_provisioning_payload, get_instance, get_morpheus_terraform_inputs
from .helpers import _add_git_integration_pat_auth, _validate_url, _add_manual_option_list, _add_input, _add_select_input, _add_python_task, _add_operational_workflow, _add_workflow_catalog_item, _add_catalog_logo

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class newClass():
    def __init__(self,url,headers,instance_map,instance_name):
        self.url = url
        self.headers = headers
        self.instance_map = instance_map
        self.instanceName = instance_name
        self.instance_id = ""
        self.class_name = self.instance_map["customOptions"]["class_name"]
        self.custom_options = self.instance_map["customOptions"]
        self.templateParameters = get_morpheus_terraform_inputs(self.custom_options)
        self.templateParameters["lab_name"] = self.instanceName.split("-")[-1]
        self.templateParameters["master_region"] = self.instance_map["customOptions"]["trainingZone"].split(",")[0]
        self.templateParameters["labs_region"] = self.instance_map["customOptions"]["trainingZone"].split(",")[1]
        self.instance_type = get_class_lab_instance_type(self.url,self.headers,f'ilt{self.instance_map["customOptions"]["class_name"][0:3]}')
        self.instance_layout_id = get_class_layout_id(self.url,self.headers,self.custom_options,self.instance_type)
        self.terraform_plan_id = get_morpheus_terraform_plan_id(self.url,self.headers)
        self.deploy_payload = get_instance_provisioning_payload(
            class_version=self.custom_options["class_version"],
            zone_id=self.instance_map["input"]["zoneId"],
            instance_name=self.instanceName,
            site_id=self.instance_map["input"]["site"]["id"],
            instance_type=self.instance_type["code"],
            instance_type_code=self.instance_type["code"],
            layout_id=self.instance_layout_id,
            plan_id=self.terraform_plan_id,
            template_parameters=self.templateParameters,
            )
        
    def deploy(self):
        try:
            logger.info(f'Attempting to deploy the instance: {self.instanceName}')
            resp = requests.post(f'{self.url}/api/instances',headers=self.headers,json=self.deploy_payload,verify=False)
        except Exception as e:
            logger.error(e)
        if "200" in str(resp):
            logger.info(f'Instance {self.instanceName} deployment successfully triggered...')
            self.instance_id = resp.json()["instance"]["id"]
            return(resp.text)
        elif "504" in str(resp):
            logger.info(f'Received a gateway timeout.')
            logger.info(f'Instance {self.instanceName} deployment possibly triggered...')
            self.instance_id = ""
            return(resp.text)
        else:
            logger.error(f'Something went wrong: {resp.json()}')
            return(resp.text)

    def status(self):
        counter = 0
        max_counter = 20
        logger.info(f'Checking the deployment status of the instance: {self.instanceName}')
        while counter < max_counter:
            if self.instance_id == "":
                logger.info(f'Instance ID not found. Attempting to get it via the instance name...')
                try:
                    resp = requests.get(f'{self.url}/api/instances/?name={self.instanceName}',headers=self.headers,verify=False)
                    counter += 1
                except Exception as e:
                    logger.error(f'Something went wrong: {e}')
                if "200" in str(resp):
                    logger.info(f'Instance {self.instanceName} instance found. Setting the ID to {resp.json()["instances"][0]["id"]}')
                    self.instance_id = resp.json()["instances"][0]["id"]
            else:
                logger.info(f'Instance ID found for instance {self.instanceName}. Checking status...')
                try:
                    resp = requests.get(f'{self.url}/api/instances/{self.instance_id}',headers=self.headers,verify=False)
                    counter += 1
                except Exception as e:
                    logger.error(f'Something went wrong: {e}')
                if "200" in str(resp):
                    logger.info(f'Status: {resp.json()["instance"]["status"]}')
                    if resp.json()["instance"]["status"] == "provisioning":
                        logger.info(f'Instance {self.instanceName} is still provisioning. Waiting 60 seconds and checking again...')
                        self.status = resp.json()["instance"]["status"]
                        time.sleep(60)
                    elif resp.json()["instance"]["status"] == "running":
                        logger.info(f'Instance {self.instanceName} is running. Continuing...')
                        self.status = resp.json()["instance"]["status"]
                        return
                    else:
                        logger.error(f'Unexpected status: {resp.json()["instance"]["status"]}')
                        self.status = resp.json()["instance"]["status"]
                        return
                else:
                    logger.error(f'Something went wrong: {resp.json()}')
                    return(resp.json())

    def lock(self):
        try:
            logger.info(f'Attempting to lock the instance: {self.instanceName}')
            resp = requests.put(f'{self.url}/api/instances/{self.instance_id}/lock',headers=self.headers,verify=False)
        except Exception as e:
            logger.error(f'Something went wrong: {e}')
        if "200" in str(resp):
            logger.info(f'Instance {self.instanceName} locked successfully.')
        else:
            logger.error(f'Something went wrong: {resp.json()}')
            return(resp.json())
        
    def get_lab_data(self):
        self.lab_data = {}
        try:
            logger.info(f'Attempting to get the lab info for the instance: {self.instanceName}')
            resp = requests.get(f'{self.url}/api/instances/{self.instance_id}/state',headers=self.headers,verify=False)
        except Exception as e:
            logger.error(f'Something went wrong: {e}')
        if "200" in str(resp):
            logger.info(f'Lab info for instance {self.instanceName} found.')
            if "administration" in self.class_name:
                logger.info(f'Class type: Administration')
                self.lab_data["lab_name"] = [i["value"] for i in resp.json()["input"]["variables"] if i["name"] == "lab_name"][0]
                self.lab_data["region"] = [i["value"] for i in resp.json()["input"]["variables"] if i["name"] == "labs_region"][0]
                self.lab_data["morpheus_external_ip"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "morpheus_external_ip"][0]
                self.lab_data["morpheus_internal_ip"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "morpheus_internal_ip"][0]
                self.lab_data["morpheus_url"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "morpheus_url"][0]
                self.lab_data["rocky_ami"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "rocky_ami"][0]
                self.lab_data["ubuntu_ami"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "ubuntu_ami"][0]
                self.lab_data["centos_7_ami"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "centos_7_ami"][0]
                self.lab_data["iam_key"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "iam_key"][0]
                self.lab_data["iam_secret"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "iam_secret"][0]
                self.lab_data["mega_vpc_id"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "mega_vpc_id"][0]
                self.lab_data["shared_vpc_id"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "shared_vpc_id"][0]
                return
            elif "automation" in self.class_name:
                logger.info(f'Class type: Automation')
                self.lab_data["lab_name"] = [i["value"] for i in resp.json()["input"]["variables"] if i["name"] == "lab_name"][0]
                self.lab_data["region"] = [i["value"] for i in resp.json()["input"]["variables"] if i["name"] == "labs_region"][0]
                self.lab_data["morpheus_external_ip"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "morpheus_external_ip"][0]
                self.lab_data["morpheus_internal_ip"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "morpheus_internal_ip"][0]
                self.lab_data["morpheus_url"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "morpheus_url"][0]
                self.lab_data["rocky_ami"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "rocky_ami"][0]
                self.lab_data["ubuntu_ami"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "ubuntu_ami"][0]
                self.lab_data["centos_7_ami"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "centos_7_ami"][0]
                self.lab_data["iam_key"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "iam_key"][0]
                self.lab_data["iam_secret"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "iam_secret"][0]
                self.lab_data["vpc_id"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "lab_vpc_id"][0]
                return
            elif "installation" in self.class_name:
                logger.info(f'Class type: Installation')
                self.lab_data["lab_name"] = [i["value"] for i in resp.json()["input"]["variables"] if i["name"] == "lab_name"][0]
                self.lab_data["region"] = [i["value"] for i in resp.json()["input"]["variables"] if i["name"] == "labs_region"][0]
                self.lab_data["morpheus_aio_url"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "morpheus_aio_url"][0]
                self.lab_data["cluster_url"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "cluster_url"][0]
                self.lab_data["iam_key"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "iam_key"][0]
                self.lab_data["iam_secret"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "iam_secret"][0]
                self.lab_data["vpc_id"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "lab_vpc_id"][0]
                self.lab_data["morpheus_aio_external_ip"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "morpheus_aio_external_ip"][0]
                self.lab_data["morpheus_aio_internal_ip"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "morpheus_aio_internal_ip"][0]
                self.lab_data["app_node_1_internal_ip"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "app_node_1_internal_ip"][0]
                self.lab_data["app_node_2_internal_ip"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "app_node_2_internal_ip"][0]
                self.lab_data["app_node_3_internal_ip"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "app_node_3_internal_ip"][0]
                # self.lab_data["app_node_4_internal_ip"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "app_node_4_internal_ip"][0]
                self.lab_data["app_node_1_external_ip"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "app_node_1_external_ip"][0]
                self.lab_data["app_node_2_external_ip"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "app_node_2_external_ip"][0]
                self.lab_data["app_node_3_external_ip"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "app_node_3_external_ip"][0]
                # self.lab_data["app_node_4_external_ip"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "app_node_4_external_ip"][0]
                self.lab_data["db_node_1_internal_ip"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "db_node_1_internal_ip"][0]
                self.lab_data["db_node_2_internal_ip"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "db_node_2_internal_ip"][0]
                self.lab_data["db_node_3_internal_ip"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "db_node_3_internal_ip"][0]
                self.lab_data["db_node_1_external_ip"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "db_node_1_external_ip"][0]
                self.lab_data["db_node_2_external_ip"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "db_node_2_external_ip"][0]
                self.lab_data["db_node_3_external_ip"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "db_node_3_external_ip"][0]
                # self.lab_data["db_endpoint"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "db_endpoint"][0]
                # self.lab_data["rds_endpoint"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "rds_endpoint"][0]
                # self.lab_data["rds_user"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "rds_user"][0]
                # self.lab_data["rds_password"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "rds_password"][0]
                return
        else:
            logger.error(f'Something went wrong: {resp.json()}')
            return(resp.json())

class existingClass():
    def __init__(self,url,headers,instance_map) :
        self.url = url
        self.headers = headers
        self.instance_map = instance_map

    def show(self):
        logger.info(f'Instance map:')
        print(json.dumps(self.instance_map, indent = 4))

    def unlock(self):
        for lab in self.instance_map["attributes"]["labs"]:
            try:
                logger.info(f'Attempting to unlock the instance: {lab["lab_name"]}')
                resp = requests.put(f'{self.url}/api/instances/{lab["instance_id"]}/unlock',headers=self.headers,verify=False)
            except Exception as e:
                logger.error(f'Something went wrong: {e}')
            if "200" in str(resp):
                logger.info(f'Instance {lab["lab_name"]} unlocked successfully.')
            else:
                logger.error(f'Something went wrong: {resp.json()}')
                return(resp.json())


    def delete(self):
        for lab in self.instance_map["attributes"]["labs"]:
            try:
                logger.info(f'Attempting to delete the instance: {lab["lab_name"]}')
                resp = requests.delete(f'{self.url}/api/instances/{lab["instance_id"]}',headers=self.headers,verify=False)
            except Exception as e:
                logger.error(f'Something went wrong: {e}')
            if "200" in str(resp):
                logger.info(f'Instance {lab["lab_name"]} delete initiated successfully.')
                tries = 0
                maxTries = 10
                while tries < maxTries:
                    try:
                        tries += 1
                        ins = get_instance(self.url,self.headers,lab["instance_id"])
                    except Exception as e:
                        logger.error(f'Something went wrong: {e}')
                    if ins["status"] == "removing":
                        logger.info(f'Instance {lab["lab_name"]} still removing.')
                        logger.info(f'Waiting 60 seconds and checking again...')
                        time.sleep(60)
                        break
                    elif ins["status"] == "stopped":
                        logger.info(f'Instance {lab["lab_name"]} stopped but not yet deleted')
                        logger.info(f'Waiting 60 seconds and checking again...')
                        time.sleep(60)
                    elif "Instance not found" in str(ins):
                        logger.info(f'Instance not found. Assuming it is gone....')
                        self.instance_map["attributes"]["labs"].remove(lab)
                        return(self.instance_map)
                logger.info(f'Instance {lab["lab_name"]} not gone after 10 minutes. You may need to check on this')
            else:
                logger.error(f'Something went wrong: {resp.json()}')
                return(resp.json())

    def get_lab_data(self):
        self.lab_data = {}
        try:
            logger.info(f'Attempting to get the lab info for the instance: {self.instanceName}')
            resp = requests.get(f'{self.url}/api/instances/{self.instance_id}/state',headers=self.headers,verify=False)
        except Exception as e:
            logger.error(f'Something went wrong: {e}')
        if "200" in str(resp):
            logger.info(f'Lab info for instance {self.instanceName} found.')
            self.lab_data["lab_name"] = [i["value"] for i in resp.json()["input"]["variables"] if i["name"] == "lab_name"][0]
            self.lab_data["region"] = [i["value"] for i in resp.json()["input"]["variables"] if i["name"] == "labs_region"][0]
            self.lab_data["morpheus_external_ip"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "morpheus_external_ip"][0]
            self.lab_data["morpheus_internal_ip"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "morpheus_internal_ip"][0]
            self.lab_data["morpheus_url"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "morpheus_url"][0]
            self.lab_data["rocky_ami"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "rocky_ami"][0]
            self.lab_data["ubuntu_ami"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "ubuntu_ami"][0]
            self.lab_data["iam_key"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "iam_key"][0]
            self.lab_data["iam_secret"] = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "iam_secret"][0]
            return
        else:
            logger.error(f'Something went wrong: {resp.json()}')
            return(resp.json())

class existingLab():
    def __init__(self,lab_map) -> None:
        self.lab_map = lab_map
        self.url = self.lab_map["morpheus_url"]
        self.user = self.lab_map["ui_user"]
        self.password = self.lab_map["ui_password"]
        self.bearer = get_morpheus_bearer_token(self.url,self.user,self.password)
        self.headers = {'Content-Type': 'application/json',"Accept":"application/json", "Authorization": "BEARER " + self.bearer}

    def setup_admin_class(self):
        appliance_settings_body = {"applianceSettings":{"userBrowserSessionTimeout": "60","userBrowserSessionWarning": "15"}}
        provisioning_settings_body = {"provisioningSettings":{"showPricing": True,"reuseSequence": True,"cloudInitUsername": "morpheusci","cloudInitPassword": "Password123?"}}
        monitoring_settings_body = { "monitoringSettings": { "autoManageChecks": True } }
        logging_settings_body = { "logSettings": { "enabled": True } }
        try:
            logger.info(f'Attempting to update appliance settings')
            resp = requests.put(f'{self.url}/api/appliance-settings',headers=self.headers,json=appliance_settings_body,verify=False)
        except Exception as e:
            logger.error(f'Something went wrong: {e}')
        try:
            logger.info(f'Attempting to update provisioning settings')
            resp = requests.put(f'{self.url}/api/provisioning-settings',headers=self.headers,json=provisioning_settings_body,verify=False)
        except Exception as e:
            logger.error(f'Something went wrong: {e}')
        try:
            logger.info(f'Attempting to update monitoring settings')
            resp = requests.put(f'{self.url}/api/monitoring-settings',headers=self.headers,json=monitoring_settings_body,verify=False)
        except Exception as e:
            logger.error(f'Something went wrong: {e}')
        try:
            logger.info(f'Attempting to update logging settings')
            resp = requests.put(f'{self.url}/api/log-settings',headers=self.headers,json=logging_settings_body,verify=False)
        except Exception as e:
            logger.error(f'Something went wrong: {e}')

        logger.info(f'Admin class setup complete')
        
    def setup_automation_class(self,**class_configs):
        logger.info(f'Begin attempt to setup Automation Class on node: {self.url}')
        # Ensure URL is https
        url = _validate_url(self.url)
        # Add the GIT integration
        integration = _add_git_integration_pat_auth(url,self.headers,class_configs["integration_name"],class_configs["git_url"],class_configs["git_branch"],class_configs["git_username"],class_configs["git_pat"])
        logger.info(f'Integration Data: {integration}')
        # Add the manual option list
        option_list_id = _add_manual_option_list(url,self.headers,class_configs["option_list_name"])
        logger.info(f'Option List ID: {option_list_id}')

        ## Create inputs
        input_ids = []
        input_ids.append(_add_input(self.url,self.headers,"AMI - CentOS", "amicentos", "text", "AMI - CentOS", "True"))
        input_ids.append(_add_input(self.url,self.headers,"AMI - Ubuntu", "amiubuntu", "text", "AMI - Ubuntu", "True"))
        input_ids.append(_add_input(self.url,self.headers,"AWS Key", "awsKey", "text", "AWS Key", "True"))
        input_ids.append(_add_input(self.url,self.headers,"AWS Secret", "awsSecret", "text", "AWS Secret", "True"))
        input_ids.append(_add_input(self.url,self.headers,"AWS VPC", "awsVpc", "text", "AWS VPC", "True"))
        input_ids.append(_add_input(self.url,self.headers,"Internal IP", "internalHost", "text", "Internal IP", "True"))
        input_ids.append(_add_select_input(self.url,self.headers,"AWS Regions", "awsRegion", option_list_id, "AWS Region", "True"))

        ## Create "Set Up My Lab" Python Task
        task_id = _add_python_task(self.url,self.headers,"Set Up My Lab", "setupMyLab", "12", "jythonTask", "value", "repository", integration["linked_code_repo_id"], "/setupmylab.py", "", "requests")

        ## Create "Set Up My Lab" Workflow
        workflow_id = _add_operational_workflow(self.url,self.headers,"Set Up My Lab", task_id, input_ids)

        ## Create catalog item
        catalog_id = _add_workflow_catalog_item(self.url,self.headers,"Set Up My Lab", workflow_id)

        ## Add logo
        logo = _add_catalog_logo(self.url,self.headers,catalog_id, "MorpheusImage.png")

class newLab():
    def __init__(self,url,headers,instance_map):
        self.url = url
        self.headers = headers
        self.instance_map = instance_map

    def setup(self):
        pass

class awsEnv():
    def __init__(self,instance_map) :
        self.instance_map = instance_map
        self.region = self.instance_map["attributes"]["labs"][0]["region"]
        access_key = self.instance_map["attributes"]["labs"][0]["iam_key"]
        secret_key = self.instance_map["attributes"]["labs"][0]["iam_secret"]
        self.ec2 = boto3.client('ec2',region_name=self.region,aws_access_key_id=access_key,aws_secret_access_key=secret_key)
        self.s3 = boto3.client('s3',region_name=self.region,aws_access_key_id=access_key,aws_secret_access_key=secret_key)
        self.rds = boto3.client('rds',region_name=self.region,aws_access_key_id=access_key,aws_secret_access_key=secret_key)
   
    def delete_s3_bucket_versions(self,bucket_name, object_versions):
        # Get all object versions
        logger.info(f'Attempting to delete all object versions in the bucket: {bucket_name}')
        versions = object_versions.get('Versions', [])
        if versions:
            delete_keys = {'Objects': [{'Key': version['Key'], 'VersionId': version['VersionId']} for version in versions]}
            try:
                resp = self.s3.delete_objects(Bucket=bucket_name, Delete=delete_keys)
                logger.info(resp)
            except Exception as e:
                logger.error(f'Something went wrong: {e}')
        
    def delete_s3_bucket_delete_markers(self,bucket_name, object_versions):
    # Get all object versions in the bucket's versioning-enabled delete marker
        logger.info(f'Attempting to delete all delete markers in the bucket: {bucket_name}')
        delete_markers = object_versions.get('DeleteMarkers', [])
        if delete_markers:
            # Delete all object versions in the bucket's versioning-enabled delete marker
            delete_marker_keys = {'Objects': [{'Key': marker['Key'], 'VersionId': marker['VersionId']} for marker in delete_markers]}
            try: 
                resp = self.s3.delete_objects(Bucket=bucket_name, Delete=delete_marker_keys)
                logger.info(resp)
            except Exception as e:
                logger.error(f'Something went wrong: {e}')

    def delete_s3_bucket(self,bucket_name):
        # Get all object versions
        logger.info(f'Attempting to delete the S3 bucket: {bucket_name}')
        object_versions = self.s3.list_object_versions(Bucket=bucket_name, MaxKeys=1000)
        while True:
            # Delete all object versions
            self.delete_s3_bucket_versions(bucket_name, object_versions)
            # Delete all delete markers
            self.delete_s3_bucket_delete_markers(bucket_name, object_versions)
            # Check if there are more object versions to delete
            if object_versions.get('IsTruncated'):
                object_versions = self.s3.list_object_versions(Bucket=bucket_name, MaxKeys=1000, KeyMarker=response['NextKeyMarker'], VersionIdMarker=response['NextVersionIdMarker'])
            else:
                break
        # Deleting S3 bucket
        self.s3.delete_bucket(bucket_name)

    def delete_db_instance(self,db_instance_identifier):
        logger.info(f'Attempting to delete the RDS instance: {db_instance_identifier}')
        try:
            self.rds.delete_db_instance(DBInstanceIdentifier=db_instance_identifier, SkipFinalSnapshot=True,DeleteAutomatedBackups=True)
        except Exception as e:
            logger.error(f'Something went wrong: {e}')

    def delete_db_cluster(self,db_cluster_identifier):
        logger.info(f'Attempting to delete the RDS cluster: {db_cluster_identifier}')
        try:
            resp = self.rds.delete_db_cluster(DBClusterIdentifier=db_cluster_identifier, SkipFinalSnapshot=True)
            logger.info(resp)
        except Exception as e:
            logger.error(f'Something went wrong: {e}')

    def terminate_ec2_instance(self,instance_id):
        logger.info(f'Attempting to terminate the EC2 instance: {instance_id}')
        try:
            resp = self.ec2.terminate_instances(InstanceIds=[instance_id])
            logger.info(resp)
        except Exception as e:
            logger.error(f'Something went wrong: {e}')

    def get_rds_clusters(self):
        rds_clusters = self.rds.describe_db_clusters()
        return(rds_clusters)
    
    def get_s3_buckets_in_region(self):
        bucket_list = []
        s3_buckets = self.s3.list_buckets()
        for bucket in s3_buckets["Buckets"]:
            if self.s3.get_bucket_location(Bucket=bucket["Name"])["LocationConstraint"] == self.region:
                bucket_list.append(bucket["Name"])
        return(bucket_list)
    
    def get_ec2_instances(self):
        ec2_instances = self.ec2.describe_instances()
        return(ec2_instances["Reservations"])


def get_morpheus_bearer_token(url,user_name,password):
    """
    The get_morpheus_api_token function is used to get a Morpheus API token.
    It takes three arguments: the URL of the Morpheus appliance, a username and password.
    The function returns an access_token which can be used in subsequent requests.
    
    :param url: Specify the morpheus api instance that is being used
    :param user_name: Specify the username of the user that is used to authenticate with the morpheus api
    :param password: Pass the password to get_morpheus_api_token function
    :return: A token for the user
    :doc-author: Trelent
    """
    if 'https://' not in url:
        url = f'https://{url}'
    endpoint = "/oauth/token?grant_type=password&scope=write&client_id=morph-api"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    body = {"username": user_name, "password": password}
    try:
        logger.info(f'Attempting to get API token')
        resp = requests.post(f'{url}{endpoint}',headers=headers,verify=False,data=body)
    except Exception as e:
        logger.info(f'Something went wrong')
    if "200" in str(resp):
        logger.info("Token acquired")
        token = resp.json()["access_token"]
        return(token)
    elif "400" in str(resp):
        logger.error('Bad credentials')
        return(resp)
    else:
        return(resp)