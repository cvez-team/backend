output "aws_vpc_id" {
  value = aws_vpc.cvez_main.id
}

output "aws_subnet_id" {
  value = aws_subnet.cvez_main.id
}

output "aws_availability_zone" {
  value = var.availability_zone
}
