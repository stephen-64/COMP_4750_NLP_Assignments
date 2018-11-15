'''
CKYdet.py
Copyright (c) 2018, Stephen Pollett
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.
* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
import sys
import io


class gNode(object):
    '''
    This class serves as a node in the CKY Table. This holds the Grammar rule 
    at this point and the location of the next rule to return to the lowest
    level.
    '''
    __slots__ = 'key','value','location'

    def __init__(self,key,value,location):
        # The left hand side of the grammar rule
        self.key = key
        # The right hand side of the grammar rule
        self.value = value
        # The location of the next simpler rule
        self.location = location

def get_grammar(filename):
    '''
    Provides the CFG as a simple dictionay of arrays
    '''
    grammar = {}
    fil = open(filename)
    lines = fil.read().strip().split('\n')
    for line in lines:
        sline = line.split('->')
        if grammar.has_key(sline[0].strip()):
            grammar[sline[0].strip()].append(sline[1].strip())
        else:
            grammar[sline[0].strip()]=[sline[1].strip()]
    return grammar



def parse(sentence,grammar):
    '''
    Parses the sentece using the given grammar and returns the 
    parse table
    '''
    #Splits the given sentence into an array based on spaces
    intern_sent = sentence.split(' ')
    w = len(intern_sent)
    #Creates an n by n array based on the size of the sentence
    P = [[dict() for x in range(w+1)] for y in range(w+1)]
    #Loads the table with empty arrays
    for j in range(1,len(intern_sent)+1):
        for i in range(j-1,-1,-1):
            for k in grammar:
                P[i][j][k] = []
    #Applies all basic rules that go to a terminal within the grammar
    for j in range(1,len(intern_sent)+1):
        for k in grammar:
            for v in grammar[k]:
                if intern_sent[j-1] in v:
                    P[j-1][j][k].append(gNode(k,v,j)) 
        #Applies all nonterminal to nonterminal rules within the grammar
        change = True
        while change:
            change = False
            for k in grammar:
                if len(P[j-1][j][k])>0:
                    for k1 in grammar:
                        val = grammar[k1]
                        for s in val:
                            if (k in s) and (check_list(k1,k,j, P[j-1][j][k1])):
                                P[j-1][j][k1].append(gNode(k1,k,j))
                                change = True
    #Fills in  the remaing portions of the table by running through it on the diaognal
    for j in range(2,len(intern_sent)+1):
        for i in range(j-2,-1,-1):

            for w in range(i+1,j-1):
                for k in grammar:
                    for val in grammar[k]:
                        rules = val.split(' ')
                        if len(rules)==2:
                            A = rules[0]
                            B = rules[1]
                            l1 = len(P[i][w][A])
                            l2 = len(P[w][j-1][B])
                            if (l1>0) and (l2>0):
                                P[i][j-1][k].append(gNode(k,A+' '+B,w))
            change = True
            while change:
                change = False
                for k in grammar:
                    if (len(P[i][j-1][k])>0):
                        for k1 in grammar:
                            val = grammar[k1]
                            for s in val:
                                if (k in s) and (check_list(k1,k,j, P[i][j-1][k1])):
                                     P[i][j-1][k1].append(gNode(k1,k,j))
                                     change = True
    #Returns the parse table
    return P


def check_list(k1,k,j,lis):
    '''
    A simple function which checks lists of gnodes to see if the contents match
    the given values 
    '''
    for node in lis:
        if (node.key == k1) and (node.value == k) and (node.location == j):
            return False
    return True


def print_tree(pharse,parsetree):
    '''
    Function developed to print the parse
    tree based on the expected output given in 
    the program specification
    '''
    parseholder = []
    ruleholder = []
    ruleholder2 = []
    counter = len(pharse.split(' '))
    loopcounter = 0
    for x in range(0,counter):
        if x < counter-1:
            if len(parsetree[x][counter-1]['S'])>0:
                ruleholder2.append(parsetree[x][counter-1]['S'][0].value)
                string = ''
                valstring = ''
                next_loc = counter-1
                next_rule = 'S'
                while (not ('"' in string)) and loopcounter<100:
                    if next_loc >= counter:
                        next_loc -=1
                    string = parsetree[x][next_loc][next_rule][0].value
                    valstring = parsetree[x][next_loc][next_rule][0].key
                    old_next_rule = next_rule
                    next_rule = parsetree[x][next_loc][next_rule][0].value.split(" ")[0]
                    next_loc = parsetree[x][next_loc][old_next_rule][0].location
                    loopcounter+=1
                loopcounter=0
                parseholder.append(string)
                ruleholder.append(valstring)
        else:
            if len(parsetree[x][counter]['S'])>0:
                ruleholder2.append(parsetree[x][counter]['S'][0].value)
                string = ''
                valstring = ''
                next_loc = counter
                next_rule = 'S'
                while (not ('"' in string)) and loopcounter<100:
                    string = parsetree[x][next_loc][next_rule][0].value
                    valstring = parsetree[x][next_loc][next_rule][0].key
                    old_next_rule = next_rule
                    next_rule = parsetree[x][next_loc][next_rule][0].value.split(" ")[0]
                    next_loc = parsetree[x][next_loc][old_next_rule][0].location
                    loopcounter+=1
                loopcounter=0
                parseholder.append(string)
                ruleholder.append(valstring)
    pharsecheck = pharse.split(" ")
    counter = 0
    try:
        for x in pharsecheck:
            if ('"'+x+'"') != parseholder[counter]:
                print " No Valid Parse"
                return
            counter +=1
    except:
        print " No Valid Parse"
        return
    for y in ruleholder2:
        if ruleholder2.count(y) > 2:
            print " No Valid Parse"
            return
    printstring = '[S '
    counter = 0
    last_string = ''
    for x in parseholder:
        if (counter < len(ruleholder2)):
            if len(ruleholder2[counter].split(' '))>1:
                if (not (last_string == ruleholder2[counter].split(' ')[0])) and (not (last_string == ruleholder[counter])) and (not( ruleholder2[counter].split(' ')[0] == ruleholder[counter])):
                    printstring+=ruleholder2[counter].split(' ')[0] +' [ '
                    last_string = ruleholder2[counter].split(' ')[0]
            else:
                if (not (last_string == ruleholder2[counter] )) and (not (last_string == ruleholder[counter])) and (not(ruleholder2[counter] == ruleholder[counter])):
                    printstring+=ruleholder2[counter] +' [ '
                    last_string = ruleholder2[counter]
        printstring+=ruleholder[counter]+' [ '
        counter+=1
        printstring +=x+' ] '
    printstring+=' ] '
    print 'Parse #1 ' + printstring
    return

    
    

                



def main():
    '''
    The function that gets callled to start the script
    '''
    if len(sys.argv)<3:
        print 'usage: python CKYdet.py *.ecfg *.utt'
        exit(1)
    grammar = get_grammar(sys.argv[1])
    word_counter = 1
    for pharse in open(sys.argv[2]).read().strip().split('\n'):
        print 'Uterance #' + str(word_counter)
        check = parse(pharse,grammar)
        print_tree(pharse,check)
        print '\n'
        word_counter +=1
    exit(0)


if __name__ == '__main__':
    main()