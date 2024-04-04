resource "aws_instance" "app_server" {
  ami           = data.aws_ami.amazon_linux_23.id
  instance_type = "t2.micro"
  key_name      = var.aws_key

  tags = {
    Name = "ExampleAppServerInstance"
  }
}
