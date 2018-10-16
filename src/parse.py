"""Contains functions related to interpreting the Neoglot DSL.

The interface essentially involves creating an instance of Parse, which will
automatically interpret the given Neoglot file.

"""
import random
import click
import sys

CURRENTLINE = 1
NAMESPACE = []

def vomit(error):
    """Shortcut error-raising function to reduce boilerplate."""
    click.echo("SYNTAX ERROR -- Line " + str(CURRENTLINE) + ": " + error)
    sys.exit(1)

def parse_def(definition):
    """For a given definition, returns a tuple containing the type of definition,
    name defined at that location, and the contents of the definition.

    """
    try:
        prefix, contents = definition.split(":")
    except ValueError: # No : in the definition, or multiple
        vomit("Expecting a single ':' in " + definition)

    if contents.strip() == '': # No definition after prefix
        vomit("Expecting a definition after ':', found nothing")

    try:
        def_type, name = prefix.strip().split(" ")
    except ValueError: # No def type or identifier
        vomit("Expecting prefix form 'type identifier:', got " + prefix)

    return def_type.strip(), name.strip(), contents.strip()

def parse_category(contents):
    """Given the contents of a category definition, returns a tuple a list of the
    phonemes it contains.

    """
    phonemes = []
    for x in contents.split(","):
        if ' ' in x.strip(): # missing comma somewhere
            vomit("Expecting ',' in " + x)
        else:
            phonemes.append(x.strip())

    if '' in phonemes: # double comma somewhere
        vomit("',,' is invalid")

    for x in phonemes:
        if x not in NAMESPACE:
            NAMESPACE.append(x)

    return phonemes

def pull_elements(syllable):
    """For a given syllable definition, returns a list of all bracket- or
    parenthesis- bounded elements.

    """
    elements = []
    endpoint = 0
    if syllable == "":
        return elements
    if syllable[0] == '[':
        endpoint = syllable.find(']')
    elif syllable[0] == '(':
        endpoint = syllable.find(')')
    else:
        vomit("expected '[' or '('")
    if endpoint == -1:
        vomit("expected ']'")

    elements.append(syllable[:endpoint+1])
    elements.extend(
        pull_elements(syllable[endpoint+1:].strip()))
    return elements


def parse_syllable(contents):
    """For a given syllable definition, returns a nested lists, each interior list
    representing a valid phoneme or phoneme group for that section of the
    syllable. If a phoneme is optional, the list includes the empty string.

    """
    syllable = []

    elements = pull_elements(contents.strip())
    for elem in elements:
        inside = elem[1:-1]
        identifiers = [x.strip() for x in inside.split("|")]
        for identifier in identifiers:
            if identifier not in NAMESPACE:
                vomit("'" + identifier + "' has not been defined")
        if elem[0] == "[":
            identifiers.append('')
        syllable.append(identifiers)
    return syllable

def parse_definitions(lines):
    """The basic parse loop. Steps through each line of the language file and
    identifies what sort of definition it is, then passes it off to the
    appropriate parsing function.

    """
    global CURRENTLINE
    categories = {}
    syllables = {}
    for definition in lines:
        CURRENTLINE += 1

        # skip empty lines
        if definition.isspace():
            continue

        def_type, name, cont = parse_def(definition)
        if name in NAMESPACE:
            vomit("'" + "' is already in use")
        else:
            NAMESPACE.append(name)

        if def_type == "cat":
            categories[name] = parse_category(cont)
        elif def_type == "syll":
            syllables[name] = parse_syllable(cont)
        else:
            vomit("'" + def_type + "' is not a valid type")
    return categories, syllables

class Parse:
    """
    Wrapper for the parse module that automatically runs
    all the parsing functions in ``__init__()`` and stores
    the parsed data in its internal variables.
    """
    categories = {}
    syllables = {}

    def __init__(self, file_contents):
        l = file_contents.readlines()
        self.categories, self.syllables = parse_definitions(l)

