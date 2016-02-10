from bs4 import BeautifulSoup
import requests
import sys
import shlex
import subprocess

word = sys.argv[1]

'''
    Features to add:
    1. Origin of the word
    2. synonyms
    3. make a cache - keep words already seen
    4. Make output attractive
'''

def get_definition(word):
    '''
        gets the definition of the argument word from the merriam-webster
        exception not handled
    '''
    s = BeautifulSoup(requests.get('http://www.merriam-webster.com/dictionary/'+word).text, 'lxml')
    l=s.find('ul', attrs={'class':"definition-list no-count"}).find_all('li')
    
    for item in l:
        print item.text

def get_free_dictionary_definition(word):
    '''
        gets the definition of the argument word from the free dictionary
        exception not handled
    '''
    s = BeautifulSoup( requests.get( 'http://www.thefreedictionary.com/' + word).text, 'lxml')
    l=s.find('div', attrs={'id':"Definition"}).find_all('div',
            attrs={'class':'ds-list'})
    
    for item in l:
        print item.text


def get_pronounciation(word):
    '''
        gets the pronounciation of word in mp3 format from link in cambridge
        exceptions not handled
    '''
    resource = 'http://dictionary.cambridge.org/dictionary/english/'
    r = requests.get(resource + word)
    s = BeautifulSoup(r.text, 'lxml')
    mp3_link = s.find(lambda tag:
        tag.has_attr('data-src-mp3')).get('data-src-mp3')
    

    with open('temp.mp3', 'wb') as f:
        f.write(requests.get(mp3_link).content)

    command = subprocess.call(shlex.split('afplay temp.mp3'))
    command = subprocess.call(shlex.split('rm -f temp.mp3'))


def check(fn, word):
    fn(word)
    return True

times_ = 10
print '==' * times_ + ' Definition : ' + word + ' '  + '==' * times_
x = check(get_free_dictionary_definition, word)
y = check(get_pronounciation, word)

