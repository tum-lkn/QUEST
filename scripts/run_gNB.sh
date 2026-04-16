#!/bin/bash                                                                                                                                           

# Set the route to access the core network                                                                                                            
ip_pc="10.162.83.10"
ip_cn="192.168.70.128/26"
#ip_cn="192.168.70.1/26"                                                                                                                              
sudo ip route add "$ip_cn" via "$ip_pc"

#Check if the filename is provided as an argument                                                                                                     
if [ $# -eq 0 ]; then
    echo "Usage: $0 <csv_file>"
    exit 1
fi

# Assign the first argument to the filename variable                                                                                                  
csv_file="$1"

if [ -f "$csv_file" ] ; then
    rm "$csv_file"
fi



# specify the target directory                                                                                                                        
cd /home/lkn/oai_gNB_HW_2024_w09/openairinterface5g/cmake_targets/ran_build/build

# run OAI  gNB                                                                                                                                        
sudo ./nr-softmodem -O ../../../targets/PROJECTS/GENERIC-NR-5GC/CONF/mygNB.conf --sa -E --continuous-tx --gNBs.[0].min_rxtxtime 6 --gNB.[0].enable_sd\
ap 1

