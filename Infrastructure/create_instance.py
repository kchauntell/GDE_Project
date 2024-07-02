import boto3

# Initialize a session using your AWS credentials

### 
# if you have configured your AWS CLI
session = boto3.Session()
# else, you can specify your credentials here
# session = boto3.Session(
#     aws_access_key_id='AKIAVEEFE3TQMZIWOMJ7',
#     aws_secret_access_key='YOUR_SECRET_KEY',
#     region_name='us-east-1'
# )
###

# Create EC2 resource and client
ec2_resource = session.resource('ec2')
ec2_client = session.client('ec2')

# Create an EC2 instance
def create_instances():
    instances = ec2_resource.create_instances(
        ImageId='ami-04a81a99f5ec58529',
        InstanceType='t2.micro',
        KeyName='GDE_Project',
        MinCount=2,
        MaxCount=2,
        SecurityGroupIds=['sg-0d4d0e275470b2a87'],
        SubnetId='subnet-04001c36f77f7c6de',
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {'Key': 'Name', 'Value': 'Created with boto3'}
                ]
            }
        ]
    )
    print("Instances created:", [instance.id for instance in instances])
    
    # Wait until all instances are running
    for instance in instances:
        print(f"Waiting for instance {instance.id} to be in running state...")
        instance.wait_until_running()
        instance.load()  # Reload the instance attributes

    print("All instances are now running.")
    
    return instances



# Create a load balancer
def create_load_balancer():
    elb_client = session.client('elbv2')
    
    # Create a load balancer
    load_balancer = elb_client.create_load_balancer(
        Name='my-load-balancer',
        Subnets=[
            'subnet-04001c36f77f7c6de',
            'subnet-0d787fab8ceefc54a',
        ],
        SecurityGroups=[
            'sg-0d4d0e275470b2a87'
        ],
        Scheme='internet-facing',
        Tags=[
            {
                'Key': 'Name',
                'Value': 'LoadBalancer created with boto3'
            },
        ],
        Type='application',
        IpAddressType='ipv4'
    )
    
    print("Load Balancer created:", load_balancer['LoadBalancers'][0]['LoadBalancerArn'])
    return load_balancer['LoadBalancers'][0]['LoadBalancerArn']

# Create target group
def create_target_group():
    elb_client = session.client('elbv2')
    
    target_group = elb_client.create_target_group(
        Name='my-targets',
        Protocol='HTTP',
        Port=80,
        VpcId='vpc-094d3bf31bcc39586',
        HealthCheckProtocol='HTTP',
        HealthCheckPort='80',
        HealthCheckEnabled=True,
        HealthCheckPath='/',
        Matcher={
            'HttpCode': '200'
        },
        TargetType='instance',
        Tags=[
            {
                'Key': 'Name',
                'Value': 'MyTargetGroup'
            },
        ],
    )
    
    print("Target Group created:", target_group['TargetGroups'][0]['TargetGroupArn'])
    return target_group['TargetGroups'][0]['TargetGroupArn']

# Register instances with target group
def register_targets(target_group_arn, instances):
    elb_client = session.client('elbv2')
    
    targets = [{'Id': instance.id} for instance in instances]
    
    response = elb_client.register_targets(
        TargetGroupArn=target_group_arn,
        Targets=targets
    )
    
    print("Instances registered with target group:", targets)

# Create listener
def create_listener(load_balancer_arn, target_group_arn):
    elb_client = session.client('elbv2')
    
    listener = elb_client.create_listener(
        LoadBalancerArn=load_balancer_arn,
        Protocol='HTTP',
        Port=80,
        DefaultActions=[
            {
                'Type': 'forward',
                'TargetGroupArn': target_group_arn
            }
        ]
    )
    
    print("Listener created:", listener['Listeners'][0]['ListenerArn'])



def main():
    instances = create_instances()
    load_balancer_arn = create_load_balancer()
    target_group_arn = create_target_group()
    register_targets(target_group_arn, instances)
    create_listener(load_balancer_arn, target_group_arn)

if __name__ == "__main__":
    main()