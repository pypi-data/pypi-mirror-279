# -*- coding: utf-8 -*-
# module core.py
#
# Copyright (c) 2015-2024  Cogniteva SAS
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# ---------------------------------------------------------------------------
# Minimal port of the ELG functionality from Cogniteva's Wolfish Record
# Linkage (WRL) Library
# ---------------------------------------------------------------------------
import pkg_resources                              #
import subprocess                                 #
import sys                                        #
import os                                         #
import platform                                   #
import hashlib                                    #
import shutil                                     #
import logging                                    #
log = logging.getLogger(__name__)                 #
# ---------------------------------------------------------------------------
def md5sum(filename):
  """
  Compute the MD5 checksum of a file.

  Args:
    filename (str): the path to the file for which the MD5 checksum is computed.

  Returns:
    str: the hexadecimal representation of the MD5 checksum.
  """
  # compute the md5 checksum
  md5_hash = hashlib.md5()
  with open(filename, 'rb') as f:
    for byte_block in iter(lambda: f.read(4096), b''):
      md5_hash.update(byte_block)

  # hexadecimal representation
  filename_md5 = md5_hash.hexdigest()
  return filename_md5
# ---------------------------------------------------------------------------
def md5sum_combine(md5_1, md5_2):
  """
  Combine two MD5 checksums into a single string of the length of one MD5 checksum.

  Args:
    md5_1 (str): the first MD5 checksum in hexadecimal.
    md5_2 (str): the second MD5 checksum in hexadecimal.

  Returns:
    str: the combined MD5 checksum in hexadecimal.
  """
  # Convert the hex strings to bytes
  bytes_1 = bytes.fromhex(md5_1)
  bytes_2 = bytes.fromhex(md5_2)

  # XOR the bytes together
  combined_bytes = bytes(a ^ b for a, b in zip(bytes_1, bytes_2))

  # Convert the combined bytes back to a hex string
  return combined_bytes.hex()
# ---------------------------------------------------------------------------
def srmdir(path, whitelist=None, blacklist=None):
  """
  Safely remove a directory, ensuring it's not a system directory.

  Args:
    path (str): The directory path to remove.
    whitelist (list): Directories allowed to be removed.
    blacklist (list): Directories not allowed to be removed.

  Raises:
    ValueError: If an attempt is made to delete a protected or root directory.
  """

  # ensure the directory is not root
  if path == "/":
    raise ValueError("attempt to delete root directory is not allowed.")

  # normalize the path to avoid issues with trailing slashes
  path = os.path.normpath(path)

  # set default whitelists and blacklists if not provided
  if whitelist is None:
    whitelist = []
  if blacklist is None:
    blacklist = ["/", "/bin", "/boot", "/dev", "/etc", "/home", "/lib",
                 "/proc", "/root", "/sys", "/usr", "/var"]

  # check if path is in the blacklist
  if path in blacklist:
    raise ValueError(f"Attempt to delete a protected directory is not allowed: {path}")

  # if a whitelist is provided, ensure the path is within the whitelist
  if whitelist and path not in whitelist:
    raise ValueError(f"attempt to delete a directory not in the whitelist: {path}")

  # check if the directory exists before attempting to delete
  if os.path.exists(path):
    shutil.rmtree(path)
