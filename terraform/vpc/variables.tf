variable "name" {
  description = "The names created resource user"
  type        = string
  default     = "minhdq30"
}

variable "vpc_cidr" {
  description = "The CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "subnet_cidr" {
  description = "The CIDR block for the Subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "availability_zone" {
  description = "Available zone of Network"
  type        = string
  default     = "ap-southeast-1b"
}

variable "rt_cidr_block" {
  description = "The CIDR block for the Route table"
  type        = string
  default     = "0.0.0.0/0"
}
