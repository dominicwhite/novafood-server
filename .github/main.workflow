workflow "Build and Deploy" {
  on = "push"
  resolves = ["Push image to GCR", "Setup Google Cloud"]
}

# Build

action "Build Docker image" {
  uses = "actions/docker/cli@master"
  args = ["build", "-t", "gcloud-example-app", "."]
}

# Deploy Filter
action "Deploy branch filter" {
  needs = ["Set Credential Helper for Docker"]
  uses = "actions/bin/filter@master"
  args = "branch master"
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
  args = ["gcloud-example-app", "gcr.io/$PROJECT_ID/$APPLICATION_NAME"]
}

action "Set Credential Helper for Docker" {
  needs = ["Setup Google Cloud", "Tag image for GCR"]
  uses = "actions/gcloud/cli@master"
  args = ["auth", "configure-docker", "--quiet"]
}

action "Push image to GCR" {
  needs = ["Setup Google Cloud", "Deploy branch filter"]
  uses = "actions/gcloud/cli@master"
  runs = "sh -c"
  env = {
    PROJECT_ID = "mattva01-generic"
    APPLICATION_NAME = "novafood-server"

    # Build

    # GKE
  }
  args = ["docker push gcr.io/$PROJECT_ID/$APPLICATION_NAME:$GITHUB_SHA"]
}

# TOD Deploy to kubectl cluster
