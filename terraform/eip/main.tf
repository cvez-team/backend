resource "aws_eip" "cvez_main" {
  instance          = var.ec2_instance_id
  network_interface = var.ec2_network_interface_id

  tags = {
    created_by = "${var.name}"
    Name       = "cvez_main"
  }
}
