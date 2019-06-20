FROM docker:stable

LABEL "com.github.actions.name"="Azurefire Docker Container"
LABEL "com.github.actions.description"="Build and publish a Docker container"
LABEL "com.github.actions.icon"="upload-cloud"
LABEL "com.github.actions.color"="blue"

LABEL "repository"="https://github.com/smashwilson/az-infra"
LABEL "maintainer"="Ash Wilson <smashwilson@gmail.com>"

ADD entrypoint.sh /entrypoint.sh
ENTRYPOINT /entrypoint.sh
