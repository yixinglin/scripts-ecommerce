# Stop and remove the current containter.
docker stop ecommerce
docker rm ecommerce

# Build and replace the previous image.
docker build --force-rm -t "yixing/ecommerce" .

# Clean unknown images
docker image prune