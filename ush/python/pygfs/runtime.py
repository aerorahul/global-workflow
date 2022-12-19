from pygw.attrdict import AttrDict
from pygw.timetools import *

def set_runtime_config(ctx):

    cfg = AttrDict()

    keys = ['PDY', 'cyc', 'CDATE'
            'NET', 'RUN', 'CDUMP',
            'HOMEgfs',
            'DATA']

    for key in keys:
        cfg[key] = ctx.key

    return ctx
