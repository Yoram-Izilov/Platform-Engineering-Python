# Manage AWS with python code
Run the program with python (install python, boto3 and aws) </br>
or follow the steps below to run it inside jenkins.

# Steps
- install docker and run the docker compose file
- inside jenkins (port 8080) add the plugins (aws cli, docker, user data)
- add the agent with the address in cloud nodes (tcp://socat:2375)
- create new jobs based on each pipeline you want to utilize
- create shared folder for both the user and the jenkins (for the s3 file upload function)
  1. sudo mkdir -p /sharedFolder
  2. sudo chmod 777 /sharedFolder/
  3. docker compose up -d

That's it! now run each job, and choose the paramaters based on your needs!
# Credits
### Yoram Izilov
