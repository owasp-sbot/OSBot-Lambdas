#aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 470426667096.dkr.ecr.eu-west-2.amazonaws.com
docker build -t 470426667096.dkr.ecr.eu-west-2.amazonaws.com/docker_playwright:latest .
docker push 470426667096.dkr.ecr.eu-west-2.amazonaws.com/docker_playwright