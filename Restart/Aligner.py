import re

# this function removes punctuation and makes sure words are lowercase, so they can be properly compared
def strip_punc(word):
	return re.sub(r'[.,!?]', '', word.lower())


# this function takes in two lists of words and finds the first matching word, returning the indexes
def find_first_matching_word(words1, words2):
	for ind1, word1 in enumerate(words1):
		for ind2, word2 in enumerate(words2):
			if strip_punc(word1) == strip_punc(word2):
				return ind1, ind2

	return None, None


# this function takes in a list of words from the real script
# and a list of words rom the speech to text script
# and the speech to text timestamps, then it uses this information to best align the scripts
# then it can best align the timestamps from the text to speech to the real words being said
def align_transcripts(real_words, fake_words, fake_timestamps):
	real_timestamps = []
	real_index = 0
	fake_index = 0
		
	# repeats until either index reaches the end of the list
	while real_index < len(real_words) or fake_index < len(fake_words):
		# if the words are the same, simply use the fake word + timestamp
		if strip_punc(real_words[real_index]) == strip_punc(fake_words[fake_index]):
			real_timestamps.append(([real_words[real_index]], fake_timestamps[fake_index][1], fake_timestamps[fake_index][2]))
			real_index += 1
			fake_index += 1
		# if the words are not the same, we find the next matching words (stopping at 8 beyond)
		else:
			next_real, next_fake = find_first_matching_word(real_words[real_index:real_index + 8], fake_words[fake_index:fake_index + 8])
			# if there are no matching words, we are probably at the end of the transcript
			# when this is the case, use remaining real words, with remaining fake time
			if next_real == None:
				real_timestamps.append((real_words[real_index:len(real_words)], fake_timestamps[fake_index][1], fake_timestamps[-1][2]))
				break

			# if there are matching words, we use real words from our current index, to the next matching word
			# and the fake time from the current index to the next matching word as well
			next_real += real_index
			next_fake += fake_index
			real_timestamps.append((real_words[real_index:next_real], fake_timestamps[fake_index][1], fake_timestamps[(next_fake - 1)][2]))
			real_index = next_real
			fake_index = next_fake

	return real_timestamps

