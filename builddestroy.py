from tkinter import *
import json
import os
import detectrequirements

def buildvm(awsKeyInput, applicationDomainInput, gitRepoInput, subnetidInput, selectedZone):
    repo_list = gitRepoInput.split("/")
    repo_name = list(filter(None, repo_list))[-1]
    git_repo = gitRepoInput
    template_id = detectrequirements.detectrequirements(repo_name, git_repo)
    if 'ERROR' in template_id:
        return template_id
    
    if selectedZone == "default (eu-west-2)":
        selectedZone = "eu-west-2"
    
    tfvars = {
        "aws_key": awsKeyInput,
        "application_domain": applicationDomainInput,
        "git_repo": git_repo,
        "git_repo_name": repo_name,
        "subnet_id": subnetidInput,
        "aws_region": selectedZone,
        "template_id": template_id
    }

    tfvars_json_object = json.dumps(tfvars, indent=4)
    with open("data.tfvars.json", "w") as outfile:
        outfile.write(tfvars_json_object)

    status = os.system("/usr/local/bin/terraform init")
    if status == 0:
        status = os.system("/usr/local/bin/terraform apply -var-file=\"data.tfvars.json\" -auto-approve")
        if status != 0:
            return ("ERROR: terraform failed apply changes, please see log file")
        else:
            return ("SUCCESS: terraform successfully applied, further information available in log file")
    else:
        return ("ERROR: terraform failed to initiate, please see log file")
    
    tfvars = {}

def destroyvm():
    status = os.system("/usr/local/bin/terraform destroy -auto-approve")
    if status == 0:
        return ("SUCCESS: terrafrom destroy successful, further information available in log file")
    else:
        return ("ERROR: terraform destroy unsuccessful, please see log file")