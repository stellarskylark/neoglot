# -*- coding: utf-8 -*-
# PyConlangWordGen v1.1.3
import sys
import random
import re

sections = ['-CATEGORIES', '-REWRITE', '-SYLLABLES', '-ILLEGAL',
            '-ILLEGALEXCEPTIONS', '-PARAMS', '']
paramlist = ['minsylls', 'maxsylls', 'showrejected', 'show_pre_rewrite',
            'show_rewrite_trigger', 'filter_duplicates', 'never_generate_file']
categories = {}
syllables = []
illegal = []
rewritekeys = []  # Normally you'd just store these as a dictionary. However, we want the program to run
rewritevalues = []  # these rules in the order the user defines them. Iterating through a dictionary doesn't always do that.
exceptions = []
# Parameters
minsyllables = 1
maxsyllables = 3
showrejected = False
show_pre_rewrite = False
show_rewrite_trigger = False

filter_duplicates = True
already_generated = []
never_generate_file = ""

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
    rules = [x.strip() for x in f.read().split("\n") if x != '']
    f.close()
except OSError:
    print("Rules file could not be found.")
    print("syntax: python pywordgen.py [RULESFILE] [NUMWORDS]")


#Recursively returns a list of clusters that fit the rule
def generate_clusters(rule):
    if len(rule) > 1:
        outp = []
        try:
            for x in categories[rule[0]]:
                for y in generate_clusters(rule[1:]):
                    outp.append(x + y)
            return outp
        except KeyError:
            for y in generate_clusters(rule[1:]):
                outp.append(rule[0] + y)
            return outp
    else:
        outp = []
        try:
            for x in categories[rule[0]]:
                outp.append(x)
            return outp
        except KeyError:
            return [rule[0]]

# Set up phoneme categories
try:
    for i in range(rules.index('-CATEGORIES') + 1, len(rules)):
        if rules[i] in sections:
            break
        cat, included = rules[i].split(':')
        cat = cat.strip()
        included = included.strip().replace(' ', '')
        if len(cat) > 1:
            print("Your category names must be only one character long.")
            print(cat + " is invalid.")
            sys.exit()
        if len(included) < 1:
            print("You must include some phonemes in category " + cat)
            sys.exit()
        categories[cat] = [char for char in included]
except ValueError:
    print("You must specify some categories.")
    sys.exit()

# Set up syllable types
try:
    for i in range(rules.index('-SYLLABLES') + 1, len(rules)):
        if rules[i].strip() in sections:
            break
        syllables.append(rules[i].strip())
except ValueError:
    print("You must specify some syllable types.")
    sys.exit()

# Set up illegal clusters
try:
    for i in range(rules.index('-ILLEGAL') + 1, len(rules)):
        if rules[i].strip() in sections:
            break
        if len(rules[i].strip()) < 2:
            print("Error with illegal cluster: " + rules[i])
            print("Illegal clusters must be longer than a single category.")
            sys.exit()

        # Recursively returns a regex that fits the rule
        def generate_regex(rule):
            if len(rule) > 2:
                try:
                    return "[" + ''.join(categories[rule[0]]) + "]" + generate_regex(rule[1:])
                except KeyError:
                    return "[" + rule[0] + "]" + generate_regex(rule[1:])
            else:
                try:
                    cat1 = ''.join(categories[rule[0]])
                except KeyError:
                    cat1 = rule[0]
                try:
                    cat2 = ''.join(categories[rule[1]])
                except KeyError:
                    cat2 = rule[1]
                finally:
                    return "[" + cat1 + "][" + cat2 + "]"

        illegal.append("(?=(" + generate_regex(rules[i].strip()) + "))")
except ValueError:
    print("Warning: No illegal clusters specified.")
    print("You don't have to specify any, but most languages do.")

# Create a list of exceptionss
try:
    for i in range(rules.index('-ILLEGALEXCEPTIONS') + 1, len(rules)):
        if rules[i].strip() in sections:
            break
        exceptions += generate_clusters(rules[i].strip())
except ValueError:
    pass  # User hasn't specified any exceptions, and that's okay.

# Set up rewrite rules
try:
    for i in range(rules.index('-REWRITE') + 1, len(rules)):
        if rules[i].strip() in sections:
            break
        inp, outp = rules[i].split('|')
        inp = inp.strip()
        outp = outp.strip()
        if len(inp) < 1:
            print("Invalid rewrite rule: " + rules[i])
            sys.exit()
        for repl in generate_clusters(inp):
            rewritekeys.append(repl)
            rewritevalues.append(outp)
except ValueError:
    pass  # The user didn't specify any rewrite rules, that's okay.

# Read parameters
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
        elif param[0].strip() == 'showrejected':
            showrejected = True if param[1].strip() == 'True' else False
        elif param[0].strip() == 'show_pre_rewrite':
            show_pre_rewrite = True if param[1].strip() == 'True' else False
        elif param[0].strip() == 'show_rewrite_trigger':
            show_rewrite_trigger = True if param[1].strip() == 'True' else False
        elif param[0].strip() == 'filter_duplicates':
            filter_duplicates = False if param[1].strip() == 'False' else True
        elif param[0].strip() == 'never_generate_file':
            never_generate_file = param[1].strip()
except ValueError:
    pass  # No parameters? No problem.

#Set up never-generate file
if never_generate_file:
    try:
        f = open(never_generate_file)
        ng = f.read().split('\n')
        already_generated += ng
    except OSError:
        print("Could not find never-generate file at \"" + never_generate_file + "\"")
        print("Please make sure the path is correct before trying again.")
        sys.exit()

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
            outp = outp + char
    return outp


def check_illegal(word):
    if word == "#%":
        return True
    if filter_duplicates and word[1:-1] in already_generated:
        if showrejected:
            print(word[1:-1] + " rejected because it's a duplicate.")
        return True
    if never_generate_file:
        if word[1:-1] in already_generated:
            if showrejected:
                print(word[1:-1] + " rejected for being a duplicate")
            return True
        # This is so it works whether the word is specified in phoneme symbols
        # or in the conlang's final orthography.
        elif rewrite_word(word).replace('#', '').replace('%', '') in already_generated:
            if showrejected:
                print(word[1:-1] + " rejected for being a duplicate")
            return True
    # So, this is an unreadable monster, isn't it?
    # This bit of code first applies each illegality rule (a regex) to the word.
    # If it matches anything, it gets the index of each bit that matched.
    #
    # Then, it takes a slice containing the illegal string and the two
    # characters on either side (which allows the user to specify exceptional
    # environments.
    #
    # Finally, it checks if any of the illegality exceptions 'pardon' the string.
    # If at any point a string is found that both fits the illegality rules and
    # is not handled by an exception, return that the word is illegal.
    for ill in illegal:
        matches = re.findall(ill, word)
        if matches:
            lastindex = 0
            for m in matches:
                lastindex = word.find(m, lastindex + 1)
                handled = False
                for ex in exceptions:
                    if len(ex) == len(m):  # Not an environment exception
                        if ex == m:
                            handled = True
                            break
                        continue
                    elif len(ex) < len(m):  # Not an exception to this rule
                        continue
                    if lastindex > 0:
                        if len(word) > 1 + len(m) + lastindex:
                            cut = word[lastindex-1:lastindex+len(m)+1]
                        else:
                            cut = word[lastindex-1:len(word)]
                    else:
                        if len(word) > 2 + len(m):
                            cut = word[0:len(m)+2]
                        else:
                            cut = word
                    if ex in cut:
                        handled = True
                        break
                if not handled:
                    if showrejected:
                            print(word[1:-1] + " rejected due to rule " + ill)
                    return True
    return False


def rewrite_word(word):
    for inp, outp in zip(rewritekeys, rewritevalues):
        if inp in word:
            if show_rewrite_trigger:
                print("Replacing " + inp + " in " + word + " with " + outp)
            word = word.replace(inp, outp)
    return word


# Actually generate words
for n in range(0, numwords):
    word = ""
    while check_illegal("#" + word + "%"):
        word = ""
        size = random.randint(minsyllables, maxsyllables)
        for s in range(0, size + 1):
            word = word + generatesyllable(s, size - 1)
    if show_pre_rewrite:
        print("Pre-Rewrite: " + word)
    # Note: # and % must be added to the word in order to allow the user to
    # specify rewrite rules including the beginning and end of the word.
    # The final two .replace() statements are the only safe way to remove
    # these characters from the output, since the rewrite rule results in
    # # and % being removed from the string. Thus, taking word[1:-1] doesn't
    # work here, even if it's cleaner.
    print(rewrite_word("#" + word + "%").replace('#', '').replace('%', ''))
    if filter_duplicates: already_generated.append(word)
