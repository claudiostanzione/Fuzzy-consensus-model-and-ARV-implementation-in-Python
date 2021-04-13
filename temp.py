# -*- coding: utf-8 -*-

import numpy as np
import os
from numpy import genfromtxt
import csv
from math import factorial
import sys

def checkmatrixreciproc(matrix):# control if the matrix is ok
    for i in range(matrix.shape[0]):
        matrix[i][i]=0.5 # if not, set diagonal with 0.5
        for j in range(matrix.shape[1]):
            if np.isnan(matrix[i][j])==True: #check if the value is nan, if yes
                matrix[i][j]=1-matrix[j][i]#set the reciprocal value
            if matrix[i][j]==0:#same control of the nan with the 0
                matrix[i][j]= 1-matrix[j][i]
    np.asarray(matrix) # transform the matrix in array
    return matrix
    

def preferencerelationalmatrix(start): #read the preference relational matrix
    i=0
    arr=np.array([])
    for name in os.listdir(start):
        i=i+1
        data2=np.array([])
        data2= genfromtxt(os.getcwd()+"\\"+start+"\\"+name, delimiter=",")#read the file in the cartel
        data2=checkmatrixreciproc(data2)
        arr= np.append(arr,data2)
        x=int((len(arr))/i)
    arrfinal= np.reshape(arr,(i,x))
    n=int(pow(len(arrfinal[0]),1/2))
    arrays=np.empty([i,n,n],dtype="float")
    for i in range(len(arrfinal)):
        arrays[i]=np.reshape(arrfinal[i],(n,n))
    arrays=np.asarray(arrays)
    return arrays

def consistencymatrix(matrix):
    dec=1
    while dec==1:
        for n in range(len(matrix)):
            for k in range(len(matrix[n])):
                for i in range(len(matrix[n][k])):
                    for x in range(len(matrix[n][k])):
                        if matrix[n][k][i] < min(matrix[n][x][i], matrix[n][k][x]):
                            dec=0
    if dec==1:
        print("CONSISTENCY OK \n")
        print("\n")
    else:
        print("CONSISTENCY NOT OK \n")
        ask= int(input("IF YOU PREFER CONTINUE DIGIT 1, ELSE DIGIT 0  \n"))#the user is able to exit if he wants to repair the comparison matrix
        print("\n")
        if ask==0: 
            sys.exit("GOOD REVISION")
                
        

        
def similaritymatrices(matrix,coeff):# calculate the similarity matrices
    x=0
    n=int(len(matrix[0][0]))
    arrays=np.empty([coeff,n,n],dtype="float")
    for i in range(len(matrix)):
        for j in range(i+1,len(matrix)):
            arrays[x]=1-abs(matrix[i]-matrix[j])
            x=x+1
    return arrays       

def consensusmatrix(matrix,coeff):#calculate the consensus matrix
    arrays=matrix[0]
    for i in range (1,len(matrix)):
        arrays=arrays+matrix[i]
    arrays=arrays/coeff
    return arrays  
    
def consensusmeasure(matrix): #calculate the consensus measure
    n=int(len(matrix[0]))
    colum=np.sum(matrix,axis=0)
    row=np.sum(matrix,axis=1) 
    tot=((colum+row)-2)
    tot=np.divide(tot, 2*(n-1))
    mean=np.mean(tot)
    return tot,mean #tot corresponds to ca values, mean is the final consensus value
      
def collectivepreferencematrix(matrix): #calculate the collective preference matrix 
    app=matrix[0]
    for i in range (1,len(matrix)):
        app=app+matrix[i]
    app=app/len(matrix)
    return app #app is the pc table
        
def collectivesimilaritymatrices(matrix,pc): # calculate the collective similarity matrices
    n=int(len(matrix[0][0]))
    c=int(len(matrix))
    arrays=np.empty([c,n,n],dtype="float")
    for i in range(len(matrix)):
        arrays[i]=(1-abs(matrix[i]-pc))
    return arrays #corresponds to the pp tables, one for each expert

def collectivesimilarmeasure(matrix): #calculate collective similarity measure and aggregated collective similarity measure
    n=int(len(matrix))
    c=int(len(matrix[0]))
    arrays=np.empty([n,c],dtype="float")
    for i in range(len(matrix)):
        colum=np.sum(matrix[i],axis=0)
        row=np.sum(matrix[i],axis=1)
        tot=((colum+row)-2)
        tot=np.divide(tot, 2*(c-1))
        arrays[i]=tot
    meanrow=np.mean(arrays,axis=1)
    return arrays,meanrow #meanrow is the aggregate collective similarity measure

def groupsadvice(weights,lambda1,lambda2):# divide the experts in three groups depending on lambdas
    groups=[]
    low=[]
    medium=[]
    high=[]
    for i in range(len(weights)):
        if weights[i]< lambda2:
            low.append(i)
        elif lambda2<=weights[i]<lambda1 :
            medium.append(i)
        else :
            high.append(i)
            
    groups.append(low)
    groups.append(medium)
    groups.append(high)
    return groups
        
def lowgroupadvice(consval,matrixes,groups,consmatrix,pc): #generate advices for the experts in the low group
    alpha1=consval
    n=len(consmatrix[0])
    p=np.empty([n,n])
    for i in range(n):
        for j in range(n):
            if consmatrix[i][j]<alpha1:
                p[i][j]=0
            else :
                p[i][j]=1
    emp=np.empty([n,n],dtype='<U10')
    for x in groups[0]:
        for i in range(len(p)):
            for j in range(len(p[i])):
                if p[i][j]==0:
                    if matrixes[x][i][j]<=pc[i][j]:
                        emp[i][j]="INCREASE"
                    else:
                        emp[i][j]="DECREASE"
                else:
                    emp[i][j]="NOT CHANGE"
        print("ADVICES FOR LOW GROUP \n")
        print("ADVICE FOR THE EXPERT ",x+1,"\n")
        print(emp, "\n")
                
def mediumgroupadvice(consval,matrixes,groups,consmatrix,pc,colmeas,ca): #advices for the medium group
    n=len(consmatrix[0])
    beta1=[]
    xch=[]
    alpha2=consval
    beta1=np.mean(colmeas,axis=0)
    p=np.zeros([n,n],dtype=int)
    for i in range(len(ca)):
        if ca[i]<alpha2:
            xch.append(i)
    for i in xch:
        p[i]=p[i]+1
    for i in range (n):
        for j in xch:
            if p[i][j]==1:
                p[i][j]=p[i][j]
            else:
                p[i][j]=p[i][j]+1
    for i in range(len(p)):
        for j in range(len(p[i])):
            if p[i][j]==1:
                if consmatrix[i][j]<alpha2:
                    p[i][j]=p[i][j]
                else:
                    p[i][j]=0
    emp=np.empty([n,n],dtype='<U10')
    for x in groups[1]:
        d=p.copy() 
        for k in xch:
            for j in range(len(d[k])):
                if d[k][j]==1:
                    if colmeas[x][k]<beta1[k]:
                        d[k][j]=1
                    else:
                        d[k][j]=0
                if d[j][k]==1:
                    if colmeas[x][k]<beta1[k]:
                        d[j][k]=1
                    else:
                        d[j][k]=0
            for i in range(len(d)):
                for a in range(len(d[i])):
                    if d[i][a]==1:
                        if matrixes[x][i][a]<=pc[i][a]:
                            emp[i][a]="INCREASE"
                        else:
                            emp[i][a]="DECREASE"
                    else:
                        emp[i][a]="NOT CHANGE"
        print("ADVICES FOR THE MEDIUM GROUP \n")
        print("ADVICE FOR THE EXPERT ",x+1,"\n")
        print(emp, "\n")
        

def highgroupadvice(consval,matrixes,groups,consmatrix,pc,colmeas,ca,pp) : #advices for the high group
    n=len(matrixes[0])
    beta2=np.zeros([n,n])
    for i in range(len(pp)):
        beta2=beta2+pp[i]
    beta2=beta2/len(pp)
    beta1=[]
    xch=[]
    alpha2=consval
    beta1=np.mean(colmeas,axis=0)
    p=np.zeros([n,n],dtype=int)
    for i in range(len(ca)):
        if ca[i]<alpha2:
            xch.append(i)
    for i in xch:
        p[i]=p[i]+1
    for i in range (n):
        for j in xch:
            if p[i][j]==1:
                p[i][j]=p[i][j]
            else:
                p[i][j]=p[i][j]+1
    for i in range(len(p)):
        for j in range(len(p[i])):
            if p[i][j]==1:
                if consmatrix[i][j]<alpha2:
                    p[i][j]=p[i][j]
                else:
                    p[i][j]=0
    emp=np.empty([n,n],dtype='<U10')
    for x in groups[2]:
        d=p.copy() 
        for k in xch:
            for j in range(len(d[k])):
                if d[k][j]==1:
                    if colmeas[x][k]<beta1[k] and pp[x][k][j]< beta2[k][j]:
                        d[k][j]=1
                    else:
                        d[k][j]=0
                if d[j][k]==1:
                    if colmeas[x][k]<beta1[k] and pp[x][j][k]< beta2[j][k]:
                        d[j][k]=1
                    else:
                        d[j][k]=0
            for i in range(len(d)):
                for a in range(len(d[i])):
                    if d[i][a]==1:
                        if matrixes[x][i][a]<=pc[i][a]:
                            emp[i][a]="INCREASE"
                        else:
                            emp[i][a]="DECREASE"
                    else:
                        emp[i][a]="NOT CHANGE"
        print("ADVICES FOR THE HIGH GROUP \n")
        print("ADVICE FOR THE EXPERT ",x+1,"\n")
        print(emp, "\n")

def readnames(name): # read the csv file for the tables with the names
    with open(name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for riga in csv_reader:
            print(riga)
    return riga    
    
       
    

name=input("PROVIDE FOLDER NAME WITH PREFERENCES MATRIX PLEASE: \n")
threshold= float(input("PROVIDE CONSENSUS THRESHOLD VALUES THAT PREFER:  \n"))
lambda1= float(input("PROVIDE LAMBDA1 VALUE PLEASE: \n"))
lambda2= float(input("PROVIDE LAMBDA2 VALUE PLEASE: \n"))
rounds=int(input("PROVIDE MAX NUMBER OF ROUNDS FOR AVOID LOOP PLEASE: \n"))
weights= input("PROVIDE FILE NAME WITH EXPERT NAMES AND WEIGHTS PLEASE(remember .csv): \n")
namealternatives=input("PROVIDE FILE NAME WITH ALTERNATIVES NAMES PLEASE(remember .csv) \n")
print("\n")
wei=genfromtxt(weights, delimiter=',')
wei=wei[1]                                          #taking into only the values of the weights
matrixes=preferencerelationalmatrix(name)
consistencymatrix(matrixes)
coefficientbinom=int(((factorial(len(matrixes)))/(factorial(2)*factorial(len(matrixes)-2))))#calculate the binomial coefficient
simmatrixes=similaritymatrices(matrixes,coefficientbinom)
print("SIMILARITY MATRIXES(ordered following the alternative number): \n",simmatrixes, "\n")                
consmatrix= consensusmatrix(simmatrixes,coefficientbinom)
print("CONSENSUS MATRIX: \n", consmatrix, "\n")
ca,consensvalue= consensusmeasure(consmatrix)
pc=collectivepreferencematrix(matrixes)
colsimmatrixes= collectivesimilaritymatrices(matrixes, pc)
colsimilmeas,aggrecolsimilmeas= collectivesimilarmeasure(colsimmatrixes)
groups=groupsadvice(wei,lambda1,lambda2)
c=name
i=0
print("\n")
print("CONSENSUS VALUES IS: ",consensvalue, " \n")
if consensvalue<threshold and i<rounds:
    print("CONSENSUS NOT OK, ENTER IN THE FEEDBACK MECHANISM: \n")
    print("COLLECTIVE PREFERENCE MATRIX(pc matrix): \n", pc, "\n")
    print("COLLECTIVE SIMILARITY MATRICES: \n", colsimmatrixes, "\n")
    print("COLLECTIVE SIMILARITY MEASURE: \n", colsimilmeas, "\n")
while consensvalue<threshold and i<rounds: #enter if consensus is not achieved or rounds are also available and repeat the same of previous steps
    low=lowgroupadvice(consensvalue,matrixes,groups,consmatrix,pc)
    medium= mediumgroupadvice(consensvalue,matrixes,groups,consmatrix,pc,colsimilmeas,ca)
    high= highgroupadvice(consensvalue,matrixes,groups,consmatrix,pc,colsimilmeas,ca,colsimmatrixes)
    name=input("Provide the folder name with file of matrix preferences modified \n")
    matrixes=preferencerelationalmatrix(name)
    consistencymatrix(matrixes)
    simmatrixes=similaritymatrices(matrixes,coefficientbinom)                
    consmatrix= consensusmatrix(simmatrixes,coefficientbinom)
    ca,consensvalue= consensusmeasure(consmatrix)
    pc=collectivepreferencematrix(matrixes)
    colsimmatrixes= collectivesimilaritymatrices(matrixes, pc)
    c=name
    colsimilmeas,aggrecolsimilmeas= collectivesimilarmeasure(colsimmatrixes)
    print("SIMILARITY MATRIXES(ordered following the alternative number): \n",simmatrixes, "\n")
    print("CONSENSUS MATRIX: \n", consmatrix, "\n")
    print("COLLECTIVE PREFERENCE MATRIX(pc matrix): \n", pc, "\n")
    print("COLLECTIVE SIMILARITY MATRICES: \n", colsimmatrixes, "\n")
    print("COLLECTIVE SIMILARITY MEASURE: \n", colsimilmeas, "\n")
    print("NOW CONSENSUS VALUE IS: ", consensvalue, " \n")
    i=i+1
print("GO TO CALCULATE BEST ALTERNATIVE \n")
a=len(matrixes)
b=len(matrixes[0])
arv=np.empty([a,b])
for i in range(len(matrixes)): #calculate the mean for each alternative for each expert
    arv[i]= np.mean(matrixes[i],axis=1)
print("MEAN ROW FOR EACH EXPERT: \n", arv, "\n")
arvs=np.argsort(arv) # mean values are ordered 
final=np.zeros([1,b],dtype=int)
for i in range(len(arvs)):
    for j in range(len(arvs[i])):# assign point to each alternative depending the position 
        val=arvs[i][j]
        final[0][val]=final[0][val]+j+1
arv=arv.round(2)
for i in range(len(arv)): #check if are alternative with the same mean and then assign the same point for each one
    for j in range(len(arv[i])-1):
        x=arvs[i][j]
        y=arvs[i][j+1]
        if arv[i][x]==arv[i][y]:
            final[0][x]=final[0][x]+1
print("FINAL SCORE OF EACH ALTERNATIVE: \n")
names=readnames(namealternatives)
print(final[0])
orde=np.argsort(final[0]) 
n=len(orde)
max1=orde[n-1]
max2=orde[n-2]
best=np.argmax(final[0])
if final[0][max1]==final[0][max2]: #if in the final choice of best alternative there are alternative with the same score calculate the mean of the column 
    summ=np.sum(arv,axis=0)
    if summ[max1]>summ[max2]:
        best=max1
    else:
        best=max2
print("\n")
print("THE BEST ALTERNATIVE IS '",names[best],"'")
    
    
        
