"""This script attempts to find words in the log file.

This is a security measure against sharing sensitive information in case you
want to share your log file.

It works only with English language for now.

Usage:
    python -m pip install english-words
    python scripts/find-words.py <vim.log>
"""
import fileinput
from pprint import pprint

from english_words import english_words_lower_set


def main():
    token_list = list(map(lambda x: x[:-1], fileinput.input(mode='r', encoding='utf-8')))
    idx = 0
    word_list = set()
    while True:
        if idx >= len(token_list):
            break
        for word_length in range(3, 10):
            if (
                word := "".join(token_list[idx : idx + word_length])
            ).lower() in english_words_lower_set:
                word_list.add(word)
                idx += word_length
                break
        idx += 1

    pprint(word_list)


if __name__ == "__main__":
    main()
