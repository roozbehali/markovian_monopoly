import sys
import numpy as np
import pandas as pd

### dual dice roll all probabilities
rollProbs = [1,2,3,4,5,6,5,4,3,2,1]
rollProbs = [x/36 for x in rollProbs]

def matrixMaker(probs, TM, counter, bound):
  if counter == bound:
    return(TM)
  
  # shifts last element to front
  probs.insert(0, probs.pop())
  TM[counter] = probs

  # recursion for next row until we reach bound
  matrixMaker(probs, TM, counter+1, bound)

### rollTM main matrix
startProbs = [0]*40
startProbs[1:12] = rollProbs
rollTM = np.zeros([40, 40])
rollTM[0] = startProbs
matrixMaker(startProbs, rollTM, 1, 40)

for i in range(1,40):
  startProbs.insert(0, startProbs.pop())
  rollTM[i] = startProbs

### Probability of going from GO TO JAIL to any square aside from jail is 0
rollTM[30] = [0]*40

### chanceTM; chance squares at 8, 23, 37;
chanceRow = [1] + [0]*39
chanceTM = np.zeros([40, 40])
chanceTM[0] = chanceRow
matrixMaker(chanceRow, chanceTM, 1, 40)

# chance square 8
chanceTM[7] = [0]*40
chanceTM[7, [0,10,24,11,39,5,4,12]] = 1.0/16
chanceTM[7][15] = 2.0/16
chanceTM[7][7] = 6.0/16

# chance square 23
chanceTM[22] = [0]*40
chanceTM[22, [0,10,24,11,39,5,19,28]] = 1.0/16
chanceTM[22][25] = 2.0/16
chanceTM[22][22] = 6.0/16

# chance square 37
chanceTM[36] = [0]*40
chanceTM[36, [0,10,24,11,39,33,12]] = 1.0/16
chanceTM[36][5] = 3.0/16
chanceTM[36][36] = 6.0/16

### communityTM; community squares at 3, 8, 34; 1/16 to go to Jail (11), 1/16 to go to Go (1), 14/16 to stay
communityRow = [1] + [0]*39
communityTM = np.zeros([40, 40])
communityTM[0] = communityRow
matrixMaker(communityRow, communityTM, 1, 40)

communityTM[2, [0, 10]] = 1.0/16
communityTM[2,2] = 14.0/16

communityTM[17, [0, 10]] = 1.0/16
communityTM[17,17] = 14.0/16

communityTM[33, [0, 10]] = 1.0/16
communityTM[33,33] = 14.0/16

### doublesTM
doublesRow = [215/216] + [0] * 39
doublesTM = np.zeros([40,40])
doublesTM[0] = doublesRow
matrixMaker(doublesRow, doublesTM, 1, 40)

doublesTM[[range(0, 40)], 10] = 1/216
doublesTM[10][10] = 1 #keep Jail Jail square the same because you cannot go to jail from jail
doublesTM[30][10] = 0 #keep GO TO JAIL Jail square the same because it is always 1
doublesTM[30][30] = 1 #it is not possible to be on the GO TO JAIL square, it will just send you to jail

# rf = pd.DataFrame(rollTM) 
# rf = df.round(decimals=4)
# print(rf)
# rf.to_csv('gotojailupdate.csv')

# chf = pd.DataFrame(chanceTM) 
# chf = chf.round(decimals=4)
# print(chf)
# chf.to_csv('chance.csv')

# cof = pd.DataFrame(communityTM) 
# cof = cof.round(decimals=4)
# print(cof)
# cof.to_csv('community.csv')

douf = pd.DataFrame(doublesTM) 
douf = douf.round(decimals=4)
douf.to_csv('doubles.csv', index=False)

# multiplying all matrices, ORDER MATTERS INITIALLY
finalMatrix = np.matmul(np.matmul(rollTM, chanceTM), communityTM)
df = pd.DataFrame(finalMatrix)
df = df.round(4)
df.to_csv('monopolyMC.csv', index=False)

# evals, evecs = np.linalg.eig(finalMatrix.T)
# evec1 = evecs[:,np.isclose(evals, 1)]
# evec1 = evec1[:, 0]
# stationary = evec1 / evec1.sum()
# stationary = stationary.real

# keys = [i for i in range(1,41)]
# display = dict(zip(keys, stationary))
# display = {k: v for k, v in sorted(display.items(), key=lambda item: item[1], reverse=True)}
# print(display)

# (pd.DataFrame.from_dict(data=display, orient='index')
#    .to_csv('ordered.csv', header=False))

eigenVector = np.linalg.eig(finalMatrix.T)[1]
steadyStateVec = eigenVector[:,0]
steadyStateVec = steadyStateVec/sum(steadyStateVec)

for i in range(len(steadyStateVec)):
  steadyStateVec[i] = steadyStateVec[i].real
pd.DataFrame(steadyStateVec).to_csv('limiting.csv', index=False)

for i in (steadyStateVec):
  print(i)

# sanity check (each row should sum to 1)
# for i in range(len(df)):
#   counter = 0
#   for j in range(len(df[i])):
#     counter += df.loc[i][j]
#   print(counter)

