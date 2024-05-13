# AWS Cloud provisioning

# Network module
module "aws_vpc" {
  source = "./vpc"
  name   = "minhdq30"
}

module "aws_ec2" {
  source                = "./ec2"
  name                  = "minhdq30"
  aws_vpc_id            = module.aws_vpc.aws_vpc_id
  aws_subnet_id         = module.aws_vpc.aws_subnet_id
  aws_availability_zone = module.aws_vpc.aws_availability_zone
}

module "aws_elastic_eip" {
  source          = "./eip"
  name            = "minhdq30"
  ec2_instance_id = module.aws_ec2.ec2_instance_id
}
