#!/bin/bash
grep "timestamp"  dundee_port_data.json | awk '{print $2}' | sed s/,// | xargs -I {} echo "{}/1000" | bc | xargs -I {} date -d @{}
