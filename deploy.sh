#/bin/bash

DC="docker-compose -f docker-compose.yml"

$DC build
$DC down || true
$DC up -d

docker image prune -f
exit 0