#!/bin/bash
shuf -i 0-240 -n 1 | xargs -I '{}' sleep {}
cd /home/fraz/github/marine_traffic_scraper && /usr/local/bin/node index.js
