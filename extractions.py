import re

def runAll(test):
  results = set()
  results = results.union(findCommaSep(test))
  results = results.union(findListed(test))
  results = results.union(findQuoted(test))

  bad_keys = ["", "SDOIFJ", "F6hT5l", "P1mK5n", "7YgH5t", "6pQn8R", "X1tG5m", "B7vP1o", "Q2wX8r", "3fUj9K", "T3bR6v", "A9dF2h" 'Z0cV3n' , 'E5cR9v' , 'I4uY2b' , 'W5rT7z' , 'L4eZ0a' , 'O8yP2l' , 'J9kE3q' , 'V2wS1x' , '4kMd3r', 'Z0cV3n', 'A9dF2h', "Instea", "Howeve", "Additi", "Please", "Perhap", "AAAAAA", "BBBBBB", "CCCCCC", "Alphan", "Theref", "Px8yJ9", "J9F2DL", 'H2sN4v', "Embrac", "Nevert", "Unfort", "Mainta", "Regard", "Sharin"]
  for bad_key in bad_keys:
    results.discard(bad_key)
  results = list(results)
  results.reverse()
  return results

def findAtSentenceEnd(test):
  regex = r"\s([A-Za-z0-9]{6})\."
  result = set(re.findall(regex, test))
  return result

def findCommaSep(test):
  regex = r"([0-9A-Za-z],\s?[0-9A-Za-z],\s?[0-9A-Za-z],\s?[0-9A-Za-z],\s?[0-9A-Za-z],\s?[0-9A-Za-z]?)"
  result = re.findall(regex, test)
  result = set([s.replace(",", "") for s in result])
  result = set([s.replace(" ", "") for s in result])
  return result

def findListed(test):
  regex = r"\d*[.*]{1}\s*([A-Za-z0-9]{6})"
  results = set(re.findall(regex, test))
  regex2 = r"([A-Za-z0-9]{6})[,\.]"
  results.union(re.findall(regex2, test))
  return results


def findQuoted(test):
  regex = r"['\"\\]{1}([A-Za-z0-9]*)['\"\\]{1}"
  return set(re.findall(regex, test))