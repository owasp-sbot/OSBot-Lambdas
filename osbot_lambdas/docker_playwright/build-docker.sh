docker build -t 470426667096.dkr.ecr.eu-west-2.amazonaws.com/docker_playwright:latest .
docker run --rm -it -v $(pwd):/var/task -p 8888:8000 470426667096.dkr.ecr.eu-west-2.amazonaws.com/docker_playwright:latest
#docker run --rm -it -p 8888:8000 470426667096.dkr.ecr.eu-west-2.amazonaws.com/docker_playwright:latest
