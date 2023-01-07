import paramiko
import boto3
import time
import os


def lamda_handler():
    try:
        if start_ec2():
            ssh_into_instance()
    except Exception as e:
        print("Error lamda_handler:", e)
    finally:
        stop_ec2()


def ssh_into_instance():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if ssh_connect_with_retry(ssh, "public_ip_address_of_the_intance", 0):
            print("Connected")
            stdin, stdout, stderr = ssh.exec_command(
                "bash start.sh")  # any bash command
            time.sleep(5)
            print('stdout:', stdout.read())
            print('stderr:', stderr.read())
            while not stdout.channel.exit_status_ready():
                if stdout.channel.recv_ready():
                    stdoutLines = stdout.readlines()
                    print(stdoutLines)
    except Exception as e:
        print("Error from ssh_into_instance: ", e)


def ssh_connect_with_retry(ssh, ip_address, retries):
    if retries > 3:
        return False
    privkey = paramiko.RSAKey.from_private_key_file(
        f"{os.getcwd()}/credential.pem")
    interval = 5
    try:
        retries += 1
        print('SSH into the instance: {}'.format(ip_address))
        ssh.connect(hostname=ip_address, username='ubuntu', pkey=privkey)
        return True
    except Exception as e:
        print(e)
        time.sleep(interval)
        print('Retrying SSH connection to {}'.format(ip_address))
        ssh_connect_with_retry(ssh, ip_address, retries)


def start_ec2():
    try:
        print("Starting EC2..")
        INSTANCE_ID = Config.EC2.get("INSTANCE_ID")
        ec2 = boto3.client('ec2', region_name=Config.EC2.get("REGION_NAME"))
        ec2.start_instances(InstanceIds=[INSTANCE_ID])
        print("EC2 started.")
        return True
    except Exception as e:
        print("Error starting EC2: ", e)


def stop_ec2():
    print("Stopping EC2..")
    INSTANCE_ID = Config.EC2.get("INSTANCE_ID")
    ec2 = boto3.client('ec2', region_name=Config.EC2.get("REGION_NAME"))
    ec2.stop_instances(InstanceIds=[INSTANCE_ID])
    while True:
        response = ec2.describe_instance_status(
            InstanceIds=[INSTANCE_ID], IncludeAllInstances=True)
        state = response['InstanceStatuses'][0]['InstanceState']
        print(f"Status: {state['Code']} - {state['Name']}")

        # If status is 80 ('stopped'), then proceed, else wait 5 seconds and try again
        if state['Code'] == 80:
            break
        else:
            time.sleep(5)
            stop_ec2()
    print('Instance stopped')


lamda_handler()
