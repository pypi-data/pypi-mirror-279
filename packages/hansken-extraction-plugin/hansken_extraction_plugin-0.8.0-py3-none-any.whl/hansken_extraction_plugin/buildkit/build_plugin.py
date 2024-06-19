"""Contains a cmd entry point to create a plugin docker image with plugin info labels."""
from shlex import join
import signal
import subprocess  # nosec
import sys

from logbook import INFO, Logger, StreamHandler  # type: ignore

from hansken_extraction_plugin.buildkit.build_utils import _plugin_info_to_labels
from hansken_extraction_plugin.framework import GRPC_API_VERSION
from hansken_extraction_plugin.runtime.reflection_util import get_plugin_class

logger = Logger(__name__)

usage_explanation = ('\033[0;31mWARNING\033[0;0m: This script is deprecated, please use `label_plugin` instead!\n'
                     '         Note that `label_plugin` is not a full drop- in replacement for this script.\n'
                     '         Please read its help-documentation for its usage.\n'
                     '\n'
                     'Usage: {} [-h] [--help] PLUGIN_FILE DOCKER_FILE_DIRECTORY [DOCKER_IMAGE_NAME] [DOCKER_ARGS]\n'
                     '  PLUGIN_FILE: Path to the python file of the plugin.\n'
                     '  DOCKER_FILE_DIRECTORY: Path to the directory containing the Dockerfile of the plugin.\n'
                     '  (Optional) [DOCKER_IMAGE_NAME]: Name of the docker image without tag. Note that docker '
                     'image names cannot start with a period or dash.\n '
                     '                                 If it starts with a dash, it will be '
                     'interpreted as an additional docker argument (see next).\n'
                     '  (Optional) [DOCKER_ARGS]: Additional arguments for the docker command, which can be as '
                     'many arguments as you like.\n\n'
                     'Example: build_plugin plugin.py . imagename --build-arg https_proxy="$https_proxy"')


def _log(message):
    logger.info(f'{message}')


def _log_error(e):
    logger.error(f'\033[0;31mAn error occurred\033[0;0m: {e}')


def _signal_handler(sig, frame):
    logger.error('\033[0;31mBUILD PLUGIN WAS INTERRUPTED\033[0;0m')
    raise InterruptedError('Build plugin was interrupted')


def _build(plugin_class, docker_file, name=None, docker_args=None) -> int:
    """
    Build an Extraction Plugin docker image according to provided arguments.

    :param plugin_class:  The class implementing BaseExtractionPlugin
    :param docker_file: Path to the directory containing the Dockerfile of the plugin.
    :param name: Name of the docker image without tag. Note that docker
            image names cannot start with a period or dash. If it starts with a dash, it will be
            interpreted as an additional docker argument (see next).
    :param docker_args: Additional arguments for the docker command, which can be as
            many arguments as you like.
    :return: returncode of the docker command
    """
    plugin_info = plugin_class().plugin_info()
    api_version = GRPC_API_VERSION
    labels = _plugin_info_to_labels(plugin_info, api_version)

    name = name or f'extraction-plugins/{plugin_info.id}'

    command = ['docker', 'build',
               docker_file,
               '-t', f'{name}:{plugin_info.version}'.lower(),
               '-t', f'{name}:latest'.lower()]

    for (label, value) in labels.items():
        command.append('--label')
        command.append(f'{label}={value}')

    command.extend(docker_args)

    _log(f'ILD_PLUGIN] Invoking Docker build with command: {join(command)}')

    # execute the command
    process = subprocess.run(command)  # nosec

    if process.returncode != 0:
        _log_error(f'Docker build failed (command was: {join(command)})\n')
    else:
        _log('Docker build finished')
    return process.returncode


def _build_using_plugin_file(plugin_file, docker_file, name=None, docker_args=None):
    plugin_class = get_plugin_class(plugin_file)
    return _build(plugin_class, docker_file, name, docker_args)


def _parse_args(argv):
    argcount = len(argv)
    if argcount > 0 and (argv[0] == '-h' or argv[0] == '--help'):
        print(usage_explanation)
        return None

    if argcount < 2:
        if argcount != 0:
            _log_error('Wrong number of arguments!\n')
        print(usage_explanation)
        return None

    plugin_file = argv[0]
    docker_file = argv[1]
    # oci image names cannot start with a dash, so if this arg starts with a dash
    # omit the name arg and expect it to be an extra docker arg
    omit_name = len(argv) <= 2 or argv[2].startswith('-')
    name = None if omit_name else argv[2]
    docker_args_start_pos = 2 if omit_name else 3
    docker_args = [] if len(argv) <= docker_args_start_pos else argv[docker_args_start_pos:]
    return plugin_file, docker_file, name, docker_args


def main():
    """Label an Extraction Plugin docker image according to provided arguments."""
    signal.signal(signal.SIGINT, _signal_handler)

    log_handler = StreamHandler(sys.stdout, level=INFO)
    log_handler.format_string = '\033[0;34m[BUILD PLUGIN]\033[0;0m {record.message}'
    with log_handler.applicationbound():
        parsed = _parse_args(sys.argv[1:])
        try:
            if parsed:
                plugin_file, docker_file, name, docker_args = parsed
                sys.exit(_build_using_plugin_file(plugin_file, docker_file, name, docker_args))
            else:
                sys.exit(1)
        except Exception as e:
            _log_error(e)
            sys.exit(1)


if __name__ == '__main__':
    main()
