import logging

from pprint import pprint
from pygw.attrdict import AttrDict
from pygw.task import Task
from pygw.logger import logit
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
        ufs_config = self._get_ufs_config()

        # Initialize the model
        self.ufs = ufswm.UFSWM(ufs_config)

    @logit(logger)
    def configure(self):
        """
        Configuration methods for a task in preparation for execution
        """
        pass

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
        cfg.atm_res = self.config.get('CASE', 'C48')
        cfg.atm_levs = self.config.get('LEVS', 128)

        cfg.fhmax = self.config.FHMAX

        cfg.do_iau = self.config.get('DOIAU', False)
        if cfg.do_iau:
            cfg.iau_offset = self.config.get('IAU_OFFSET', 6)

        return cfg
