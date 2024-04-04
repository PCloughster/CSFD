provider "aws" {
  profile = "default"
  region  = "us-east-1"
}

data "aws_ami" "amazon_linux_23" {
  most_recent = true

  owners = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-kernel-*-x86_64"]
  }

}