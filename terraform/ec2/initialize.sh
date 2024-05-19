#!/bin/bash
sudo yum update -y
# Install Docker
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user
# Install docker compose
sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s | tr '[:upper:]' '[:lower:]')-$(uname -m) -o /usr/bin/docker-compose
sudo chmod 755 /usr/bin/docker-compose
# Send message for check availability
sudo yum install -y httpd
sudo systemctl start httpd
sudo systemctl enable httpd
echo "<h2>Hello EC2!</h2>" | sudo tee /var/www/html/index.html