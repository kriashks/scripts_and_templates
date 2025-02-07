## Description: A tiny script to start an AWS EC2 Instance using Python
from subprocess import run

run("aws ec2 start-instances --instance-ids <ec2_id>")
