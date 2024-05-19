resource "aws_instance" "cvez_main" {
  ami           = var.ami
  instance_type = var.instance_type
  user_data     = file("./ec2/initialize.sh")
  key_name      = var.access_key_name

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
    Name       = "cvez_main"
  }

  tags = {
    created_by = "${var.name}"
    Name       = "cvez_main"
  }
}

resource "aws_network_interface" "cvez_main" {
  subnet_id       = var.aws_subnet_id
  private_ips     = var.private_ips
  security_groups = [aws_security_group.cvez_main.id]

  tags = {
    created_by = "${var.name}"
    Name       = "cvez_main"
  }
}

resource "aws_security_group" "cvez_main" {
  vpc_id      = var.aws_vpc_id
  name        = "cvez_main"
  description = "Allow traffics to the EC2 instance"

  dynamic "ingress" {
    iterator = port
    for_each = var.sg_ingress_ports
    content {
      from_port   = port.value
      to_port     = port.value
      protocol    = "TCP"
      cidr_blocks = var.sg_allow_address
    }
  }

  dynamic "egress" {
    iterator = port
    for_each = var.sg_egress_ports
    content {
      from_port   = port.value
      to_port     = port.value
      protocol    = "TCP"
      cidr_blocks = var.sg_allow_address
    }
  }

  tags = {
    created_by = "${var.name}"
    Name       = "cvez_main"
  }
}

# resource "aws_network_interface_sg_attachment" "cvez_main" {
#   security_group_id    = aws_security_group.cvez_main.id
#   network_interface_id = aws_instance.cvez_main.primary_network_interface_id
# }
