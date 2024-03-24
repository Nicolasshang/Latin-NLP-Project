from cltk.stem.latin.j_v import JVReplacer
from cltk.stem.latin.declension import CollatinusDecliner
from cltk.lemmatize.latin.backoff import BackoffLatinLemmatizer
from cltk.prosody.latin.macronizer import Macronizer
from cltk.tokenize.line import LineTokenizer
from cltk.tokenize.latin.sentence import SentenceTokenizer
from cltk.corpus.utils.formatter import remove_non_latin
from cltk.tokenize.word import WordTokenizer
import re

# pl.txt is usually the test data
def read(name):
  with open(f"data/{name}", "r") as f:
    return f.read()

def write(name, text):
  with open(f"data/{name}", "w", encoding = "utf-8") as f:
    f.write(text)

# Replaces the j's with i's and v's with u's (and vice versa as well)
def replace_jv(text):
  replacer = JVReplacer()
  text = replacer.replace(text)
  return text

# Deletes everthing in square brackets or parenthesis, and removes excessive whitespace
def clean(text, lower=False):
  for i in range(2):
    text = re.sub(r"([\(\[].*?[\)\]])|( +[\.,:;!])", "", text)
  cleaned_data = re.sub(r" {2,}", " ", text)
  
  if lower:
    lower_cleaned_data = cleaned_data.lower()
    return (cleaned_data, lower_cleaned_data)
  
  return cleaned_data

# Find all wordforms when given a lemma (usually in the nom. sing.)
def decline(words):
  decliner = CollatinusDecliner()
  dec_words = {}

  try:
    for word in words:
      dec_word = decliner.decline(word)
      dec_words[word] = dec_word
  except:
    # Skip any word that gives a lemma error or a KeyError
    Exception

  return dec_words

# Find the lemma using CLTK's backoff lemmatizer
def find_lemma(tokens):
  lemmatizer = BackoffLatinLemmatizer()
  tokens = lemmatizer.lemmatize(tokens)
  return tokens

# Add Macrons
def macronize(text):
  macronizer = Macronizer("tag_ngram_123_backoff")
  text = macronizer.macronize_text(text)
  return text

# Tokenize by line
def line_tokenize(text):
  tokenizer = LineTokenizer("latin")
  text = tokenizer.tokenize(text)
  return text

# Tokenize by sentence
def sentence_tokenize(text, punctuation=True):
  sentence_tokenizer = SentenceTokenizer()
  sentences = sentence_tokenizer.tokenize(text)
  new_sentences = []

  if punctuation:
    for sent in sentences:
      new_sentences.append(remove_non_latin(sent).lower())
    return new_sentences
  
  return sentences

# Tokenize by word
def word_tokenize(text):
  word_tokenizer = WordTokenizer("latin")
  words = word_tokenizer.tokenize(text)
  return words

if __name__ == "__main__":
  text = read("data.txt")
  text = replace_jv(text)
  text = clean(text)

  # Accessing the first sentence and getting the lemma of each word
  sentence = sentence_tokenize(text, True)[0]
  words = find_lemma(word_tokenize(sentence))

  wordforms = []
  for word in words:
    wordforms.append(word[1])

  # Getting the lemma + lexeme of any word in the corpus
  print(decline(wordforms)["filius"])