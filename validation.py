import re

def validateDomain(domain):
    regex = "^((?!-)[A-Za-z0-9-]" + "{1,63}(?<!-)\\.)" +"+[A-Za-z]{2,6}"
    p = re.compile(regex)
    if(re.search(p, domain)):
        return True
    else:
        return False

def checkGitLink(domain):
    regex = "^(?:(?:https?|git)://)?(?:www\.)?github\.com/.+$"
    p = re.compile(regex)
    if(re.search(p, domain)):
        return True
    else:
        return False