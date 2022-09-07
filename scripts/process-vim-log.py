import fileinput
import os
import re
import signal
import sys

DEBUG = os.environ.get("DEBUG", False)

INVALID_INPUT_LIST = (
    # Vim Leave/Enter events
    '\\x1b[O',
    '\\x1b[I',
)

interrupted = False


def sigpipe_handler(_signo, _frame):
    global interrupted # pylint: disable=global-statement
    interrupted = True


signal.signal(signal.SIGPIPE, sigpipe_handler)


def main():
    timestamp_pattern = rb"\s*\d+.\d+\s+:\s+"

    # Patterns to leave out irrelevant `modes`.
    enter_command_line_window = re.compile(
        timestamp_pattern + rb"::Entering command-line window::"
    )
    enter_command_line_mode = re.compile(
        timestamp_pattern + rb"::Entering command-line mode::"
    )
    enter_insert_mode = re.compile(timestamp_pattern + rb"::Entering Insert Mode::")
    leave_command_line_window = re.compile(
        timestamp_pattern + rb"::Leaving command-line window::"
    )
    leave_command_line_mode = re.compile(
        timestamp_pattern + rb"::Leaving command-line mode::"
    )
    leave_insert_mode = re.compile(timestamp_pattern + rb"::Leaving Insert Mode::")

    raw_key_input = re.compile(
        timestamp_pattern + rb'raw key input: "(?P<key>.{,10}?)"'
    )

    def match_enter(line) -> bool:
        return bool(
            enter_command_line_window.match(line)
            or enter_command_line_mode.match(line)
            or enter_insert_mode.match(line)
        )

    def match_leave(line) -> bool:
        return bool(
            leave_command_line_window.match(line)
            or leave_command_line_mode.match(line)
            or leave_insert_mode.match(line)
        )

    in_ignored_block = False
    lineno = 0
    try:
        for line in fileinput.input(mode="rb"):
            if interrupted:
                break
            lineno += 1
            line: bytes
            if match_enter(line):
                in_ignored_block = True
                continue
            if match_leave(line):
                in_ignored_block = False
                continue
            if in_ignored_block:
                continue

            if (m := raw_key_input.match(line)) is not None:
                if DEBUG:
                    print(f'{lineno} {m.group("key")}')
                else:
                    token = repr(m.group("key"))[2:-1]
                    if token not in INVALID_INPUT_LIST:
                        print(token)
            sys.stdout.flush()
    except BrokenPipeError:
        # Python flushes standard streams on exit; redirect remaining output
        # to devnull to avoid another BrokenPipeError at shutdown
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        sys.exit(1)  # Python exits with error code 1 on EPIPE


if __name__ == "__main__":
    main()
