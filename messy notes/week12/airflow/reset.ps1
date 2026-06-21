$env:DOCKER_CONFIG = Join-Path $PSScriptRoot ".docker-config"
New-Item -ItemType Directory -Force -Path $env:DOCKER_CONFIG | Out-Null

docker compose down -v
docker compose up -d --build
