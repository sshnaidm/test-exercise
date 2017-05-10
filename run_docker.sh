#!/bin/bash
docker run --name server -p 4000:4000 -v $(pwd)/testex:/app/testex:z -e "FLASK_DEBUG=false" -d testex
