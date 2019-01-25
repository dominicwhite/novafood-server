workflow "New workflow" {
  on = "push"
  resolves = ["Set Credential Helper for Docker"]
}

action "Build Image" {
  uses = "actions/docker/cli@c08a5fc9e0286844156fefff2c141072048141f6"
  args = "build -t novafood-server ."
}

action "Setup Google Cloud" {
  uses = "actions/gcloud/auth@master"
  secrets = ["GCLOUD_AUTH"]
}

action "Set Credential Helper for Docker" {
  needs = ["Setup Google Cloud", "GitHub Action for Docker"]
  uses = "actions/gcloud/cli@master"
  args = ["auth", "configure-docker", "--quiet"]
}





