resource "aws_security_group" "demo" {
  name = "insecure-demo"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_ebs_volume" "demo" {
  availability_zone = "us-east-1a"
  size              = 10
  encrypted         = false
}

variable "demo_credentials" {
  default = {
    password = "demo_password"
  }
}