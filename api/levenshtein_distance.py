def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def find_most_similar_words(input_word, n=5):
    file_path = '/Users/rizalilham/Documents/Projects/books_authors_management/books_authors_management/books_title.txt'
    with open(file_path, 'r') as file:
        words = file.read().splitlines()

    distance_list = [(word, levenshtein_distance(input_word, word)) for word in words]

    most_similar = sorted(distance_list, key=lambda x: x[1])[:n]

    return [word for word, _ in most_similar]
