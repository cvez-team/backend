# AWS Cloud provisioning


# Networl module
module "aws_vpc" {
  source = "./vcp"
  name   = "minhdq30"
}

module "aws_ec2" {
  source                = "./ec2"
  name                  = "minhdq30"
  aws_vpc_id            = module.aws_vpc.aws_vpc_id
  aws_subnet_id         = module.aws_vpc.aws_subnet_id
  aws_availability_zone = module.aws_vpc.aws_availability_zone
}
