# Imports
import matplotlib.pyplot as plt
import nltk
import requests
from bs4 import BeautifulSoup
from nltk import word_tokenize
from wordcloud import WordCloud


# FUNCTION: Turns all elements in a list into a single string
def list_to_string(lts):
    empty_string = ' '
    return empty_string.join(lts)


# Asks the user for a website url
url = input('Enter a website with an HTML version of the book from https://www.gutenberg.org/: ')

# Checks if the website is valid (comes from BBC reviews website), if it's not valid, it asks for the website again
wb = 'https://www.gutenberg.org/cache/epub'
while wb not in url:
    url = input('Invalid input! Please enter a website starting from https://www.gutenberg.org/cache/epub: ')
else:
    pass

# Gets the entire content of the website specified by the user and parses it
website = requests.get(url)
soup = BeautifulSoup(website.content, 'html.parser')

# Pulls review sections from the webpage and adds them to an empty list
book_text = []
for book in soup.select('p'):
    book_text.append(book.text)

# FUNCTION: Turns all elements in a list into a single string
book_as_string = list_to_string(book_text)

# Separates the string and turns it into a list
tokens = word_tokenize(book_as_string)

# Matches words with parts of speech, turns the list into a nested list e.g. [('cat', 'NOUN'), ('the', 'DET')] etc.
book_with_tags = nltk.pos_tag(tokens, tagset='universal')

# Pulls only the adjectives without 'ADJ' tags from the nested list and adds them to an empty list
# Gets rid of non alpha characters and words shorter than 2 letters that the tokenizer produces
adjectives_list = []
for i in book_with_tags:
    if 'ADJ' in i[1] and i[0].isalpha() and len(i[0]) > 2:
        adjectives_list.append(i[0])

# FUNCTION: Turns all elements in a list into a single string and makes them all lower case
adjectives_list_as_string = list_to_string(adjectives_list).lower()

# Generates a word cloud from the counted instances made out of 250 most popular words in the set
wordcloud = WordCloud(width=500, height=500,
                      prefer_horizontal=0.5,
                      min_font_size=7,
                      max_words=250).generate(adjectives_list_as_string)

# Creates a figure to contain the word cloud and puts it there
plt.figure(figsize=(6, 6))
plt.imshow(wordcloud)

# Turns off axis lines and labels
plt.axis('off')

# Adjusts the padding around the plot so that it takes up all the space in the figure
plt.tight_layout(pad=0)

plt.show()
