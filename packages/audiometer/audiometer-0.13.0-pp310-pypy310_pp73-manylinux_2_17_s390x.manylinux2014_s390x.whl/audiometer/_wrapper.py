from __future__ import annotations

import functools
import shutil
import subprocess
from collections.abc import Callable
from pathlib import Path
from typing import Any, TypedDict

import pydub

from audiometer import _audiometer

from . import stream


class LUFS(TypedDict):
    integrated: float
    momentary: list[float]


def required(executable_name: str) -> Callable[..., Any]:
    def decorator(func: Callable[..., Any]):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            if shutil.which(executable_name) is None:
                raise ValueError(f"{executable_name} is not installed")
            return func(*args, **kwargs)

        return wrapper

    return decorator


def calculate_rms(segment: pydub.AudioSegment) -> float:
    return round(
        _audiometer.calculate_rms_inner(
            samples=segment.get_array_of_samples(),
            channels=segment.channels,
            max_amplitude=segment.max_possible_amplitude,
            sample_rate=segment.frame_rate,
        ),
        1,
    )


def calculate_peak(segment: pydub.AudioSegment) -> float:
    return round(
        _audiometer.calculate_peak_inner(
            samples=segment.get_array_of_samples(),
            channels=segment.channels,
            max_amplitude=segment.max_possible_amplitude,
        ),
        1,
    )


def calculate_lufs(segment: pydub.AudioSegment) -> LUFS:
    filter_output = stream.with_file(
        export=functools.partial(segment.export, format="wav", codec="pcm_s24le"),
        func=apply_ebur128_filter,
        suffix=".wav",
    )
    return dict(
        integrated=_audiometer.parse_integrated_loudness(filter_output),
        momentary=_audiometer.parse_momentary_loudness(filter_output),
    )


def calculate_integrated_loudness(segment: pydub.AudioSegment) -> float:
    filter_output = stream.with_file(
        export=functools.partial(segment.export, format="wav", codec="pcm_s24le"),
        func=apply_ebur128_filter,
        suffix=".wav",
    )
    return _audiometer.parse_integrated_loudness(filter_output)


def calculate_momentary_loudness(segment: pydub.AudioSegment) -> list[float]:
    filter_output = stream.with_file(
        export=functools.partial(segment.export, format="wav", codec="pcm_s24le"),
        func=apply_ebur128_filter,
        suffix=".wav",
    )
    return _audiometer.parse_momentary_loudness(filter_output)


@required("ffmpeg")
def apply_ebur128_filter(input_path: str | Path) -> str:
    cmd = f"ffmpeg -i {input_path} -filter_complex ebur128=peak=true -f null -"
    return subprocess.run(cmd.split(" "), capture_output=True).stderr.decode()
