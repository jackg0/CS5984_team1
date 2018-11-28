freq_words.py - Finds the most frequent words in a json file that contains a sentences field. Requires a file to be passed through the -f option.

pos_tagging.py - Performs basic part-of-speech tagging on a json file that contains a sentences field. Requires a file to be passed through the -f option.

textrank_summarizer.py - Performs TextRank summarization with a json file that contains a sentences field. Requires a file to be passed through the -f option.

template_summarizer.py - Performs template summarization with a json file that contains a sentences field. Requires a file to be passed through the -f option.

wikipedia_content.py - Extracts content from a Wikipedia page given a topic and formats the information for the pointer-generator network using the “make_datafiles.py” script. Requires a topic to be given in the -t option and an output directory for “make_datafiles.py” to read from with the -o option.

make_datafiles.py - Called by "wikipedia_content.py" to convert story files to
.bin files.

jusText.py - Used to clean up the large dataset

requirements.txt - Used with Anaconda for installing all of the dependencies.

small_dataset.json - Properly formatted json file for use with other files.
