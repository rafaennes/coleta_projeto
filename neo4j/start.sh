sudo docker run --rm -e NEO4J_AUTH=none -e 'NEO4J_PLUGINS=["apoc"]' -p 7474:7474 -v $PWD/plugins:/plugins -p 7687:7687 neo4j:5.19.0
