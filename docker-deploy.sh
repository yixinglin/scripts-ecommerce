# Stop and remove the current containter.
docker compose -f docker-compose-s.yml down

# Build and replace the previous image.
docker build --force-rm -t "yixing/ecommerce" .

# Clean unknown images
docker image prune