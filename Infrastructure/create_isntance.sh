#!/bin/bash
aws ec2 run-instances \
    --image-id ami-04a81a99f5ec58529  \
    --instance-type t2.micro \
    --key-name  GDE_Project\
    --security-group-ids sg-0d4d0e275470b2a87 \
    --subnet-id subnet-04001c36f77f7c6de \
    --count 1 \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=created with aws cli}]' \
--output json > instance-details.json


# aws ec2 describe-instances
# aws ec2 describe-instances --instance-ids <id>