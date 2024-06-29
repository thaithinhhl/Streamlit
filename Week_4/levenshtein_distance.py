import streamlit as st

# Create dictionary


def load_vocab(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        words = sorted(set([line.strip().lower() for line in lines]))
        return words


# Load vocabulary
vocabs = load_vocab(file_path=r'E:\source\source\data\vocab.txt')


def levenshtein_distance(token1, token2):
    len1 = len(token1)
    len2 = len(token2)

    # Initialize distances matrix
    distances = [[0] * (len2 + 1) for _ in range(len1 + 1)]

    # Initialize first row and first column
    for t1 in range(len1 + 1):
        distances[t1][0] = t1
    for t2 in range(len2 + 1):
        distances[0][t2] = t2

    # Fill the rest of the matrix
    for t1 in range(1, len1 + 1):
        for t2 in range(1, len2 + 1):
            if token1[t1 - 1] == token2[t2 - 1]:
                substitution_cost = 0
            else:
                substitution_cost = 1

            # Calculate minimum distance
            distances[t1][t2] = min(distances[t1 - 1][t2] + 1,  # Deletion
                                    distances[t1][t2 - 1] + 1,  # Insertion
                                    distances[t1 - 1][t2 - 1] + substitution_cost)  # Substitution

    return distances[len1][len2]

# Main function


def main():
    st.title("Word Correction using Levenshtein Distance")
    word = st.text_input('Word:')

    if st.button("Compute"):
        if not word:
            st.warning("Please enter a word.")
            return

        # Compute Levenshtein distance
        leven_distances = {}
        for vocab in vocabs:
            leven_distances[vocab] = levenshtein_distance(word, vocab)

        # Sort by distance
        sorted_distances = dict(
            sorted(leven_distances.items(), key=lambda item: item[1]))

        # Display results
        if sorted_distances:
            correct_word = list(sorted_distances.keys())[0]
            st.write('Correct word:', correct_word)

            col1, col2 = st.columns(2)
            col1.write('Vocabulary:')
            col1.write(vocabs)

            col2.write('Distances:')
            col2.write(sorted_distances)
        else:
            st.warning("No vocabulary loaded.")


if __name__ == "__main__":
    main()
