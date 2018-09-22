import random

categories = {}
syllables = {}
namespace = []

f = open("samplelanguage.txt", "r")

lines = f.readlines()
currentline = 1

def vomit(error):
    raise SyntaxError("Line" + str(currentline) + ": " + error)

def parsecategory(definition):
    prefix, contents = definition.split(":")
    name = prefix.split(" ")[1]
    phonemes = [x.strip() for x in contents.split(",")]

    namespace.append(name)
    for x in phonemes:
        if x not in namespace: namespace.append(x)

    categories[name] = phonemes

def pullelements(syllable):
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
        pullelements(syllable[endpoint+1:]))
    return elements


def parsesyllable(definition):
    prefix, contents = definition.split(":")
    name = prefix.split(" ")[1]
    syllable = []

    elements = pullelements(contents.strip())
    for x in elements:
        if x[0] == "[":
            syllable.append([x[1:-1], ""])
        else:
            syllable.append([x[1:-1]])
    syllables[name] = syllable

def parsedefinitions (lines):
    global currentline
    for definition in lines:
        currentline += 1
        if definition.isspace():
            continue

        lead = definition.split(" ")[0]
        if lead == "cat":
            parsecategory(definition)
        elif lead == "syll":
            parsesyllable(definition)
        else:
            vomit("'" + lead + "' is not a valid type")

def genword (num):
    for i in range(0, num):
        print(gensyll() + gensyll() + gensyll())

def gensyll():
    syll = ""
    syllstruct = []
    sylltype = random.choice(list(syllables.keys()))
    for element in syllables[sylltype]:
        syllstruct.append(random.choice(element))

    for cat in syllstruct:
        if cat == '':
            continue
        syll += random.choice(categories[cat])

    return syll

parsedefinitions(lines)
print(categories)
print(syllables)
print(namespace)

genword(10)
