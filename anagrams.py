import load_dictionary

word_list = load_dictionary.load('/Users/john/Projects/anagrams/words.txt')


# get the name
def get_name():
    name = input('Enter a SINGLE word or name below to find its anagrams(s):')
    print(f'\nInput name = {name}')
    name = name.lower()
    print(f'\nUsing name = {name}')
    return name

# sort name & find anagrams


def find_anagram(name):
    # sort name & find anagrams
    name_sorted = sorted(name)
    anagram_list = []
    for word in word_list:
        word = word.lower()
        if word != name:
            if sorted(word) == name_sorted:
                anagram_list.append(word)
    return anagram_list


def main():
    name = get_name()
    anagram_list = find_anagram(name)

    # print out list of anagrams
    print()
    if len(anagram_list) == 0:
        print('You need a larger dictionary or a new name!')
    else:
        print('Anagrams = ', *anagram_list, sep='\n')


if __name__ == '__main__':
    main()
