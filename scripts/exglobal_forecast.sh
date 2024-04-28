#! /usr/bin/env bash

################################################################################
## UNIX Script Documentation Block
## Script name:         exglobal_forecast.sh
## Script description:  Runs a global UFS-weather-model forecast
##
## Author:   Fanglin Yang       Organization: NCEP/EMC       Date: 2016-11-15
## Abstract: This script runs a single GFS forecast with UFS-weather-model
##
## Script history log: (See git log for detailed history)
## 2016-11-15  Fanglin Yang   First Version.
##
## Attributes:
##   Language: Bourne Again SHell
##   Machines: This script is platform independent
##
## Usage (Arguments)
##	No command line argument
##
## Data input (location, name)  TODO: Need to complete this for each component
## 	Warm start files:
## 		1. restart file except sfc_data, $gmemdir/RESTART/$PDY.$cyc.*.nc
##		2. sfcanl_data, $memdir/RESTART/$PDY.$cyc.*.nc
##		3. coupler_res, $gmemdir/RESTART/$PDY.$cyc.coupler.res
##		4. increment file, $memdir/${CDUMP}.t${cyc}z.atminc.nc
##			OR $DATA/INPUT/fv3_increment.nc
##	Cold start files:
##		1. initial condition, $memdir/INPUT/*.nc
##	Restart files:
##
##	Fix files: TODO: Need to complete this for each component
##		1. computing grid, ${FIXgfs}/orog/$CASE/${CASE}_grid.tile${n}.nc
##		2. orography data, ${FIXgfs}/orog/$CASE/${CASE}.mx${OCNRES}_oro_data.tile${n}.nc
##		3. mosaic data, ${FIXgfs}/orog/$CASE/${CASE}_mosaic.nc
##		4. Global O3 data, ${FIXgfs}/am/${O3FORC}
##		5. Global H2O data, ${FIXgfs}/am/${H2OFORC}
##		6. Global solar constant data, ${FIXgfs}/am/global_solarconstant_noaa_an.txt
##		7. Global surface emissivity, ${FIXgfs}/am/global_sfc_emissivity_idx.txt
##		8. Global CO2 historical data, ${FIXgfs}/am/global_co2historicaldata_glob.txt
##		8. Global CO2 monthly data, ${FIXgfs}/am/co2monthlycyc.txt
##		10. Additional global CO2 data, ${FIXgfs}/am/fix_co2_proj/global_co2historicaldata
##		11. Climatological aerosol global distribution
##			${FIXgfs}/am/global_climaeropac_global.txt
## 		12. Monthly volcanic forcing ${FIXgfs}/am/global_volcanic_aerosols_YYYY-YYYY.txt
##
## Data output (location, name) TODO: Need to complete this for each component
##	If quilting=true and output grid is gaussian grid:
##	   1. atmf data, $memdir/${CDUMP}.t${cyc}z.atmf${FH3}.$OUTPUT_FILE
##	   2. sfcf data, $memdir/${CDUMP}.t${cyc}z.sfcf${FH3}.$OUTPUT_FILE
##	   3. logf data, $memdir/${CDUMP}.t${cyc}z.logf${FH3}.$OUTPUT_FILE
##
## Status output
##	0: Normal
##	others: Error
################################################################################

source "${USHgfs}/preamble.sh"

# include all subroutines. Executions later.
source "${USHgfs}/forecast_predet.sh" 	# include functions for variable definition
source "${USHgfs}/forecast_det.sh"  # include functions for run type determination
source "${USHgfs}/forecast_postdet.sh"	# include functions for variables after run type determination
source "${USHgfs}/parsing_ufs_configure.sh"	 # include functions for ufs_configure processing

source "${USHgfs}/atparse.bash"  # include function atparse for parsing @[XYZ] templated files

# Coupling control switches, for coupling purpose, off by default
cpl=${cpl:-.false.}
cplflx=${cplflx:-.false.} # default off,import from outside source
cplwav=${cplwav:-.false.} # ? how to control 1-way/2-way?
cplchm=${cplchm:-.false.} # Chemistry model
cplice=${cplice:-.false.} # ICE model

OCNTIM=${OCNTIM:-1800}
DELTIM=${DELTIM:-450}
ICETIM=${DELTIM}

CPL_SLOW=${CPL_SLOW:-${OCNTIM}}
CPL_FAST=${CPL_FAST:-${ICETIM}}

echo "MAIN: Loading common variables before determination of run type"
common_predet

echo "MAIN: Loading variables before determination of run type"
FV3_predet
[[ ${cplflx} = .true. ]] && CMEPS_predet
[[ ${cplflx} = .true. ]] && MOM6_predet
[[ ${cplwav} = .true. ]] && WW3_predet
[[ ${cplice} = .true. ]] && CICE_predet
[[ ${cplchm} = .true. ]] && GOCART_predet
echo "MAIN: Variables before determination of run type loaded"

echo "MAIN: Determining run type"
UFS_det
echo "RERUN = ${RERUN}, warm_start = ${warm_start}"
echo "MAIN: run type determined"

echo "MAIN: Post-determination set up of run type"
FV3_postdet
[[ ${cplflx} = .true. ]] && CMEPS_postdet
[[ ${cplflx} = .true. ]] && MOM6_postdet
[[ ${cplwav} = .true. ]] && WW3_postdet
[[ ${cplice} = .true. ]] && CICE_postdet
[[ ${cplchm} = .true. ]] && GOCART_postdet
echo "MAIN: Post-determination set up of run type finished"

echo "MAIN: Writing namelists and model configuration"
FV3_nml
[[ ${cplflx} = .true. ]] && MOM6_nml
[[ ${cplwav} = .true. ]] && WW3_nml
[[ ${cplice} = .true. ]] && CICE_nml
[[ ${cplchm} = .true. ]] && GOCART_rc
UFS_configure
echo "MAIN: Name lists and model configuration written"

#------------------------------------------------------------------
# run the executable

if [[ "${esmf_profile:-}" = ".true." ]]; then
  export ESMF_RUNTIME_PROFILE=ON
  export ESMF_RUNTIME_PROFILE_OUTPUT=SUMMARY
fi

if [[ "${USE_ESMF_THREADING:-}" == "YES" ]]; then
  unset OMP_NUM_THREADS
else
  export OMP_NUM_THREADS=${UFS_THREADS:-1}
fi

${NCP} "${EXECgfs}/${FCSTEXEC}" "${DATA}/"
${APRUN_UFS} "${DATA}/${FCSTEXEC}" 1>&1 2>&2
export ERR=$?
export err=${ERR}
${ERRSCRIPT} || exit "${err}"

FV3_out
[[ "${cplflx}" == ".true." ]] && MOM6_out
[[ "${cplflx}" == ".true." ]] && CMEPS_out
[[ "${cplwav}" == ".true." ]] && WW3_out
[[ "${cplice}" == ".true." ]] && CICE_out
[[ "${cplchm}" == ".true." ]] && GOCART_out
[[ "${cplchm}" == ".true." ]] && GOCART_out
[[ "${esmf_profile:-}" == ".true." ]] && CPL_out
echo "MAIN: Output copied to ROTDIR"

#------------------------------------------------------------------

exit "${err}"
