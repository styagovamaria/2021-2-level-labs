"""
Lab 3
Language classification using n-grams
"""
#print(list(map(int, input('?').split(' '))))
import re

class LetterStorage:    
    
    def __init__(self):
        self.uid = 0
        #self.storage = {'errors':0}
        self.storage = {}
        self.errors = 0

    def e(self,txt):
        self.errors +=1
        print('ERROR #' ,self.errors,txt )
        return  self.errors
    
    def _put_letter(self, letter: str) -> int:
        if not type(letter)  is str:
            self.e('_put_letter')
            print(letter)
            return -1
        
        if letter not in self.storage:
            self.storage[letter] = self.uid
            self.uid+=1
            return 0

        return self.storage[letter]

        
    def get_id_by_letter(self, letter):
        if letter in self.storage:
            return self.storage[letter]
        else:
            return -1
        
    def get_letter_by_id(self, index):
        for key,val in  self.storage.items():
            if val==index:
                return key
            return -1
    
    def update(self,sentences):
        ss = sentences
        if type(ss) is not tuple:
            self.e('update')
            return -1

        uniques = {}
        for sent in ss:
            for word in sent:
                for letter in word:
                    self._put_letter(letter)

        return 0

def show(hint, rez):
    print()
    print(hint)
    for sent in rez:
        print()
        for word in sent:
            print('\t' , word)


def eq(test, rez, lvl):
    print()
    for i in range(0, max(len(test), len(rez))):
        #print('\t'*lvl*2 , test[i] if i<len(test) else 'XXXXX',rez[i] if i<len(rez) else 'XXXXX' ,)
        eqq = test[i] if i<len(test) else 'XXXXX' == rez[i] if i<len(rez) else 'XXXXX'
        if not eqq:
            print('\t'*lvl, i,'!' )
            eq(test[i] if i<len(test) else 'XXXXX',rez[i] if i<len(rez) else 'XXXXX' ,lvl+1 ) 
        
           

def tokenize_by_sentence(text: str) -> tuple:
    
    
    if type(text) is not str:
        return tuple()
    UnlautsReplacements = {
        'ö': 'oe', 
        'ü': 'ue', 
        'ä': 'ae',  
        'ß': 'ss',
        'Ö': 'Oe', 
        'Ü': 'Ue', 
        'Ä': 'Ae',  
        'ß': 'ss',
        'ẞ': 'Ss'

    }

    def normalize(a):
        
        a = a.strip()
        a =  re.sub(r'[^A-Za-z0-9\s]{1,}','',a)
        for x,y in UnlautsReplacements.items():
            a = a.replace(x,y)
        return a
    #-------------------
     
    #f = open('text.txt','r')
    #text =  ''.join(f.readlines())


    text = text.replace('\r\n',' ')
    text = text.replace('\n',' ')
    text = text.replace('\t',' ')
    #Break Sentences properly
    alltextstr = (text) #list(map(normalize, f.readlines()))
    print('alltextstr',alltextstr)
    sentences= re.split(r"[!.?]\W(?=[\wöüäßÜÖÄẞ])", alltextstr)

    sentences = re.split(r'[.!?]{1,3}[\s]{1,}(?=[\wßÜÖÄ^a-z^öüäß]{1})'  ,alltextstr)  #re.split(r"[!.?]\W(?=[\wöüäßÜÖÄẞ])", text)
    print('sentences',sentences)
    sentences = list(map(normalize,sentences ))
                             
    #Lexemizations
    Lexs = LetterStorage()
 
    i=0
    TkSentences = []
    for sent in sentences:
        
        print(i,')',sent+'')
        i+=1
        tkSent =  re.split(r'[\s]{1,}', sent)
        tkSent2 = []
        for word in tkSent:
            #print('\t<',word,'>',sep='', end='    =    ')
            if word=='':
                continue
            word = word.lower()
            clearword  = [symb for symb in word if symb.isalpha() and Lexs._put_letter(symb)]

            clearword.append('_')
            clearword.insert(0,'_')
            clearword = tuple(clearword)
            #print('\t<',clearword,'>',sep='')
            tkSent2.append(clearword)
            
        if len(tkSent2)==0:
            continue   
        TkSentences.append(tuple(tkSent2))

    '''
    #output
    i=0
    outstr = ''
    for sent in TkSentences:
        outstr+= str(i) + ')' + str(sent) +'\n'
        for word in sent:
            outstr+= '\t' + str(word)+ '\n'
        i+=1

    print(outstr)
    '''
    for key,value in Lexs.storage.items():
        print(key,'=',value)
    return tuple(TkSentences)


#print(rez)
letter_storage = LetterStorage()
sentences = (
            (('_', 't', 'e', 's', 't', '_'),),
        )
actual = letter_storage.update(sentences)
print(len(letter_storage.storage), 4)
  
letter_storage.storage = {'w': 1}
expected = 'w'
actual = letter_storage.get_letter_by_id(1)
print(expected, actual)
