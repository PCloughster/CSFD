import tkinter as tk
from tkinter import *
import json
import os
import detectrequirements
import subprocess

def buildvm():
    repo_list = gitRepoInput.get().split("/")
    repo_name = list(filter(None, repo_list))[-1]
    git_repo = gitRepoInput.get()
    template_id = detectrequirements.detectrequirements(repo_name, git_repo)
    
    if selectedZone.get() == "default (eu-west-2)":
        awsZone = "eu-west-2"
    else:
        awsZone = selectedZone.get()
    
    tfvars = {
        "aws_key": awsKeyInput.get(),
        "application_domain": applicationDomainInput.get(),
        "git_repo": git_repo,
        "git_repo_name": repo_name,
        "subnet_id": subnetidInput.get(),
        "template_id": template_id
    }
    print("aws Zone:"+awsZone)

    tfvars_json_object = json.dumps(tfvars, indent=4)
    with open("data.tfvars.json", "w") as outfile:
        outfile.write(tfvars_json_object)
  
    

    os.system("/usr/local/bin/terraform init")
    # TODO - add validation which shows the user the plan as well as a console to the gui
    # terraformPlan = subprocess.check_output(["/usr/local/bin/terraform", "plan", "-var-file=data.tfvars.json"])
    # terraformPlan = terraformPlan.split(b"\\n")
    # terraformOutput = []
    # for line in terraformPlan:
    #     if b"#" in line:
    #         terraformOutput.append(line)
    #     elif b"Plan:" in line:
    #         terraformOutput.append(line)
    # for line in terraformOutput:
    #     print(line)

    os.system("/usr/local/bin/terraform apply -var-file=\"data.tfvars.json\" -auto-approve")

    tfvars = {}
    awsZone.set("")    
    awsKeyInput.set("")
    applicationDomainInput.set("")
    gitRepoInput.set("")
    subnetidInput.set("")

def destroyvm():
    os.system("terraform destroy -auto-approve")
    # TODO - add validation which shows the user the destroy plan before getting them to confirm

def open_popup(popup_text):
   top= Toplevel(win)
   top.geometry("100x100")
   top.title("Continue?")
   Label(top, text= popup_text).place(x=150,y=80)

root=tk.Tk()
root.geometry("550x100")

awsKeyInput=tk.StringVar()
applicationDomainInput=tk.StringVar()
gitRepoInput=tk.StringVar()
subnetidInput=tk.StringVar()

#TODO - add dropdown for supported project or an auto detect checkbox which greys this out
AWSzones = [ 
    "default (eu-west-2)",
    "eu-west-1",
    "eu-west-2",
    "eu-south-1", 
    "eu-north-1", 
    "eu-central-2", 
    "us-west-1", 
    "us-east-1", 
    "me-central-1",
    "me-south-1",
    "af-south-1", 
    "ap-east-1", 
    "ap-south-1", 
    "sa-east-1"
]

selectedZone = StringVar()
selectedZone.set("default (eu-west-2)") 

key_label = tk.Label(root, text = 'AWS Key Pair Name*', font=('calibre',10, 'bold'))
key_entry = tk.Entry(root,textvariable = awsKeyInput, font=('calibre',10,'normal'))

domain_label = tk.Label(root, text = 'Application Domain*', font = ('calibre',10,'bold'))
domain_entry =tk.Entry(root, textvariable = applicationDomainInput, font = ('calibre',10,'normal'))

repo_label = tk.Label(root, text = 'Git repo link*', font=('calibre',10, 'bold'))
repo_entry = tk.Entry(root,textvariable = gitRepoInput, font=('calibre',10,'normal'))

subnet_label = tk.Label(root, text = 'AWS subnet id*', font=('calibre',10, 'bold'))
subnet_entry = tk.Entry(root,textvariable = subnetidInput, font=('calibre',10,'normal'))

awsRegion_label = tk.Label(root, text = 'AWS region', font=('calibre',10, 'bold'))
awsRegion_drop = OptionMenu( root , selectedZone , *AWSzones ) 

build_btn=tk.Button(root,text = 'Build VM', command = buildvm)
destroy_btn=tk.Button(root,text = 'Destroy VM', command = destroyvm)

key_label.grid(row=0,column=0)
key_entry.grid(row=0,column=1)
domain_label.grid(row=0,column=2)
domain_entry.grid(row=0,column=3)
repo_label.grid(row=1,column=0)
repo_entry.grid(row=1,column=1)
subnet_label.grid(row=1,column=2)
subnet_entry.grid(row=1,column=3)
awsRegion_label.grid(row=2, column=0)
awsRegion_drop.grid(row=2, column=1)
build_btn.grid(row=2,column=2)
destroy_btn.grid(row=2,column=3)
root.mainloop()


