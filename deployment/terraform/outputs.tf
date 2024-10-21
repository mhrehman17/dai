# Terraform Outputs Configuration

# Output for the public IP addresses of the instances
output "instance_public_ips" {
  description = "Public IP addresses of the instances created"
  value       = aws_instance.dai_instances.*.public_ip
  condition   = var.provider == "aws"
}

# Output for the VPC ID
output "vpc_id" {
  description = "ID of the VPC created for the infrastructure"
  value       = aws_vpc.dai_vpc.id
  condition   = var.provider == "aws"
}

# Output for the Load Balancer DNS name
output "lb_dns_name" {
  description = "DNS name of the Load Balancer"
  value       = aws_lb.dai_load_balancer.dns_name
  condition   = var.provider == "aws"
}

# Output for Kubernetes Cluster Endpoint (if using EKS or GKE)
output "k8s_cluster_endpoint" {
  description = "Endpoint of the Kubernetes cluster"
  value       = aws_eks_cluster.dai_cluster.endpoint
  condition   = var.provider == "aws"
}

# Output for Google Cloud Storage bucket name
output "gcs_bucket_name" {
  description = "Name of the GCS bucket created for the infrastructure"
  value       = google_storage_bucket.dai_bucket.name
  condition   = var.provider == "gcp"
}

# Output for Azure resource group name
output "azure_resource_group" {
  description = "Name of the Azure resource group created"
  value       = azurerm_resource_group.dai_rg.name
  condition   = var.provider == "azure"
}
