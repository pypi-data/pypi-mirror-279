from typing import Optional, List


class Word:
    def __init__(
        self,
        word: str,
        start_time_ms: int,
        end_time_ms: int
    ):
        self._word = word
        self._start_time_ms = start_time_ms
        self._end_time_ms = end_time_ms

    @property
    def word(self):
        return self._word

    @property
    def start_time_ms(self):
        return self._start_time_ms

    @property
    def end_time_ms(self):
        return self._end_time_ms

    def __str__(self) -> str:
        return f"{self._word} [{self._start_time_ms / 1000:.3f}, {self._end_time_ms / 1000:.3f}]"

    def __repr__(self) -> str:
        return f"{self._word} [{self._start_time_ms / 1000:.3f}, {self._end_time_ms / 1000:.3f}]"


class Utterance:
    def __init__(
        self,
        text: str,
        start_time_ms: int,
        end_time_ms: int,
        normalized_text: Optional[str] = None,
        words: Optional[List[Word]] = None
    ):
        self._text = text
        self._start_time_ms = start_time_ms
        self._end_time_ms = end_time_ms
        self._normalized_text = normalized_text
        self._words = words

    @property
    def text(self):
        return self._text

    @property
    def start_time_ms(self):
        return self._start_time_ms

    @property
    def end_time_ms(self):
        return self._end_time_ms

    @property
    def normalized_text(self):
        return self._normalized_text

    def has_normalized_text(self):
        return self._normalized_text is not None

    @property
    def words(self):
        return self._words

    def has_words(self) -> bool:
        return self._words is not None

    def __repr__(self) -> str:
        return f'- {self._normalized_text if self._normalized_text else self._raw_text} [{self._start_time_ms / 1000:.3f}, {self._end_time_ms / 1000:.3f}]'

    def __str__(self) -> str:
        return f'- {self._normalized_text if self._normalized_text else self._raw_text} [{self._start_time_ms / 1000:.3f}, {self._end_time_ms / 1000:.3f}]'


class Transcription:
    def __init__(
        self,
        raw_text: str,
        normalized_text: Optional[str] = None,
        words: Optional[List[Word]] = None,
        utterances: Optional[List[Utterance]] = None,
        channel: Optional[str] = None,
    ):
        self._raw_text = raw_text
        self._normalized_text = normalized_text
        self._words = words
        self._utterances = utterances
        self._channel = channel

    @property
    def raw_text(self):
        return self._raw_text

    @property
    def normalized_text(self):
        return self._normalized_text

    def has_normalized_text(self):
        return self._normalized_text is not None

    @property
    def words(self):
        return self._words

    def has_words(self) -> bool:
        return self._words is not None

    @property
    def utterances(self):
        return self._utterances

    def has_utterances(self) -> bool:
        return self._utterances is not None

    @property
    def channel(self):
        return self._channel

    def __repr__(self) -> str:
        return self._normalized_text if self._normalized_text else self._raw_text

    def __str__(self) -> str:
        return self._normalized_text if self._normalized_text else self._raw_text
