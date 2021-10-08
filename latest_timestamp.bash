#!/bin/bash
tail -n 42 dundee_port_data.json | grep "timestamp" | awk '{print $2}' | sed s/,// | xargs -I {} echo "{}/1000" | bc | xargs -I {} date -d @{}
