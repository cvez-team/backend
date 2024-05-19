output "ec2_instance_id" {
  value = aws_instance.cvez_main.id
}

output "ec2_network_interface_id" {
  value = aws_network_interface.cvez_main.id
}
