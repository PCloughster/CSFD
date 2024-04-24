from tkinter import *
import json
import os
import detectrequirements
import subprocess
import datetime
import getIP

def buildvm(awsKeyInput, applicationDomainInput, gitRepoInput, subnetidInput, selectedZone):
    repo_list = gitRepoInput.split("/")
    repo_name = list(filter(None, repo_list))[-1]
    git_repo = gitRepoInput
    template_id = detectrequirements.detectrequirements(repo_name, git_repo)
    if 'ERROR' in template_id:
        return template_id
    
    if selectedZone == "default (eu-west-2)":
        selectedZone = "eu-west-2"
    localIP = getIP.getExternalIP()
    
    warning = ""

    if not localIP:
        warning = "WARNING: Unable to whitelist local IP, please follow manual guide."
    
    if applicationDomainInput == "":
        applicationDomainInput = "default_server"

    tfvars = {
        "aws_key": awsKeyInput,
        "application_domain": applicationDomainInput,
        "git_repo": git_repo,
        "git_repo_name": repo_name,
        "subnet_id": subnetidInput,
        "aws_region": selectedZone,
        "template_id": template_id,
        "user_ip": localIP
    }

    tfvars_json_object = json.dumps(tfvars, indent=4)
    with open("data.tfvars.json", "w") as outfile:
        outfile.write(tfvars_json_object)

    status = os.system("/usr/local/bin/terraform init")
    if status == 0:
        currentDatetime = datetime.datetime.now()
        formattedDatetime = currentDatetime.strftime("%Y-%m-%d_%H-%M-%S")
        if not os.path.exists("applyLogs"):
            os.makedirs("applyLogs")
        logName =  f"applyLogs/apply_log_{formattedDatetime}.txt"
        with open(logName, "w") as output_file:
            process = subprocess.Popen(
                ["/usr/local/bin/terraform", "apply", "-var-file=data.tfvars.json", "-auto-approve"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, 
                universal_newlines=True  
            )
            for line in process.stdout:
                if "Apply complete!" in line:
                    successmessage = line
                output_file.write(line)
        status = process.wait()

        #status = os.system("/usr/local/bin/terraform apply -var-file=\"data.tfvars.json\" -auto-approve")
        if status != 0:
            return ("ERROR: terraform failed apply changes, please see log file:\n:"+logName)
        else:
            return ("SUCCESS:"+successmessage+"\n further information available in log file:\n "+logName + warning)
    else:
        return ("ERROR: terraform failed to initiate, please ensure terraform is installed correctly")
    
    tfvars = {}

def destroyvm():
    currentDatetime = datetime.datetime.now()
    formattedDatetime = currentDatetime.strftime("%Y-%m-%d_%H-%M-%S")
    if not os.path.exists("destroyLogs"):
            os.makedirs("destroyLogs")
    logName =  f"destroyLogs/destroyLog_log_{formattedDatetime}.txt"
    
    with open(logName, "w") as output_file:
        process = subprocess.Popen(
            ["/usr/local/bin/terraform", "destroy", "-auto-approve"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, 
            universal_newlines=True  
        )
        for line in process.stdout:
            output_file.write(line)
    status = process.wait()
    #status = os.system("/usr/local/bin/terraform destroy -auto-approve")
    if status == 0:
        return ("SUCCESS: terrafrom destroy successful, further information available in log file:\n" +logName)
    else:
        return ("ERROR: terraform destroy unsuccessful, please see log file:\n" +logName)