#!/bin/sh
docker run --name dserver --rm -p 4000:4000 -v $(pwd)/testex:/app/testex:z -it --entrypoint "sh" testex
