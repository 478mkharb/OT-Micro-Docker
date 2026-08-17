packer {
  required_plugins {
    amazon = {
      version = ">= 1.2.8"
      source  = "github.com/hashicorp/amazon"
    }
  }
}

source "amazon-ebs" "employee_api" {
  ami_name      = "dev-otms-employee-api-golden-ami-{{timestamp}}"
  instance_type = "t3.micro"
  region        = "us-east-1"
  ssh_username  = "ubuntu"

  source_ami_filter {
    filters = {
      name                = "ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"
      root-device-type    = "ebs"
      virtualization-type = "hvm"
    }
    most_recent = true
    owners      = ["099720109477"]
  }

  tags = {
    Name = "dev-otms-employee-api-golden-ami"
  }
}

build {
  sources = ["source.amazon-ebs.employee_api"]

  # FIX: Create the destination folder first so SCP doesn't panic
  provisioner "shell" {
    inline = ["mkdir -p /home/ubuntu/Employee_API"]
  }

  # 1. Upload local application code from the parent directory
  provisioner "file" {
    source      = "../"
    destination = "/home/ubuntu/Employee_API/"
  }

  # 2. Upload systemd service file from the current packer directory
  provisioner "file" {
    source      = "./employee-api.service"
    destination = "/tmp/employee-api.service"
  }

  # 3. Install Go 1.22.12, compile application, and setup systemd service
  provisioner "shell" {
    inline = [
      "sudo apt-get update -y",
      "sudo apt-get install -y wget tar git",

      # Install Go 1.22.12 directly
      "wget -q https://go.dev/dl/go1.22.12.linux-amd64.tar.gz",
      "sudo rm -rf /usr/local/go",
      "sudo tar -C /usr/local -xzf go1.22.12.linux-amd64.tar.gz",
      "rm go1.22.12.linux-amd64.tar.gz",

      # Build the application using Go 1.22.12
      "export PATH=$PATH:/usr/local/go/bin",
      "cd /home/ubuntu/Employee_API",
      "/usr/local/go/bin/go mod tidy",
      "/usr/local/go/bin/go build -o employee-api",

      # Configure systemd unit file
      "sudo mv /tmp/employee-api.service /etc/systemd/system/employee-api.service",
      "sudo systemctl daemon-reload",
      "sudo systemctl enable employee-api.service"
    ]
  }

  # FIXED: Added post-processor to generate manifest.json for Jenkins to read the AMI ID
  post-processor "manifest" {
    output     = "manifest.json"
    strip_path = true
  }
}
