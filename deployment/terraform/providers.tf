# Terraform Providers Configuration

# Define the provider based on the variable 'provider'
provider "aws" {
  region = var.region
  profile = "default"
  version = "~> 3.0"
}

provider "azure" {
  features {}
}

provider "google" {
  credentials = file("${var.google_credentials_file}")
  project     = var.google_project
  region      = var.region
}

# Conditional Logic for Selecting Providers
locals {
  selected_provider = var.provider
}

terraform {
  required_version = ">= 0.13"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
    azure = {
      source  = "hashicorp/azurerm"
      version = "~> 2.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 3.0"
    }
  }
}

# Using dynamic provider selection
provider "aws" {
  count  = local.selected_provider == "aws" ? 1 : 0
  region = var.region
}

provider "azurerm" {
  count = local.selected_provider == "azure" ? 1 : 0
}

provider "google" {
  count       = local.selected_provider == "gcp" ? 1 : 0
  credentials = file("${var.google_credentials_file}")
  project     = var.google_project
  region      = var.region
}
