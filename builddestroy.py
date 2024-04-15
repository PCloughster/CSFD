from tkinter import *
import json
import os
import detectrequirements

def buildvm(awsKeyInput, applicationDomainInput, gitRepoInput, subnetidInput, selectedZone):
    repo_list = gitRepoInput.split("/")
    repo_name = list(filter(None, repo_list))[-1]
    git_repo = gitRepoInput
    template_id = detectrequirements.detectrequirements(repo_name, git_repo)
    
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

    os.system("/usr/local/bin/terraform init")
    os.system("/usr/local/bin/terraform apply -var-file=\"data.tfvars.json\" -auto-approve")

    tfvars = {}

def destroyvm():
    os.system("/usr/local/bin/terraform destroy -auto-approve")