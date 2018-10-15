import random


CURRENTLINE = 1
NAMESPACE = []

def vomit(error):
    """Shortcut error-raising function to reduce boilerplate."""
    raise SyntaxError("Line" + str(CURRENTLINE) + ": " + error)

def parse_name(definition):
    """
    For a given line, returns an array containing the name
    defined at that location, and the contents of the definition.
    """
    prefix, contents = definition.split(":")
    name = prefix.split(" ")[1]
    return name, contents

def parse_category(definition):
    """Reads a phoneme category and stores it in CATEGORIES"""
    name, contents = parse_name(definition)
    phonemes = [x.strip() for x in contents.split(",")]

    NAMESPACE.append(name)
    for x in phonemes:
        if x not in NAMESPACE:
            NAMESPACE.append(x)

    return name, phonemes

def pull_elements(syllable):
    """
    For a given syllable definition, returns a list of all
    bracket- or parenthesis- bounded elements.
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


def parse_syllable(definition):
    """
    For a given syllable definition, reads it and
    stores it in SYLLABLES.

    Syllables are stored as nested lists, each interior
    list representing a valid phoneme or phoneme group
    for that section of the syllable. If a phoneme is
    optional, the list includes the empty string.
    """
    name, contents = parse_name(definition)

    if name in NAMESPACE:
        vomit("'" + "' is already in use")

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
    return name, syllable

def parse_definitions(lines):
    """
    The basic parse loop. Steps through each line of the
    language file and identifies what sort of definition
    it is, then passes it off to the appropriate parsing
    function.
    """
    global CURRENTLINE
    categories = {}
    syllables = {}
    for definition in lines:
        CURRENTLINE += 1

        # skip empty lines
        if definition.isspace():
            continue

        # lead is the first word of the line
        lead = definition.split(" ")[0]
        if lead == "cat":
            name, cat = parse_category(definition)
            categories[name] = cat
        elif lead == "syll":
            name, syll = parse_syllable(definition)
            syllables[name] = syll
        else:
            vomit("'" + lead + "' is not a valid type")
    return categories, syllables

class Parse:
    categories = {}
    syllables = {}

    def __init__(self, file):
        f = open(file, 'r')
        l = f.readlines()
        self.categories, self.syllables = parse_definitions(l)

