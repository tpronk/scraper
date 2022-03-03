# *** Load data
import pickle
data = []
fh = open('data/data_parsed.pickle', 'rb')
more_rows = True
while more_rows:
  try:
    row = pickle.load(fh, encoding='bytes')
    data.append(row)
  except:
    more_rows = False
fh.close()


# *** Prepare data

# *** Find rows with duplicate topic IDs and merge them
# Merged topics
topics = []
# Report
print('Found ' + str(len(data)) + ' rows of data')
# Properties to copy from row to topic
properties_to_copy = ['topic_id', 'topic_title', 'topic_category', 'topic_tags']
answer_info_to_copy = ['answer_user', 'answer_date', 'answer_position', 'answered']
# Unique topic IDs
import numpy
topic_ids = [row['topic_id'] for row in data]
unique_ids = numpy.unique(topic_ids)
print('Found ' + str(len(unique_ids)) + ' unique topic IDs')
# Merge each topic
for current_id in unique_ids:
  # Initialize topic with default answer info and posts
  topic = {
    'answer_user': None, 
    'answer_date': None, 
    'answer_position': None, 
    'answered': False,
    'posts': []
  }
  # Rows matching current topic ID
  rows = list(filter(
    lambda row: row['topic_id'] == current_id,
    data
  ))
  first_row = True
  # Merge current row
  for row in rows:
    # First row? copy properties
    if first_row:
      # URL without page=<x> part
      topic['topic_url'] = row['topic_url'].split('?page=')[0]
      # Properties
      for property in properties_to_copy:
        topic[property] = row[property]
    # Later rows? check properties
    else:
      for property in properties_to_copy:
        if topic[property] != row[property]:
          raise Exception(
            'Mismatched property for topic_id' + str(current_id) +
            '. Found values "' + str(topic[property]) +
            '" and "' + str(row[property]) + '"'
          )
    # If there answer info in row, copy that to topic
    for answer_info in answer_info_to_copy:
      topic[answer_info] = row[answer_info]
    # Copy posts
    for post in row['posts']:
      topic['posts'].append(post)
    first_row = False
  # Sort posts by position
  topic['posts'] = sorted(topic['posts'], key = lambda post: post['position'])
  # Add to output
  topics.append(topic)

# *** Convert to JSON and save
import json
json_data = json.dumps(topics)
with open("data/data_processed.json", "w") as fh:
  fh.write(json_data)


