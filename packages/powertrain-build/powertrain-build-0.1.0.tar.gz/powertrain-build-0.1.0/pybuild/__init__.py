# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Main package of the pybuild application."""
from pbr.version import VersionInfo
from pathlib import Path
from pybuild.lib import logger, helper_functions
from pybuild.environmentcheck import check_python_string

LOGGER = logger.create_logger(__file__)
__version__ = VersionInfo('pt-pybuild').release_string()
LOGGER.info('Current pybuild version is %s', __version__)
__config_version__ = '0.2.1'
__required_python_lower__ = '3.6'
__required_python_upper__ = '3.10'


workspace = helper_functions.get_repo_root()
requirement_path = Path(
    workspace, 'Script', 'PyTools', 'requirements.txt'
    )
if requirement_path.exists():
    with requirement_path.open("r") as requirement_file:
        expected_package = "pt-pybuild==" + __version__
        for line in requirement_file:
            if expected_package in line:
                LOGGER.info('PyBuild version matched requirements!')
                break
            elif "pt-pybuild==" in line and expected_package not in line:
                LOGGER.warning('PyBuild version does not match requirements!')
                break

else:
    LOGGER.warning('Current repository does not have a requirement file' +
                   ' in expected location: %s', str(requirement_path))

check_python_string(__required_python_lower__, __required_python_upper__)
