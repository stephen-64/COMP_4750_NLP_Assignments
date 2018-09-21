'''
tcomp1.py

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
the n-grams stored within them using the given value n as the type of gram
ex: n=2 will look for 2-grams
usage: python tcomp1.py filename n file1name file2name ...
'''
import sys
import io

'''
An instance of this class is created for every file
passed as a cmd line argument to the program. 
This class will hold the file,it's name and create the dictionary containing it's
n-grams
'''
class nfile(): 

    '''
    Initilizases the class and calls get_grams() to calculate the n-grams 
    '''
    def __init__(self,fname,ng):
        self.ngrams={}
        self.ngrams_list=[]
        self.total_grams=0.0
        self.name = fname
        self.f = open(fname)
        self.ngrm = ng
        self.contents = self.f.read()
        self.get_grams()

    '''
    Calculates the n-grams contained within this file and stores them in a list
    '''
    def get_grams(self):
        counter = 0
        for char in self.contents:
            ngram = char
            seccount = 1
            while(char!='\n' and char !=' ' and (seccount<self.ngrm) and ((seccount+counter)<len(self.contents)) and (self.contents[seccount+counter] != " ") and (self.contents[seccount+counter] != "\n")): 
                ngram+=self.contents[seccount+counter]
                seccount+=1
            if((len(ngram))==self.ngrm):
                self.ngrams_list.append(ngram)
            counter+=1
        self.get_grams_dict()
    
    '''
    Converts the list of n-grams into the dictionary required by the assignment 
    which will be used in the final processing
    '''
    def get_grams_dict(self):
        for st in self.ngrams_list:
            if(not self.ngrams.has_key(st)):
                self.ngrams[st] = 1
                self.total_grams+=1
            else:
                self.ngrams[st]+=1
                self.total_grams+=1
        for x in self.ngrams:
            self.ngrams[x]/=self.total_grams
            
            

'''
This call as it's names implies proccesses and creates the nfiles required to 
perform the processing and find the value for Sim
'''
class file_processor():

    '''
    Parses through the gvien cmd line input and will create the required nfiles and 
    variables to process the files
    '''
    def __init__(self,args):
        self.flist =[]
        count = 1
        if(len(args) < 4):
            print 'usage: python tcomp1.py filename n file1name file2name ...'
            exit(1)
        self.n = int(args[2])
        for x in args[1:]:
            if(count == 2):
                self.n=int(x)
                count+=1
            else:
                self.flist.append(nfile(x,self.n))
                count+=1
        del count

    '''
    Implements the Diff function described in the assignments
    program spec using a dictionary for n-gram calculations
    '''
    def Diff(self,x,y):
        counter = 0.0
        for val in x.ngrams:
            if(y.ngrams.has_key(val)):
                counter += abs(x.ngrams[val]-y.ngrams[val])
            else:
                counter += x.ngrams[val]
        for val in y.ngrams:
            if(not x.ngrams.has_key(val)):
                counter += y.ngrams[val]
        return counter

    '''
    Performs the final Sim calculations and 
    returns the vaules as a float
    '''
    def Sim(self,x,y):
        return 1.0-(self.Diff(self.flist[x],self.flist[y])/2.0)

    '''
    The main running point of the program which processes the files and 
    produces the formatted data output
    '''
    def run_sim(self):
        totals={}
        for x in range(1,len(self.flist)):
            print 'Sim("' + str(self.flist[0].name) + '","' + str(self.flist[x].name)+'") = '+str(round(self.Sim(0,x),3))
            totals[self.flist[x].name]=round(self.Sim(0,x),3)
        total=0.0
        name=''
        for x in totals:
            if totals[x]>total:
                total=totals[x]
                name=x
        print 'File "'+ name+'" is most similar to file "'+self.flist[0].name+'"'

    '''
    Closes all open files
    '''
    def done_files(self):
        for file in self.flist:
            file.f.close()

            

def main():
    fp = file_processor(sys.argv)
    fp.run_sim()
    fp.done_files()


if(__name__=='__main__'):
    main()