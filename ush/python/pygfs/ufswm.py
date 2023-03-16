import os
import re
import logging
from pprint import pprint
from typing import Dict, Any, List

from pygw.attrdict import AttrDict
from pygw.yaml_file import YAMLFile
from pygw.logger import logit

logger = logging.getLogger(__name__.split('.')[-1])


class UFSWM:

    @logit(logger, name="UFSWM")
    def __init__(self, config):

        self.config = config

        # ufs_config = config.get('UFS_CONFIG_FILE')
        # ufs_yaml = YAMLFile(ufs_config)

        self.atm = self._setup_atm(
            atm_res=config.atm_res, atm_levs=config.atm_levs)
        # self.restart_interval = self.get_restart_interval()
        # pprint(self.restart_interval)

    @staticmethod
    @logit(logger)
    def _setup_atm(atm_res: str = 'C48', atm_levs: int = 128, ntiles: int = 6) -> Dict[str, Any]:

        atm = AttrDict()
        atm.ntiles = ntiles

        # FV3 specific variables
        atm.res = atm_res
        _res = int(atm_res[1:])
        atm.jcap = 2 * _res - 2
        atm.lonb = 4 * _res
        atm.latb = 2 * _res
        atm.npx = _res + 1
        atm.npy = _res + 1
        atm.npz = atm_levs - 1

        return atm

    @logit(logger)
    def _setup_nsst(self):
        nsst = AttrDict({
            'model': 0,
            'spinup': 0,
            'resv': 0,
            'zsea1': 0,
            'zsea2': 0})

        return nsst

    @logit(logger)
    def get_restart_interval(self):

        cdump = self.runtime_config.get('CDUMP', 'gdas')
        do_iau = self.config.do_iau
        offset = self.config.iau_offset

        restart_interval = None

        if cdump in ['gdas']:
            restart_interval = [3, 6] if do_iau else [6]

        if cdump in ['gfs']:
            rint = self.config.get('restart_interval_gfs', 12)
            fhmax = self.config.get('FHMAX_GFS', 120)
            restart_interval = self.get_restart_interval_hours(rint, fhmax, offset)

        return restart_interval

    def get_time_vars(self):

        fhmin = self.config.get('FHMIN', 0)
        fhout_hf = self.config.get('FHOUT_HF', 0)
        fhmax_hf = self.config.get('FHMAX_HF', 0)
        fhmax = self.config.get('FHMAX')
        fhout = self.config.get('FHOUT')

        output_fhrs = self.get_output_hours(fhmin, fhmax_hf, fhout_hf, fhmax, fhout)
        offset = self.config.iau_offset
        fhrot = int(offset / 2.)
        restart_interval = self.get_restart_interval(self.config.restart_interval, fhmax, offset)


        return None

    @logit(logger)
    def get_restart_time(self):
        restart_dir = self.config.ROTDIR

        # Find all matching YYYYMMDD.HH0000.coupler.res files in restart_dir
        files = [ff for ff in os.listdir(restart_dir) if re.match(
            r'(\d{4})(\d{2})(\d{2}).(\d{2})0000.coupler.res', ff)]

        return None

    def fv3(self):
        pass

    def mom6(self):
        pass

    def cice6(self):
        pass

    def ww3(self):
        pass

    def model_configure(self):
        pass

    def nems_configure(self):
        nems_configure_file = self.config.get('')
        pass

    def fv3_INPUT_files(self):
        # This information could be in a yaml file, but these are resolution dependent
        grid_spec = 'grid_spec.nc'
        grid_data = [f'grid.tile{nn}.nc' for nn in range(1, self.fv3.ntiles+1)]
        oro_data = [f'oro_data.tile{nn}.nc' for nn in range(
            1, self.fv3.ntiles+1)]

    def fv3_ics(self):

        cold_ics = ['gfs_ctrl.nc'] + \
                   [f'gfs_data.tile{nn}.nc' for nn in range(1, self.fv3.ntiles+1)] + \
                   [f'sfc_data.tile{nn}.nc' for nn in range(
                       1, self.fv3.ntiles+1)]

        warm_ics = ['coupler.res', 'fv_core.res.nc']
        ftypes = ['fv_core.res', 'fv_srf_wnd.res',
                  'fv_tracer.res', 'phy_data', 'sfc_data', 'ca_data']
        warm_ics += [
            f'{ftype}.tile{nn}.nc' for ftype in ftypes for nn in range(1, self.fv3.ntiles+1)]

        ics = warm_ics if self.warm_start else cold_ics

        return ics

    @staticmethod
    def model_configure_defaults() -> AttrDict:
        cfg = AttrDict()
        return cfg

    def setup_model_configure(self):
        """
        return dictionary extracting elements for model_configure
        """

        model_configure_yaml = os.path.join(
            self.config.HOMEgfs, 'parm/ufs/model_configure.yaml')
        cfg = YAMLFile(path=model_configure_yaml)

        def _to_F90Bool(logical):
            return ".true." if logical else ".false."

        cfg = AttrDict()

        cfg.QUILTING = _to_F90Bool(self.config.QUILTING)
        cfg.WRITE_GROUP = self.config.WRITE_GROUP
        cfg.WRTTASK_PER_GROUP = self.config.WRTTASK_PER_GROUP
        cfg.ITASKS = 1
        cfg.IDEFLATE = 1
        # There is no use case where this is .false.
        cfg.OUTPUT_HISTORY = ".true."
        cfg.WRITE_DOPOST = _to_F90Bool(self.config.WRITE_DOPOST)
        cfg.WRITE_NSFLIP = ".true."

        cfg.NUM_FILES = self.config.
        cfg. = self.config.
        cfg. = self.config.
        cfg. = self.config.
        cfg. = self.config.
        cfg. = self.config.

        return None

    @staticmethod
    def get_output_hours(fhmin: int, fhmax_hf: int, fhout_hf: int, fhmax: int, fhout: int) -> List:
        """
        Return a list of forecast hours given bounds and high and low frequency output

        Parameters
        ----------
        fhmin : int
           Minimum forecast hour (typically 0)
        fhmax_hf : int
            Maximum forecast hour for high frequency output
        fhout_hf : int
            Forecast interval for high frequency output
            Interval must be > 0
        fhmax : int
            Maximum forecast length
        fhout : int
            Forecast interval for low (regular) frequency output
            Interval must be > 0

        Returns
        -------
        List
            List of forecast hours at which forecast will be output
        """

        if 0 in (fhout, fhout_hf):
            raise ValueError(
                f'Forecast output frequency fhout={fhout}, fhout_hf={fhout_hf} cannot be 0')

        fhrs_hf = range(fhmin, fhmax_hf + fhout_hf, fhout_hf)
        fhrs_lf = range(fhrs_hf[-1] + fhout, fhmax + fhout, fhout)
        fhrs = list(fhrs_hf) + list(fhrs_lf)

        return fhrs

    @staticmethod
    def get_restart_interval_hours(interval: int, fhmax: int, offset: int = 0) -> List:
        """
        Return a list of forecast hours at which to write out restarts

        Parameters
        ----------
        interval : int
            Interval between restarts
        fhmax : int
            Maximum forecast length
        offset : int
            Offset from the interval to start the list, by default 0

        Returns
        -------
        List
            List of forecast hours at which restarts will be written out
        """

        start = interval + int(offset / 2.)  # This assumes offset bisects the window and should be even
        restart_interval = range(start, fhmax, interval)

        return list(restart_interval)
