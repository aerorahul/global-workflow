#! /usr/bin/env bash

HOMEgfs="$(cd "$(dirname  "${BASH_SOURCE[0]}")/.." >/dev/null 2>&1 && pwd )"

# Detect machine (sets MACHINE_ID)
source "${HOMEgfs}/ush/detect_machine.sh"
#source "${HOMEgfs}/ush/module-setup.sh"

module use ${HOMEgfs}/modulefiles
module load gw_${MACHINE_ID}.intel
module list
