import tempfile
from collections.abc import Callable
from typing import Any, TypeVar

import pydub

FunctionResult = TypeVar("FunctionResult")


def with_file(
    export: Callable[[str], pydub.AudioSegment],
    func: Callable[[str], FunctionResult],
    **kwargs: Any,
) -> FunctionResult:
    with tempfile.NamedTemporaryFile(**kwargs) as f:
        export(f.name)
        result = func(f.name)

    return result
