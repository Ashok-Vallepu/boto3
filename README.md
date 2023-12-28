Testcase:- A
1- ASG desire running count should be same as running instances. if mismatch fails
2- If more than 1 instance running on ASG, then the ec2 instance should on available and distributed on multiple availibity zones.
3- SecuirtyGroup, ImageID and VPCID should be same on ASG running instances. Do not just print.
4- Findout uptime of ASG running instances and get the longest running instance.

Testcase:- B
Find the Scheduled actions of the given ASG which is going to run next and calculate elapsed in hh:mm: ss from the current time.
Calculate the total number of instances launched and terminated on the current day for the given ASG.

Perform below steps before executing the scripts
1) The following examples show how you can configure environment variables
   
   export aws_access_key_id = "xxxxxxxxx"
   
   export aws_secret_access_key = "xxxxxxxxx"

2) Boto3 is the name of the Python SDK for AWS. It allows us to create, update, and delete AWS resources from Python scripts
   To install boto3 SDK run this command :
   pip3 install boto3
