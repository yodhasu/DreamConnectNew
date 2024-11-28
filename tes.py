import token
import tokenize
import nltk
import re
from nltk.tokenize import word_tokenize
from urlextract import URLExtract

usrinput = input("String: ")
path_pattern = path_pattern = r"'([A-Za-z]:\\(?:[^\\/:*?\"<>|\r\n]+\\)*[^\\/:*?\"<>|\r\n]+)'"
# input = input.replace("\\", "/")
# tokenized = word_tokenize(input)
# tokenized

match = re.search(path_pattern, usrinput)
extractor = URLExtract()
if match:
    file_path = match.group(1)
    
    # Replace backslashes with forward slashes in the file path
    processed_path = file_path.replace("\\", "/")
    
    # Remove the file path from the original text
    remaining_text = usrinput.replace(file_path, "").strip()
    
    # Tokenize the remaining text
    tokenized_text = word_tokenize(remaining_text)
    
    # Print the results
    print("File Path:", processed_path)
    print("Remaining Text:", tokenized_text)
else:
    urls = extractor.find_urls(usrinput)
    if len(urls) < 1:
        print("No file path found in the input text.")
    else:
        print(''.join(urls))