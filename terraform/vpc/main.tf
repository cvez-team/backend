# VPC
resource "aws_vpc" "cvez_main" {
  cidr_block = var.vpc_cidr

  tags = {
    created_by = "${var.name}"
    Name       = "cvez_main"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "cvez_main" {
  vpc_id = aws_vpc.cvez_main.id

  tags = {
    created_by = "${var.name}"
    Name       = "cvez_main"
  }
}

# Zone Subnets
resource "aws_subnet" "cvez_main" {
  vpc_id                  = aws_vpc.cvez_main.id
  cidr_block              = var.subnet_cidr
  availability_zone       = var.availability_zone
  map_public_ip_on_launch = true

  tags = {
    created_by = "${var.name}"
    Name       = "cvez_main"
  }
}

# Route Table
resource "aws_route_table" "cvez_main" {
  vpc_id = aws_vpc.cvez_main.id

  route {
    cidr_block = var.rt_cidr_block
    gateway_id = aws_internet_gateway.cvez_main.id
  }

  tags = {
    created_by = "${var.name}"
    Name       = "cvez_main"
  }
}

# Route Table Association
resource "aws_route_table_association" "cvez_main" {
  subnet_id      = aws_subnet.cvez_main.id
  route_table_id = aws_route_table.cvez_main.id
}
