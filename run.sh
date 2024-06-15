# SERVER | DOCKERFILE
export PORT=8080
export NUM_WORKERS=1
export NUM_THREADS=1
export MAX_REQUESTS=100
export MAX_REQUESTS_JITTER=1

# APPLICATION
export CLOUD=False
export PROJECT_ID=default

# COMPOSE
export DOCKERFILE=dev.Dockerfile

# IF PRIVATE REPO IS NEEDED
PRIVATE_REPO=some-repo
REGION=us-central1
# export PRIVATE_ARTIFACT_REPOSITORY="https://oauth2accesstoken:$(gcloud auth print-access-token)@${REGION}-python.pkg.dev/${PROJECT_ID}/${REPO}/simple/"

docker compose -f compose.yaml up --build -w

docker compose down