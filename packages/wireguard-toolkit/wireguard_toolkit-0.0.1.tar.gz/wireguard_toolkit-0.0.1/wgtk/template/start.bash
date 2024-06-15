#! /bin/bash

set -euo pipefail
IFS=$$'\n\t'



ip link add dev ${network_name} type wireguard
ip address add dev ${network_name} ${interface_address}
wg setconf ${network_name} /etc/wireguard/${network_name}/${peer_name}.conf

ip link set up dev ${network_name}
