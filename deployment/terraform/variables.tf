# Terraform Variables File

# Cloud Provider Configuration
variable "provider" {
  description = "Cloud provider to use (e.g., aws, azure, gcp)"
  type        = string
  default     = "aws"
}

# Region Configuration
variable "region" {
  description = "Region to deploy the infrastructure"
  type        = string
  default     = "us-east-1"
}

# Instance Configuration
variable "instance_type" {
  description = "Instance type to use for nodes (e.g., t2.micro, t3.large)"
  type        = string
  default     = "t3.large"
}

variable "number_of_instances" {
  description = "Number of instances to deploy"
  type        = number
  default     = 3
}

# Network Configuration
variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "subnet_cidr" {
  description = "CIDR block for the subnet"
  type        = string
  default     = "10.0.1.0/24"
}

# Security Configuration
variable "allowed_ip" {
  description = "IP address range allowed to access the services"
  type        = string
  default     = "0.0.0.0/0"
}

# Storage Configuration
variable "volume_size" {
  description = "Size of EBS volumes (in GB) for each instance"
  type        = number
  default     = 50
}

# Autoscaling Configuration
variable "min_instances" {
  description = "Minimum number of instances in the autoscaling group"
  type        = number
  default     = 2
}

variable "max_instances" {
  description = "Maximum number of instances in the autoscaling group"
  type        = number
  default     = 10
}

variable "scale_up_cpu_threshold" {
  description = "CPU usage threshold for scaling up"
  type        = number
  default     = 75
}

variable "scale_down_cpu_threshold" {
  description = "CPU usage threshold for scaling down"
  type        = number
  default     = 25
}

# Tags Configuration
variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default = {
    Environment = "Production"
    Project     = "Decentralized AI System"
  }
}

# SSH Configuration
variable "ssh_key_name" {
  description = "Name of the SSH key pair to access instances"
  type        = string
  default     = "dai_system_key"
}

# Load Balancer Configuration
variable "lb_type" {
  description = "Type of load balancer (e.g., application, network)"
  type        = string
  default     = "application"
}
