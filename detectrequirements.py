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
        if "artisan" == file:
            with open(file) as f:
                if 'LARAVEL_START' in f.read():
                    laravel = True
        elif "package.json" in file:
            with open(file) as f:
                if 'react' in f.read():
                    react = True
        file = file.split(".")
        file = list(filter(None, file))[-1]
        extDict[file] = extDict.get(file,0)+1

    os.chdir("..")
    shutil.rmtree(repo_name)

    if react:
        return "react_proj"
    elif laravel:
        return "laravel_proj"
    elif "html" in extDict:
        return "html_proj"
    else:
        return "php_proj"

    # if .lock file exists and required.json exists
    # check what .lock file it is (composer etc) then run the required install statement


    # if extDict only contains html, css and misc, only install an hmtl site
    # check file extensions (php, html, etc)
    # check for lock file, if a lock file present check what file that is
    # check if pip needed
    # check for composer files
    # check for lock files
    # Specify the directory path you want to start from


