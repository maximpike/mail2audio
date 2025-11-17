FROM ubuntu:latest
LABEL authors="maxpike"

ENTRYPOINT ["top", "-b"]