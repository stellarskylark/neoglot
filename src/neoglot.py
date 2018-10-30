#!/usr/bin/env python3

"""The primary executable file for Neoglot. Uses ``click`` to
provide a command-line interface.

The function run() is not picked up by Sphinx because of ``click``,
but it is the actual command which the CLI runs.
"""

import click
import random
import sys

CATEGORIES = {}
SYLLABLES = {}


@click.command()
@click.argument("file")
@click.option('--count', default=20,
              help='number of words to generate')
@click.option('--minsylls', default=1,
              help='minimum number of syllables per word')
@click.option('--maxsylls', default=3,
              help='maximum number of syllables per word')
def run(file, count, minsylls, maxsylls):
    """Actually runs the generator. Note that all parameters are
    supplied by the CLI through click.
    """
    # Perform error checking
    if minsylls > maxsylls:
        click.echo("Error: minsylls cannot be greater than maxsylls")
        sys.exit(2)
    elif minsylls < 1:
        click.echo("Error: minsylls must be greater than 1")
        sys.exit(2)
    elif count < 1:
        click.echo("Error: count must be greater than 1")
        sys.exit(2)

    try:
        file_contents = open(file, 'r')
    except FileNotFoundError:
        click.echo("Error: file " + file + " does not exist")
        sys.exit(2)

    global CATEGORIES, SYLLABLES
    parser = Parse(file_contents)
    CATEGORIES = parser.categories
    SYLLABLES = parser.syllables
    print_words(count, minsylls, maxsylls)


def print_words(count, minsylls, maxsylls):
    """Prints a number of valid words."""
    for _ in range(count):
        click.echo(gen_word(minsylls, maxsylls))


def gen_word(minsylls, maxsylls):
    """Generates a word with the specified number of syllables."""
    word = ""
    for _ in range(random.randint(minsylls, maxsylls)):
        word += gen_syll()
    return word


def gen_syll():
    """Generates a syllable with a random syllable structure."""
    syll = ""
    syllstruct = []
    sylltype = random.choice(list(SYLLABLES.keys()))
    for element in SYLLABLES[sylltype]:
        syllstruct.append(random.choice(element))

    for cat in syllstruct:
        if cat == '':
            continue
        if cat in CATEGORIES.keys():
            syll += random.choice(CATEGORIES[cat])
        else:
            syll += cat
    return syll


if __name__ == '__main__':
    run()
