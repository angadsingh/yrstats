"""
This module provides functions for parsing and prettifying `"stats.dmp"` file.
"""

import base64
import os.path
import re
from collections import defaultdict
from struct import unpack
from typing import DefaultDict, Dict, Union

import mappings


_DecodedBlockType = Union[bytes, bool, int, str, Dict[str, int]]


def bytes_to_ascii(binary_blob: bytes) -> str:
    """
    Convert bytes to ASCII string, replace invalid symbols with "?".

    Args:
        binary_blob: Input bytes.

    Returns:
        Decoded ASCII string.
    """
    binary_blob = re.sub(rb"[^\x20-\x7E]", b"?", binary_blob)
    return binary_blob.decode("ascii")


class BlockHeader:
    """
    Class for storing block header and decoding block data.
    """

    _tag: str
    _type: int
    _length: int

    def __init__(self, tag: str, type_: int, length: int) -> None:
        if not isinstance(tag, str):
            raise TypeError(
                f"`tag` argument should be a string, "
                f"but value {tag} of type {type(tag)} received."
            )
        self._tag = tag
        if not isinstance(type_, int):
            raise TypeError(
                f"`type_` argument should be an integer, "
                f"but value {type_} of type {type(type_)} received."
            )
        self._type = type_
        if not isinstance(length, int):
            raise TypeError(
                f"`length` argument should be an integer, "
                f"but value {length} of type {type(length)} received."
            )
        if length < 0:
            raise ValueError(
                f"`length` argument should be non-negative, but {length} received."
            )
        self._length = length

    @property
    def tag(self) -> str:
        """
        Block tag.
        """
        return self._tag

    @property
    def type(self) -> int:
        """
        Block type.
        """
        return self._type

    @property
    def length(self) -> int:
        """
        Block data length.
        """
        return self._length

    @property
    def padding(self) -> int:
        """
        Block data padding.
        """
        if self._length % 4:
            return 4 - self._length % 4
        return 0

    @classmethod
    def from_bytes(cls, binary_blob: bytes) -> "BlockHeader":
        """
        Parse a block header from bytes.
        """
        if len(binary_blob) != 8:
            raise ValueError(
                f"Block header should have length 8, "
                f"but binary blob of length {len(binary_blob)} received."
            )
        binary_tag, type_, length = unpack(">4sHH", binary_blob)
        tag = bytes_to_ascii(binary_tag)
        return cls(tag, type_, length)

    def decode_block(self, binary_blob: bytes) -> _DecodedBlockType:
        """
        Parse a block data from bytes.
        """
        # pylint: disable=too-many-return-statements
        if len(binary_blob) != self._length:
            raise ValueError(
                f"Block data should have length {self._length}, "
                f"but binary blob of length {len(binary_blob)} received."
            )
        if self._type == 1:
            # A single byte.
            return unpack(">c", binary_blob)[0]
        if self._type == 2:
            # A single boolean.
            return unpack(">?", binary_blob)[0]
        if self._type == 3:
            # A single short.
            return unpack(">h", binary_blob)[0]
        if self._type == 4:
            # A single unsigned short.
            return unpack(">H", binary_blob)[0]
        if self._type == 5:
            # A single long.
            return unpack(">l", binary_blob)[0]
        if self._type == 6:
            # A single unsigned long.
            return unpack(">L", binary_blob)[0]
        if self._type == 7:
            # Multiple b"\x00"-terminated chars.
            return bytes_to_ascii(binary_blob.rstrip(b"\x00"))
        if self._type == 20:
            # Custom type and length.
            if self._tag[:3] in mappings.HUMAN_READABLE_COUNTABLES:
                # Multiple unsigned longs.
                if self._length % 4:
                    raise ValueError(
                        f"Length of block data should be multiple of 4, "
                        f"but {self._length} received."
                    )
                counts = unpack(f">{int(self._length / 4)}L", binary_blob)
                return {
                    mappings.COUNTABLE_TYPES[self._tag[:2]][i]: count
                    for i, count in enumerate(counts)
                    if count > 0
                }
            # Raw bytes.
            # Bytes are not json serializable, so encode them as base64.
            return base64.b64encode(binary_blob).decode("ascii")
        raise ValueError(f"Decoding rule for type {self._type} is unknown.")


def parse_stats(filepath: str) -> Dict[str, _DecodedBlockType]:
    """
    Parse a `"stats.dmp"` file to dict.

    Args:
        filepath: Path to a `"stats.dmp"` file.

    Returns:
        Parsed statistics.
    """
    if not os.path.isfile(filepath):
        raise FileNotFoundError(
            f'Given path "{filepath}" does not exist or is not a file.'
        )
    stats: Dict[str, _DecodedBlockType] = {}
    with open(filepath, "rb") as file:
        # Read file header.
        binary_blob = file.read(4)
        if len(binary_blob) < 4:
            raise ValueError(
                f"File header should have length 4, but binary blob of length "
                f"{len(binary_blob)} received."
            )
        while True:
            # Read and parse block header.
            binary_blob = file.read(8)
            if len(binary_blob) == 0:
                break  # End of file.
            block_header = BlockHeader.from_bytes(binary_blob)
            # Read and parse block data.
            binary_blob = file.read(block_header.length)
            stats[block_header.tag] = block_header.decode_block(binary_blob)
            # Skip block padding.
            file.read(block_header.padding)
    return stats


def prettify_stats(
    raw_stats: Dict[str, _DecodedBlockType], save_raw: bool
) -> Dict[str, Dict[str, _DecodedBlockType]]:
    """
    Prettify the parsed statistics from a `"stats.dmp"` file.

    Args:
        raw_stats: Parsed statistics (output of `parse_stats` function).
        save_raw: Whether to save not prettified values too.

    Returns:
        Prettified statistics.
    """
    stats: DefaultDict[str, Dict[str, _DecodedBlockType]] = defaultdict(dict)
    for tag, value in raw_stats.items():
        if tag[-1] in "01234567":
            # Player-specific data.
            key = raw_stats["NAM" + tag[-1]]
            tag = tag[:-1]
        else:
            # Common game data.
            key = "game"
        # Prettify data.
        # Player-specific tags.
        if tag == "CMP":
            for code, status in mappings.COMPLETION_CODES.items():
                stats[key][status] = bool(value & code)
        elif tag == "RSG":
            stats[key]["quit"] = value
        elif tag == "DED":
            stats[key]["defeated"] = value
        elif tag == "SPC":
            stats[key]["spectator"] = value
        elif tag in ("LCN", "CON"):
            stats[key]["disconnected"] = value
        elif tag == "CTY":
            stats[key]["side"] = mappings.SIDES[value]
        elif tag == "NAM":
            stats[key]["name"] = value
        elif tag == "CRD":
            stats[key]["credits_left"] = value
        # Common tags.
        elif tag == "DURA":
            stats[key]["duration"] = value
        elif tag == "AFPS":
            stats[key]["fps"] = value
        elif tag == "FINI":
            stats[key]["finished"] = value
        elif tag == "TIME":
            stats[key]["timestamp"] = value
        elif tag == "SCEN":
            stats[key]["map"] = value
        elif tag == "UNIT":
            stats[key]["starting_units"] = value
        elif tag == "CRED":
            stats[key]["starting_credits"] = value
        elif tag == "SUPR":
            stats[key]["superweapons"] = bool(value)
        elif tag == "CRAT":
            stats[key]["crates"] = bool(value)
        elif tag == "PLRS":
            stats[key]["human_players"] = value
        elif tag == "BAMR":
            stats[key]["mcv_repacks"] = bool(value & 1)
            stats[key]["build_off_ally_conyards"] = bool(value & 2)
        elif tag == "SHRT":
            stats[key]["short_game"] = bool(value)
        elif tag == "AIPL":
            stats[key]["ai_players"] = value
        elif tag == "VERS":
            stats[key]["game_version"] = value
        elif tag in mappings.HUMAN_READABLE_COUNTABLES:
            human_readable_tag = mappings.HUMAN_READABLE_COUNTABLES[tag]
            stats[key][f"total_{human_readable_tag}"] = sum(value.values(), 0)
            stats[key][human_readable_tag] = value
        elif save_raw:
            stats[f"{key}_raw"][tag] = value
    for key, value in stats.items():
        if key.startswith("game") or key.endswith("raw"):
            continue
        for suffix in ("built", "killed", "left", "captured", "found"):
            stats[key][f"total_{suffix}"] = sum(
                (
                    value
                    for key, value in value.items()
                    if key.startswith("total") and key.endswith(suffix)
                ),
                0,
            )
    return stats
