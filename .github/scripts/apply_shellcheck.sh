#!/bin/bash

set -u

apply_shellcheck() {
  local filename=${1:?}
  local code=${2:-""}
  echo "Applying ${code} on ${filename}"
  shellcheck -i "${code}" "${filename}" -f diff | git apply
}

file=${1:?}  # File to fix shellcheck errors
apply_shellcheck "${file}" SC2292  # Prefer [[ ]] over [ ] for tests in Bash/Ksh
apply_shellcheck "${file}" SC2250  # Prefer putting braces around variable e.g. ${variable}
apply_shellcheck "${file}" SC2248  # Prefer double quoting
apply_shellcheck "${file}" SC2086  # Double quote to prevent globbing and word splitting
