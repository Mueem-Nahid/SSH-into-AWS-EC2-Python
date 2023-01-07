**SSH into AWS EC2 in Python:**

If you are trying to make a project where you will start an AWS EC2 instance and run commands or run any cron-related project from another IAM roles enabled EC2 instance, then can follow this project. 
This is code first we will trigger an EC2 instance from another EC2 instance. First, we have to start that EC2 using [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.start_instances), then SSH into that instance using SSH secret key using [paramiko](https://docs.paramiko.org/en/stable/).  Then we can [execute commands](https://docs.paramiko.org/en/stable/api/client.html). 

> Note: You will need all the configurations of AWS EC2 instance.

**Some useful links about this topic:**

 - https://www.maskaravivek.com/post/how-to-ssh-into-an-ec2-instance-using-boto3/
 - https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html
 - https://stackoverflow.com/questions/49622575/schedule-to-start-an-ec2-instance-and-run-a-python-script-within-it
 - https://stackoverflow.com/questions/28485647/wait-until-task-is-completed-on-remote-machine-through-python

