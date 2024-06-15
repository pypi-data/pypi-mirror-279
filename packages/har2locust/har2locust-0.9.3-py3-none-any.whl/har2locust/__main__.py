import ast
import importlib
import json
import logging
import os
import pathlib
import sys
import unicodedata
from argparse import Namespace

import jinja2

from .argument_parser import get_parser
from .plugin import astprocessor, entriesprocessor, entriesprocessor_with_args, outputstringprocessor


def __main__(arguments=None):
    args = get_parser().parse_args(arguments)
    logging.basicConfig(level=args.loglevel.upper())
    load_plugins(
        args.plugins.split(",") if args.plugins else [], args.disable_plugins.split(",") if args.disable_plugins else []
    )
    har_path = pathlib.Path(args.input)
    name = generate_class_name(har_path.stem)  # build class name from filename
    with open(har_path, encoding="utf8") as f:
        har = json.load(f)
    logging.debug(f"loaded {har_path}")

    template_values = process(har, args)
    template_values["class_name"] = name
    py = render(args.template, template_values)
    print(py)


def load_plugins(plugins: list[str] = [], disable_plugins: list[str] = []):
    package_root_dir = pathlib.Path(__file__).parents[1]
    plugin_dir = package_root_dir / "har2locust/default_plugins"
    default_plugins = [str(d.relative_to(package_root_dir)) for d in plugin_dir.glob("*.py")]
    default_plugins.sort()  # ensure deterministic ordering
    default_and_extra_plugins = default_plugins + plugins

    plugins_copy = default_and_extra_plugins.copy()
    for dp in disable_plugins:
        for p in default_and_extra_plugins[:]:
            if p.endswith(dp):
                default_and_extra_plugins.remove(p)
                logging.debug("Disabled plugin: " + p)
                break
        else:
            raise Exception(f"Tried to disable unknown plugin: {dp}. Known plugins are {plugins_copy}")

    sys.path.append(os.path.curdir)  # accept plugins by relative path
    for plugin in default_and_extra_plugins:
        # in  windows OS   print(plugin) echo  har2locust\default_plugins\1_resourcefilter.py
        import_path = plugin.replace("/", ".").replace("\\", ".").rstrip(".py")
        importlib.import_module(import_path)
        logging.debug("imported " + import_path)
    logging.debug(f"loaded plugins {default_and_extra_plugins}")


# process har dictionary and return a dict of values to render
def process(har: dict, args: Namespace) -> dict:
    if har["log"]["version"] != "1.2":
        logging.warning(f"Untested har version {har['log']['version']}")
    entries = har["log"]["entries"]
    logging.debug(f"found {len(entries)} entries")

    for e in entries:
        # set defaults
        e["request"]["fname"] = "client.request"
        e["request"]["extraparams"] = [("catch_response", True)]
    values = {"entries": entries}
    for p in entriesprocessor.processors:
        values |= p(entries) or {}
        # logging.debug(f"{len(entries)} entries after applying {p.__name__}")
    for p in entriesprocessor_with_args.processors:
        values |= p(entries, args) or {}
        # logging.debug(f"{len(entries)} entries after applying with_args {p.__name__}")
    logging.debug(f"{len(entries)} entries after applying entriesprocessors")

    return values


def render(name: str, values: dict) -> str:
    logging.debug(f'about to load template "{name}"')
    if pathlib.Path(name).exists():
        template_path = pathlib.Path(name)
    else:
        template_path = pathlib.Path(__file__).parents[0] / name
        if not template_path.exists():
            raise Exception(f"Template {name} does not exist, neither in current directory nor as built in")

    template_dir = template_path.parents[0]

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
    template = env.get_template(template_path.name)
    logging.debug("template loaded")

    py = template.render(values)
    logging.debug("template rendered")

    try:
        tree = ast.parse(py, type_comments=True)
    except ValueError as e:
        logging.debug(py)
        levelmessage = " (set log level DEBUG to see the whole output)" if logging.DEBUG < logging.root.level else ""
        logging.error(f"{e} when parsing rendered template{levelmessage}")
        raise
    except SyntaxError as e:
        logging.debug(py)
        levelmessage = " (set log level DEBUG to see the whole output)" if logging.DEBUG < logging.root.level else ""
        logging.error(f"{e.msg} when parsing rendered template{levelmessage}")
        raise

    for p in astprocessor.processors:
        p(tree, values)
    py = ast.unparse(ast.fix_missing_locations(tree))
    logging.debug("astprocessors applied")

    for p in outputstringprocessor.processors:
        py = p(py)
    logging.debug("outputstringprocessors applied")

    return py


@entriesprocessor_with_args
def transform_payload_strings(entries: list[dict], args):
    for entry in entries:
        request = entry["request"]
        if "postData" in request and "text" in request["postData"] and request["fname"] != "rest":
            request["postData"]["text"] = ast.unparse(ast.Constant(value=request["postData"]["text"]))


# Generate a valid identifier (https://docs.python.org/3.8/reference/lexical_analysis.html#identifiers) by replacing
# invalid characters with "_".
def generate_class_name(file_name: str) -> str:
    VALID_STARTING_CHARACTER_CATEGORIES = ["Lu", "Ll", "Lt", "Lm", "Lo", "Nl"]
    OTHER_ID_START_CHARACTERS = ["\u1885", "\u1886", "\u2118", "\u212e", "\u309b", "\u309c"]
    VALID_CONTINUATION_CHARACTER_CATEGORIES = VALID_STARTING_CHARACTER_CATEGORIES + ["Mn", "Mc", "Nd", "Pc"]
    OTHER_ID_CONTINUE_CHARACTERS = ["\u00b7", "\u0387", "\u1369", "\u1370", "\u1371", "\u19da"]

    def valid_continuation_character(character: str) -> bool:
        normalized_character = unicodedata.normalize("NFKC", character)
        for character in normalized_character:
            if (
                unicodedata.category(character) not in VALID_CONTINUATION_CHARACTER_CATEGORIES
                and character not in OTHER_ID_START_CHARACTERS + OTHER_ID_CONTINUE_CHARACTERS
                and character != "_"
            ):
                return False
        return True

    def valid_starting_character(character: str) -> bool:
        normalized_character = unicodedata.normalize("NFKC", character)
        first = normalized_character[0]
        if (
            unicodedata.category(first) not in VALID_STARTING_CHARACTER_CATEGORIES
            and first not in OTHER_ID_START_CHARACTERS
            and first != "_"
        ):
            return False
        for character in normalized_character[1:]:
            if not valid_continuation_character(character):
                return False
        return True

    first_character = file_name[0]
    name = first_character if valid_starting_character(first_character) else "_"

    for character in file_name[1:]:
        name += character if valid_continuation_character(character) else "_"

    return name


if __name__ == "__main__":
    __main__()
