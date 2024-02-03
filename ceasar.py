import string 

def ceasar(msg, step):
  def shift(alphabet):
    return alphabet[step:] + alphabet[:step]

  alphabets = [string.ascii_lowercase, string.ascii_uppercase]

  shifted_alphabets = tuple(map(shift, alphabets))
  joined_aphabets = ''.join(alphabets)
  joined_shifted_alphabets = ''.join(shifted_alphabets)
  table = str.maketrans(joined_aphabets, joined_shifted_alphabets)
  return msg.translate(table)