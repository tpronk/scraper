# Load data
import pickle
data = []
fh = open('data.pickle', 'rb')
more_rows = True
while more_rows:
  try:
    row = pickle.load(fh, encoding='bytes')
    data.append(row)
  except:
    more_rows = False
fh.close()

# Report
print('Found ' + str(len(data)) + ' rows of data')

# Convert to JSON
import json
json_data = json.dumps(data)

# Save
with open("data.json", "w") as fh:
  fh.write(json_data)


