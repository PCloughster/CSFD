import os, shutil, time

repo_name = "CSFD-test-repo"
git_repo = "https://github.com/PCloughster/CSFD-test-repo"

try:
    shutil.rmtree(repo_name)
    print("Directory already exists, removing") 
except:
    print("Directory doesn't exist, proceeding") 

os.mkdir(repo_name)
os.chdir(repo_name)
os.system("touch test")
os.system("git init")
os.system("git clone "+git_repo)


os.chdir("..")
shutil.rmtree(repo_name)