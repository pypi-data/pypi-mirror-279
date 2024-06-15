#! /bin/bash

set -euo pipefail
IFS=$$'\n\t'



cp /etc/wireguard/${network_name}/control/wg-${network_name}.service /etc/systemd/system/wg-${network_name}.service
