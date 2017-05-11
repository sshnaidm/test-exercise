Test exercise
=============

The application that returns the difference between two base64 encoded binaries

Purpose
--------
Flask based REST API which receives two base64 encoded binary data parameters
and returns difference between them.

Requirements
------------
Application is python 3 compatible. The following modules are required:
* `Flask` and `Flask-SQLAlchemy` for API
* `pycco` for documentation generation
* `pytest`, `ddt`, `flask-testing` for testing purpose

Usage:
------
You can run API server with docker:
- `./run_docker.sh` where server is running on port 4000. 
- Other option is to run it in debug mode: `./run_debug_server.sh` and when
you're inside the container, run `../run_server.sh` which will run the server
in debug mode.

API
---

Documentation
-------------
Documentation is located in `testex/docs` folder. For generating new docs, just
run `pycco testext/*py`.
