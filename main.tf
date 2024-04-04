resource "aws_security_group" "vm" {
  name        = "${var.git_repo_name}-sg"
  description = "network rules for VM"
}

resource "aws_security_group_rule" "inbound_http_to_vm" {
  security_group_id = aws_security_group.vm.id
  description       = "Allow http protocol inbound from any IP"
  type              = "ingress"
  from_port         = "80"
  to_port           = "80"
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "inbound_https_to_vm" {
  security_group_id = aws_security_group.vm.id
  description       = "Allow https protocol inbound from any IP"
  type              = "ingress"
  from_port         = "443"
  to_port           = "443"
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "inbound_ssh_to_vm" {
  security_group_id = aws_security_group.vm.id
  description       = "Allow ssh protocol inbound from any IP"
  type              = "ingress"
  from_port         = "22"
  to_port           = "22"
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "vm_outbound_any" {
  security_group_id = aws_security_group.vm.id
  description       = "Allow VM to connect out to any IP on any port"
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "all"
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_network_interface" "main" {
  subnet_id       = var.subnet_id
  security_groups = [aws_security_group.vm.id]

  tags = {
    Name = "primary-interface"
  }
}

resource "aws_instance" "app_server" {
  ami           = data.aws_ami.amazon_linux_23.id
  instance_type = "t2.micro"
  key_name      = var.aws_key
  user_data     = templatefile("./templates/${var.template_id}.tpl", { 
  git_repo = var.git_repo, 
  git_repo_name = var.git_repo_name, 
  application_domain = var.application_domain
  }) 

  tags = {
    Name = var.git_repo_name
  }
}
