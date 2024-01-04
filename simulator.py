from revised import finalMatrix as df
import random
import pandas as pd

start = 0 #start at GO square (index 0)
frequencies = [0] * 40 #array that keeps track of how many times each square is visited
squares = [x for x in range(40)] #square indexes array

#simulate 1000 moves
current = start
for i in range(1000):
  nextSquare = random.choices(squares, weights=df[current], k=1)
  frequencies[nextSquare[0]] += 1
  current = nextSquare[0]

print(frequencies)

# initialize csv with visiting frequencies
df = pd.DataFrame(frequencies)
df.round(4)
df.to_csv('csv/ranked.csv', index=False)

# update visiting frequencies with each new walkthrough
df = pd.read_csv('csv/ranked.csv')
for i in range(40):
  df.loc[i] += frequencies[i]

# df.to_csv('ranked.csv', index=False)

# average out all values
df = pd.read_csv('csv/ranked.csv')
for i in range(40):
  df.loc[i] /= 1000

# df.to_csv('ranked.csv', index=False)

# sort all values and put them in final ordered csv
values = (pd.read_csv('csv/ranked.csv', sep='\t', header=None))
values = [x for x in values[0].values]
keys = [i for i in range(1,41)]
display = dict(zip(keys, values))
display = {k: v for k, v in sorted(display.items(), key=lambda item: item[1], reverse=True)}
print(display)

(pd.DataFrame.from_dict(data=display, orient='index')
   .to_csv('csv/ordered.csv', header=False))