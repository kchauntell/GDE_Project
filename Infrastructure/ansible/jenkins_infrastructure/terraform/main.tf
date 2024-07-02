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

resource "aws_instance" "jenkins-main" {
  ami           = "ami-04a81a99f5ec58529"
  instance_type = "t2.micro"
  count        = 1
  key_name      = "GDE_Project"
  tags = {
    Name = "jenkins-main"
    Environment = "dev"
  }
}

resource "aws_instance" "jenkins-agent" {
  ami           = "ami-04a81a99f5ec58529"
  instance_type = "t2.micro"
  count        = 1
  key_name      = "GDE_Project"
  tags = {
    Name = "jenkins-agent"
    Environment = "dev"
  }
}


resource "null_resource" "ansible_provisioner" {
  provisioner "local-exec" {
    command = <<EOT
      cd .. && ansible-playbook -i inventory_aws_ec2.yaml playbook.yaml
    EOT
    environment = {
      ANSIBLE_HOST_KEY_CHECKING = "False"
    }
  }

  depends_on = [aws_instance.jenkins-main, aws_instance.jenkins-agent]
}


output "jenkins-main" {
  value = aws_instance.jenkins-main[*].public_ip
}

output "jenkins-agent" {
  value = aws_instance.jenkins-agent[*].public_ip
}