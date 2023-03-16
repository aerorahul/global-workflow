import os
import logging
from typing import Dict, List

from pprint import pprint
from pygw.attrdict import AttrDict
from pygw.task import Task
from pygw.logger import logit
from pygw.file_utils import FileHandler
from pygw.file_utils import FileHandler
from pygw.template import Template, TemplateConstants
from pygw.yaml_file import YAMLFile
from pygfs import ufswm

logger = logging.getLogger(__name__.split('.')[-1])


class GFSForecast(Task):
    """
    UFS-weather-model forecast task for the GFS
    """

    @logit(logger, name="GFSForecast")
    def __init__(self, config, *args, **kwargs):
        """
        Parameters
        ----------
        config : Dict
                 dictionary object containing configuration from environment

        *args : tuple
                Additional arguments to `Task`

        **kwargs : dict, optional
                   Extra keyword arguments to `Task`
        """

        super().__init__(config, *args, **kwargs)

    @logit(logger)
    def initialize(self):
        """
        Initialize methods for a task
        """

        # Collect items needed for the model from the config
        self.ufs_config = self._get_ufs_config()

        # Initialize the model
        self.ufs = ufswm.UFSWM(self.ufs_config)

        self.stage()

    @logit(logger)
    def configure(self):
        """
        Configuration methods for a task in preparation for execution
        """
        self._configure_model_configure()
        self._configure_nems_configure()
        self._configure_input_nml()

        # self._stage_ics()  # TODO: should stage_ics be here or in ufswm.py?

    @logit(logger)
    def execute(self):
        """
        Execute methods for a task
        """
        pass

    @logit(logger)
    def finalize(self):
        """
        Methods for after the execution that produces output task
        """
        pass

    @logit(logger)
    def clean(self):
        """
        Methods to clean after execution and finalization prior to closing out a task
        """
        pass

    @logit(logger)
    def _get_ufs_config(self):

        cfg = AttrDict()

        # Get fix files
        FIX_dir = os.path.join(self.config.HOMEgfs, 'fix')
        cfg.FIX_am = os.path.join(FIX_dir, 'am')
        cfg.FIX_aer = os.path.join(FIX_dir, 'aer')
        cfg.FIX_orog = os.path.join(FIX_dir, 'orog')
        cfg.FIX_ugwd = os.path.join(FIX_dir, 'ugwd')
        cfg.FIX_lut = os.path.join(FIX_dir, 'lut')

        # Get and read the relevant config yaml file
        cfg.ufs_config_yaml = self.config.UFS_CONFIG_YAML
        cfg.ufs_config_dict = YAMLFile(path=cfg.ufs_config_yaml)

        # Get and set static parameters
        cfg.atm_levs = self.config.get('LEVS')
        cfg.atm_res = self.config.get('CASE')
        cfg.ocn_res = self.config.get('OCNRES')
        cfg.ice_res = self.config.get('ICERES')

        cfg.fhmax = self.config.FHMAX

        cfg.do_iau = self.config.get('DOIAU', False)
        if cfg.do_iau:
            cfg.iau_offset = self.config.get('IAU_OFFSET', 6)

        return cfg



    @logit(logger)
    def stage(self):
        """
        Super method for staging static and templated data
        """

        # Create the empty directories
        stage_yaml = self.ufs_config.ufs_config_dict.stage
        conf = AttrDict()
        conf.DATA = self.runtime_config.DATA

        stage_data = Template.substitute_structure(
            stage_yaml, TemplateConstants.DOLLAR_PARENTHESES, conf.get)
        FileHandler(stage_data).sync()

        # Stage static and fix data to $(DATA)
        # self._stage_fix()  # TODO: temporarily disable copying fix files to speed up testing.

        # Stage diag_table.tmpl to $(DATA)
        self._stage_tables(table='diag_table', target='diag_table.tmpl')

        # Stage field_table to $(DATA)
        self._stage_tables(table='field_table', target='field_table')

        # Stage model_configure, nems.configure, input.nml etc. to $(DATA)
        self._stage_configs()

    def _stage_fix(self):

        # Get the stage section from ufs_config_dict
        fix_yaml = self.ufs_config.ufs_config_dict.fix

        # Construct the conf dict for staging
        conf = AttrDict()
        conf.HOMEgfs = self.config.HOMEgfs
        conf.DATA = self.runtime_config.DATA
        conf.atm_res = self.ufs_config.atm_res
        conf.ocn_res = self.ufs_config.ocn_res
        conf.FIX_orog = self.ufs_config.FIX_orog
        conf.FIX_am = self.ufs_config.FIX_am
        conf.FIX_aer = self.ufs_config.FIX_aer
        conf.FIX_ugwd = self.ufs_config.FIX_ugwd
        conf.FIX_lut = self.ufs_config.FIX_lut

        fix_data = Template.substitute_structure(
            fix_yaml, TemplateConstants.DOLLAR_PARENTHESES, conf.get)
        FileHandler(fix_data).sync()

    def _stage_tables(self, table, target):
        """
        Prepare diag_table.tmpl and field_table for staging
        """

        # Get the name of the diag_tables from ufs_config_dict
        yaml = self.ufs_config.ufs_config_dict.get(table)

        conf = AttrDict()
        conf.HOMEgfs = self.config.HOMEgfs
        tables = Template.substitute_structure(
            yaml, TemplateConstants.DOLLAR_PARENTHESES, conf.get)

        destination = os.path.join(
            self.runtime_config.get('DATA'), target)

        # Loop over the tables and concatenate into the target
        with open(destination, 'w') as fh:
            for tt in tables:
                with open(tt, 'r') as fih:
                    fh.write(fih.read())

    def _stage_configs(self):
        """
        Fetch and stage model_configure, nems.configure and input.nml into $(DATA)
        """

        conf = AttrDict()
        conf.HOMEgfs = self.config.HOMEgfs
        conf.DATA = self.runtime_config.DATA

        # Extract and stage these configs (there may be more)
        wanted = ['model_configure', 'nems_configure', 'input_nml']
        yaml = AttrDict(
            (kk, self.ufs_config.ufs_config_dict[kk]) for kk in wanted)

        configs = Template.substitute_structure(
            yaml, TemplateConstants.DOLLAR_PARENTHESES, conf.get)
        for key in configs.keys():
            FileHandler(configs[key]).sync()

    def _configure_model_configure(self):
        conf = AttrDict()
        pass

    def _configure_nems_configure(self):
        """
        Read in nems.configure.tmpl, substitute the templated variables and write out nems.configure
        """

        conf = AttrDict()

        # Handle atmosphere
        conf.atm_model = 'fv3'
        conf.atm_petlist_bounds = self.config.ATMPETS

        # TODO: add other keys to conf depending on configuration e.g. ocean, ice, waves, etc.

        nems_file_in = os.path.join(self.runtime_config.DATA, 'nems.configure.tmpl')
        nems_file_out = os.path.join(self.runtime_config.DATA, 'nems.configure')

        with open(nems_file_in, 'r') as fhi, open(nems_file_out, 'w') as fho:
            nems_in = fhi.read()
            nems_out = Template.substitute_structure(
                nems_in, TemplateConstants.AT_SQUARE_BRACES, conf.get)
            fho.write(nems_out)

    def _configure_input_nml(self):
        pass
