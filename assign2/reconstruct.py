'''
reconstruct.py

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
import io
import sys

'''
A Simple Class representing a set of values on
an FST Path. 
'''
class UpperLower(object):
    __slots__=['upper','lower','path']
    def __init__(self,l,u,p):
        self.lower=l
        self.upper=u
        self.path=p

'''
A class that represents a FST Node 
containing all the paths out of the FST and which Node it is 
along with wether it is a Finishing Node or not.
'''
class FST_Node(object):
    __slots__=['is_final','number','paths']
    def __init__(self):
        self.is_final=''
        self.number=''
        self.paths=[]
        #self.next = None
        #self.library=''
'''
Holds all the nodes in the FST
'''
class node_holder(object):
    __slots__=['holder','states','transitions']
    def __init__(self):
        self.holder = []
        self.states=0
        self.transitions=0

'''
Reads in the contents of the given file and stores it as a node_holder
'''
def readFST(filename):
    retnode = node_holder()
    tempnode = FST_Node()
    f=open(filename)
    lines_in_file=f.read()
    lines_list=lines_in_file.strip().split('\n')
    transitions = 0
    counter = 0
    for line in lines_list:
        if counter == 0:
            pass
        elif (('F' in line) or ('N' in line)) and (line[0]=='1'):
            tempnode.is_final = line[2]
            tempnode.number = line[0]
        elif line[0]==' ':
            transitions+=1
            tempnode.paths.append(UpperLower(line[2],line[4],line[6]))
        elif ('F' in line) or ('N' in line):
            retnode.holder.append(tempnode)
            tempnode = FST_Node()
            tempnode.is_final = line[2]
            tempnode.number = line[0]
        counter+=1
    retnode.holder.append(tempnode)
    retnode.states = len(retnode.holder)
    retnode.transitions = transitions
    return retnode


'''
Combines the two given FST's and returns the combination
'''
def composeFST(F1,F2):
    retnode = node_holder()
    for node in F1.holder:
        for node1 in F2.holder:
            for ul in node.paths:
                for ul1 in node1.paths:
                    if ul.upper==ul1.lower:
                        retnode.transitions+=1
                        tempul = UpperLower(ul.lower,ul1.upper,(ul.path+ul1.path))
                        tempnum = node.number + node1.number
                        if node.is_final == 'F' and node1.is_final == 'F':
                            tempfinal = 'F'
                        else:
                            tempfinal ='N'
                        checker = False
                        counter = 0
                        for n in retnode.holder:
                            if n.number == tempnum:
                                checker = True
                                break
                            counter +=1
                        if checker:
                            retnode.holder[counter].paths.append(tempul)
                        else:
                            retnode.states+=1
                            temp = FST_Node()
                            temp.number = tempnum
                            temp.is_final = tempfinal
                            temp.paths.append(tempul)
                            retnode.holder.append(temp)
                    if ul.upper== '-' and ul1.lower!='-':
                        retnode.transitions+=1
                        tempul = UpperLower(ul.lower,'-',(ul.path+node1.number))
                        tempnum = node.number + node1.number
                        if node.is_final == 'F' and node1.is_final == 'F':
                            tempfinal = 'F'
                        else:
                            tempfinal ='N'
                        checker = False
                        counter = 0
                        for n in retnode.holder:
                            if n.number == tempnum:
                                checker = True
                                break
                            counter +=1
                        if checker:
                            retnode.holder[counter].paths.append(tempul)
                        else:
                            retnode.states+=1
                            temp = FST_Node()
                            temp.number = tempnum
                            temp.is_final = tempfinal
                            temp.paths.append(tempul)
                            retnode.holder.append(temp)
                    if ul.upper!= '-' and ul1.lower=='-':
                        retnode.transitions+=1
                        tempul = UpperLower(ul.lower,'-',(node.number+ul1.path))
                        tempnum = node.number + node1.number
                        if node.is_final == 'F' and node1.is_final == 'F':
                            tempfinal = 'F'
                        else:
                            tempfinal ='N'
                        checker = False
                        counter = 0
                        for n in retnode.holder:
                            if n.number == tempnum:
                                checker = True
                                break
                            counter +=1
                        if checker:
                            retnode.holder[counter].paths.append(tempul)
                        else:
                            retnode.states+=1
                            temp = FST_Node()
                            temp.number = tempnum
                            temp.is_final = tempfinal
                            temp.paths.append(tempul)
                            retnode.holder.append(temp)
                    
    return retnode
    
'''
Reconsturcts the Upper Portions of the given lower form. 
Parses through the lower word and creates the respective higher values 
'''
def reconstructUpper(L,F):
    stateholder=''
    returnholder=''
    for n in F.holder[0].number:
        stateholder+='1'
    for s in L:
        numhold = get_pos_in_array(stateholder,F)
        for q in F.holder[numhold].paths:
            if s==q.lower:
                returnholder += q.upper
                stateholder = q.path
        if returnholder=='':
            break
    return returnholder

def get_pos_in_array(state,F):
    num = 0
    for n in F.holder:
        if n.number == state:
            return num
        num +=1
    return num-1

'''
Reconsturcts the Lower Portions of the given upper form. 
Parses through the upper word and creates the respective lower values 
'''
def reconstructLower(U,F):
    stateholder=''
    returnholder=''
    for n in F.holder[0].number:
        stateholder+='1'
    for s in U:
        numhold = get_pos_in_array(stateholder,F)
        for q in F.holder[numhold].paths:
            if s==q.upper:
                returnholder += q.lower
                stateholder = q.path
    return returnholder

'''
Main body of the script runs when it is called
'''
if __name__ =="__main__":
    args=sys.argv
    if len(args)==1:
        print 'usage: python reconstruct.py surface/lexical wlf/wsf F1 F2 ... Fn'
        exit(1)
    if args[1]=='surface':
        if len(args)==4:
            ty = readFST(sys.argv[3])
        else:
            ty = ''
            holder =[]
            for x in range(len(args)):
                if x==3:
                    ty = readFST(args[x])
                elif x>3:
                    holder.append(readFST(args[x]))
            for z in holder:
                ty = composeFST(ty,z)
        f=open(args[2])
        lines = f.read().strip().split('\n')
        print 'Composed FST has ' +str(ty.states) + ' states and ' + str(ty.transitions) +' transitions'
        for l in lines:
            print 'Lexical Form: ' + l
            print 'Reconstructed surface forms: '
            print reconstructUpper(l,ty)
            print '------------------------'
    elif args[1]=='lexical':
        if len(args)==4:
            ty = readFST(sys.argv[3])
        else:
            ty = ''
            holder =[]
            for x in range(len(args)):
                if x==3:
                    ty = readFST(args[x])
                elif x>3:
                    holder.append(readFST(args[x]))
            for z in holder:
                ty = composeFST(ty,z)
        f=open(args[2])
        lines = f.read().strip().split('\n')
        print 'Composed FST has ' +str(ty.states) + ' states and ' + str(ty.transitions) +' transitions'
        for l in lines:
            print 'Surface Form: ' + l
            print 'Reconstructed Lexial forms: '
            print reconstructLower(l,ty)
            print '------------------------'
    #Test Code
    # elif args[1]=='t1':
    #     q=readFST('vcePlu.fst')
    #     z=readFST('addVowPlu.fst')
    #     print q.states
    #     print q.transitions
    #     print z.states
    #     print z.transitions
    #     print reconstructUpper('potPs',q)
    #     print reconstructLower('podz',q)
    else:
        print 'usage: python reconstruct.py surface/lexical wlf/wsf F1 F2 ... Fn'
        exit(1)