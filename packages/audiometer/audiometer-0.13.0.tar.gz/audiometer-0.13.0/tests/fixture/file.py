from pathlib import Path

import pydub
import pytest


@pytest.fixture
def audio_path() -> Path:
    return Path(__file__).parent.joinpath("test.wav")


@pytest.fixture
def audio(audio_path: Path) -> pydub.AudioSegment:
    return pydub.AudioSegment.from_file(audio_path)
