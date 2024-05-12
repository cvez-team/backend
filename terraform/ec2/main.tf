resource "aws_instance" "cvez_main" {
  ami           = var.ami
  instance_type = var.instance_type

  tags_all = {
    created_by = "${var.name}"
  }
}

resource "aws_network_interface" "cvez_main" {
  subnet_id   = var.aws_subnet_id
  private_ips = var.private_ips

  tags_all = {
    created_by = "${var.name}"
  }
}

resource "aws_ebs_volume" "cvez_main" {
  availability_zone = var.aws_availability_zone
  type              = var.volume_type
  size              = var.volume_size

  tags_all = {
    created_by = "${var.name}"
  }
}

resource "aws_security_group" "cvez_main" {
  vpc_id      = var.aws_vpc_id
  name        = "cvez_main"
  description = "Allow traffics to the EC2 instance"

  tags_all = {
    created_by = "${var.name}"
  }
}
