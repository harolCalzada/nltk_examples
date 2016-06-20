from bs4 import BeautifulSoup
import urllib2


def getPostText(url, token):
    '''
            Get  data of web page and remove html tags
    '''
    text = ''

    try:
        page = urllib2.urlopen(url).read().decode('utf8')
    except:
        return None

    soup = BeautifulSoup(page)

    if soup is None:
        return (None, None)

    if soup.find_all(token) is not None:
        text = ''.join(map(lambda p: p.text, soup.find_all(token)))
        soup2 = BeautifulSoup(text)
        if soup2.find_all('p') is not None:
            text = ''.join(map(lambda p: p.text, soup2.find_all('p')))

    return text, soup.title.text


class FrequencySummarizer:
    '''
        Compute frequencies of words in article
    '''
    def __init__(self, min_cut=0.1, max_cut=0.9):
        self._min_cut = min_cut
        self._max_cut = max_cut
        self._stopwords = set(stopwords.words('english') +
                                            list(punctuation) + [u" 's", ' " '])

    def _comute_frequencies(self, word_sent, customStopWords=None):
        freq = defaultdict(int)
        if customStopWords is None:
            stopwords = set(self._stopwords)
        else:
            stopwords = set(customStopWords).union(self._stopwords)
        for sentence in word_sent:
            for word in sentence:
                if word not in stopwords:
                    freq[word] += 1
        m = float(max(freq.values()))
        for word in freq.keys():
            freq[word] = freq[word]/m
            if freq[word] >= self._max_cut or freq[word <= self._min_cut]:
                del freq[word]
        return freq

def sumarize(self, article, n):
    text = article[0]
    title = article[1]

    sentences = sent_tokenize(text)
    word_sent = [word_tokenize(s.lower() for s in sentences)]
    self._freq = self._compute_frequencies(word_sent)
    ranking = defaultdict(int)
    for i, sentence in enumerate(word_sent):
        for word in sentence:
            if word in self._freq:
                ranking[i] += self._freq[word]
    sentences_index = nlargest(n, ranking, key=ranking.get)
    return [sents[j] for j in sentences_index]
