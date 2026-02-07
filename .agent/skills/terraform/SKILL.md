---
name: Terraform
description: Infrastructure as code, providers, state management
---

# Terraform Skill

## Basic Structure

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"

  tags = {
    Name = "WebServer"
  }
}
```

## Variables

```hcl
variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
}

resource "aws_instance" "web" {
  instance_type = var.instance_type
}
```

## Outputs

```hcl
output "public_ip" {
  value = aws_instance.web.public_ip
}
```

## Commands

```bash
terraform init      # Initialize
terraform plan      # Preview changes
terraform apply     # Apply changes
terraform destroy   # Tear down
terraform state list  # List resources
```

## State Management

- Use remote backend (S3 + DynamoDB)
- Never edit state manually
- Use `terraform import` for existing resources
- Lock state during operations

## When to Apply
Use when provisioning cloud infrastructure or managing IaC.
