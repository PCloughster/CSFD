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

def detectrequirements(repo_name, git_repo):
    laravel = False
    react = False
    codeigniter = False
    try:
        shutil.rmtree(repo_name)
        print("Directory already exists, removing") 
    except:
        print("Directory doesn't exist, proceeding") 

    os.mkdir(repo_name)
    os.chdir(repo_name)
    status = os.system("git init")
    if status == 0:
        status = os.system("git clone "+git_repo)
        if status != 0:
            os.chdir("..")
            shutil.rmtree(repo_name)
            return "ERROR: git repo, "+git_repo+" inaccessible"
    else:
        os.chdir("..")
        shutil.rmtree(repo_name)
        return "ERROR: git not present on system"
    fileList = list_files_recursive('./')
    extDict = {}



    for file in fileList:
        if "artisan" in file:
            with open(file) as f:
                if 'LARAVEL_START' in f.read():
                    laravel = True
        elif "package.json" in file:
            with open(file) as f:
                if 'react' in f.read():
                    react = True
        elif "env" in file:
            with open(file) as f:
                if 'CI_ENVIRONMENT' in f.read():
                    codeigniter = True
        file = file.split(".")
        file = list(filter(None, file))[-1]
        extDict[file] = extDict.get(file,0)+1

    os.chdir("..")
    shutil.rmtree(repo_name)

    if react:
        return "react_proj"
    elif laravel:
        return "laravel_proj"
    elif codeigniter:
        return "ci_proj"
    elif "php" in extDict:
        return "php_proj"
    else:
        return "html_proj"