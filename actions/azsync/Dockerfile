FROM alpine:3.10

LABEL "com.github.actions.name"="Azurefire Synchronization"
LABEL "com.github.actions.description"="Build and publish a Docker container"
LABEL "com.github.actions.icon"="refresh-cw"
LABEL "com.github.actions.color"="green"

LABEL "repository"="https://github.com/smashwilson/az-infra"
LABEL "maintainer"="Ash Wilson <smashwilson@gmail.com>"

RUN apk add --no-cache curl

ADD entrypoint.sh /entrypoint.sh
ENTRYPOINT /entrypoint.sh
