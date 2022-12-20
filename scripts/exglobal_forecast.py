#!/usr/bin/env python3

import os

from pygw.logger import Logger
from pygw.yaml_file import save_as_yaml
from pygw.configuration import cast_strdict_as_dtypedict
from pygfs.task.gfs_forecast import GFSForecast as Forecast


if __name__ == '__main__':

    # initialize root logger
    logger = Logger(level='DEBUG', colored_log=True)

    # instantiate the forecast
    config = cast_strdict_as_dtypedict(os.environ)
    save_as_yaml(config, f'{config.EXPDIR}/fcst.yaml')  # Temporarily save the input to the Forecast

    fcst = Forecast(config)

