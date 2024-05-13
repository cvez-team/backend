resource "aws_instance" "cvez_main" {
  ami           = var.ami
  instance_type = var.instance_type

  network_interface {
    network_interface_id = aws_network_interface.cvez_main.id
    device_index         = 0
  }

  ebs_block_device {
    device_name           = "/dev/sda1"
    volume_size           = var.volume_size
    volume_type           = var.volume_type
    delete_on_termination = true
  }

  volume_tags = {
    created_by = "${var.name}"
  }

  tags = {
    created_by = "${var.name}"
  }
}

resource "aws_network_interface" "cvez_main" {
  subnet_id   = var.aws_subnet_id
  private_ips = var.private_ips

  tags = {
    created_by = "${var.name}"
  }
}

resource "aws_security_group" "cvez_main" {
  vpc_id      = var.aws_vpc_id
  name        = "cvez_main"
  description = "Allow traffics to the EC2 instance"

  tags = {
    created_by = "${var.name}"
  }
}
