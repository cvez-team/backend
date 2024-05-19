variable "name" {
  description = "The names created resource user"
  type        = string
  default     = "minhdq30"
}

variable "ec2_instance_id" {
  description = "Default EC2 Instance Id"
  type        = string
}

variable "ec2_network_interface_id" {
  description = "Network interface of EC2"
  type        = string
}
