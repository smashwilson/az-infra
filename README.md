# Azurefire infrastructure

![shipit](https://github.com/smashwilson/az-infra/workflows/shipit/badge.svg)

Infrastructure for [azurefire.net](https://azurefire.net/) and [pushbot.party](https://pushbot.party/). Hosting for a bunch of services that @smashwilson wants to stash somewhere, deployed to AWS as immutable infrastructure.

## Services

These containers run persistently on the CoreOS host:

* [pushbot](https://github.com/smashwilson/pushbot): A [hubot](https://hubot.github.com/) instance who's here to protect you from the terrible secret of space.
* [azurefire-nginx](https://github.com/smashwilson/azurefire-nginx): An [nginx](https://nginx.org/en/docs/) server that terminates incoming TLS connections and proxies requests to other services.

## Cron

These containers are triggered on a schedule:

* [azurefire-tls](https://github.com/smashwilson/azurefire-tls): Daily verification that the TLS certificate issued from [Let's Encrypt](https://letsencrypt.org/) is up to date. When expiration is near, acquire a new certificate with a DNS challenge and rebuild the infrastructure.

## Deployment

Each time a new commit is merged into the master branch of this repository, its [Travis build](https://travis-ci.org/smashwilson/azurefire-infra/branches/):

1. Ensures that an [Elastic Load Balancer](http://docs.aws.amazon.com/elasticloadbalancing/latest/classic/introduction.html) exists and collects information about any pre-existing instances.
2. Creates a temporary SSH keypair and uploads it to [EC2](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html).
3. Launches an [EC2 instance](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html) with a [CoreOS]() image and waits for it to begin listening on port 22.
4. Creates a bash script from a [Jinja2 template](./template/bootstrap.sh.j2) and executes it over an SSH connection to the new host. The bash script pulls and runs containers for each of the services listed above.
5. Registers the new host on the load balancer.
6. De-registers any prior hosts from the load balancer. Terminates any prior instances and deletes any unused security groups and keypairs.
