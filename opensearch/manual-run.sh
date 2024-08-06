docker rm -f opensearch

docker run -d \
  --name opensearch \
  -p 9200:9200 \
  -p 9600:9600 \
  -e discovery.type=single-node \
  -e OPENSEARCH_INITIAL_ADMIN_PASSWORD=aRT/[sqA7^  \
  opensearchproject/opensearch:latest