# Custom Servers For Developers (CSFD)

CSFD is a python/terraform project designed to automate the process of hosting your github web application project on an AWS EC2 Linux virtual machine.

CSFD provides a gui frontend and after some pre-requisite work in setting up AWS, when provided with your Git repo, domain, AWS key name, and subnet-id will detect what project is being used and configure all services on a virtual machine, the only requirement after setup is to point your DNS to your new IP, and transfer over database content. 

Currently there are 5 different types of projects which are supported by this program:
no framework HTML
no framework PHP
Laravel projects
React projects
Codeigniter projects

## Prerequisites
Currently CSFD has only been tested on OSX and requires the Terraform CLI and AWS CLI along with an AWS account and associated credentials.

Creating your AWS account:
```
https://aws.amazon.com/resources/create-account/
```
Install Terraform CLI:
```
https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli
```
Install AWS CLI:
```
https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
```
You'll need to create a new AWS access key and provide the key id and secret key to terraform to start launching projects, this can be created by logging into aws and going to the following link:
```
https://console.aws.amazon.com/iam/home?region=us-east-1#/security_credentials
```
From here create an access key and provide the output values to the below commands:
```
# export AWS_ACCESS_KEY_ID=
```
Now, set your secret key.
```
# export AWS_SECRET_ACCESS_KEY=
```
For the next steps it is important to consider which region you'll be hosting your application in as these steps will need to be completed in the region you intend to use, see AWS region documentation below:
```
https://aws.amazon.com/about-aws/global-infrastructure/regions_az/
```
Within AWS you will also need to create a key pair (make sure to save this as you'll need this to SSH to your virtual machine at the end), this can be done with the following guide:
```
https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/create-key-pairs.html
```
Following on from this before creating anything else you will need to have a subnet which can be created with the following guide, make sure to take note of the ID:
```
https://docs.aws.amazon.com/vpc/latest/userguide/create-subnets.html
```
If you already have a subnet, you can find its ID by going to subnets and choosing the ID of your prefered subnet from that screen.


Python 3 is also required to be installed locally along with the pip extension requests.

Python:
```
https://www.python.org/downloads/
```
Requests:
```
https://www.activestate.com/resources/quick-reads/how-to-pip-install-requests-python-package/
```

Once these prerequsities have been completed you can move onto project installation below.

## Installation
Clone the files from this repository to your perfered directory. Or download directly from git if you don't want to clone.

## Usage

Once the project has been downloaded and all prerequisites setup run main.py this will present you with a GUI for creating virtual machines based on your repositories and a button to destroy anything terraform creates. 

Below is a list of important directories:

NGINX configuration:
```
/etc/nginx/conf.d/your-repo-name.conf
```
Your application location:
```
/var/www/vhosts/your-repo-name
```
Php-fpm is used for the handling of php requests and will install as the latest version of php. The latest MySQL will also be installed and configured for use. 

## Maintaining the virtual machine after deployment
Once your virtual machine has been created your DNS will need to be updated to point to the IP address of the VM. 
You will also need to setup any data into the created databases but nginx, php, and MySQL will all have been setup for you with your MySQL root credentials visible in '.my.cnf' and your application credentials in your .env variable. 

You may also have noticed a script called setupcert.sh in your root directory, once your dns has been moved, run this script to setup an auto renewing SSL certificate. 

If you wish to add aditional projects of the same type the Nginx config can be used as a template with directories and domain name needing to be updated.

## License

MIT License

Copyright (c) 2024 Patrick Joseph Sibbit Clough

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
