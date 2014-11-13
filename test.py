import pickle

a = {'hello': 'world'}

with open('filename.pickle', 'wb') as handle:
  pickle.dump(a, handle)

with open('filename.pickle', 'rb') as handle:
  b = pickle.load(handle)

print a == b