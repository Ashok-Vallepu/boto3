import boto3
import os
import sys
from datetime import datetime
aws_access_key_id=os.environ['aws_access_key_id']
aws_secret_access_key=os.environ['aws_secret_access_key']
# client = boto3.client('autoscaling')
client = boto3.client('autoscaling',aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key,region_name='us-west-1')
def check_asg_instances(asg_name):
    # Create an AWS Auto Scaling client
    # Describe the Auto Scaling Group
    response = client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])

    # Extract relevant information
    asg_info = response['AutoScalingGroups'][0]
    desired_capacity = asg_info['DesiredCapacity']
    running_instances = len(asg_info['Instances'])
    # Compare the desired capacity with the actual number of instances
    if desired_capacity != running_instances:
        raise ValueError(f"Error: Desired capacity ({desired_capacity}) does not match the actual number of running instances ({running_instances}) in {asg_name}!")
    print(f"Desired capacity matches the actual number of running instances in {asg_name}.")
    return response

def create_or_update_asg(asg_name, min_size, max_size, desired_capacity, subnet_ids):
    # Create or update the Auto Scaling Group
    client.create_auto_scaling_group(
        AutoScalingGroupName=asg_name,
        MinSize=min_size,
        MaxSize=max_size,
        DesiredCapacity=desired_capacity,
        VPCZoneIdentifier=','.join(subnet_ids),  # Comma-separated list of subnet IDs
        AvailabilityZones=[],  # This parameter is deprecated, and VPCZoneIdentifier should be used instead
        # Add other parameters as needed
    )

def check_asg_instances_resource_id(asg_name):
    # Describe the Auto Scaling Group
    response = client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])
    # Extract relevant information
    asg_info = response['AutoScalingGroups'][0]
    desired_sg_id = asg_info['VPCZoneIdentifier']
    desired_image_id = asg_info['LaunchConfigurations'][0]['ImageId']
    desired_vpc_id = asg_info['VPCId']
    # Describe instances in the Auto Scaling Group
    instances_response = client.describe_auto_scaling_instances(InstanceIds=[instance['InstanceId'] for instance in asg_info['Instances']])
    # Check each instance for matching Security Group, Image ID, and VPC ID
    for instance in instances_response['AutoScalingInstances']:
        instance_sg_id = instance['VPCZoneIdentifier']
        instance_image_id = instance['LaunchConfigurationName'].split('/')[-1]
        instance_vpc_id = instance['VPCId']
        if desired_sg_id != instance_sg_id or desired_image_id != instance_image_id or desired_vpc_id != instance_vpc_id:
            raise ValueError(f"Error: Security Group, Image ID, or VPC ID mismatch for instance {instance['InstanceId']} in {asg_name}!")
    print("Security Group, Image ID, and VPC ID match for all instances in the Auto Scaling Group.")

def get_instance_uptime(instance_launch_time):
    now = datetime.utcnow()
    launch_time = datetime.strptime(instance_launch_time, "%Y-%m-%dT%H:%M:%S.%fZ")
    uptime = now - launch_time
    return uptime
def find_longest_running_instance(asg_name):
    # Describe the Auto Scaling Group
    response = client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])
    # Extract information about instances in the Auto Scaling Group
    instances = response['AutoScalingGroups'][0]['Instances']
    # Calculate uptime for each instance
    instance_uptimes = {}
    for instance in instances:
        instance_id = instance['InstanceId']
        launch_time = instance['LaunchTime']
        uptime = get_instance_uptime(launch_time)
        instance_uptimes[instance_id] = uptime
    # Find the instance with the longest uptime
    longest_running_instance = max(instance_uptimes, key=instance_uptimes.get)
    longest_running_time = instance_uptimes[longest_running_instance]
    print(f"The instance with ID {longest_running_instance} has been running for {longest_running_time}.")
 
def main(argv):
    print(sys.argv)
    if len(sys.argv)>1:
        return sys.argv[1]
    else:
        print("Please pass correct arguments")
        print("Usage ./sample-test.py asgname")
 
		
if __name__ == "__main__":
    # Replace 'YourASGName' with the actual name of your Auto Scaling Group
    #asg_name = 'YourASGName'
    asg_name = main(sys.argv)
    #   ass 1
    try:
        check_asg_instances(asg_name)
    except ValueError as e:
        print(str(e))
        # Add corrective action here, e.g., send an alert, terminate instances, adjust desired capacity, etc.
        exit(1)
    # ass 2
    # Replace with your Auto Scaling Group configuration
    min_size = 1
    max_size = 1
    desired_capacity = 1
    subnet_ids = ['subnet-abc123', 'subnet-def456', 'subnet-ghi789']  # Replace with your subnet IDs
    create_or_update_asg(asg_name, min_size, max_size, desired_capacity, subnet_ids)
    # ass 3
    try:
        check_asg_instances_resource_id(asg_name)
    except ValueError as e:
        print(str(e))
        # Add corrective action here, e.g., terminate instances, update ASG configuration, send an alert, etc.
        exit(1)
    # ass 4
    find_longest_running_instance(asg_name)