#!/bin/bash
echo
echo 'Pulling ollama phi3 model'
echo
docker exec -it ollama ollama pull phi3

echo
echo 'Pulling ollama phi3.5 model'
echo
docker exec -it ollama ollama pull phi3.5
