packer {
  required_plugins {
    amazon = {
      version = ">= 1.2.8"
      source  = "github.com/hashicorp/amazon"
    }
  }
}

variable "ami_prefix" {
  type    = string
  default = "otms-frontend"
}

variable "github_token" {
  type      = string
  sensitive = true
  default   = env("GITHUB_TOKEN")
}

locals {
  timestamp = regex_replace(timestamp(), "[- TZ:]", "")
}

source "amazon-ebs" "frontend" {
  ami_name      = "${var.ami_prefix}-${local.timestamp}"
  instance_type = "t3.small"
  region        = "us-east-1"

  launch_block_device_mappings {
    device_name           = "/dev/sda1"
    volume_size           = 20
    volume_type           = "gp3"
    delete_on_termination = true
  }

  source_ami_filter {
    filters = {
      name                = "ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"
      root-device-type    = "ebs"
      virtualization-type = "hvm"
    }
    most_recent = true
    owners      = ["099720109477"] # Canonical (Ubuntu)
  }

  ssh_username = "ubuntu"

  tags = {
    Name        = "dev-otms-frontend-ami"
    Application = "otms"
    Owner       = "Infra-Titans"
    Environment = "dev"
    CostCenter  = "Snaatak"
  }
}

build {
  name = "otms-frontend-build"
  sources = [
    "source.amazon-ebs.frontend"
  ]

  # UPDATED PATH: Pointing to the files/ directory
  provisioner "file" {
    source      = "files/frontend.service"
    destination = "/tmp/frontend.service"
  }

  # UPDATED PATH: Pointing to the scripts/ directory
  provisioner "shell" {
    environment_vars = [
      "GITHUB_TOKEN=${var.github_token}"
    ]
    script = "scripts/setup.sh"
  }

  # REQUIRED FOR JENKINS: Outputs the AMI ID to manifest.json
  post-processor "manifest" {
    output     = "manifest.json"
    strip_path = true
  }
}
