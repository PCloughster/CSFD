variable "project_name" {
  default = "CSFD_Test"
}

variable "aws_region" {
  default = "us-east-1"
}

variable "aws_key" {
  default = "CSFD"
}

variable "application_domain" {
  default = "default_server"
}

variable "git_repo" {
  default = "https://github.com/PCloughster/0161festival"
}

variable "git_repo_name" {
  default = "0161festival"
}

variable "subnet_id" {
  default = "subnet-0ecb42a04844714dc"
}

variable "template_id" {
  default = "otherproj"
}

resource "random_password" "db_pass" {
  length           = 16
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}
