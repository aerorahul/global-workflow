#!/bin/bash

set -eu

apply_shellcheck() {
  local filename=${1:?}
  local code=${2:-""}
  echo "Applying ${code} on ${filename}"
  patch="/tmp/patch.${RANDOM}"  # Do not use PWD, as this will create tons of patch files
  [[ -f "${patch}" ]] && rm -f "${patch}"
  shellcheck -i "${code}" "${filename}" -f diff > "${patch}"
  rc=$?
  if [[ "${rc}" -ne 0 ]]; then
    git apply "${patch}"
  fi
  rm -f "${patch}"
}

file=${1:?}  # File to fix shellcheck errors
apply_shellcheck "${file}" SC2292  # Prefer [[ ]] over [ ] for tests in Bash/Ksh
apply_shellcheck "${file}" SC2250  # Prefer putting braces around variable e.g. ${variable}
apply_shellcheck "${file}" SC2248  # Prefer double quoting
apply_shellcheck "${file}" SC2086  # Double quote to prevent globbing and word splitting
