"""
	Copyright 2015 Jason Randoplh Eads
	
	Licensed under the Apache License, Version 2.0 (the "License");
	you may not use this file except in compliance with the License.
	You may obtain a copy of the License at
	
	http://www.apache.org/licenses/LICENSE-2.0
	
	Unless required by applicable law or agreed to in writing, software
	distributed under the License is distributed on an "AS IS" BASIS,
	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
	See the License for the specific language governing permissions and
	limitations under the License.
"""
	
"""
	This script looks through each record and attempts to break it down.
	
	It stores each eye and attempts to match it with it's mate.
	
	metrics are collected and displayed.
	
"""




MAX_RECORDS = None
#MAX_RECORDS = 7

# for eye pair, classify as one combination type


eye_count = 0
pair_count = 0

# eye_type_counts {Eye Type #: count}
eye_type_counts = {}
eye_type_counts[0] = 0
eye_type_counts[1] = 0
eye_type_counts[2] = 0
eye_type_counts[3] = 0
eye_type_counts[4] = 0

# pair_type_counts {Pair Type #'s as a sorted tuple: count}
pair_type_counts = {}


'''
	Pair Type
	
	0 0 - 0
	0 1 - 1
	0 2 - 2
	0 3 - 3
	0 4 - 4
	1 1 - 5
	1 2 - 6
	1 3 - 7
	1 4 - 8
	2 3 - 9
	2 4 - 10
	3 4 - 11
	4 4 - 12
	
	
	
	'''

# (id,rl,class)
unmatched_eyes = []

records_processed = 0




# break down a record and compute consequences
# TODO: increase cohesion, break out compute consequences
def process_record(record):
	
	global records_processed
	global unmatched_eyes
	global eye_count
	global pair_count
	global pair_type_counts
	global eye_type_counts

	#print 'processing record %d: %s' % (records_processed, str(record))
	
	#collect id number
	#underscore
	#collect left / right
	# comma
	#classification number

	id_number_str = ''
	id = None
	
	left_right_str = ''
	left_right = None # True if left
	
	classification_number_str = ''
	classification = None
	
	# collect id
	i = 0
	while i < len(record):
		if record[i] == '_':
			i+=1
			break
		id_number_str += record[i]
		i+=1
		if i == len(record):
			print 'ERROR in record %d: EOR when collecting ID' % records_processed
			return
	id = int(id_number_str)

	# Collect left/right
	while i < len(record):
		if record[i] == ',':
			i+=1
			break
		left_right_str += record[i]
		i+=1
		if i == len(record):
			print 'ERROR in record %d: EOR when collecting left/right' % records_processed
			return
	if left_right_str == 'left':
		left_right = True
	else:
		left_right = False

	# collect class
	while i < len(record):
		classification_number_str += record[i]
		i+=1
	classification = int( classification_number_str )

	# determine data


	# see if it makes a pair
	mated = False
	mate = None
	#print ( 'unmatched: ' + str(unmatched_eyes) )
	for e in unmatched_eyes:
		if e[0] == id:
			# match!
			mated = True
			mate = e
			break

	if mated:
		unmatched_eyes.remove(mate)
		pair_count += 1
		classes = [e[2],classification]
		classes.sort()
		classes_index = tuple(classes)
		if pair_type_counts.has_key(classes_index):
			pair_type_counts[classes_index] += 1
		else:
			pair_type_counts[classes_index] = 1
	else:
		unmatched_eyes.append((id, left_right, classification))

	eye_type_counts[classification] += 1
	eye_count += 1

	# static count
	records_processed += 1


#if __name__ == "__main__":

train_labels_csv = open("trainLabels.csv","r").read()

# process all records
record = ''
header_clipped = False
for c in train_labels_csv:
	if c == '\n':
		if header_clipped:
			process_record(record)
			if MAX_RECORDS:
				if records_processed >= MAX_RECORDS:
					break
		else:
			header_clipped = True
		record = ''
	else:
		record += c

# output results
print 'completed!'
print
print 'records processed:    %d' % records_processed
print 'eye count:            %d' % eye_count
print 'eye type count / pairs:'
eye_type_instance_sum = 0
keys = eye_type_counts.keys()
keys.sort()
for eye_type in keys:
	eye_type_instance_sum += eye_type_counts[eye_type]
for eye_type in keys:
	eye_type_percentage = (float(eye_type_counts[eye_type]) / eye_type_instance_sum ) * 100
	print ('    ' + str(eye_type) + ':  % ' + ('%7.4f' % eye_type_percentage) + ', ' + str(eye_type_counts[eye_type]))
print
print 'pair count:           %d' % pair_count
print 'pair types:'
pair_type_instance_sum = 0
keys = pair_type_counts.keys()
keys.sort()
for pair_type in keys:
	print ('    ' + str(pair_type) + ':  ' + str(pair_type_counts[pair_type]))
	pair_type_instance_sum += pair_type_counts[pair_type]
print
if len(unmatched_eyes):
	print 'unmatched eyes:'
	for unmatched_eye in unmatched_eyes:
		print ('    ' + str(unmatched_eye))
	print


#


# error checking

if eye_type_instance_sum != eye_count:
	print 'ERROR: eye count check did not match'
	print( '    eye_type_instance_sum:  ' + str(eye_type_instance_sum))
	print( '    eye_count:              ' + str(eye_count))

if pair_type_instance_sum != pair_count:
	print 'ERROR: pair count check did not match'
	print( '    pair_type_instance_sum:  ' + str(pair_type_instance_sum))
	print( '    pair_count:              ' + str(pair_count))


