from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

BOLD_UPPER_A = 0x1D5D4
BOLD_LOWER_A = 0x1D5EE
BOLD_DIGIT_0 = 0x1D7EC
ITALIC_UPPER_A = 0x1D608
ITALIC_LOWER_A = 0x1D622
BULLET = "\u2022 "


def _configure_stdio() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")


def _translate_char(char: str, *, upper_start: int, lower_start: int, digit_start: int | None = None) -> str:
    if "A" <= char <= "Z":
        return chr(upper_start + ord(char) - ord("A"))
    if "a" <= char <= "z":
        return chr(lower_start + ord(char) - ord("a"))
    if digit_start is not None and "0" <= char <= "9":
        return chr(digit_start + ord(char) - ord("0"))
    return char


def to_bold(text: str) -> str:
    return "".join(
        _translate_char(
            char,
            upper_start=BOLD_UPPER_A,
            lower_start=BOLD_LOWER_A,
            digit_start=BOLD_DIGIT_0,
        )
        for char in text
    )


def to_italic(text: str) -> str:
    return "".join(
        _translate_char(
            char,
            upper_start=ITALIC_UPPER_A,
            lower_start=ITALIC_LOWER_A,
        )
        for char in text
    )


def markdown_to_linkedin(markdown_text: str) -> str:
    lines = markdown_text.splitlines()
    output: list[str] = []
    in_code_block = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue

        if in_code_block:
            output.append(line)
            continue

        heading_match = re.match(r"^(#{1,6})\s+(.*)", line)
        if heading_match:
            heading_text = heading_match.group(2).strip()
            if output and output[-1] != "":
                output.append("")
            output.append(to_bold(heading_text.upper()))
            output.append("")
            continue

        line = re.sub(
            r"!\[(.*?)\]\((.*?)\)",
            lambda match: f"{match.group(1) or 'Image'}: {match.group(2)}",
            line,
        )
        line = re.sub(
            r"\[(.*?)\]\((.*?)\)",
            lambda match: f"{match.group(1)} ({match.group(2)})",
            line,
        )
        line = re.sub(
            r"(\*\*|__)(.+?)\1",
            lambda match: to_bold(match.group(2)),
            line,
        )
        line = re.sub(
            r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)",
            lambda match: to_italic(match.group(1)),
            line,
        )
        line = re.sub(
            r"(?<!_)_(?!_)(.+?)(?<!_)_(?!_)",
            lambda match: to_italic(match.group(1)),
            line,
        )
        line = re.sub(r"`([^`]+)`", r"[\1]", line)
        line = re.sub(r"^\s*[-*]\s+", BULLET, line)

        output.append(line)

    return "\n".join(output).strip()


def _read_markdown(markdown_file: str | None) -> str:
    if markdown_file:
        return Path(markdown_file).read_text(encoding="utf-8")
    return sys.stdin.read()


def main(argv: list[str] | None = None) -> int:
    _configure_stdio()

    parser = argparse.ArgumentParser(
        description="Convert Markdown text into a LinkedIn-friendly post body.",
    )
    parser.add_argument(
        "markdown_file",
        nargs="?",
        help="Optional markdown file path. If omitted, content is read from stdin.",
    )
    args = parser.parse_args(argv)

    markdown_text = _read_markdown(args.markdown_file)
    if not markdown_text.strip():
        raise ValueError("No markdown content provided.")

    print(markdown_to_linkedin(markdown_text))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as err:
        print(str(err), file=sys.stderr)
        raise SystemExit(1)
