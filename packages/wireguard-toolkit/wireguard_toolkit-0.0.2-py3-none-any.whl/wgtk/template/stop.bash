#! /bin/bash

set -euo pipefail
IFS=$$'\n\t'



ip link set down dev ${network_name}
