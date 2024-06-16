import argparse
import json
import subprocess
import logging.handlers
from progressbar import *


def create_logger():
    logger = logging.getLogger('root')
    stream_handler = logging.StreamHandler()
    file_handler = logging.handlers.RotatingFileHandler(
        'generate_docs.log',
        maxBytes=1048576,
        backupCount=30,
    )
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.INFO)
    return logger


_LOG = create_logger()


def generate_documentation(
        tool_name: str,
        commands_def_path: str,
        result_md_path: str | None = None,
) -> None:
    result_md_path = result_md_path or '.'
    helps_array = []
    if not os.path.isfile(commands_def_path):
        _LOG.error(
            f'Specified path to the commands file "{commands_def_path}" '
            f'is not valid!'
        )
        return
    with open(commands_def_path, 'r+') as f:
        command_def = json.load(f).get('commands')

    PROGRESS_WIDGET = ['Gathering helps | ', Percentage(), ' | ', ETA()]
    pbar = ProgressBar(widgets=PROGRESS_WIDGET, maxval=len(command_def.keys()))
    pbar.start()
    progress_bar_iterator = 0
    # ========================= Logic part =====================================
    for cmd_name in command_def.keys():
        help_string = f'{tool_name} {cmd_name}'
        raw_help = subprocess.check_output(
            help_string + ' --full-help',
            stderr=subprocess.STDOUT,
            shell=True,
        ).decode('utf-8')
        if raw_help.startswith('You are using an outdated version of m3-cli'):
            raw_help = '\n'.join(raw_help.split('\n')[3:])
        helps_array.append('*' + help_string + '*' + os.linesep + raw_help)
        # ===================== Logic part =====================================
        progress_bar_iterator += 1
        pbar.update(progress_bar_iterator)
    pbar.finish()

    result_md_path = os.path.join(result_md_path, f'{tool_name}.md')
    with open(result_md_path, 'w+') as f:
        f.write(os.linesep.join(helps_array))
    _LOG.info(
        f'Result doc file has been successfully created by path: '
        f'{result_md_path}'
    )


parser = argparse.ArgumentParser()
parser.add_argument(
    '-name', '--tool_name', type=str, required=True,
    help='The name of the tool for which the doc will be genarated'
)
parser.add_argument(
    '-cmd_path', '--commands_def_path', type=str, required=True,
    help='The path to the file "commands_def.json"'
)
parser.add_argument(
    '-res_path', '--result_md_path', type=str,
    help='The path to the result file MD file'
)
try:
    generate_documentation(**vars(parser.parse_args()))
except Exception as ex:
    _LOG.exception(ex)
