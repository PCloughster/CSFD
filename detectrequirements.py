import os, shutil

def list_files_recursive(path='.', fileList=[]):
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            if ".git" not in full_path: 
                list_files_recursive(full_path, fileList)
        else:
            fileList.append(full_path)
    return fileList

repo_name = "CSFD-test-repo"
git_repo = "https://github.com/PCloughster/CSFD-test-repo"

try:
    shutil.rmtree(repo_name)
    print("Directory already exists, removing") 
except:
    print("Directory doesn't exist, proceeding") 

os.mkdir(repo_name)
os.chdir(repo_name)
os.system("git init")
os.system("git clone "+git_repo)
fileList = list_files_recursive('./')
extDict = {}
for file in fileList:
    file = file.split(".")
    file = list(filter(None, file))[-1]
    extDict[file] = extDict.get(file,0)+1
print(extDict)

os.chdir("..")
shutil.rmtree(repo_name)