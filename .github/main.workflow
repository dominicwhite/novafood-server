workflow "Build and Deploy" {
  on = "push"
  resolves = ["Push image to GCR", "Setup Google Cloud"]
}

# Build

action "Build Docker image" {
  uses = "actions/docker/cli@master"
  args = ["build", "-t", "novafood-api", "."]
}


# GKE

action "Setup Google Cloud" {
  uses = "actions/gcloud/auth@master"
  secrets = ["GCLOUD_AUTH"]
}

action "Tag image for GCR" {
  needs = ["Setup Google Cloud", "Build Docker image"]
  uses = "actions/docker/tag@master"
  env = {
    PROJECT_ID = "mattva01-generic"
    APPLICATION_NAME = "novafood-server"

    # Build

    # GKE
  }
  args = ["novafood-api", "gcr.io/$PROJECT_ID/$APPLICATION_NAME"]
}

action "Set Credential Helper for Docker" {
  needs = ["Setup Google Cloud", "Tag image for GCR"]
  uses = "actions/gcloud/cli@master"
  args = ["auth", "configure-docker", "--quiet"]
}

action "Push image to GCR" {
  needs = ["Set Credential Helper for Docker"]
  uses = "actions/gcloud/cli@master"
  runs = "sh -c"
  env = {
    PROJECT_ID = "mattva01-generic"
    APPLICATION_NAME = "novafood-server"

    # Build

    # GKE
  }
  args = ["docker push gcr.io/$PROJECT_ID/$APPLICATION_NAME"]
}

# TOD Deploy to kubectl cluster
