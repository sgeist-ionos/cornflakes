"""cornflakes config generation."""
import inspect
import logging
import os
import sysconfig
from types import ModuleType
from typing import Dict, List, Union

import cornflakes.builder.config_template
from cornflakes.common import import_component
from cornflakes.decorator.config import Loader, config_group, is_config


def generate_group_module(
    source_module: Union[ModuleType, str],
    source_config: Union[str, List[str], Dict[str, Union[str, List[str]]]] = None,
    target_module_file: str = None,
    class_name: str = None,
    loader: Loader = Loader.INI_LOADER,
    *args,
    **kwargs,
):
    """Module with function to generate automatically config group module."""
    if not target_module_file:
        target_module_file = f'{source_module.__name__.replace(".", "/")}/default.py'

    with open(cornflakes.builder.config_template.__file__) as file:
        template = file.read()

    if class_name:
        template = template.replace("class Config", f"class {class_name}")
        template = template.replace('["Config"]', f'["{class_name}"]')

    # Write Template to prevent import errors
    with open(target_module_file, "w") as file:
        file.write(template)

    if isinstance(source_module, str):
        source_module = import_component(source_module)

    ini_config_objects = {}
    imports = []
    files = []
    for cfg_name, cfg_class in inspect.getmembers(source_module):
        if inspect.isclass(cfg_class) and is_config(cfg_class):
            cfg = getattr(cfg_class, str(loader.value))(source_config)
            ini_config_objects.update(cfg)
            imports.append(cfg_name)
            files.extend([file for file in cfg.__config_files__ if file not in files])

    logging.debug(f"Found configs: {imports}")

    declaration = [
        (
            f"{cfg_name}: List[{cfg[0].__class__.__name__}] = field(default_factory={cfg.__class__.__name__})"
            if isinstance(cfg, list)
            else f"{cfg_name}: {cfg.__class__.__name__} = {cfg.__class__.__name__}()"
        )
        for cfg_name, cfg in ini_config_objects.items()
    ]

    extra_imports = ["from dataclasses import field", "from typing import List"] if declaration else []

    kwargs.update(
        {"files": [*kwargs.get("files", []), *(file for file in files if file not in kwargs.get("files", []))]}
    )

    if args or kwargs:
        template = template.replace(
            f"@{config_group.__name__}",
            (
                f"@{config_group.__name__}("
                f"{', '.join([*args, *[f'{key}={repr(value)}' for key, value in kwargs.items()]])})"
            ),
        )

    template = template.replace(
        "from",
        (
            f"""{'''
'''.join(extra_imports)}\n\nfrom {source_module.__name__} import ({''',
    '''.join(imports)}
    )\nfrom"""
        ),
    )
    template = template.replace(
        "pass",
        f"""{'''
    '''.join(declaration)}""",
        1,
    )

    with open(target_module_file, "w") as file:
        file.write(template)

    if "black" in os.listdir(sysconfig.get_paths()["purelib"]):
        # fix format
        os.system(f"black {source_config} {target_module_file}")  # noqa: S605
