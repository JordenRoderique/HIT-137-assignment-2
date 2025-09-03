# Question 1
'''
Generative AI used to assist with
clear and concise docstrings.
'''

# Constants ----------------------------------------------------------

LOWER_A = 97     # 'a'
LOWER_N = 110    # 'n'
LOWER_Z1 = 123   # 'z' + 1 (range stop)
UPPER_A = 65     # 'A'
UPPER_N = 78     # 'N'
UPPER_Z1 = 91    # 'Z' + 1 (range stop)
ALPHA_SPAN = 26


# Problem Analysis Helper --------------------------------------------

def check_26_char_wrap(shift_ceil: int = ALPHA_SPAN) -> None:
  '''
  This function is to check whether a 26 char wrap is possible.
  Each char when encrypted should map to a unique value in
  order to get the original back from the decryption function.
  If any of the sets have a length of less than 26 it means
  the there were duplicates stored during encryption and therefore
  accurate decryption isn't possible without storing extra data in
  the encrypted file.

  As a result we will be wrapping in the 13 char window the encryption
  algorithm applies to so appropriate decryption can be applied.

  Args:
    shift_ceil: Exclusive upper bound for shift1/shift2 grid search.

  Side Effects:
    Prints diagnostic lines for each (shift1, shift2) pair.
  '''
  for i in range(shift_ceil):
    for j in range(shift_ceil):
      lowercase_set: set[int] = set()
      uppercase_set: set[int] = set()
      for k in range(ALPHA_SPAN):
        if k < 13:
          lower = (k + (i * j)) % ALPHA_SPAN
          upper = (k - i) % ALPHA_SPAN
          lowercase_set.add(lower)
          uppercase_set.add(upper)
        else:
          lower = (k - (i + j)) % ALPHA_SPAN
          upper = (k + (j ** 2)) % ALPHA_SPAN
          lowercase_set.add(lower)
          uppercase_set.add(upper)
      print(
        f"shift1: {i}, shift2: {j}",
        f"lowercase_set: {len(lowercase_set)}",
        f"uppercase_set: {len(uppercase_set)}"
      )


# Utilities -----------------------------------------------------------

def get_text(path: str) -> str:
  """
    Read the entire contents of a text file.

    Args:
        path: Path to a UTF-8 text file.

    Returns:
        File contents as a string.

    Raises:
        SystemExit: If reading the file fails.
  """
  try:
    with open(path, "r") as file:
      return file.read()
  except Exception as e:
    print("There was a problem reading the file: ", e)
    raise SystemExit(1)


def get_user_input() -> int:
  """
  Prompt the user until a valid integer is provided.

  Returns:
      The integer value entered by the user.
  """
  userInput = input("")
  try:
      return int(userInput)
  except ValueError:
      print("Please enter a valid number: ", end="")
      return get_user_input()


def wrap_code(code: int) -> int:
  """
  Wrap an integer into the 13-value window used by this scheme.

  Args:
      code: Arbitrary integer (can be negative).

  Returns:
      code modulo 13.
  """
  return code % 13


# Low Level Character Handling ----------------------------------------------

def encrypt_lowercase_char(char: str, shift1: int, shift2: int) -> str:
  """
  Encrypt a single lowercase character per the assignment rules.

  Rules:
      a–m:  shift forward by (shift1 * shift2), wrapped in 13.
      n–z:  shift backward by (shift1 + shift2), wrapped in 13.

  Args:
      char: A single character assumed to be lowercase.
      shift1: First shift parameter.
      shift2: Second shift parameter.

  Returns:
      Encrypted character, or original if outside a–z.
  """
  code = ord(char)

  if code in range(LOWER_A, LOWER_N):
    normalized_code = code - LOWER_A
    encrypted_code = normalized_code + (shift1 * shift2)
    encrypted_char = chr(wrap_code(encrypted_code) + LOWER_A)
    return encrypted_char

  if code in range(LOWER_N, LOWER_Z1):
    normalized_code = code - LOWER_N
    encrypted_code = normalized_code - (shift1 + shift2)
    encrypted_char = chr(wrap_code(encrypted_code) + LOWER_N)
    return encrypted_char

  return char


def encrypt_uppercase_char(char: str, shift1: int, shift2: int) -> str:
  """
  Encrypt a single uppercase character per the assignment rules.

  Rules:
      A–M:  shift backward by shift1, wrapped in 13.
      N–Z:  shift forward by (shift2 ** 2), wrapped in 13.

  Args:
      char: A single character assumed to be uppercase.
      shift1: First shift parameter.
      shift2: Second shift parameter.

  Returns:
      Encrypted character, or original if outside A–Z.
  """
  code = ord(char)

  if code in range(UPPER_A, UPPER_N):
    normalized_code = code - UPPER_A
    encrypted_code = normalized_code - shift1
    encrypted_char = chr(wrap_code(encrypted_code) + UPPER_A)
    return encrypted_char

  if code in range(UPPER_N, UPPER_Z1):
    normalized_code = code - UPPER_N
    encrypted_code = normalized_code + (shift2 ** 2)
    encrypted_char = chr(wrap_code(encrypted_code) + UPPER_N)
    return encrypted_char

  return char


def encrypt_char(char: str, shift1: int, shift2: int) -> str:
  """
  Handles single character encryption, dispatching by case.

  Non-alphabetic characters are passed through unchanged.
  """
  if char.islower():
    return encrypt_lowercase_char(char, shift1, shift2)

  if char.isupper():
    return encrypt_uppercase_char(char, shift1, shift2)

  return char


def decrypt_lowercase_char(char: str, shift1: int, shift2: int) -> str:
  # Inverse transform for lowercase encryption.
  code = ord(char)

  if code in range(LOWER_A, LOWER_N):
    normalized_code = code - LOWER_A
    decrypted_code = normalized_code - (shift1 * shift2)
    decrypted_char = chr(wrap_code(decrypted_code) + LOWER_A)
    return decrypted_char

  if code in range(LOWER_N, LOWER_Z1):
    normalized_code = code - LOWER_N
    decrypted_code = normalized_code + (shift1 + shift2)
    decrypted_char = chr(wrap_code(decrypted_code) + LOWER_N)
    return decrypted_char

  return char


def decrypt_uppercase_char(char: str, shift1: int, shift2: int) -> str:
  # Inverse transform for uppercase encryption.
  code = ord(char)

  if code in range(UPPER_A, UPPER_N):
    normalized_code = code - UPPER_A
    decrypted_code = normalized_code + shift1
    decrypted_char = chr(wrap_code(decrypted_code) + UPPER_A)
    return decrypted_char

  if code in range(UPPER_N, UPPER_Z1):
    normalized_code = code - UPPER_N
    decrypted_code = normalized_code - (shift2 ** 2)
    decrypted_char = chr(wrap_code(decrypted_code) + UPPER_N)
    return decrypted_char

  return char


def decrypt_char(char: str, shift1: int, shift2: int) -> str:
  """
  Handles single character decryption, dispatching by case.

  Non-alphabetic characters are passed through unchanged.
  """
  if char.islower():
    return decrypt_lowercase_char(char, shift1, shift2)

  if char.isupper():
    return decrypt_uppercase_char(char, shift1, shift2)

  return char


# Function Implementations for Question ---------------------------------------------------

def encrypt(
    shift1: int,
    shift2: int,
    in_path: str = "raw_text.txt",
    out_path: str = "encrypted_text.txt"
    ):
  """
  Encrypt an input file and write the result.

  Args:
      shift1: First shift parameter.
      shift2: Second shift parameter.
      in_path: Path of plaintext input.
      out_path: Path to write ciphertext.
  """
  raw_text = get_text(in_path)
  encrypted_text = "".join([encrypt_char(char, shift1, shift2) for char in raw_text])

  with open(out_path, "w") as file:
    file.write(encrypted_text)


def decrypt(
    shift1: int,
    shift2: int,
    in_path: str = "encrypted_text.txt",
    out_path: str = "decrypted_text.txt"
    ):
  """
  Decrypt an input file and write the result.

  Args:
      shift1: First shift parameter used for encryption.
      shift2: Second shift parameter used for encryption.
      in_path: Path of ciphertext input.
      out_path: Path to write plaintext output.
  """
  encrypted_text = get_text(in_path)
  decrypted_text = "".join([decrypt_char(char, shift1, shift2) for char in encrypted_text])

  with open(out_path, "w") as file:
    file.write(decrypted_text)


def verify(
    raw_path: str = "raw_text.txt",
    decrypted_path: str = "decrypted_text.txt"
    ) -> bool:
  """
  Check whether decryption reproduced the original exactly.

  Args:
      raw_path: Path to the original plaintext file.
      decrypted_path: Path to the decrypted output file.

  Returns:
      True if contents match byte-for-byte, otherwise False.

  Side Effects:
      Prints a human-readable message.
  """
  raw_text = get_text(raw_path)
  decrypted_text = get_text(decrypted_path)

  if raw_text == decrypted_text:
    print("The decryption was successful")
    return True
  else:
    print("The decryption was not successful")
    return False


def main() -> None:
  # Prompt for parameters, run encrypt → decrypt → verify.
  print("Please provide your shift1 value: ", end="")
  shift1 = get_user_input()
  print("Please provide your shift2 value: ", end="")
  shift2 = get_user_input()
  print("Encrypting file...")
  encrypt(shift1, shift2)
  print("Encryption complete.")
  print("Decrypting file...")
  decrypt(shift1, shift2)
  print("Decryption complete.")
  print("Verifying decrypted file matches the original file...")
  verify()


if __name__ == "__main__":
  main()
  # Uncomment below to view the check
  # check_26_char_wrap()
