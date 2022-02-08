import markovify
import pronouncing
import random
import re
from collections import defaultdict
import os.path

def print_list(the_list):
    for a in the_list:
        if a == None or a == "None":
            continue
        else:
            print(a)
    return

def generate_poetry_corpus(number, state_size, char_min=0, char_max=140):
    with open("CorpusPoetry.txt", encoding="utf-8") as f:
        text = f.read()
 
    text_model = markovify.NewlineText(text, state_size=state_size)
    lines = []
    for a in range(number):
        text = text_model.make_short_sentence(char_max, char_min)
        if text == "None" or text == None or text == "None ":
            continue
        lines.append(text)
    return lines
        

def generate_rhyme_corpus(corpus, min_char, max_char):
    text = corpus.split('\n')
    by_rhyming_part = defaultdict(lambda: defaultdict(list))
    for a in text:
        if not(min_char < len(a) < max_char):
            continue
        match = re.search(r'(\b\w+\b)\W*$', a)
        if match:
            last_word = match.group()
            pronounciations = pronouncing.phones_for_word(last_word)
            if len(pronounciations) > 0:
                for i in range(len(pronounciations)):
                    rhyming_part = pronouncing.rhyming_part(pronounciations[i])
                    by_rhyming_part[rhyming_part][last_word.lower()].append(a)
        
    return(by_rhyming_part)
        
def convertTuple(tup):
    st = ''.join(tup)
    return st

def do_it(corpus, i, state_size):
    string = convertTuple(("aipoetry/Corpuses/",str(state_size),"/CorpusRhyme_",str(i),".txt"))
    f = open(string, "a", encoding="utf-8")
    if isinstance(corpus, str):
        f.write(corpus)
    else:
        f.write('\n'.join(corpus))
        f.write('\n')
    f.close()
    return

def push_corpus(corpus, state_size):
    i = 1
    while True:
        string = convertTuple(("aipoetry/Corpuses/",str(state_size),"/CorpusRhyme_",str(i),".txt"))
        if os.path.isfile(string):
            i += 1
        else:
            do_it(corpus, i, state_size)
            return
                          
                          
def get_random_corpus(state_size):
    string = convertTuple(("aipoetry/Corpuses/",str(state_size),"/"))
    file = random.choice(os.listdir(string))
    extra = string + file
    with open(extra, encoding="utf-8") as f:
        text = f.read()
    return text
        
def generate_rhyme_abab_poetry(no_lines_total, state_size, char_min, char_max):
    lines = []
    dictionary_rhyming = generate_rhyme_corpus(get_random_corpus(state_size), char_min, char_max)
    rhyme_groups = [group for group in dictionary_rhyming.values() if len(group) >= 2]
    group = random.choice(rhyme_groups)
    group_two = random.choice(rhyme_groups)
    while group == group_two:
            group_two = random.choice(rhyme_groups)
    while len(lines) < no_lines_total:
        words = random.sample(list(group.keys()), 2)
        words_two = random.sample(list(group_two.keys()), 2)
        a = random.choice(group[words[0]])
        b = random.choice(group_two[words_two[0]])
        lines.append(a)
        lines.append(b)
    return lines

def generate_rhyme_aabb_poetry(no_lines_total, state_size, char_min, char_max):
    lines = []
    dictionary_rhyming = generate_rhyme_corpus(get_random_corpus(state_size), char_min, char_max)
    rhyme_groups = [group for group in dictionary_rhyming.values() if len(group) >= 2]
    for i in range(int(no_lines_total/2)): # Make this while to later implement minimum/maximum characters
        group = random.choice(rhyme_groups)
        words = random.sample(list(group.keys()), 2)
        lines.append(random.choice(group[words[0]]))
        lines.append(random.choice(group[words[1]]))
    return lines

def generate_rhyme_a_poetry(no_lines_total, state_size, char_min, char_max):
    lines = []
    dictionary_rhyming = generate_rhyme_corpus(get_random_corpus(state_size), char_min, char_max)
    rhyme_groups = [group for group in dictionary_rhyming.values() if len(group) >= 4]
    group = random.choice(rhyme_groups)
    while len(lines) < no_lines_total:
        words = random.sample(list(group.keys()), 2)
        lines.append(random.choice(group[words[0]]))
    return lines

def generate_rhyme_aaa_poetry(no_lines_total, state_size, char_min, char_max):
    lines = []
    dictionary_rhyming = generate_rhyme_corpus(get_random_corpus(state_size), char_min, char_max)
    rhyme_groups = [group for group in dictionary_rhyming.values() if len(group) >= 3]
    for i in range(int(no_lines_total/3)): # Make this while to later implement minimum/maximum characters
        group = random.choice(rhyme_groups)
        words = random.sample(list(group.keys()), 2)
        lines.append(random.choice(group[words[0]]))
        lines.append(random.choice(group[words[1]]))
        lines.append(random.choice(group[words[2]]))
    return lines
