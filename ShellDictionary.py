from bs4 import BeautifulSoup
import requests
import sys
import shlex
import subprocess

if len(sys.argv) >= 2:
    word = sys.argv[1].lower()
else:
    word = 'nothing'

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
        gets the definition of the argument word from thefreedictionary.com
    '''
    s = BeautifulSoup( requests.get( 'http://www.thefreedictionary.com/' + word).text, 'lxml')
    div_id_def = s.find('div', attrs={'id':"Definition"})
    
    definition = ''
    try:
        all_defs = div_id_def.find_all('div', attrs={'class':'ds-list'})
        for item in all_defs:
            definition += item.text + '\n'
    except:
        definition = 'Are you sure that\'s an English word? HINT: check spelling.'

    return definition


def get_pronunciation(word):
    '''
        gets the pronounciation of word in mp3 format from link in cambridge
    '''
    resource = 'http://dictionary.cambridge.org/dictionary/english/'
    r = requests.get(resource + word)
    s = BeautifulSoup(r.text, 'lxml')
    mp3_link_area = s.find(lambda tag: tag.has_attr('data-src-mp3'))
    
    try:
        mp3_link = mp3_link_area.get('data-src-mp3')
        with open('temp.mp3', 'wb') as f:
            f.write(requests.get(mp3_link).content)
        command = subprocess.call(shlex.split('afplay temp.mp3'))
        command = subprocess.call(shlex.split('rm -f temp.mp3'))
        status = ''
    except:
        status = 'Sorry! Pronunciation not found!'
    
    return status

def doit(fn, word):
    '''
        does nothing except returning function
    '''
    return fn(word)

if __name__ == '__main__':
    definition = doit(get_free_dictionary_definition, word)
    times_ = 10; print '==' * times_ + ' Definition : ' + word + ' '  + '==' * times_
    print definition
    
    status = doit(get_pronunciation, word)
    print status
