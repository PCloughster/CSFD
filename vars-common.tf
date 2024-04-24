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
  default = ""
}

variable "git_repo_name" {
  default = ""
}

variable "subnet_id" {
  default = ""
}

variable "template_id" {
  default = ""
}

variable "user_ip" {
  default = "0.0.0.0"
}

resource "random_password" "db_pass" {
  length           = 16
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}
