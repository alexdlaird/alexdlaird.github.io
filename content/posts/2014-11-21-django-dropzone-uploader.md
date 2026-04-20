---
title: "Django Dropzone Uploader"
date: 2014-11-21
tags: 
  - "instructional"
  - "programming"
---

Ever been on a trip and, upon return, needed a quick and easy way for all your friends to send you their pictures and videos without burning CDs, sending massive emails, or using third-party services? Or, maybe a better question, ever wondered how to construct a basic Django application with Amazon's web services, for instance S3?

Look no further. Below is the basic code for a drag-and-drop Django web application that allows users to upload files directly to an Amazon S3 bucket.

# [](https://github.com/alexdlaird/django-dropzone-to-s3#basic-deployment)Deployment Setup

The code for this project [can be found on GitHub](https://github.com/alexdlaird/django-dropzone-to-s3).

You'll need the following installed before cloning or forking the source code:

- [Python 2.7](https://www.python.org/downloads/)
- [PyCrypto](https://www.dlitz.net/software/pycrypto/) (if you're on Windows, look at [these installers](http://www.voidspace.org.uk/python/modules.shtml#pycrypto))
- [PIP](http://pip.readthedocs.org/en/latest/installing.html)

This project will write to an [Amazon Web Services (AWS)](http://aws.amazon.com/) S3 storage bucket, so it's assumed you have an AWS account. If not, create one. S3 is a storage platform from Amazon, and EC2 allows you to spin up virtual servers, which you can use to host this project. If you're new to AWS, Amazon will likely give you the first year of their smallest EC2 instance free.

This project also includes a deployment script, which allows you to easily deploy the project from your local computer to your server.

Here's what you need to setup in AWS to ensure your account is ready to receive a deployment of this project:

- [Launch an EC2 instance](http://aws.amazon.com/ec2) running Ubuntu Server (or some other Debian-based operating system)
- Save the .pem key pair file for the EC2 instance as ~/.ssh/myserver.pem
- Create an EC2 Security Group that has port 80 opened
- [Create an S3 bucket](http://aws.amazon.com/s3/)
- Generate an AWS Access Key and Secret Access Key
- (Optional) Create an elastic IP and associate it with the EC2 instace you created
- (Optional) Create a DNS entry of your choosing to point to the elastic IP (AWS will generate their own DNS entry that you can also use, if you don't have your own domain name)

# Fork the Code

Now you're ready to clone, configure, and deploy the code to your EC2 server.

- Fork the repository on GitHub
- Clone your forked repository
- Modify the variables at the bottom of djangodropzonetos3/settings.py to customize the application
- You must specify valid values for AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_STORAGE_BUCKET_NAME in settings.py
- Modify the HOSTNAME variables at the top of fabfile.py to point to your EC2 instance's DNS entry
- Modify the REPO_URL variable at the top of fabfile.py to point to your fork of the repository

# Deploy

The fabfile.py in the repository will take care of setting up the environment for you, including installing and configuring a web server. Isn't that handy? So you're ready to deploy by doing the following:

- From the Command Line at the root of the cloned source, execute "pip install -r reqs.txt"
- From the Command Line at the root of the cloned source, execute "fab deploy"

That's it. If this deployment is successful, you should be able to navigate to the hostname for your server in a web browser, drop and save the files, and see them stored in your S3 bucket.

Now, start poking around in the code to learn the ease and awesomeness of Django and how this was accomplished! Leave your thoughts in the comments section below!
