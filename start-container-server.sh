echo "docker compose $1"
docker compose -f docker-compose-s.yml $1 \
          ecommerce-gls_s ecommerce-sl_s
