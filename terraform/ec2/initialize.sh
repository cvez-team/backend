#!/bin/bash
sudo yum update -y
# Install Docker
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user
# Install docker compose
sudo mkdir -p /usr/local/lib/docker/cli-plugins/
sudo curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 -o /usr/local/lib/docker/cli-plugins/docker-compose
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
# Send message for check availability
sudo yum install -y httpd
sudo systemctl start httpd
sudo systemctl enable httpd
echo "<h2>Hello EC2!</h2>" | sudo tee /var/www/html/index.html