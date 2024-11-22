terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "weatherapp" {
  ami           = "ami-04a81a99f5ec58529"
  instance_type = "t2.micro"
  count        = 1
  key_name      = "GDE_Project"
  tags = {
    Name = "weatherapp"
    Environment = "dev"
  }
  
}

resource "aws_instance" "advisor" {
  ami           = "ami-04a81a99f5ec58529"
  instance_type = "t2.micro"
  count        = 1
  key_name      = "GDE_Project"
  tags = {
    Name = "advisor"
    Environment = "dev"
  }
}


output "weatherapp_public_ip" {
  value = aws_instance.weatherapp[*].public_ip
}

output "advisor_public_ip" {
  value = aws_instance.advisor[*].public_ip
}