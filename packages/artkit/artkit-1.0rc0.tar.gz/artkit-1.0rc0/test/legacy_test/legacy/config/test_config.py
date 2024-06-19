import json
import logging
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest
import yaml

from legacy.config import JSONReader, PersonaParser, YAMLReader
from legacy.config.base import ConfigFileReader
from legacy.persona import Persona

log = logging.getLogger(__name__)


_TEST_PARAMS = (
    [
        "reader_type",
        "dump_fn",
    ],
    [
        [YAMLReader, yaml.dump],
        [JSONReader, json.dumps],
    ],
)


@pytest.mark.parametrize(*_TEST_PARAMS)
def test_persona_parser(
    tmp_path: Path,
    reader_type: type[ConfigFileReader],
    dump_fn: Callable[[str], str],
) -> None:
    hacker = Persona(archetype="Hacker", description="A sneaky hacker.")

    path = tmp_path / "failure_modes.yaml"
    with path.open("w") as file:
        file.write(dump_fn(_strip_dict_repr(hacker.to_dict())))

    parsed = PersonaParser(reader=reader_type(str(path))).parse()

    assert parsed == hacker


def test_invalid_file_structure(tmp_path: Path) -> None:
    path = tmp_path / "invalid.yaml"
    with path.open("w") as file:
        file.write("not a dict")

    with pytest.raises(ValueError, match="File .* must contain a single dictionary"):
        PersonaParser(reader=YAMLReader(str(path))).parse()


#
# Helper functions
#


def _strip_dict_repr(obj: Any) -> Any:
    """
    Strip fields added by HasDictRepr from a dict
    """
    if isinstance(obj, dict):
        if "cls" in obj:
            return _strip_dict_repr(obj["params"])
        elif "root" in obj:
            return _strip_dict_repr(obj["root"]["params"])
        else:
            return {k: _strip_dict_repr(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return list(map(_strip_dict_repr, obj))
    else:
        return obj
