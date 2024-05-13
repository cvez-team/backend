variable "name" {
  description = "The names created resource user"
  type        = string
  default     = "minhdq30"
}

variable "ami" {
  description = "OS version ami in EC2"
  type        = string
  default     = "ami-05b46bc4327cf9d99" # Amazon Linux
}

variable "instance_type" {
  description = "Type of machine in EC2"
  type        = string
  default     = "t2.micro" # Free-tier
}

variable "aws_vpc_id" {
  description = "VPC ID of EC2"
  type        = string
}

variable "aws_subnet_id" {
  description = "Subnet ID of EC2"
  type        = string
}

variable "aws_availability_zone" {
  description = "Volume for EC2"
  type        = string
}

variable "private_ips" {
  description = "Private IPs of EC2"
  type        = list(string)
  default     = ["10.0.1.100"]
}

variable "volume_type" {
  description = "Type of storage"
  type        = string
  default     = "gp3"
}

variable "volume_size" {
  description = "Size of storage"
  type        = number
  default     = 16
}

variable "sg_ingress_ports" {
  description = "Ingress rule for Security Group"
  type        = list(number)
  default     = [80, 443, 22]
}

variable "sg_egress_ports" {
  description = "Egress rule for Security Group"
  type        = list(number)
  default     = [80, 443]
}

variable "sg_allow_address" {
  description = "Allow address of Security Group"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}
