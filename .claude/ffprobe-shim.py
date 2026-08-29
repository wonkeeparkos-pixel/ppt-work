#!/usr/bin/env python3
"""Minimal ffprobe replacement backed by PyAV, for environments where the real
ffprobe binary cannot be installed (e.g. remote containers without apt access).

Supports the invocation shape used by the watch skill:
  ffprobe -v quiet -print_format json -show_format [-show_streams] <file>
Emits the ffprobe JSON fields the skill reads: format.duration, format.size,
streams[].codec_type/codec_name/width/height/duration.

Install:  pip install av && cp .claude/ffprobe-shim.py /usr/local/bin/ffprobe && chmod +x /usr/local/bin/ffprobe
"""
import json
import os
import sys


def main() -> int:
    args = sys.argv[1:]
    show_format = "-show_format" in args
    show_streams = "-show_streams" in args
    # Input file: last argument that is not a flag or a flag's value.
    flag_with_value = {"-v", "-print_format", "-of", "-select_streams", "-show_entries"}
    path = None
    i = 0
    while i < len(args):
        a = args[i]
        if a in flag_with_value:
            i += 2
            continue
        if a.startswith("-"):
            i += 1
            continue
        path = a
        i += 1
    if not path or not os.path.exists(path):
        print(f"ffprobe-shim: input file not found: {path}", file=sys.stderr)
        return 1

    try:
        import av
    except ImportError:
        print("ffprobe-shim: PyAV missing — run: pip install av", file=sys.stderr)
        return 1

    try:
        container = av.open(path)
    except Exception as exc:
        print(f"ffprobe-shim: cannot open {path}: {exc}", file=sys.stderr)
        return 1

    duration = float(container.duration) / 1_000_000.0 if container.duration else 0.0
    out = {}
    if show_format:
        out["format"] = {
            "filename": path,
            "format_name": container.format.name if container.format else "",
            "duration": f"{duration:.6f}",
            "size": str(os.path.getsize(path)),
        }
    if show_streams:
        streams = []
        for s in container.streams:
            entry = {
                "index": s.index,
                "codec_type": s.type,
                "codec_name": getattr(s.codec_context, "name", "") or "",
            }
            if s.type == "video":
                entry["width"] = s.codec_context.width
                entry["height"] = s.codec_context.height
            if s.duration is not None and s.time_base is not None:
                entry["duration"] = f"{float(s.duration * s.time_base):.6f}"
            elif duration:
                entry["duration"] = f"{duration:.6f}"
            streams.append(entry)
        out["streams"] = streams

    json.dump(out, sys.stdout, indent=1)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
