from pygw.attrdict import AttrDict
from pygw.task import Task
from pygw.logger import Logger, logit


logger = Logger(__name__)

class GFSForecast(Task):
    """
    UFS-weather-model forecast task for the GFS
    """

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

        super().__init(AttrDict(config), *args, **kwargs)

        self.runtime_config = None


    def initialize(self):
        """
        Initialize methods for a task
        """
        pass

    def configure(self):
        """
        Configuration methods for a task in preparation for execution
        """
        pass

    def execute(self):
        """
        Execute methods for a task
        """
        pass

    def finalize(self):
        """
        Methods for after the execution that produces output task
        """
        pass

    def clean(self):
        """
        Methods to clean after execution and finalization prior to closing out a task
        """
        pass
