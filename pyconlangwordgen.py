# -*- coding: utf-8 -*-
# PyConlangWordGen v1.0
import sys
import random
import re

sections = ['-CATEGORIES', '-REWRITE', '-SYLLABLES', '-ILLEGAL',
            '-ILLEGALEXCEPTIONS', '-PARAMS', '']
paramlist = ['minsylls', 'maxsylls']
categories = {'#':['#'], '%':['%']}
syllables = []
illegal = []
rewrite = {'#':'', '$':''}
exceptions = []
minSyllables = 1
maxSyllables = 3

# Check that arguments are correct
if len(sys.argv) < 3 or len(sys.argv) > 3:
    print("Invalid arguments.")
    print("syntax: python pywordgen.py [RULESFILE] [NUMWORDS]")
    sys.exit()

# Check that our arguments are typed correctly
try:
    rules = sys.argv[1]
    numwords = int(sys.argv[2])
except ValueError:
    print("Invalid arguments")
    print("syntax: python pywordgen.py [RULESFILE] [NUMWORDS]")
    sys.exit()

# Ensure that the rules file actually exists
try:
    f = open(rules)
    rules = None  # I want to keep using the rules variable
    rules = f.read().split("\n")
    f.close()
except OSError:
    print("Rules file could not be found.")
    print("syntax: python pywordgen.py [RULESFILE] [NUMWORDS]")

# Set up phoneme categories
try:
    for i in range(rules.index('-CATEGORIES') + 1, len(rules)):
        if rules[i] in sections:
            break
        cat, included = rules[i].split(':')
        if len(cat) > 1:
            print("Your category names must be only one character long.")
            print(cat + " is invalid.")
            sys.exit()
        if len(included) < 1:
            print("You must include some phonemes in category " + cat)
            sys.exit()
        categories[cat] = [char for char in included]
        for phone in included:
            categories[phone] = phone
except ValueError:
    print("You must specify some categories.")
    sys.exit()

# Set up syllable types
try:
    for i in range(rules.index('-SYLLABLES') + 1, len(rules)):
        if rules[i] in sections:
            break
        syllables.append(rules[i])
except ValueError:
    print("You must specify some syllable types.")
    sys.exit()

# Set up rewrite rules
try:
    for i in range(rules.index('-REWRITE') + 1, len(rules)):
        if rules[i] in sections:
            break
        inp, outp = rules[i].split('|')
        if len(inp) < 1 or len(outp) < 1:
            print("Invalid rewrite rule: " + rules[i])
            sys.exit()
        rewrite[inp] = outp
except ValueError:
    pass  # The user didn't specify any rewrite rules, that's okay.

# Set up illegal clusters
try:
    for i in range(rules.index('-ILLEGAL') + 1, len(rules)):
        if rules[i] in sections:
            break
        if len(rules[i]) < 2:
            print("Error with illegal cluster: " + rules[i])
            print("Illegal clusters must be longer than a single category.")
            sys.exit()

        # Recursively returns a regex that fits the rule
        def generate_regex(rule):
            if len(rule) > 2:
                return "[" + ''.join(categories[rule[0]]) + "]" + generate_regex(rule[1:])
            else:
                return "[" + ''.join(categories[rule[0]]) + "][" + ''.join(categories[rule[1]]) + "]"

        illegal.append("(?=(" + generate_regex(rules[i]) + "))")
except ValueError:
    print("Warning: No illegal clusters specified.")
    print("You don't have to specify any, but most languages do.")

# Create a list of exceptionss
try:
    for i in range(rules.index('-ILLEGALEXCEPTIONS') + 1, len(rules)):
        if rules[i] in sections:
            break

        #Recursively returns a list of clusters that fit the rule
        def generate_clusters(rule):
            if len(rule) > 2:
                outp = []
                for x in categories[rule[0]]:
                    for y in generate_clusters(rule[1:]):
                        outp.append(x + y)
                return outp
            else:
                outp = []
                for x in categories[rule[0]]:
                    for y in categories[rule[1]]:
                        outp.append(x + y)
                return outp
        exceptions += generate_clusters(rules[i])
except ValueError:
    pass  # User hasn't specified any exceptions, and that's okay.

# Read language-specific parameters
try:
    for i in range(rules.index('-PARAMS') + 1, len(rules)):
        if rules[i] in sections:
            break
        param = rules[i].split("=")
        if param[0].strip() not in paramlist:
            print(param[0] + " is not a valid parameter. Make sure  you have spelled the parameter name correctly.")
        elif param[0].strip() == 'minsylls':
            try:
                minSyllables = int(param[1])
            except ValueError:
                print(rules[i] + " is an invalid parameter declaration. Using default value of minsylls: " + str(minSyllables))
        elif param[0].strip() == 'maxsylls':
            try:
                maxSyllables = int(param[1])
            except ValueError:
                print(rules[i] + " is an invalid parameter declaration. Using default value of minsylls: " + str(maxSyllables))
except ValueError:
    pass  # No parameters? No problem.

def generatesyllable(index, size):
    syll = random.choice(syllables)
    # Ensure that we aren't putting a word-initial or word-final syllable
    # in the middle of the word.
    while ("#" in syll and index != 0) or ("%" in syll and index != size):
        syll = random.choice(syllables)
    syll = syll[1:] if "#" in syll else syll
    syll = syll[:-1] if "%" in syll else syll
    outp = ""
    for char in syll:
        try:
            outp = outp + random.choice(categories[char])
        except KeyError:
            print(char + " in syllable " + syll + " is not a defined category.")
    return outp


def check_illegal(word):
    if word == "#%":
        return True
    for ill in illegal:
        check = re.findall(ill, word)
        if check:
            lastindex = 0
            for ch in check:
                lastindex = word.find(ch, lastindex + 1)
                for ex in exceptions:
                    handled = False
                    if lastindex > 0:
                        if len(word) > 4 + lastindex:
                            cut = word[lastindex-1:len(ch)+2]
                        else:
                            cut = word[lastindex-1:len(word)]
                    else:
                        if len(word) > 4:
                            cut = word[0:len(ch)+2]
                        else:
                            cut = word
                    if ex in cut:
                        handled = True
                if not handled:
                    return True
    return False


def rewrite_word(word):
    if len(rewrite) < 1:
        return word
    for inp, outp in rewrite.items():
        if inp in word:
            word = word.replace(inp, outp)
    return word


# Actually generate words
for n in range(0, numwords):
    word = ""
    while check_illegal("#" + word + "%"):
        word = ""
        size = random.randint(minSyllables, maxSyllables)
        for s in range(0, size):
            word = word + generatesyllable(s, size - 1)
    print(rewrite_word(word))