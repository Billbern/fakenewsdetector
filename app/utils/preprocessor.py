import re
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

def preprocess(df, text_vectorizer):
    """
    Preprocess user input in the same way we preprocessed the training data.

    1. Remove non-alphabetic characters, convert to lowercase
    2. Tokenize (word_tokenizer from nltk)
    3. Lemmatize (WordNetLemmatizer)
    4. Vectorize (CountVectorizer)

    Use the same CountVectorizers from training in order to extract
    the same features and have the same output dimensions.
    """
    lemmatizer = WordNetLemmatizer()

    text_processed = []
    for text in df.text:
        # remove punctuation and lowercase
        text = re.sub(r'[^a-zA-Z]', ' ', text)
        text = text.lower()

        # tokenize and lemmatize tokens
        tokens = word_tokenize(text)
        tokens = [lemmatizer.lemmatize(x) for x in tokens]
        text_processed.append(' '.join(tokens))

    # vectorize
    text_matrix = text_vectorizer.transform(text_processed).toarray()

    # return np matrix
    return text_matrix