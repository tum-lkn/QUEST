#!/bin/bash

# specify the target directory
theIPaddress=$(ip addr show oaitun_ue1| grep "inet\b" | awk '{print $2}' | cut -d/ -f1)
sudo route add default gw $theIPaddress
#sudo ifconfig oaitun_ue1 mtu 800

# ping demo container from UE
output_file="time1.csv"
{ echo "time"; ping -c 1 192.168.70.135 | grep "time=" | awk -F'=' '{print$4}';} > "$output_file" &
PID1=$!

# wait for pings to finish
if wait $PID1
then echo $IP1 is reachable, internet is working; exit 0
fi

# none reachable
echo "Core network unreachable"
exit 1


