# Main Terraform Configuration File for Deploying Infrastructure

provider "aws" {
  region  = var.region
  profile = "default"
}

provider "google" {
  credentials = file("${var.google_credentials_file}")
  project     = var.google_project
  region      = var.region
}

provider "azurerm" {
  features {}
}

# VPC Configuration for AWS
resource "aws_vpc" "dai_vpc" {
  cidr_block = var.vpc_cidr

  tags = {
    Name = "dai-vpc"
  }
}

# Subnet Configuration for AWS
resource "aws_subnet" "dai_subnet" {
  vpc_id                  = aws_vpc.dai_vpc.id
  cidr_block              = var.subnet_cidr
  availability_zone       = "${var.region}a"

  tags = {
    Name = "dai-subnet"
  }
}

# Security Group for Instances
resource "aws_security_group" "dai_sg" {
  vpc_id = aws_vpc.dai_vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.allowed_ip]
  }

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = [var.allowed_ip]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "dai-security-group"
  }
}

# EC2 Instance for Orchestrator
resource "aws_instance" "dai_instances" {
  count         = var.number_of_instances
  instance_type = var.instance_type
  ami           = "ami-0c55b159cbfafe1f0"  # Example AMI ID, replace with actual
  key_name      = var.ssh_key_name

  subnet_id              = aws_subnet.dai_subnet.id
  vpc_security_group_ids = [aws_security_group.dai_sg.id]

  tags = {
    Name = "dai-instance-${count.index}"
  }
}

# Load Balancer Configuration
resource "aws_lb" "dai_load_balancer" {
  name               = "dai-lb"
  internal           = false
  load_balancer_type = var.lb_type
  security_groups    = [aws_security_group.dai_sg.id]
  subnets            = [aws_subnet.dai_subnet.id]

  tags = {
    Name = "dai-load-balancer"
  }
}

# Google Cloud Storage Bucket
resource "google_storage_bucket" "dai_bucket" {
  name     = "dai-storage-bucket"
  location = var.region
}

# Azure Resource Group
resource "azurerm_resource_group" "dai_rg" {
  name     = "dai-resource-group"
  location = var.region
}
