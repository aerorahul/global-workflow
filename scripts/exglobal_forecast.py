#!/usr/bin/env python3

import os
from pygw import Logger
from pygfs.task.gfs_forecast import GFSForecast as Forecast


if __name__ == '__main__':

    # initialize logger
    logger = Logger()

    # instantiate the forecast
    fcst = Forecast(os.environ)

