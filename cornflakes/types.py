import dataclasses
from dataclasses import dataclass
from enum import Enum
import inspect
from typing import (
    Any,
    Callable,
    ClassVar,
    Dict,
    Generic,
    Iterable,
    List,
    Optional,
    Protocol,
    Type,
    TypeVar,
    Union,
    runtime_checkable,
)

_T = TypeVar("_T", covariant=True)  # type: ignore


class GenericType(Generic[_T]):
    ...


class _HiddenDefault(str):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, "***")


class _WithoutDefault:
    pass


WITHOUT_DEFAULT = _WithoutDefault()
WITHOUT_DEFAULT_TYPE = _WithoutDefault
MISSING_TYPE = dataclasses._MISSING_TYPE
MISSING = dataclasses.MISSING
HAS_DEFAULT_FACTORY = getattr(dataclasses, "_HAS_DEFAULT_FACTORY", None)
INSPECT_EMPTY_TYPE = getattr(inspect, "_empty", None)
HIDDEN_DEFAULT = _HiddenDefault()
HIDDEN_DEFAULT_TYPE = type(HIDDEN_DEFAULT)


class FuncatTypes(Enum):
    WRAP = "wrap"
    BEFORE = "before"
    AFTER = "after"


class Loader(Enum):
    """Config Loader Enums."""

    INI = "from_ini"
    YAML = "from_yaml"
    DICT = "from_dict"
    FILE = "from_file"
    CUSTOM = "from_custom"


class Writer(Enum):
    """Config Writer Enums."""

    INI = "to_ini"
    YAML = "to_yaml"
    DICT = "to_dict"
    FILE = "to_file"
    CUSTOM = "to_custom"


@dataclass(frozen=True)
class ConfigOption:
    """Config Option Constants."""

    ENABLED: str = "__auto_option_enabled__"
    READ_CONFIG_METHOD: str = "__auto_option_init__"
    ATTRIBUTES: str = "__auto_option_attributes__"
    PASSED_DECORATE_KEY: str = "__auto_option_key__"
    ADD_CONFIG_FILE_OPTION_PARAM_VAR: str = "config_file"
    ADD_CONFIG_FILE_OPTION_PARAM: str = "--config-file"
    ADD_CONFIG_FILE_OPTION_PARAM_SHORT: str = "-cfg"
    SHOW_CONFIG_FILES_OPTION_PARAM_VAR: str = "show_config_files"
    SHOW_CONFIG_FILES_OPTION_PARAM: str = "--show-config-files"
    SHOW_CONFIG_FILES_OPTION_PARAM_SHORT: str = "-scf"


@dataclass(frozen=True)
class ConfigDecoratorArgs:
    """Config Arguments Arguments."""

    FILES: str = "files"
    SECTIONS: str = "sections"
    USE_REGEX: str = "use_regex"
    IS_LIST: str = "is_list"
    DEFAULT_LOADER: str = "default_loader"
    ALLOW_EMPTY: str = "allow_empty"


@dataclass(frozen=True)
class ConfigDecorator:
    """Config Decorator Constants."""

    FILES: str = "__config_files__"
    SECTIONS: str = "__config_sections__"
    USE_REGEX: str = "__multi_config__"
    IS_LIST: str = "__config_list__"
    DEFAULT_LOADER: str = "__default_loader__"
    CUSTOM_LOADER: str = "__custom_loader__"
    ALLOW_EMPTY: str = "__allow_empty_config__"
    CHAIN_FILES: str = "__chain_files__"
    VALIDATE: str = "__validate__"

    SECTION_NAME_KEY: str = "section_name"


@dataclass(frozen=True)
class DataclassDecorator:
    """Dataclass Decorator Constants."""

    FIELDS: str = "__dataclass_fields__"
    DICT_FACTORY: str = "__dict_factory__"
    TUPLE_FACTORY: str = "__tuple_factory__"
    VALUE_FACTORY: str = "__value_factory__"
    EVAL_ENV: str = "__eval_env__"
    IGNORED_SLOTS: str = "__ignored_slots__"
    IGNORE_NONE: str = "__ignore_none__"
    VALIDATORS: str = "__cornflakes_validators__"
    REQUIRED_KEYS: str = "__cornflakes_required_keys__"


@dataclass(frozen=True)
class Constants:
    """Constants."""

    DEFAULT_LOADER: Loader = Loader.INI
    DEFAULT_CONFIG_FILE: str = "config.ini"
    config_option: Type[ConfigOption] = ConfigOption
    config_decorator_args: Type[ConfigDecoratorArgs] = ConfigDecoratorArgs
    config_decorator: Type[ConfigDecorator] = ConfigDecorator
    dataclass_decorator: Type[DataclassDecorator] = DataclassDecorator


ConfigArgument = Optional[Optional[Union[Dict[Optional[str], Union[List[str], str]], List[str], str]]]


@runtime_checkable
class LoaderMethod(Protocol):
    """Config loader method protocol."""

    @classmethod
    def __call__(
        cls,
        files: ConfigArgument = None,
        sections: ConfigArgument = None,
        keys: ConfigArgument = None,
        defaults: ConfigArgument = None,
        eval_env: bool = False,
        *args,
        **kwargs
    ) -> Any:
        """Config loader method protocol.

        Methods generated by the Methods implemented in:
        from_yaml -> :meth:`cornflakes.decorator.config.yaml.create_yaml_file_loader`
        from_ini -> :meth:`cornflakes.decorator.config.ini.create_ini_file_loader`
        from_dict -> :meth:`cornflakes.decorator.config.dict.create_dict_file_loader`
        """
        ...


@runtime_checkable
class MappingWrapper(Protocol[_T]):
    def __getitem__(self, key: str) -> _T:
        ...

    def keys(self) -> Iterable[str]:
        ...

    def __len__(self) -> int:
        ...

    @classmethod
    def __new__(cls: Type[_T], *args, **kwargs) -> "MappingWrapper[_T]":
        """Create and return a new object."""
        ...

    def __call__(self, *args, **kwargs) -> _T:
        """Return a new descriptor object."""
        ...

    def __init__(self, *args, **kwargs) -> None:
        ...


@runtime_checkable
class StandardDataclass(Protocol):
    __dataclass_fields__: ClassVar[Dict[str, Any]]
    __dataclass_params__: ClassVar[Any]  # in reality `dataclasses._DataclassParams`
    __post_init__: ClassVar[Callable[..., None]]

    __args__: ClassVar[List[Any]]
    __name__: ClassVar[str]


@runtime_checkable
class StandardCornflakesDataclass(StandardDataclass, Protocol[_T]):
    # @classmethod
    # def __new__(cls: Type[_T], *args, **kwargs) -> _T:
    #     ...
    def __int__(self, *args, **kwargs) -> None:
        ...

    @classmethod
    def validate_kwargs(cls, validate=False, **kwargs) -> Dict[str, Any]:
        """Validate kwargs.

        Method implemented in :meth:`cornflakes.decorator.dataclass._validate.validate_dataclass_kwargs`.
        """
        ...
        from cornflakes.decorator.dataclasses import validate_dataclass_kwargs

        return validate_dataclass_kwargs(cls, validate=validate, **kwargs)

    @classmethod
    def check_kwargs(cls, validate=False, **kwargs) -> Dict[str, Any]:
        """Check dataclass kwargs.

        Method implemented in :meth:`cornflakes.decorator.dataclass._validate.check_dataclass_kwargs`.

        """
        from cornflakes.decorator.dataclasses import check_dataclass_kwargs

        return check_dataclass_kwargs(cls, validate=validate, **kwargs)


@runtime_checkable
class DataclassInstance(StandardCornflakesDataclass, Protocol[_T]):
    def __int__(self, *args, **kwargs):
        ...

    def __call__(self, *args, **kwargs) -> _T:
        ...

    def __getitem__(self, key: str) -> _T:
        """Get the value associated with the given key."""
        ...

    def keys(self) -> Iterable[str]:
        """Return an iterable of all the keys."""
        ...

    def __contains__(self, *args, **kwargs):
        """True if the dictionary has the specified key, else False."""
        ...

    def __iter__(self, *args, **kwargs):
        """Implement iter(self)."""
        ...

    def __len__(self, *args, **kwargs):
        """Return len(self)."""

    @classmethod
    def __new__(cls: Type[_T], *args, **kwargs) -> "DataclassInstance[_T]":
        """Create and return a new object.  See help(type) for accurate signature."""
        ...

    def to_dict(self) -> dict:
        """Parse config to dict.

        Method implemented in :meth:`cornflakes.decorator.dataclass._dataclass.to_dict`.
        """
        ...
        from cornflakes.decorator.dataclasses import to_dict

        return to_dict(self)

    def to_tuple(self) -> tuple:
        """Parse config to tuple.

        Method implemented in :meth:`cornflakes.decorator.dataclass._dataclass.to_tuple`.
        """
        ...
        from cornflakes.decorator.dataclasses import to_tuple

        return to_tuple(self)

    def to_ini(self, out_cfg: Optional[str] = None) -> Optional[bytearray]:
        """Parse config to ini file / bytes.

        Method implemented in :meth:`cornflakes.decorator.config.ini.to_ini`.
        """
        ...
        from cornflakes.decorator.dataclasses import to_ini

        return to_ini(self, out_cfg=out_cfg)

    def to_yaml(self, out_cfg: Optional[str] = None, *args, **kwargs) -> Optional[bytearray]:
        """Parse config to yaml file / bytes.

        Method implemented in :meth:`cornflakes.decorator.config.yaml.to_yaml`.
        """
        ...
        from cornflakes.decorator.dataclasses import to_yaml

        return to_yaml(self, out_cfg=out_cfg, *args, **kwargs)


class CornflakesType:
    def __getitem__(self, key):
        return type(key)


@runtime_checkable
class CornflakesDataclass(StandardCornflakesDataclass, Protocol[_T]):
    """Dataclass instance protocol."""

    __eval_env__: bool

    @classmethod
    def __call__(cls: Type[_T], *args, **kwargs) -> DataclassInstance[_T]:
        ...

    def __int__(self, *args, **kwargs) -> None:
        ...


@runtime_checkable
class StandardConfigArgs(Protocol):
    __config_files__: ClassVar[Optional[Union[List[str], str]]]
    __config_sections__: ClassVar[Optional[Union[List[str], str]]]
    __multi_config__: ClassVar[bool]
    __config_list__: ClassVar[bool]
    __default_loader__: ClassVar[Loader]
    __allow_empty_config__: ClassVar[bool]
    __chain_files__: ClassVar[bool]


@runtime_checkable
class StandardConfigMethods(Protocol):
    def from_ini(
        self,
        files: ConfigArgument = None,
        sections: ConfigArgument = None,
        keys: ConfigArgument = None,
        defaults: ConfigArgument = None,
        eval_env: bool = False,
        *args,
        **kwargs
    ):
        """Method to load a config from ini files."""
        ...
        from cornflakes.decorator.dataclasses._helper import get_loader_callback
        from cornflakes.decorator.dataclasses.config._load_config import create_file_loader

        return create_file_loader(cls=self, _loader_callback=get_loader_callback(Loader.INI), _instantiate=True)(
            files=files, sections=sections, keys=keys, defaults=defaults, eval_env=eval_env, *args, **kwargs
        )

    def from_yaml(
        self,
        files: ConfigArgument = None,
        sections: ConfigArgument = None,
        keys: ConfigArgument = None,
        defaults: ConfigArgument = None,
        eval_env: bool = False,
        *args,
        **kwargs
    ):
        """Method to load a config from yaml files."""
        ...
        from cornflakes.decorator.dataclasses._helper import get_loader_callback
        from cornflakes.decorator.dataclasses.config._load_config import create_file_loader

        return create_file_loader(cls=self, _loader_callback=get_loader_callback(Loader.YAML), _instantiate=True)(
            files=files, sections=sections, keys=keys, defaults=defaults, eval_env=eval_env, *args, **kwargs
        )

    def from_dict(
        self,
        files: ConfigArgument = None,
        sections: ConfigArgument = None,
        keys: ConfigArgument = None,
        defaults: ConfigArgument = None,
        eval_env: bool = False,
        *args,
        **kwargs
    ):
        """Method to load a config from dict files."""
        ...
        from cornflakes.decorator.dataclasses._helper import get_loader_callback
        from cornflakes.decorator.dataclasses.config._load_config import create_file_loader

        return create_file_loader(cls=self, _loader_callback=get_loader_callback(Loader.DICT), _instantiate=True)(
            files=files, sections=sections, keys=keys, defaults=defaults, eval_env=eval_env, *args, **kwargs
        )

    def from_file(
        self,
        files: ConfigArgument = None,
        sections: ConfigArgument = None,
        keys: ConfigArgument = None,
        defaults: ConfigArgument = None,
        eval_env: bool = False,
        *args,
        **kwargs
    ) -> Any:
        """Method to load a config from files."""
        ...
        from cornflakes.decorator.dataclasses._helper import config_files, get_default_loader, get_loader_callback
        from cornflakes.decorator.dataclasses.config._load_config import create_file_loader

        return create_file_loader(
            cls=self,
            _loader_callback=get_loader_callback(get_default_loader(files or config_files(self))),
            _instantiate=True,
        )(files=files, sections=sections, keys=keys, defaults=defaults, eval_env=eval_env, *args, **kwargs)


@runtime_checkable
class StandardConfigGroupArgs(Protocol):
    __allow_empty_config__: ClassVar[bool]
    __config_files__: ClassVar[Optional[Union[List[str], str]]]
    __chain_files__: ClassVar[bool]


@runtime_checkable
class StandardConfigGroupMethods(Protocol):
    def from_file(
        self,
        files: ConfigArgument = None,
        sections: ConfigArgument = None,
        keys: ConfigArgument = None,
        defaults: ConfigArgument = None,
        eval_env: bool = False,
        *args,
        **kwargs
    ) -> Any:
        """Method to load a config from files."""
        ...
        from cornflakes.decorator.dataclasses._helper import config_files, get_default_loader, get_loader_callback
        from cornflakes.decorator.dataclasses.config._load_config import create_file_loader

        return create_file_loader(
            cls=self,
            _loader_callback=get_loader_callback(get_default_loader(files or config_files(self))),
            _instantiate=True,
        )(files=files, sections=sections, keys=keys, defaults=defaults, eval_env=eval_env, *args, **kwargs)


@runtime_checkable
class ConfigInstance(StandardConfigMethods, StandardConfigArgs, DataclassInstance, Protocol[_T]):
    """Config Protocol Type."""

    ...


class Config(StandardConfigMethods, StandardConfigArgs, CornflakesDataclass, Protocol[_T]):
    """Config Protocol Type."""

    @classmethod
    def __new__(cls: Type[_T], *args, **kwargs) -> ConfigInstance[_T]:  # type: ignore
        ...


@runtime_checkable
class ConfigGroupInstance(StandardConfigGroupMethods, StandardConfigArgs, DataclassInstance, Protocol[_T]):
    """ConfigGroup Protocol Type."""


@runtime_checkable
class ConfigGroup(StandardConfigGroupMethods, StandardConfigGroupArgs, CornflakesDataclass, Protocol[_T]):
    """ConfigGroup Protocol Type."""

    @classmethod
    def __new__(cls: _T, *args, **kwargs) -> ConfigGroupInstance[_T]:  # type: ignore
        ...
