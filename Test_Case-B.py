import boto3
import sys
from datetime import datetime, timedelta

# Create an AWS Auto Scaling client
client = boto3.client('autoscaling')

def next_scheduled_action(asg_name):
    # Describe the scheduled actions for the Auto Scaling Group
    response = client.describe_scheduled_actions(AutoScalingGroupName=asg_name)
    
    # Get the current time
    now = datetime.utcnow()

    # Find the next scheduled action
    next_scheduled_action = None
    min_time_difference = float('inf')

    for action in response['ScheduledUpdateGroupActions']:
        scheduled_time = action['StartTime']
        scheduled_datetime = datetime.strptime(scheduled_time, "%Y-%m-%dT%H:%M:%SZ")

        # Calculate time difference
        time_difference = scheduled_datetime - now

        if time_difference.total_seconds() >= 0 and time_difference < timedelta(seconds=min_time_difference):
            min_time_difference = time_difference.total_seconds()
            next_scheduled_action = action
            print("Next Scheduled Action: {}".format(next_scheduled_action))
    
    return next_scheduled_action, min_time_difference

def format_time_difference(time_difference):
    # Convert seconds to HH:MM:SS format
    hours, remainder = divmod(time_difference, 3600)
    minutes, seconds = divmod(remainder, 60)
    return '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))

def current_day_activity(asg_name):

    # Get the current date and time in UTC
    current_time = datetime.utcnow()

    # Describe the scheduled actions for the Auto Scaling Group
    response = client.describe_scaling_activities(AutoScalingGroupName=asg_name)

    # Calculate the start time for the current day
    start_time = current_time.replace(hour=0, minute=0, second=0, microsecond=0)

    # Filter activities launched or terminated on the current day
    launched_count = 0
    terminated_count = 0

    for activity in response['Activities']:
        activity_time = activity['StartTime']

        # Convert activity time to datetime object
        activity_datetime = datetime.strptime(activity_time, "%Y-%m-%dT%H:%M:%S.%fZ")

        # Check if the activity occurred on the current day
        if start_time <= activity_datetime <= current_time:
            if activity['StatusCode'] == 'Successful':
                if activity['Description'].startswith('Launching EC2 instance'):
                    launched_count += 1
                elif activity['Description'].startswith('Terminating EC2 instance'):
                    terminated_count += 1

    return launched_count, terminated_count

def main(argv):
    print(sys.argv)
    if len(sys.argv)>1:
        return sys.argv[1]
    else:
        print("Please pass correct arguments")
        print("Usage ./sample-test.py asgname")

if __name__ == "__main__":
    asg_name = main(sys.argv)

    next_action, time_difference = next_scheduled_action(asg_name)
    launched_count, terminated_count = current_day_activity(asg_name)

    print("Total instances launched today: {}".format(launched_count))
    print("Total instances terminated today: {}".format(terminated_count))


    if next_action:
        print("The next scheduled action is: {}".format(next_action['ScheduledActionName']))
        print("Time until next action: {}".format(format_time_difference(time_difference)))
    else:
        print("No upcoming scheduled actions found.")


    
