# Converted with ipynb-to-py.py on 2022-09-09 12:19

from collections import Counter
from pprint import pprint

ascii_control_codes = {
    '\\x00': '^@',
    '\\x01': '^A',
    '\\x02': '^B',
    '\\x03': '^C',
    '\\x04': '^D',
    '\\x05': '^E',
    '\\x06': '^F',
    '\\x07': '^G',
    '\\x08': '^H',
    '\\x09': '^I',
    '\\x0a': '^J',
    '\\x0b': '^K',
    '\\x0c': '^L',
    '\\x0d': '^M',
    '\\x0e': '^N',
    '\\x0f': '^O',
    '\\x10': '^P',
    '\\x11': '^Q',
    '\\x12': '^R',
    '\\x13': '^S',
    '\\x14': '^T',
    '\\x15': '^U',
    '\\x16': '^V',
    '\\x17': '^W',
    '\\x18': '^X',
    '\\x19': '^Y',
    '\\x1a': '^Z',
    '\\x1b': '^[',
    '\\x1c': '^\\',
    '\\x1d': '^]',
    '\\x1e': '^^',
    '\\x1f': '^_',
    '\\x7f': '^?',
}

def human_readable(token):
    if token in ascii_control_codes:
        return ascii_control_codes[token]
    return token

frequencies_for_tokens = Counter()
frequencies_for_bigrams = Counter()
frequencies_for_trigrams = Counter()
previous_token = None
preprevious_token = None
with open('vim.log', 'r') as f:
    for line in f:
        token = line.replace('\n', '')
        token = human_readable(token)
        frequencies_for_tokens[token] += 1
        if previous_token is not None:
            frequencies_for_bigrams[previous_token+token] += 1
        if preprevious_token is not None:
            frequencies_for_trigrams[preprevious_token+previous_token+token] += 1
        preprevious_token = previous_token
        previous_token = token

pprint(frequencies_for_tokens.most_common(10))

pprint(frequencies_for_bigrams.most_common(10))

pprint(frequencies_for_trigrams.most_common(10))
