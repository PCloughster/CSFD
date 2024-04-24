import tkinter as tk
from tkinter import *
from tkinter import messagebox
import builddestroy
import validation
import webbrowser

if __name__ == "__main__":
    def validateInputs():
        errors = []
        if awsKeyInput.get().strip() == "":
            errors.append("Required Field AWS Key left blank")
        if validation.validateDomain(applicationDomainInput.get()) == False and applicationDomainInput.get() != "":
            errors.append("Invalid domain provided")
        if validation.checkGitLink(gitRepoInput.get()) == False:
            errors.append("Invalid git repository provided")
        if subnetidInput.get().strip() == "":
            errors.append("Required Field Subnet ID left blank")
        if len(errors) == 0:
            return None
        else:
            return errors
    
    def onBuildButton():
        errors = validateInputs()
        if errors != None:
            errormessage = ""
            for error in errors:
                errormessage = errormessage+error+"\n"
            displayMessage(errormessage)
        else:
            response = messagebox.askyesno("Confirmation", "Are you sure you wish to apply terraform with the entered variables?")
            if response:
                runningWin = tk.Toplevel()
                runningWin.geometry("200x40")
                tk.Label(runningWin, text="Terraform applying......").pack()
                runningWin.update()
                returnVar = builddestroy.buildvm(awsKeyInput.get(), applicationDomainInput.get(), gitRepoInput.get(), subnetidInput.get(), selectedZone.get())
                runningWin.destroy()
                if "ERROR" in returnVar:
                    builddestroy.destroyvm()
                displayMessage(returnVar)
    
    def onDestroyButton():
        response = messagebox.askyesno("Confirmation", "Are you sure you wish to destroy all created terraform resources?")
        if response:
            runningWin = tk.Toplevel()
            runningWin.geometry("200x40")
            tk.Label(runningWin, text="Terraform destroying......").pack()
            runningWin.update()
            returnVar = builddestroy.destroyvm()
            runningWin.destroy()
        displayMessage(returnVar)
    def displayMessage(message): 
        tk.messagebox.showinfo("Alert!",  message) 

    def openLink(event):
        webbrowser.open_new(event.widget.cget("text"))

    root=tk.Tk()
    root.title('CSFD')
    root.geometry("570x160")

    awsKeyInput=tk.StringVar()
    applicationDomainInput=tk.StringVar()
    gitRepoInput=tk.StringVar()
    subnetidInput=tk.StringVar()

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

    domain_label = tk.Label(root, text = 'Application Domain', font = ('calibre',10,'bold'))
    domain_entry =tk.Entry(root, textvariable = applicationDomainInput, font = ('calibre',10,'normal'))

    repo_label = tk.Label(root, text = 'Git repo link*', font=('calibre',10, 'bold'))
    repo_entry = tk.Entry(root,textvariable = gitRepoInput, font=('calibre',10,'normal'))

    subnet_label = tk.Label(root, text = 'AWS subnet id*', font=('calibre',10, 'bold'))
    subnet_entry = tk.Entry(root,textvariable = subnetidInput, font=('calibre',10,'normal'))

    awsRegion_label = tk.Label(root, text = 'AWS region', font=('calibre',10, 'bold'))
    awsRegion_drop = OptionMenu( root , selectedZone , *AWSzones ) 

    build_btn = tk.Button(root, text='Build VM', command = onBuildButton)
    destroy_btn=tk.Button(root,text = 'Destroy VM', command = onDestroyButton)
    readme_label = tk.Label(root, text="Once your virtual machine has been setup, please see the readme for the next steps \nand tips on maintaining your environment\n the readme also contains information on creating a key pair and subnet:")
    readme_link = tk.Label(root, text="https://github.com/PCloughster/CSFD/blob/main/README.md", fg="cyan", cursor="target")
    readme_link.bind("<Button-1>", openLink)

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
    readme_label.grid(row=3, columnspan=4)
    readme_link.grid(row=4, columnspan=4)
    root.mainloop()