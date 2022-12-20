#! /usr/bin/env bash

source "${HOMEgfs}/ush/preamble.sh"

###############################################################
# Source FV3GFS workflow modules
. "${HOMEgfs}/ush/load_fv3gfs_modules.sh"
status=$?
[[ "${status}" -ne 0 ]] && exit "${status}"

export job="fcst"
export jobid="${job}.$$"

###############################################################
# exglobal_forecast.py requires the following in PYTHONPATH
# This will be moved to a module load when ready
pygwPATH="${HOMEgfs}/ush/python:${HOMEgfs}/ush/python/pygw/src"
[[ -n ${PYTHONPATH:-} ]] && PYTHONPATH="${PYTHONPATH}:${pygwPATH}" || PYTHONPATH="${pygwPATH}"
export PYTHONPATH

###############################################################
# Execute the JJOB
"${HOMEgfs}/jobs/JGLOBAL_FORECAST"
status=$?

exit "${status}"
