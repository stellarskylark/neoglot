# Neoglot
A word generator for conlangs with a simple and readable language-definition
DSL.

# Why the name change?
Two reasons. First, PyConlangWordGen is a disgusting and awkward name. Neoglot
(a word I coined to mean "speaker of new languages") is way cooler. Also, it
symbolizes that this really not the same project as PyConlangWordGen, though it
is a continuation of its (admittedly minor and unimpressive) legacy. I was
fundamentally unsatisfied with the original PyConlangWordGen and its absolutely
monstrous parsing code. Furthermore, I thought that the conlang-definition DSL
could be improved quite a bit. I essentially stole the original syntax from Mark
Rosenfelder's word generator on zompist.com. However, I found his DSL clunky to
use and to parse (though this may have been due to my own lack of knowledge when
I originally wrote PyConlangWordGen).

Introducing Neoglot:
```
cat consonant: m, n, p, t, ', h, w, l, s, sh
cat vowel: a, e, i, o, u

syll main: [consonant] (vowel | n | l) [vowel] [n]
```
This code snippet is equivalent to the following code snippet of Rosenfelder's
DSL:

```
# Categories:
C=mnpt'hwls0
R=nl
V=aeiou

# Rewrite rules
0|sh

# Syllable types:
V
CV
CVV
CR
CRV
CRn
CRVn
```

Neoglot is superior here in several ways. First, the syllable definition is much
more concise. While the zompist.com DSL requires you to list every possible
syllable type, Neoglot generates them automatically from a defined structure.
Second, Neoglot supports category names longer than a single letter, enabling
the user to use more descriptive names. Third, Neoglot supports phonemes of
arbitrary length (digraphs, trigraphs, even duodecagraphs if that suits your
fancy), eliminating the need for rewrite rules.

# Neoglot To-Do List
- Interpreter
  - [x] Phoneme categories
  - Syllable definitions
    - [x] Mandatory vs optional elements
    - [x] Multiple options within an element
    - [ ] Embed other syllable types
  - Illegality rules
    - [ ] Define illegal patterns
    - [ ] Define exceptions to illegality rules
    - [ ] Check for illegal patterns within a syllable
    - [ ] Check for illegal patterns between syllable boundaries
  - Transformations
    - [ ] Define phonemic transformations for certain environments, ie English
          intervocalic flapping
    - [ ] Define exceptions to transformation rules
    - [ ] Check for and apply transformations within a syllable
    - [ ] Check for and apply transformations between syllable boundaries
- Generator
  - [ ] Generate a specified number of words
  - [ ] Allow user to specify a range for length of words in syllables
  - [ ] Optionally generate text in sentence-style environments
  - [ ] Optional probability dropoff for phonemes and syllable types; the ones
        defined first appear more commonly
  - [ ] Command-line interface
  - [ ] GUI interface
