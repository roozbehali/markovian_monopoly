import sys
import numpy as np
import pandas as pd

### dual dice roll all probabilities
rollProbs = [1,2,3,4,5,6,5,4,3,2,1]
rollProbs = [x/36 for x in rollProbs]

### rollTM main matrix
startProbs = [0]*40
startProbs[2:13] = rollProbs
rollTM = np.zeros([40, 40])
rollTM[0] = startProbs

for i in range(1,40):
  startProbs.insert(0, startProbs.pop())
  rollTM[i] = startProbs

### Probability of going from GO TO JAIL to any square aside from jail is 0
rollTM[30] = [0]*40
rollTM[30][10] = 1

### chanceTM; chance squares at 8, 23, 37;
chanceRow = [1] + [0]*39
chanceTM = np.zeros([40, 40])
chanceTM[0] = chanceRow

for i in range(1,40):
  chanceRow.insert(0, chanceRow.pop())
  chanceTM[i] = chanceRow

# chance square 8
chanceTM[7] = [0]*40
chanceTM[7, [0,4,5,10,11,12,24,39]] = 1.0/16
chanceTM[7][15] = 2.0/16
chanceTM[7][7] = 6.0/16

# chance square 23
chanceTM[22] = [0]*40
chanceTM[22, [0,5,10,11,19,24,28,39]] = 1.0/16
chanceTM[22][25] = 2.0/16
chanceTM[22][22] = 6.0/16

# chance square 37
chanceTM[36] = [0]*40
chanceTM[36, [0,10,11,12,24,33,39]] = 1.0/16
chanceTM[36][5] = 3.0/16
chanceTM[36][36] = 6.0/16

### communityTM; community squares at 3, 18, 34
communityRow = [1] + [0]*39
communityTM = np.zeros([40, 40])
communityTM[0] = communityRow

for i in range(1,40):
  communityRow.insert(0, communityRow.pop())
  communityTM[i] = communityRow

communityTM[2, [0, 10]] = 1.0/16
communityTM[2,2] = 14.0/16

communityTM[17, [0, 10]] = 1.0/16
communityTM[17,17] = 14.0/16

communityTM[33, [0, 10]] = 1.0/16
communityTM[33,33] = 14.0/16

### doublesTM; 1/216 chance to go to Jail from almost every square, multiply everything else by 215/216 to account
doublesRow = [215/216] + [0] * 39
doublesTM = np.zeros([40,40])
doublesTM[0] = doublesRow

for i in range(1,40):
  doublesRow.insert(0, doublesRow.pop())
  doublesTM[i] = doublesRow

doublesTM[[range(0, 40)], 10] = 1/216
doublesTM[10][10] = 1 #keep Jail Jail square the same because you cannot go to jail from jail
doublesTM[30][10] = 0 #keep GO TO JAIL Jail square the same because it is always 1
doublesTM[30][30] = 1 #it is not possible to be on the GO TO JAIL square, it will just send you to jail

### CSV's for all seperate matrices to check validity
# rf = pd.DataFrame(rollTM) 
# rf = rf.round(decimals=4)
# rf.to_csv('csv/gotojailupdate.csv', index=False)

# chf = pd.DataFrame(chanceTM) 
# chf = chf.round(decimals=4)
# chf.to_csv('csv/chance.csv', index=False)

# cof = pd.DataFrame(communityTM) 
# cof = cof.round(decimals=4)
# cof.to_csv('csv/community.csv', index=False)

# douf = pd.DataFrame(doublesTM) 
# douf = douf.round(decimals=4)
# douf.to_csv('csv/doubles.csv', index=False)

# multiplying all matrices, ORDER MATTERS INITIALLY
finalMatrix = np.matmul(np.matmul(np.matmul(rollTM, chanceTM), communityTM), doublesTM)
df = pd.DataFrame(finalMatrix)
df = df.round(4)
df.to_csv('csv/multiplied.csv', index=False)

# sanity check (each row should sum to 1)
# for i in range(len(df)):
#   counter = 0
#   for j in range(len(df[i])):
#     counter += df.loc[i][j]
#   print(counter)