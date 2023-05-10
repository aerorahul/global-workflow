import os
import tempfile

from .executable import which

__all__ = ['Hpss', 'hsi', 'htar']

class Hpss:
    def __init__(self, *args, **kwargs):
        pass

    def contents(self):
        pass


def ls(path):
    return Hpss.contents(path)


def isdir(path):
    return Hpss.isdir(path)


def isfile(path):
    return Hpss.isfile(path)


def islink(path):
    return Hpss.islink(path)


def hsi(*args):
    """
    Wrapper for hpss.hsi
    Parameters
    ----------
    args

    Returns
    -------
    stdout, stderr from `hsi` command
    """

    tmpdir = tempfile.gettempdir()
    tmpfile = os.path.join(tmpdir, 'hsi.txt')

    cmd = which('hsi', required=True)
    cmd.add_default_arg(f"-O {tmpfile}")  # place stdout, stderr from hsi commands to this file
    for arg in args:
        cmd.add_default_arg(arg)

    # Make the hsi call
    cmd()

    # Read the stdout, stderr from the tmpfile
    with open(tmpfile) as fh:
        stdout = fh.read()

    # Remove the tmpfile
    os.remove(tmpfile)

    return stdout


def htar(*args):
    """
    Wrapper for hpss.htar
    Parameters
    ----------
    args

    Returns
    -------
    stdout, stderr from `htar` command
    """

    tmpdir = tempfile.gettempdir()
    stdout = os.path.join(tmpdir, 'htar.stdout')
    stderr = os.path.join(tmpdir, 'htar.stderr')

    cmd = which('htar', required=True)
    for arg in args:
        cmd.add_default_arg(arg)

    cmd(output=str(stdout), error=str(stderr))

    with open(stdout) as fho, open(stderr) as fhe:
        out = fho.read()
        err = fhe.read()

    # Remove the tmp files
    os.remove(stdout)
    os.remove(stderr)

    return out, err
