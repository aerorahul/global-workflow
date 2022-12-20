import logging

from pygw.attrdict import AttrDict
from pygw.task import Task
from pygw.logger import logit


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

        self.runtime_config = None


    @logit(logger)
    def initialize(self):
        """
        Initialize methods for a task
        """
        pass

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
