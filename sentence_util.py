def create_sentence(word_list):
    num_words = len(word_list)

    if num_words < 2:
        return " ".join(word_list)

    subject = identify_subject(word_list)
    verb = word_list[-1]
    objects = " ".join(word for word in word_list if word != subject and word != verb)
    plural_verb = 'are' if subject.endswith('s') else 'is'

    sentence = f"The {subject} {plural_verb} {verb} {objects}"
    return sentence


def identify_subject(word_list):
    subject_keywords = ['person', 'he', 'she', 'him', 'her']
    for word in word_list:
        if word.lower() in subject_keywords:
            return word
    return word_list[0].lower()


def add_doing_if_needed(sentence):
    words = sentence.split()
    if 'is' in words:
        index_of_is = words.index('is')
        if index_of_is < len(words) - 1 and not words[index_of_is + 1].endswith('ing'):
            words.insert(index_of_is + 1, 'doing')
    return " ".join(words)


def remove_consecutive_words(sentence):
    words = sentence.split()
    cleaned_words = [words[0]]

    for i in range(1, len(words)):
        if words[i - 1] != words[i]:
            cleaned_words.append(words[i])

    return " ".join(cleaned_words)