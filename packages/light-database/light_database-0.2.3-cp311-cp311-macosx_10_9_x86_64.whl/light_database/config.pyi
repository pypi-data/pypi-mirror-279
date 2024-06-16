# (generated with --quick)

import pathlib
from typing import List, Optional, Union
from configparser import ConfigParser
from cryptography.fernet import Fernet


class EnvConfig:
    _config_path: pathlib.Path
    _fernet: Fernet
    @classmethod
    def delete(cls, section: str) -> None: ...
    @classmethod
    def init_configer(cls) -> ConfigParser: ...
    @classmethod
    def read(cls, sections: Optional[Union[str, List[str]]] = None, configer: Optional[ConfigParser] = None) -> str: ...
    @classmethod
    def sections(cls) -> str: ...
    @classmethod
    def write(cls, section: str, force: bool = False, **kwargs) -> None: ...
