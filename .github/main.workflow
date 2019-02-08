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
  needs = ["Build Docker image"]
  uses = "actions/docker/tag@master"
  env = {
    PROJECT_ID = "mattva01-generic"
    APPLICATION_NAME = "novafood-server"

    # Build

    # GKE
  }
  args = ["novafood-api", "gcr.io/$PROJECT_ID/$APPLICATION_NAME"]
}

action "Better tagging" {
  needs = ["Tag image for GCR"]
  uses = "actions/docker/cli@master"
  env = {
    PROJECT_ID = "mattva01-generic"
    APPLICATION_NAME = "novafood-server"
  }
  args = "tag novafood-api gcr.io/$PROJECT_ID/$APPLICATION_NAME:$IMAGE_SHA-$IMAGE_REF"
}

action "Set Credential Helper for Docker" {
  needs = ["Setup Google Cloud"]
  uses = "actions/gcloud/cli@master"
  args = ["auth", "configure-docker", "--quiet"]
}

action "Push image to GCR" {
  needs = ["Set Credential Helper for Docker", "Better tagging"]
  uses = "actions/gcloud/cli@master"
  runs = "sh -c"
  env = {
    PROJECT_ID = "mattva01-generic"
    APPLICATION_NAME = "novafood-server"
  }
  args = "echo \"$PROJECT_ID/$APPLICATION_NAME:$IMAGE_SHA-$IMAGE_REF\""
}

# TOD Deploy to kubectl cluster
