"""
Command line entrypoint
"""
import argparse
import ast
import importlib
import logging
import re
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from . import __PROJECT_NAME__
from .config_loader import get_config_loader
from .configs import DEFAULT_MSORT_ORDERING_SECTION
from .configs import DEFAULT_MSORT_PARAMS_SECTION
from .configs import format_msort_response
from .formatting import format_msort
from .logger import set_logging
from .method_describers import get_method_describer


def parse_commandline() -> Tuple[argparse.Namespace, Dict[str, Any]]:
    """Parse CLI arguments using argparse"""
    parser = argparse.ArgumentParser(
        description=f"Takes as input the path to .py file or directory containing .py files and re-orders methods of "
        f"classes according to {__PROJECT_NAME__} guidelines."
    )
    parser.add_argument("files", nargs="*")
    parser.add_argument(
        "-ip",
        "--input-path",
        type=str,
        default="./",
        help="Relative filepath to python source code files",
    )
    parser.add_argument(
        "-o",
        "--output-path",
        type=str,
        default=None,
        help="Relative filepath to where formatted source should be saved. If None, then original files will be "
        "modified.",
    )
    parser.add_argument(
        "-cp",
        "--config-path",
        type=str,
        default=None,
        help="Relative filepath to a msort.ini or pyproject.toml file.",
    )
    parser.add_argument(
        "-sp",
        "--skip-patterns",
        action="append",
        help="Provide patterns to look for in .py file and avoid running msort on these scripts.",
    )
    parser.add_argument(
        "--check",
        default=False,
        action="store_true",
        help=f"fUse --check to run {__PROJECT_NAME__} without changing any files and instead return a code indicating how many files"
        "would be changed.",
    )
    parser.add_argument(
        "--diff",
        default=False,
        action="store_true",
        help=f"Use --diff to run {__PROJECT_NAME__} without changing any files and print the changes which would be made.",
    )
    parser.add_argument(
        "-f",
        "--force",
        default=False,
        action="store_true",
        help="Use --force to override exception raised if the user specifies a sorting level higher than "
        "fixed defaults",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        type=int,
        default=1,
        help=f"Set the verbosity of the {__PROJECT_NAME__} output. Use 0, 1, or 2.",
    )
    parser.add_argument(
        "-p", "--parser", type=str, default="cst", choices=["ast", "cst"], help="Choose a parser. Either ast or cst."
    )
    parser.add_argument(
        "-pg",
        "--use-property-groups",
        default=False,
        action="store_true",
        help="Use --use-property-groups to group getters, setters and deleters.",
    )
    # params = parser.parse_args()
    params, args = parser.parse_known_args()
    kwargs: Dict[str, Any] = {}
    for arg in args:
        if "=" in arg:
            k, v = arg.split("=")
            kwargs[k.replace("--", "")] = v
        else:
            kwargs[arg.replace("--", "")] = None

    return params, kwargs


def _validate_paths_input_file(
    input_path: Path, output_path: Optional[Path] = None, check_only: bool = False
) -> Tuple[List[str], List[Optional[str]]]:
    """
    Validate that the input file path and output path are compatible when the user has specified a specific input file
    Args:
        input_path: file path to a .py file
        output_path: output path to a file or directory
        check_only: If True, then outputs will be None and no code will be changed

    Returns:
        py_scripts: list of paths to .py scripts for formatting
        outputs: list of paths where formatted scripts will be written to
    """
    py_scripts = [input_path.as_posix()]
    outputs: List[Optional[str]]
    if check_only:
        outputs = [None] * len(py_scripts)
    elif output_path is None:
        outputs = [input_path.as_posix()]
    elif output_path.as_posix().endswith(".py"):
        outputs = [output_path.as_posix()]
    else:
        logging.info("Treating output path %s as a directory!", output_path.as_posix())
        outputs = [output_path.joinpath(input_path.name).as_posix()]
    return py_scripts, outputs


def _validate_paths_input_dir(
    input_path: Path, output_path: Optional[Path] = None, check_only: bool = False
) -> Tuple[List[str], List[Optional[str]]]:
    """
    Validate that the input file path and output path are compatible when the user has specified an input directory
    Args:
        input_path: file path to a directory containing .py files
        output_path: output path to a file or directory
        check_only: If True, then outputs will be None and no code will be changed

    Returns:
        py_scripts: list of paths to .py scripts for formatting
        outputs: list of paths where formatted scripts will be written to
    """
    py_scripts = [script.as_posix() for script in input_path.rglob(pattern="*.py")]
    outputs: List[Optional[str]]
    if check_only:
        outputs = [None] * len(py_scripts)
    elif output_path is None:
        outputs = list(py_scripts)
    elif output_path.as_posix().endswith(".py"):
        raise ValueError("Input path is a directory but output path is a .py file!")
    else:
        logging.info("Treating output path %s as a directory!", output_path.as_posix())
        outputs = [output_path.joinpath(Path(script).name).as_posix() for script in py_scripts]
    return py_scripts, outputs


def validate_paths(
    files: List[str],
    input_path: Optional[str] = None,
    output_path: Optional[str] = None,
    check_only: bool = False,
) -> Tuple[List[str], List[Optional[str]]]:
    """
    Validate that the user provided input and output paths are compatible.

    Args:
        files: paths to .py file captured as positional arguments on command line
        input_path: file path to input script or directory of scripts
        output_path: path to output script or output directory
        check_only: If True, then outputs will be None and no code will be changed

    Returns:
        py_scripts: list of paths to .py scripts for formatting
        outputs: list of paths where formatted scripts will be written to
    """
    if files:
        output_files: List[Optional[str]] = [f for f in files if f is not None]
        logging.info("Found %s files as positional args: %s", len(files), files)
        return files, output_files
    if input_path is None:
        raise ValueError("Must provide an input path if positional args 'files' is None!")
    input_pure_path = Path(input_path)
    output_pure_path = Path(output_path) if output_path is not None else None

    if not input_pure_path.exists():
        raise FileNotFoundError("Input path does not exist!")

    if check_only and output_path is not None:
        logging.warning("Overriding output path as running in check only mode!")

    if input_pure_path.is_file():
        py_scripts, outputs = _validate_paths_input_file(input_pure_path, output_pure_path, check_only)
    elif input_pure_path.is_dir():
        py_scripts, outputs = _validate_paths_input_dir(input_pure_path, output_pure_path, check_only)
    else:
        raise ValueError("Input path is neither a file or a directory! ")
    return py_scripts, outputs


def update_config_ordering(cfg: Dict[str, Any], args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update the ordering section of config using command line arguments
    Args:
        cfg: config extracted from msort.ini
        args: command line arguments

    Returns:
        cfg: updated if necessary by command line arguments
    """
    for param in cfg[DEFAULT_MSORT_ORDERING_SECTION]:
        if param in args or param.replace("_", "-") in args:
            logging.info("Overriding %s order : set to %s", param, args[param.replace("_", "-")])
            cfg[DEFAULT_MSORT_ORDERING_SECTION][param.replace("-", "_")] = args[param.replace("_", "-")]
    return cfg


def update_config_general(cfg: Dict[str, Any], args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update the general params section of config using command line arguments
    Args:
        cfg: config extracted from msort.ini
        args: command line arguments

    Returns:
        cfg: updated if necessary by command line arguments
    """
    for param in cfg[DEFAULT_MSORT_PARAMS_SECTION]:
        possible_params = [param, param.replace("_", "-"), f"n_{param}", f"n-{param.replace('_', '-')}"]
        for p in possible_params:
            if p in args:
                value: str = args[p]
                value = (not re.match(r"^n[-_]", p)) if value is None else value
                logging.info("Overriding %s : set to %s", param, value)
                cfg[DEFAULT_MSORT_PARAMS_SECTION][param] = str(value)
    return cfg


def update_config(cfg: Dict[str, Any], args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update the config using command line arguments
    Args:
        cfg: config extracted from msort.ini
        args: command line arguments

    Returns:
        cfg: updated if necessary by command line arguments
    """
    cfg = update_config_ordering(cfg, args)
    cfg = update_config_general(cfg, args)
    return cfg


def main() -> None:
    params, args = parse_commandline()
    set_logging(params.verbose)
    skip_patterns = [] if params.skip_patterns is None else params.skip_patterns

    py_scripts, outputs = validate_paths(
        files=params.files,
        input_path=params.input_path,
        output_path=params.output_path,
        check_only=params.check or params.diff,
    )

    if len(py_scripts) == 0:
        logging.warning("No Python scripts found in %s", params.input_path)
    else:
        logging.info("Checking %s python scripts ...", len(py_scripts))

    logging.info("Using the %s parser!", str.upper(params.parser))
    code_parser = importlib.import_module(f"msort.{params.parser}_functions")
    config_loader = get_config_loader(config_path=params.config_path)
    cfg = config_loader.config

    # command line can be used to override some options
    auto_static_param = cfg[DEFAULT_MSORT_PARAMS_SECTION]["auto_static"]
    auto_static = ast.literal_eval(auto_static_param) if isinstance(auto_static_param, str) else auto_static_param
    auto_static = True if "auto-static" in args else auto_static
    auto_static = False if "n-auto-static" in args else auto_static
    property_groups_param = cfg[DEFAULT_MSORT_PARAMS_SECTION]["use_property_groups"]
    property_groups = (
        ast.literal_eval(property_groups_param) if isinstance(property_groups_param, str) else property_groups_param
    )
    property_groups = True if "property_groups" in args else property_groups
    property_groups = False if "n-property_groups" in args else property_groups

    cfg = update_config(cfg, args)

    # instantiate method describer
    method_describer = get_method_describer(parser_type=params.parser, config=cfg, override_level_check=params.force)

    responses: List[format_msort_response] = []
    for input_script, output_script in zip(py_scripts, outputs):
        if any(skip_pat in Path(input_script).stem for skip_pat in skip_patterns):
            logging.debug("Skipping %s", input_script)
            continue
        logging.debug("Reformatting %s ...", input_script)
        response = format_msort(
            file_path=input_script,
            output_py=output_script,
            parser=code_parser,
            method_describer=method_describer,
            auto_static=auto_static,
            use_property_groups=property_groups,
        )
        responses.append(response)
    n = sum(resp["code"] for resp in responses)
    if params.check:
        logging.info(
            f"\n----\n{__PROJECT_NAME__} ran in check mode : %s / %s files would be changed!\n----", n, len(py_scripts)
        )
    elif params.diff:
        diff = "\n\n".join([resp["diff"] for resp in responses])
        logging.info(f"\n ----- \n{__PROJECT_NAME__} ran in diff mode : %s", diff)
    else:
        logging.info(f"\n----\n{__PROJECT_NAME__} modified %s / %s files!\n----", n, len(py_scripts))


if __name__ == "__main__":
    main()
