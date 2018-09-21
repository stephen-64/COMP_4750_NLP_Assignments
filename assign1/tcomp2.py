'''
tcomp2.py

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
'''
This script process the files given as command line arguments and extracts
the word count within the file and them compares them outputting the value to the
terminal
usage: python tcomp2.py filename file1name file2name ...
'''
import sys
import io

'''
This class will hadle everything to do with the files 
storing them as word_files which contain all tools nedded to manage the files
'''
class file_handler():
    
    '''
    Sorts through the given command line inputs and stores them as word_files
    containing all the data required to work with them
    '''
    def __init__(self):
        self.flist = []
        if(len(sys.argv)<3):
            print 'usage: python tcomp2.py filename file1name file2name ...'
            exit(1)
        for arg in sys.argv[1:]:
            self.flist.append(word_files(arg))

    '''
    Closes the open files when done with them
    '''
    def close_files(self):
        for fi in self.flist:
            fi.close_file()

    '''
    Runs the defined Sim adding the sums together as expected by the program spec
    returning a float representing the similarity
    '''
    def Sim(self,x,y):
        nWx=self.flist[x].num_words
        nWy=self.flist[y].num_words
        SD = self.SD(self.flist[x].word_list,self.flist[y].word_list)
        return 1.0 - (SD/(nWx+nWy))

    '''
    Checks the given values and looks for the differnece in words
    within them returning a modified sum contianing the difference
    '''
    def SD(self,x,y):
        total_count = 0.0
        for xnum in x:
            if xnum not in y:
                total_count+=1.0
        for ynum in y:
            if ynum not in y:
                total_count+=1.0
        return total_count

    '''
    Runs the program properly formating the output as 
    per the given program spec
    '''
    def run_sim(self):
        totals = {}
        for num in range(1,len(self.flist)):
            print 'Sim("' + str(self.flist[0].name) + '","' + str(self.flist[num].name)+'") = '+str(round(self.Sim(0,num),3))
            totals[self.flist[num].name]=round(self.Sim(0,num),3)
        total=0.0
        name=''
        for x in totals:
            if totals[x]>total:
                total=totals[x]
                name=x
        print 'File "'+ name+'" is most similar to file "'+self.flist[0].name+'"'



'''
Holds the files given as command line arguments and looks for the 
words placing them in a set as specified
'''
class word_files():

    '''
    Initializes the class storing the file and it's name
    along with it's word count using get_word_list
    '''
    def __init__(self,fname):
        self.name = fname
        self.file = open(fname)
        self.contents = self.file.read()
        self.word_list=set()
        self.get_word_list()
        
    '''
    Closes the open file
    '''
    def close_file(self):
        self.file.close()

    '''
    Genertates the set of all words in the given 
    file and stores them to a class variabl
    '''
    def get_word_list(self):
        paragraph_list=self.contents.splitlines()
        word_holder=[]
        for st in paragraph_list:
            word_holder.append(st.split(' '))
        for cont in word_holder:
            for stri in cont:
                self.word_list.add(stri)
                if '' in self.word_list:
                    self.word_list.remove('')
                if ' ' in self.word_list:
                    self.word_list.remove(' ')

        self.num_words=float(len(self.word_list))




def main():
    fh = file_handler()
    fh.run_sim()
    fh.close_files()

if(__name__=='__main__'):
    main()

    