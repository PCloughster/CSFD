import tkinter as tk
import json
import os

def buildvm():
    repo_list = gitRepoInput.get().split("/")
    repo_name = list(filter(None, repo_list))[-1]

    tfvars = {
        "aws_key": awsKeyInput.get(),
        "application_domain": applicationDomainInput.get(),
        "git_repo": gitRepoInput.get(),
        "git_repo_name": repo_name,
        "subnet_id": subnetidInput.get()
    }

    tfvars_json_object = json.dumps(tfvars, indent=4)
    with open("data.tfvars.json", "w") as outfile:
        outfile.write(tfvars_json_object)
  
    os.system("terraform init")
    # TODO - add validation which shows the user the plan as well as a console to the gui
    os.system("terraform apply -var-file=\"data.tfvars.json\" -auto-approve")
    
    awsKeyInput.set("")
    applicationDomainInput.set("")
    gitRepoInput.set("")
    subnetidInput.set("")

def destroyvm():
    os.system("terraform destroy -auto-approve")
    # TODO - add validation which shows the user the destroy plan before getting them to confirm

root=tk.Tk()
root.geometry("550x100")

awsKeyInput=tk.StringVar()
applicationDomainInput=tk.StringVar()
gitRepoInput=tk.StringVar()
subnetidInput=tk.StringVar()

#TODO - add dropdown for supported project or an auto detect checkbox which greys this out

key_label = tk.Label(root, text = 'AWS Key Pair Name*', font=('calibre',10, 'bold'))
key_entry = tk.Entry(root,textvariable = awsKeyInput, font=('calibre',10,'normal'))

domain_label = tk.Label(root, text = 'Application Domain*', font = ('calibre',10,'bold'))
domain_entry =tk.Entry(root, textvariable = applicationDomainInput, font = ('calibre',10,'normal'))

repo_label = tk.Label(root, text = 'Git repo link*', font=('calibre',10, 'bold'))
repo_entry = tk.Entry(root,textvariable = gitRepoInput, font=('calibre',10,'normal'))

subnet_label = tk.Label(root, text = 'AWS subnet id*', font=('calibre',10, 'bold'))
subnet_entry = tk.Entry(root,textvariable = subnetidInput, font=('calibre',10,'normal'))

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
build_btn.grid(row=2,column=1)
destroy_btn.grid(row=2,column=3)
root.mainloop()


