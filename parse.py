import random


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

    CATEGORIES[name] = phonemes

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
        pull_elements(syllable[endpoint+1:]))
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
        print(identifiers)
        for identifier in identifiers:
            if identifier not in NAMESPACE:
                vomit("'" + identifier + "' has not been defined")
        if elem[0] == "[":
            identifiers.append('')
        syllable.append(identifiers)
    SYLLABLES[name] = syllable

def parse_definitions(lines):
    """
    The basic parse loop. Steps through each line of the
    language file and identifies what sort of definition
    it is, then passes it off to the appropriate parsing
    function.
    """
    global CURRENTLINE
    for definition in lines:
        CURRENTLINE += 1

        # skip empty lines
        if definition.isspace():
            continue

        # lead is the first word of the line
        lead = definition.split(" ")[0]
        if lead == "cat":
            parse_category(definition)
        elif lead == "syll":
            parse_syllable(definition)
        else:
            vomit("'" + lead + "' is not a valid type")

def gen_word(num):
    """Temporary function for testing purposes."""
    for _ in range(0, num):
        print(gen_syll() + gen_syll() + gen_syll())

def gen_syll():
    """Temporary function for testing purposes."""
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

CATEGORIES = {}
SYLLABLES = {}
NAMESPACE = []

f = open("samplelanguage.txt", "r")

l = f.readlines()
CURRENTLINE = 1


parse_definitions(l)
print(CATEGORIES)
print(SYLLABLES)
print(NAMESPACE)

gen_word(10)
