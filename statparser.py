"""
This module provides functions for parsing and prettifying `"stats.dmp"` file.
"""

import base64
import json
import os
import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from struct import unpack
from typing import Dict, List, Union

import mappings


PLAYER_SUFFIXES = "01234567"


_DecodedBlockType = Union[bool, int, str, Dict[str, int]]
_PrettifiedStatsType = Dict[str, Union[_DecodedBlockType, Dict[str, _DecodedBlockType]]]


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


def write_dict_to_json(data: Dict, output_file: str) -> None:
    """
    Save a dict as file in human readable JSON format.

    Args:
        data: Dict to save.
        output_file: Output file.
    """
    with open(output_file, "w") as file:
        json.dump(data, file, indent=4, sort_keys=True)


@dataclass(frozen=True)
class BlockHeader:
    """
    Class for storing block header and decoding block data.
    """

    tag: str
    type: int
    length: int

    @property
    def padding(self) -> int:
        """
        Block data padding.
        """
        if self.length % 4:
            return 4 - self.length % 4
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
        if len(binary_blob) != self.length:
            raise ValueError(
                f"Block data should have length {self.length}, "
                f"but binary blob of length {len(binary_blob)} received."
            )
        if self.type == 1:
            # A single byte.
            return unpack(">c", binary_blob)[0]
        if self.type == 2:
            # A single boolean.
            return unpack(">?", binary_blob)[0]
        if self.type == 3:
            # A single short.
            return unpack(">h", binary_blob)[0]
        if self.type == 4:
            # A single unsigned short.
            return unpack(">H", binary_blob)[0]
        if self.type == 5:
            # A single long.
            return unpack(">l", binary_blob)[0]
        if self.type == 6:
            # A single unsigned long.
            return unpack(">L", binary_blob)[0]
        if self.type == 7:
            # Multiple b"\x00"-terminated chars.
            return bytes_to_ascii(binary_blob.rstrip(b"\x00"))
        if self.type == 20:
            # Custom type and length.
            if self.tag[:3] in mappings.HUMAN_READABLE_COUNTABLES:
                # Multiple unsigned longs.
                if self.length % 4:
                    raise ValueError(
                        f"Length of block data should be multiple of 4, "
                        f"but {self.length} received."
                    )
                counts = unpack(f">{self.length // 4}L", binary_blob)
                return {
                    mappings.COUNTABLE_TYPES[self.tag[:2]][i]: count
                    for i, count in enumerate(counts)
                    if count > 0
                }
            # Raw bytes.
            # Bytes are not json serializable, so encode them as base64.
            return base64.b64encode(binary_blob).decode("ascii")
        raise ValueError(f"Decoding rule for type {self.type} is unknown.")


def parse_stats(filepath: str) -> Dict[str, _DecodedBlockType]:
    """
    Parse a `"stats.dmp"` file to dict.

    Args:
        filepath: Path to a `"stats.dmp"` file.

    Returns:
        Parsed statistics.
    """
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


def prettify_player_stats(
    raw_stats: Dict[str, _DecodedBlockType]
) -> _PrettifiedStatsType:
    """
    Prettify stats of a player. Only tags (keys of `raw_stats`) of one player
    without specific suffix expected.
    """
    stats: _PrettifiedStatsType = {}
    detailed_counts: Dict[str, int] = {}
    raw: Dict[str, _DecodedBlockType] = {}
    for tag, value in raw_stats.items():
        if tag == "CMP":
            for code, status in mappings.COMPLETION_CODES.items():
                stats[status] = bool(value & code)
        elif tag == "RSG":
            stats["quit"] = value
        elif tag == "DED":
            stats["defeated"] = value
        elif tag == "SPC":
            stats["spectator"] = value
        elif tag in ("LCN", "CON"):
            stats["disconnected"] = value
        elif tag == "CTY":
            stats["side"] = mappings.SIDES[value]
        elif tag == "NAM":
            stats["name"] = value
        elif tag == "CRD":
            stats["funds_left"] = value
        elif tag in mappings.HUMAN_READABLE_COUNTABLES:
            human_readable_tag = mappings.HUMAN_READABLE_COUNTABLES[tag]
            stats[human_readable_tag] = sum(value.values(), 0)
            detailed_counts[human_readable_tag] = value
        else:
            raw[tag] = value
    stats["raw"] = raw
    stats["detailed_counts"] = detailed_counts
    return stats


def prettify_game_stats(
    raw_stats: Dict[str, _DecodedBlockType]
) -> _PrettifiedStatsType:
    """
    Prettify stats of a game. Only non-player specific tags (keys of
    `raw_stats`) expected.
    """
    stats: _PrettifiedStatsType = {}
    raw: Dict[str, _DecodedBlockType] = {}
    for tag, value in raw_stats.items():
        if tag == "DURA":
            stats["duration"] = value
        elif tag == "AFPS":
            stats["fps"] = value
        elif tag == "FINI":
            stats["finished"] = value
        elif tag == "TIME":
            stats["epoch_time"] = value
        elif tag == "SCEN":
            stats["map"] = value
        elif tag == "UNIT":
            stats["starting_units"] = value
        elif tag == "CRED":
            stats["starting_credits"] = value
        elif tag == "SUPR":
            stats["superweapons"] = bool(value)
        elif tag == "CRAT":
            stats["crates"] = bool(value)
        elif tag == "PLRS":
            stats["players_in_game"] = value
        elif tag == "BAMR":
            stats["mcv_repacks"] = bool(value & 1)
            stats["build_off_ally_conyards"] = bool(value & 2)
        elif tag == "SHRT":
            stats["short_game"] = bool(value)
        elif tag == "AIPL":
            stats["ai_players"] = value
        elif tag == "VERS":
            stats["game_version"] = value
        else:
            raw[tag] = value
    stats["raw"] = raw
    return stats


def process_stats(stats_file: str, output_folder: str, reporter_name: str) -> str:
    """
    Backup, parse and prettify a `"stats.dmp"` file.

    Args:
        stats_file: `"stats.dmp"` file.
        output_folder: Backup folder.
        reporter_name: Name of the current player to parse the game status from.

    Returns:
        Path to the prettified stats in JSON format.
    """
    if not os.path.isfile(stats_file):
        raise FileNotFoundError(
            f'Given path "{stats_file}" does not exist or is not a file.'
        )

    raw_stats = parse_stats(stats_file)
    players_stats = []
    for suffix in PLAYER_SUFFIXES:
        player_raw_stats = {
            tag[:-1]: value for tag, value in raw_stats.items() if tag.endswith(suffix)
        }
        if player_raw_stats:
            players_stats.append(prettify_player_stats(player_raw_stats))
    game_raw_stats = {
        tag: value for tag, value in raw_stats.items() if tag[-1] not in PLAYER_SUFFIXES
    }
    game_stats = prettify_game_stats(game_raw_stats)
    game_result = "unknown"
    for player_stats in players_stats:
        if player_stats["name"] == reporter_name:
            for status in mappings.COMPLETION_CODES.values():
                if player_stats[status] is True:
                    game_result = status
                    break

    stats: Dict[str, Union[str, _PrettifiedStatsType, List[_PrettifiedStatsType]]] = {
        "gameReport": game_stats,
        "playerStats": players_stats,
        "gameResult": game_result,
    }

    timestamp = game_stats["epoch_time"]
    output_folder = os.path.join(
        output_folder,
        datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H-%M-%S"),
    )
    os.makedirs(output_folder, exist_ok=True)
    shutil.copy(stats_file, os.path.join(output_folder, f"{timestamp}_stats.dmp"))
    write_dict_to_json(
        raw_stats, os.path.join(output_folder, f"{timestamp}_stats_raw.json")
    )
    stats_json_file = os.path.join(output_folder, f"{timestamp}_stats_parsed.json")
    write_dict_to_json(stats, stats_json_file)
    return stats_json_file
