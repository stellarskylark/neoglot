# PyConlangWordGen
A word generator, written in Python, intended for conlangs. As the name implies.

#Usage Instructions
1. Install the latest version of Python 3 from http://python.org.
2. Download PyConlangWordGen.
3. Open CMD in the folder containing PyConlangWordGen.
4. Run "python pyconlangwordgen.py samplelanguage.txt 20"
5. PyConlangWordGen should print twenty words according to the constraints defined in samplelanguage.txt
6. Write a rules file for your conlang. Run PyConlangWordGen again, but replace "samplelanguage.txt" with your rules file.
7. Start building yourself a lexicon!

For details on writing rules files, see userguide.txt

#So why did you make this?
I'm a geek.

Okay, but seriously. I've done a bit of conlanging, and I've used Mark Rosenfelder's word generator at http://zompist.com/gen.html quite a bit. But as much as I like Mark Rosenfelder, his Language Construction Kit (responsible for most of my linguistics knowledge), and his brilliant SCA<sup>2</sup>, one thing about his word generator always bothered me: it doesn't let you specify illegality rules.

Let's say your conlang has (C)CV(C) syllable structure, and two illegality rules: no /nasal/+/fricative/, and no /stop/+/nasal/. In Mark Rosenfelder's generator, to ensure that these clusters are never generated, you have to define every syllable type that is allowed:

```
CV
CVC
SSV
SSVC
FFV
FFVC
NNV
NNVC
NSV
NSVC
SFV
SFVC
FNV
FNVC
```

If you're clever, you might can reduce the size of the list. But I was not clever, and kept having to make syllable lists this long. And even after all of this, *there's still no guarantee you won't get illegal clusters between syllable boundaries.* I got kinda sick of it, and so I wrote PyConlangWordGen, which lets you define illegality rules. The above example is reduced to:

```
-SYLLABLES
CV
CVC
CCV
CCVC
-ILLEGAL
NF
SN
```

That's it. You'll get words with (C)CV(C) syllable structure that never contain /nasal/+/fricative/ or /stop/+/nasal/. If you want, you can even define exceptions. Maybe /nasal/+/fricative/ is *mostly* illegal, but /n/ + /s/ is okay before /o/ or at the beginning of words.

```
-ILLEGALEXCEPTIONS
nso
#ns
```

I'm fairly pleased with this system. Maybe it's just because I'm the one who wrote the script, but doing it this way just makes more sense to me.
