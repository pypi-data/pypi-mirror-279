# -*- coding: utf-8 -*-
# module worker.py
#
# Copyright (c) 2021  CorTexT Platform
# Copyright (c) 2021  Cogniteva SAS
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
__doc__ = """
Worker for Parscival - methods to parse and store datasets
=============================================================================

This module implements a generic approach to parse and
store datasets according to a specification
"""
__author__  = "Cristian Martinez, Lionel Villard"
__license__ = "MIT"
from parscival import __version__
# ---------------------------------------------------------------------------
import pluginlib                                 #

import argparse                                  #
import logging                                   #
import logging.handlers                          #
import sys                                       #
import os                                        #
import shutil                                    #
import psutil                                    #

import contextlib                                #
import mmap                                      #
import re                                        #

import yaml                                      #
import site                                      #

import klepto                                    #

from pathlib import Path                         #

import atexit                                    #

from logging.handlers import RotatingFileHandler #
from rich.logging import RichHandler             #
from rich.console import Console                 #
from rich.theme import Theme                     #
from rich.text import Text                       #

from rich.panel import Panel                     #
from rich.rule import Rule                       #
from rich.syntax import Syntax                   #
from rich.table import Table                     #

from parsimonious.grammar import Grammar         #
from parsimonious.nodes import NodeVisitor       #
from parsimonious.exceptions import ParseError   #

from rich.progress import (                      #
  BarColumn,                                     #
  Progress,                                      #
  SpinnerColumn,                                 #
  TextColumn,                                    #
  TimeElapsedColumn,                             #
  TimeRemainingColumn,                           #
)

from contextlib import suppress                  #
from dotenv import load_dotenv                   #
import semver                                    #
# ---------------------------------------------------------------------------
import jinja2                                    #
from jinja2 import Environment, meta             #
# ---------------------------------------------------------------------------
from parscival.utils import get_custom_metadata
from parscival.utils import get_version_major_minor_patch
# ---------------------------------------------------------------------------
# parscival engine version
engine_version = None
# ---------------------------------------------------------------------------
log = logging.getLogger(__name__)
# short log levels names
# according to the RCF5424
# @see https://datatracker.ietf.org/doc/html/rfc5424
logging.addLevelName(logging.DEBUG,    "(%%)")
logging.addLevelName(logging.INFO,     "(II)")
logging.addLevelName(logging.WARNING,  "(WW)")
logging.addLevelName(logging.ERROR,    "(EE)")
logging.addLevelName(logging.CRITICAL, "(CC)")
logging.addLevelName(logging.NOTSET,   "(--)")

# create a custom logging theme
# level names must be in lowercase
log_theme = Theme({
  "repr.number": "",
  "repr.error": "bold red",
  "logging.level.(%%)": "green",
  "logging.level.(ii)": "blue",
  "logging.level.(ww)": "blue",
  "logging.level.(ee)": "red",
  "logging.level.(cc)": "red",
  "logging.level.(@@)": "red",
  "logging.level.(--)": "white"
})

# setup rich console for logging
console = Console(
  record=True,
  theme=log_theme)
# ---------------------------------------------------------------------------

# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from parscival.main import process_datasets`,
# when using this Python module as a library.

def load_datasets_info(parsing_spec, parsing_data):
  """Get metadata about the documents to parse
  """
  log.info("Getting documents information...")
  records_total = 0
  files_total = 0

  # get the record separator from the parsing spec
  spec_identifier = (parsing_spec.get('spec', {})
                              .get('identifier', 'unknown'))

  spec_category = parsing_spec.get('category', {})

  # add misc regex to the parsing spec
  record_split = {
    'raw' : '',
    'len' : 0,
    'regex' : {
      'bytes' : {},
      'text'  : {}
    }
  }

  parsing_spec['misc']['record_finalizer'] = record_split
  parsing_spec['misc']['record_separator'] = record_split

  # get the record separator from the parsing spec
  record_separator = (parsing_spec.get('spec', {})
                                  .get('parsing', {})
                                  .get(spec_category, {})
                                  .get('record_separator', None))

  # continue only if a record separator is defined
  if record_separator is None:
    log.error("[yellow]{}[/yellow] - undefined grammar.record_separator".format(spec_identifier))
    return False

  parsing_spec['misc']['record_separator']['raw'] = record_separator
  parsing_spec['misc']['record_separator']['len'] = len(record_separator)

  # compile the record separator as a regex bytes
  record_separator_regex_bytes = re.compile(bytes(record_separator, encoding= 'utf-8'))
  parsing_spec['misc']['record_separator']['regex']['bytes'] = record_separator_regex_bytes

  # compile the record separator as a regex text
  record_separator_regex_text = re.compile(record_separator)
  parsing_spec['misc']['record_separator']['regex']['text']  = record_separator_regex_text

  # get the record finalizer from the parsing spec
  record_finalizer = (parsing_spec.get('spec', {})
                                  .get('parsing', {})
                                  .get(spec_category, {})
                                  .get('record_finalizer', None))

  # set record finalizer_regex
  if record_finalizer is not None:
    # compile the record finalizer as a regex bytes
    record_finalizer_regex_bytes = re.compile(bytes(record_finalizer, encoding= 'utf-8'))
    # compile the record finalizer as a regex text
    record_finalizer_regex_text = re.compile(record_finalizer)
    # compile the reverse record finalizer as a regex text
    record_finalizer_regex_text_reverse = re.compile(record_finalizer[::-1])

    parsing_spec['misc']['record_finalizer']['raw'] = record_finalizer
    parsing_spec['misc']['record_finalizer']['len'] = len(record_finalizer)
    parsing_spec['misc']['record_finalizer']['regex']['bytes'] = record_finalizer_regex_bytes
    parsing_spec['misc']['record_finalizer']['regex']['text']  = record_finalizer_regex_text
    parsing_spec['misc']['record_finalizer']['regex']['text_reverse'] = record_finalizer_regex_text_reverse

  # loop over each file
  for f in parsing_data['files']:
    file_path = Path(f.name)
    filename  = file_path.name

    # ensure that we have an existing non empty file
    if not file_path.exists() or file_path.stat().st_size == 0:
      log.warn("[cyan]{}[/cyan] is empty".format(filename))
      continue

    # @see https://stackoverflow.com/a/11692134/2042871
    mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    with contextlib.closing(mm) as dataset:
      records = record_separator_regex_bytes.findall(dataset)
      records_count = len(records)
      records_total = records_total + records_count
      files_total  += 1

      # update documents information
      parsing_data['datasets'].append({
        'file'     : f,
        'documents': [],
        'filename' : filename,
        'shortname': os.path.basename(filename),
        'stats' : {
          'total'    : records_count,
          'parsed'   : 0,
          'missed'   : 0,
          'lines'    : 0
        }
      })

    log.info("[cyan]{}[/cyan] - found {} documents".format(filename, records_count))

  # report about the number of documents and files to parse
  log.info("Preparing to parse {} documents from {} files".format(records_total,
                                                    len(parsing_data['datasets'])))

  # update the number of documents
  parsing_data['stats']['total'] = records_total
  parsing_data['stats']['files'] = files_total

  return True

def check_parsing_spec_referenced_variables(section_name, section,
                                            parsing_keys, mapping_keys):
  """
  Validates that all referenced variables within a given section are defined
  either in the 'keys.parsing' or 'keys.mapping' sections

  Args:
      section_name (str): The name of the section being checked, used for logging purposes.
      section (any): The section data to be checked, which can be a dict, list, or str.
      parsing_keys (set): A set of keys defined in 'keys.parsing'.
      mapping_keys (set): A set of keys defined in 'keys.mapping'.

  Returns:
      bool: True if all referenced variables are defined, False otherwise.

  The function recursively checks nested structures within the section.
  It ignores variables of the form '{{_...}}' or '{{ _... }}' as they are considered safe.
  """
  safe_variable_pattern = re.compile(r'{{\s*_\[.*?\]\s*}}')

  if isinstance(section, dict):
    for key, items in section.items():
      if isinstance(items, dict):
        if not check_parsing_spec_referenced_variables(
               f'{section_name}.{key}', items, parsing_keys, mapping_keys):
          return False
      elif isinstance(items, list):
        for index, item in enumerate(items):
          if isinstance(item, dict):
            if not check_parsing_spec_referenced_variables(
                   f'{section_name}.{key}[{index}]', item, parsing_keys, mapping_keys):
              return False
          elif isinstance(item, str):
            variables = re.findall(r'{{(.*?)}}', item)
            for var in variables:
              if (not safe_variable_pattern.match(f'{{{{ {var} }}}}') and
                      var not in parsing_keys and var not in mapping_keys):
                log.error(f"Undefined variable '{var}' in '{section_name}.{key}[{index}]'")
                return False
      elif isinstance(items, str):
        variables = re.findall(r'{{(.*?)}}', items)
        for var in variables:
          if (not safe_variable_pattern.match(f'{{{{ {var} }}}}') and
                  var not in parsing_keys and var not in mapping_keys):
            log.error(f"Undefined variable '{var}' in '{section_name}.{key}'")
            return False
  elif isinstance(section, list):
    for index, item in enumerate(section):
      if isinstance(item, dict):
        if not check_parsing_spec_referenced_variables(
               f'{section_name}[{index}]', item, parsing_keys, mapping_keys):
          return False
      elif isinstance(item, str):
        variables = re.findall(r'{{(.*?)}}', item)
        for var in variables:
          if (not safe_variable_pattern.match(f'{{{{ {var} }}}}') and
                  var not in parsing_keys and var not in mapping_keys):
            log.error(f"Undefined variable '{var}' in '{section_name}[{index}]'")
            return False
  elif isinstance(section, str):
    variables = re.findall(r'{{(.*?)}}', section)
    for var in variables:
      if (not safe_variable_pattern.match(f'{{{{ {var} }}}}') and
              var not in parsing_keys and var not in mapping_keys):
        log.error(f"Undefined variable '{var}' in '{section_name}'")
        return False
  return True

def check_parsing_spec_key_values_consistency(section_name, section,
                                              key_to_check, valid_values, path=""):
  """
  Validates that the specified key within a section has values consistent with the allowed values.

  Args:
      section_name (str): The name of the section being checked, used for logging purposes.
      section (any): The section data to be checked, which can be a dict, list, or str.
      key_to_check (str): The specific key whose values need to be validated.
      valid_values (set): A set of allowed values for the specified key.
      path (str): The current path within the section being checked, used for logging purposes.

  Returns:
      bool: True if all values of the specified key are valid, False otherwise.

  The function recursively checks nested structures within the section.
  Logs an error with the specific path if an invalid value is found.
  """
  if isinstance(section, dict):
    for key, value in section.items():
      new_path = f"{path}.{key}" if path else key
      if key == key_to_check:
        if value not in valid_values:
          log.error(f"Invalid value '{value}' for key '{key}' in '{section_name}.{new_path}'")
          return False
      if isinstance(value, (dict, list)):
        if not check_parsing_spec_key_values_consistency(section_name, value,
                                                         key_to_check, valid_values, new_path):
          return False
  elif isinstance(section, list):
    for index, item in enumerate(section):
      new_path = f"{path}[{index}]"
      if isinstance(item, (dict, list)):
        if not check_parsing_spec_key_values_consistency(section_name, item,
                                                         key_to_check, valid_values, new_path):
          return False
  elif isinstance(section, str):
    variables = re.findall(r'{{(.*?)}}', section)
    for var in variables:
      if var not in valid_values:
        log.error(f"Undefined variable '{var}' in '{section_name}.{path}'")
        return False
  return True

def check_parsing_spec_target_template_circular_references(mapping, section_name):
  """
  Checks for circular references in template mappings within a specified section.

  Args:
    template_mapping (dict): The template mappings to be checked. Each key maps to a dictionary with a template.
      Example:

      .. code-block:: python

        {
          'key1': {'template': '{{key2}} ...'},
          'key2': {'template': '{{key3}} ...'}
        }

    section_name (str): The name of the section being checked, used for logging purposes.

  Returns:
    bool: True if no circular references are found, False if a circular reference is detected.

  Logs an error if a circular reference is detected, specifying the exact key and section.
  """
  circular_reference_found = False

  env = jinja2.Environment()

  for key, value in mapping.items():
    if 'template' in value:
      template = value['template']
      # parse the template
      ast = env.parse(template)
      # create a list of variables
      template_variables = meta.find_undeclared_variables(ast)

      if key in template_variables:
        log.error(f"Circular reference detected for key '{key}' in '{section_name}'")
        circular_reference_found = True

  return not circular_reference_found

def check_parsing_spec_source_target_circular_references(mapping, section_name):
  """
  Checks for circular references in key mappings within a specified section.

  Args:
    mapping (dict): The key mappings to be checked. Each key maps to a list of target dictionaries.

      Example:

      .. code-block:: python

        {
          'key1': [{'target': 'key2'}],
          'key2': [{'target': 'key3'}]
        }

    section_name (str): The name of the section being checked, used for logging purposes.

  Returns:
    bool: True if no circular references are found, False if a circular reference is detected.

  The function uses a depth-first search (DFS) approach to detect circular references by tracking visited keys.
  Logs an error if a circular reference is detected, specifying the exact key and section.
  """
  def find_references(key, visited):
    if key in visited:
      log.error(f"Circular reference detected for key '{key}' in '{section_name}'")
      return False
    visited.add(key)
    targets = mapping.get(key, [])
    for target in targets:
      if isinstance(target, dict) and 'target' in target:
        if not find_references(target['target'], visited):
          return False
    visited.remove(key)
    return True

  for key in mapping.keys():
    if not find_references(key, set()):
      return False
  return True

def check_parsing_spec_mapping_duplicate_variables(mapping):
  """
  Validates that no 'target' in mapping.source_targets is present as a key in mapping.target_template.

  Args:
    mapping (dict): The mapping to be validated. Expected to have 'source_targets' and 'target_template' keys.
      Example:

      .. code-block:: python

        {
          'source_targets': {
            'key1': [{'target': 'key2'}]
          },
          'target_template': {
            'key2': {'template': '...'}
          }
        }

  Returns:
    bool: True if the mapping is valid, False if a target is present as a key in target_template.

  Logs an error if an invalid mapping is detected.
  """
  source_targets = mapping.get('source_targets', {})
  target_template = mapping.get('target_template', {})

  # collect all targets in source_targets
  targets = set()
  for source, targets_list in source_targets.items():
    for target_dict in targets_list:
      if 'target' in target_dict:
        targets.add(target_dict['target'])

  # check if any target is present as a key in target_template
  invalid_targets = targets.intersection(target_template.keys())
  if invalid_targets:
    for invalid_target in invalid_targets:
      log.error(f"Invalid mapping: target '{invalid_target}' in 'source_targets' is also a key in 'target_template'")
    return False

  return True

def check_parsing_spec_required_structure(section, required_structure, section_name):
  """
  Validates that a section adheres to a specified required structure.

  Args:
      section (dict): The section to be checked.
      required_structure (dict): A dictionary representing the required structure.
          Keys represent required fields, and values specify the type or further nested structure.
          To check for a list of dictionaries, use [{}].
      section_name (str): The name of the section being checked, used for logging purposes.

  Returns:
      bool: True if the section adheres to the required structure, False otherwise.

  The function recursively checks nested structures, ensuring that each required key
  exists and has the correct type.
  Logs an error with the specific path if any required structure is missing or invalid.
  """
  if isinstance(section, dict):
    for key, value in section.items():
      new_path = f"{section_name}.{key}" if section_name else key
      if isinstance(value, dict):
        for req_key, req_value in required_structure.items():
          if req_key not in value:
            log.error(f"Missing required field '{req_key}' in '{new_path}'")
            return False
          if isinstance(req_value, dict):
            if not check_parsing_spec_required_structure(
                   value[req_key], req_value, f"{new_path}.{req_key}"):
              return False
          elif isinstance(req_value, list) and req_value == [{}]:
            # Check that each item in the list is a dictionary
            if not isinstance(value[req_key], list):
              log.error(f"Expected a list for '{new_path}.{req_key}'")
              return False
            for index, item in enumerate(value[req_key]):
              if not isinstance(item, dict):
                log.error(f"Invalid structure in '{new_path}.{req_key}[{index}]', expected a dictionary")
                return False
              if 'params' in item and not isinstance(item['params'], dict):
                log.error(f"Invalid structure for 'params' in '{new_path}.{req_key}[{index}]', expected a dictionary")
                return False
      else:
        log.error(f"Invalid structure in '{new_path}', expected a dictionary")
        return False
  else:
    log.error(f"Invalid structure in '{section_name}', expected a dictionary")
    return False
  return True

def check_parsing_spec_valid_plugins_recursive(plugin_group, section_path, section_content, plugins):
  """
  Recursively validates if the given section contains valid plugins.

  Args:
      section_name (str): The name and path of the section being checked, used for logging purposes.
      section (dict or list): The section data to be checked for valid plugins.
      plugins (obj): The loaded plugins.

  Returns:
      bool: True if all plugins are valid, False otherwise.

  The function recursively checks each plugin in the given section to ensure it exists
  in the provided plugins dictionary. Logs an error with the specific path if an unknown
  plugin is found.
  """
  if isinstance(section_content, dict):
    for key, value in section_content.items():
      new_section_path = f"{section_path}.{key}" if section_path else key
      if key == 'plugins':
        # Check plugins directly
        for plugin_call in value:
          plugin_category = list(plugin_call.keys())[0]
          plugin_name = plugin_call[plugin_category]
          plugin_id = "{}.{}.{}".format(plugin_group,plugin_category, plugin_name)
          if plugin_group not in plugins or (
            plugin_id   not in plugins[plugin_group]):
            log.error("Requesting to call an unknown plugin '{}' in section '{}'".format(plugin_id, new_section_path))
            return False
      elif isinstance(value, (dict, list)):
        if not check_parsing_spec_valid_plugins_recursive(plugin_group, new_section_path, value, plugins):
          return False
  elif isinstance(section_content, list):
    for index, item in enumerate(section_content):
      new_section_path = f"{section_path}[{index}]"
      if not check_parsing_spec_valid_plugins_recursive(plugin_group, new_section_path, item, plugins):
        return False
  return True

def check_parsing_spec_valid_plugin_group(sections_to_check, plugin_group, parsing_spec_path):
  """
  Validates if the given sections contain valid plugins for the specified plugin group.

  Args:
      sections_to_check (list): List of section names to be checked.
      plugin_group (str): The name of the plugin group.
      parsing_spec_path (dict): The dictionary representing the path in the specification to be checked.

  Returns:
      bool: True if all plugins are valid, False otherwise.

  The function checks each plugin in the given sections and plugin group to ensure they
  exist in the provided plugins dictionary.
  Logs an error with the specific path if an unknown plugin is found.
  """
  # Try to load plugins
  loader = get_plugins_loader(plugin_group)
  # Exit early if we failed to get the interface of the loader
  if loader is None:
    log.error(f"Failed to load plugins for plugin group '{plugin_group}'")
    return False

  # Get the nested dictionary of plugins
  plugins = loader.plugins

  # Check in the given sections
  for section_name in sections_to_check:
    if section_name in parsing_spec_path:
      section_path = f"{plugin_group}.{section_name}"
      if not check_parsing_spec_valid_plugins_recursive(plugin_group, section_path, parsing_spec_path[section_name], plugins):
        return False

  return True

def check_parsing_spec_version(file_spec_version, engine_version):
    file_version = semver.VersionInfo.parse(file_spec_version)
    engine_version = semver.VersionInfo.parse(engine_version)
    # Compare major versions
    if file_version.major == engine_version.major:
        return True
    return False

def check_parsing_spec(parsing_spec):
  """
  Validates the structure and referenced variables of a Parscival specification.

  Args:
      parsing_spec (dict): The specification to be validated.

  Returns:
      bool: True if the specification is valid, False otherwise.

  The function performs the following checks:
      - Ensures engine and file specification are compatible.
      - Ensures required top-level keys are present.
      - Ensures 'keys' contains both 'parsing' and 'mapping'.
      - Validates that keys in the first child of 'parsing' are defined in 'keys.parsing'.
      - Ensures target keys in 'mapping.source_targets' are defined in 'keys.mapping'.
      - Ensures variables in 'mapping.target_template' are defined in 'keys.parsing' or 'keys.mapping'.
      - Ensures variables in the 'curating' section are defined in 'keys.parsing' or 'keys.mapping'.
      - Ensures 'type' consistency in 'keys.parsing' and 'keys.mapping'
      - Ensures 'qualifier' consistency in 'keys.parsing' and 'keys.mapping'
      - Ensures no circular references in 'mapping.source_targets'
      - Ensures required structure in 'storing'
      - Ensures required 'mapping', 'curating' plugins are available
  """
  file_spec_version = parsing_spec.get('parscival_spec_version', '1.0.0')
  if not check_parsing_spec_version(file_spec_version, engine_version):
    log.error(f"The specification v{file_spec_version} is not compatible with the Parscival Engine v{engine_version}")
    return False

  required_top_level_keys = ['parscival_spec_version','description',
                             'source', 'schema', 'format', 'version', 'author',
                             'keys', 'parsing', 'mapping', 'storing']
  required_keys_in_keys = ['parsing', 'mapping']

  # check for required top-level keys
  for key in required_top_level_keys:
    if key not in parsing_spec:
      log.error(f"Missing top-level key: '{key}'")
      return False

  # check for required keys under 'keys'
  for key in required_keys_in_keys:
    if key not in parsing_spec['keys']:
      log.error(f"Missing key under 'keys': '{key}'")
      return False

  # ensure keys in the first child of 'parsing' are defined in 'keys.parsing'
  parsing_keys = set(parsing_spec['keys']['parsing'].keys())

  first_child_key = next(iter(parsing_spec['parsing'].keys()))
  first_child = parsing_spec['parsing'][first_child_key]

  for key, value in first_child.get('keys', {}).items():
    if key not in parsing_keys:
      log.error(f"Non declared key in 'parsing.{first_child_key}.keys': '{key}'")
      return False

  # ensure keys in 'mapping.source_targets' targets are defined in 'keys.mapping'
  mapping_keys = set(parsing_spec['keys']['mapping'].keys())
  for source, targets in parsing_spec['mapping'].get('source_targets', {}).items():
    for target in targets:
      if target['target'] not in mapping_keys:
        log.error(f"Undefined target key in 'mapping.source_targets': '{target['target']}'")
        return False

  # ensure keys in 'mapping.target_template' are defined in 'keys.mapping'
  for target, sources in parsing_spec['mapping'].get('target_template', {}).items():
    if target not in mapping_keys:
      log.error(f"Undefined target key in 'mapping.target_template': '{target}'")
      return False

    # ensure variables referenced in source are defined in 'keys.parsing' or 'keys.mapping'
    for source in sources:
      if not check_parsing_spec_referenced_variables(
             f'mapping.target_template.{target}.source', source, parsing_keys, mapping_keys):
        return False

  # ensure variables in 'curating' are defined in 'keys.parsing' or 'keys.mapping'
  curating_sections = parsing_spec.get('curating', {})
  if not check_parsing_spec_referenced_variables(
        'curating', curating_sections, parsing_keys, mapping_keys):
    return False

  # check key types consistency in 'keys.parsing' and 'keys.mapping'
  keys_section = parsing_spec.get('keys', {})
  keys_valid_values = {'string', 'integer', 'date'}
  key_to_check = 'type'
  for section_name in ['parsing', 'mapping']:
    if section_name in keys_section:
      if not check_parsing_spec_key_values_consistency(
             f"keys.{section_name}", keys_section[section_name], key_to_check, keys_valid_values):
        return False

  # check qualifier consistency in 'keys.parsing' and 'keys.mapping'
  qualifier_valid_values = {'optional', 'required', 'repeated'}
  key_to_check = 'qualifier'
  for section_name in ['parsing', 'mapping']:
    if section_name in keys_section:
      if not check_parsing_spec_key_values_consistency(
             f"keys.{section_name}", keys_section[section_name], key_to_check, qualifier_valid_values):
        return False

  # check for circular references in 'mapping.target_template'
  if 'mapping' in parsing_spec and 'target_template' in parsing_spec['mapping']:
    if not check_parsing_spec_target_template_circular_references(
           parsing_spec['mapping']['target_template'], 'mapping.target_template'):
      return False

  # check there is not duplicated mappings beetwen mapping.source_targets and
  # mapping.target_template
  if not check_parsing_spec_mapping_duplicate_variables(parsing_spec['mapping']):
    return False

  # check required structure in 'storing'
  required_structure = {
    'plugins': [{}]
  }
  if 'storing' in parsing_spec:
    if not check_parsing_spec_required_structure(parsing_spec['storing'], required_structure, 'storing'):
      return False

  # check mapping plugins
  plugin_group = 'mapping'
  sections_to_check = ['source_targets', 'target_template']
  if not check_parsing_spec_valid_plugin_group(sections_to_check, plugin_group,
                                               parsing_spec.get('mapping')):
    return False

  # check curating plugins
  plugin_group = 'curating'
  sections_to_check = ['before_ingesting',   'before_parsing',
                       'before_mapping',     'before_storing',
                       'before_finishing',
                       'after_initializing', 'after_ingesting',
                       'after_parsing',      'after_mapping',
                       'after_storing']
  if not check_parsing_spec_valid_plugin_group(sections_to_check, plugin_group,
                                               parsing_spec.get('curating')):
    return False

  return True

def get_parsing_spec(file_parsing_spec):
  """Get the parscival specification including grammar
  """
  parsing_spec  = {
    'spec' : { },
    'misc' : { },
    'category': '',
    'type': '',
    'valid': True
  }

  try:
    parsing_spec['spec'] = yaml.safe_load(file_parsing_spec)
    parsing_spec['file'] = file_parsing_spec

    log.info(f"Checking specification in [yellow]{Path(file_parsing_spec.name).name}[/yellow]...")
    if not check_parsing_spec(parsing_spec['spec']):
      raise ValueError("Specification is invalid")
    log.info(f"Specification is valid")

    parser_category = next(iter(parsing_spec['spec']['parsing']))

    # shorthand for cateroty and the type of parser
    parsing_spec['category'] = parser_category
    parsing_spec['type']     = parsing_spec['spec']['parsing'].get(parser_category)['type']

  except yaml.YAMLError as e:
    log.error("Error while parsing spec {}".format(str(e.problem_mark).strip()))
    parsing_spec['valid'] = False
  except Exception as e:
    log.error("Error loading the parscival specification from '{}': {} - {}".format(
    Path(file_parsing_spec.name).name, type(e).__name__, e))
    parsing_spec['valid'] = False

  return parsing_spec

def parse_dataset(parsing_spec, dataset_info, main_task, main_progress):
  """parse files

  Args:

  Returns:
    Boolean: True if the parsing was successful, False otherwise
  """
  filename_short = dataset_info['shortname']

  if dataset_info['stats']['total'] <= 0:
    log.warning("[cyan]{}[/cyan] - no documents found".format(filename_short))
    return False

  log.info("[cyan]{}[/cyan] - parsing...".format(filename_short))

  # show the progress of the current file parsing
  local_task = main_progress.add_task(
               "[green]Parsing {:<20s}".format(filename_short),
               total=dataset_info['stats']['total'])

  # parse document by document
  document_info  = {
    'buffer'  : "",
    'line': {
      'start': 0
    },
    'tree' : None
  }

  document_info['buffer'] = ""
  document_parsed_count = 0
  dataset_line_count = 0
  parser = parsing_spec['parser']

  mm = mmap.mmap(dataset_info['file'].fileno(), 0, access=mmap.ACCESS_READ)
  with contextlib.closing(mm) as dataset:
    for line in iter(dataset.readline, b""):
      # as mmap file is open in read binary (r+b) mode we need to
      # decode it as UTF-8 to use match() and parse()
      line = line.decode('utf-8')

      # increment the number of lines processed
      dataset_line_count += 1

      # for suppress(Exception):
      # @see https://stackoverflow.com/a/15566001/2042871

      # START
      try:
        if parser.can_parse(parsing_spec,
                            dataset_info,
                            document_info,
                            line):
          # test if we have a document buffer to process
          if document_info['buffer']:
            if parser.process(parsing_spec,
                              dataset_info,
                              document_info):
              document_parsed_count += 1


            main_progress.update(main_task, advance=1)
            main_progress.update(local_task, advance=1)

          # reinitialize the document buffer
          document_info['buffer'] = parser.buffer_restart(
                                           parsing_spec,
                                           dataset_info,
                                           document_info,
                                           line)
          document_info['line']['start'] = dataset_line_count
          continue

      except ParseError:
        pass

      except Exception as e:
        log.error(e)
        return False

      # MEMBER OR END
      document_info['buffer'] += line

    # try to parse the last document
    # this is because above documents are only parsed whenever
    # a new document is found
    if document_info['buffer']:
      if parser.process(parsing_spec,
                        dataset_info,
                        document_info):
        # increment only if at least 1 well formed document was found
        if len(dataset_info['documents']):
          document_parsed_count += 1

      main_progress.update(main_task, advance=1)
      main_progress.update(local_task, advance=1)

  # update the number of the documents found
  dataset_info['stats']['parsed'] = document_parsed_count

  # update the number of lines scanned
  dataset_info['stats']['lines'] = dataset_line_count

  # document with errors
  document_error_count  = 0

  # documents parsed
  log.info("[cyan]{}[/cyan] - {} of {} documents were parsed".format(
    dataset_info['filename'],
    dataset_info['stats']['parsed'],
    dataset_info['stats']['total']
  ))

  # documents missed
  dataset_info['stats']['missed'] = (
    dataset_info['stats']['total'] -
    (dataset_info['stats']['parsed'] + document_error_count))

  # if we found less documents than expected
  if dataset_info['stats']['missed'] > 0:
    # update progress to reflect the number of missed documents
    main_progress.update(main_task, advance=dataset_info['stats']['missed'])
    main_progress.update(local_task, advance=dataset_info['stats']['missed'])
    log.warning("[cyan]{}[/cyan] - {} malformed documents were missing".format(
      dataset_info['filename'], dataset_info['stats']['missed']
    ))

  # lines scanned
  log.info("[cyan]{}[/cyan] - {} lines scanned".format(dataset_info['filename'],
                                                       dataset_info['stats']['lines']))

  return True

def get_plugins_loader(plugin_group):
  """get the pluginlib interface to import and access plugins of a targeted type

  Args:
    plugin_group(str): Retrieve plugins of a group ('storing', 'mapping', ...)

  Returns:
    Class: Interface for importing and accessing plugins
  """
  # get the plugin loader
  loader = pluginlib.PluginLoader()

  # return early if the group is already loaded
  if loader is not None and plugin_group in loader.plugins:
    return loader

  try:
    # get the semicolon delimited list of paths from environment
    plugins_paths = os.getenv('PARSCIVAL_PLUGINS_PATHS')

    # create a list of paths
    if plugins_paths is not None:
      plugins_paths = plugins_paths.split(';')
    else:
      plugins_paths = []

    # compute a fallback path relative to project
    plugins_fallback_path = str(Path.joinpath(
                              Path(__file__).parent.parent.relative_to
                              (Path(__file__).parent.parent.parent),
                              'parscival_plugins'))
    plugins_paths.insert(0, plugins_fallback_path)

    # add some extra paths from site-packages directories
    sitepackages = site.getsitepackages() + [site.getusersitepackages()]
    for path in sitepackages:
      plugins_paths.insert(0, str(Path.joinpath(Path(path), 'parscival_plugins')))

    # append the plugin type to each of paths
    plugins_type_paths = [ os.path.join(p, plugin_group) for p in plugins_paths ]
    # remove non-existing paths
    plugins_type_paths = [ p for p in plugins_type_paths if os.path.isdir(p) ]

    # test if there is at least one valid path
    if not plugins_type_paths:
      log.error("There are not valid paths pointed out by '%s'",
                'PARSCIVAL_PLUGINS_PATHS')
      return None

    # recursively load plugins from paths
    loader = pluginlib.PluginLoader(paths = plugins_type_paths)

  except pluginlib.PluginImportError as e:
      if e.friendly:
        log.error("{}".format(e))
      else:
        log.error("Unexpected error loading %s plugins", plugin_group)
      return None

  # and return loader
  return loader

def data_binary_search_id(data_list, target_id):
  left, right = 0, len(data_list) - 1
  result = []

  # perform binary search to find one occurrence of the target id
  while left <= right:
    mid = (left + right) // 2
    mid_id = data_list[mid]['id']

    if mid_id == target_id:
      # find all occurrences of the target id
      result.append(data_list[mid])

      # search to the left of mid
      l = mid - 1
      while l >= 0 and data_list[l]['id'] == target_id:
        result.append(data_list[l])
        l -= 1

      # search to the right of mid
      r = mid + 1
      while r < len(data_list) and data_list[r]['id'] == target_id:
        result.append(data_list[r])
        r += 1

      return result

    elif mid_id < target_id:
      left = mid + 1
    else:
      right = mid - 1

  # return empty list if the id is not found
  return result

def group_mapping_nodes(data):
  """
  Groups mapping items by 'id', 'rank', and 'parserank', and includes
  additional metadata in the output.

  Args:
    data (dict): A dictionary where keys are mapping key names and values are lists
      of dictionaries containing the following keys:
      - 'id' (int): The identifier for the group.
      - 'rank' (int): The rank within the group.
      - 'parserank' (int): The parserank within the group.
      - 'data' (str): The data associated with the entry.

  Returns:
    list: A list of dictionaries where each dictionary represents a grouped entry.

    Each dictionary contains:
      - '_id' (int): The identifier for the group.
      - '_rank' (int): The rank within the group.
      - '_parserank' (int): The additional ranking metric.
      - [source_name] (str or list): The data associated with the entry,
        either as a single string if there's one entry or as a list of strings
        if there are multiple entries.

  Example:
    .. code-block:: python

      data = {
          'OtherSourceDate': [
              {'file': 'file1.html', 'id': 1, 'rank': 2, 'parserank': 0, 'data': '2020-01-01'},
              {'file': 'file2.html', 'id': 1, 'rank': 2, 'parserank': 1, 'data': '2020-01-02'}
          ],
          'OtherSourceName': [
              {'file': 'file3.html', 'id': 1, 'rank': 2, 'parserank': 0, 'data': 'Source A'},
              {'file': 'file4.html', 'id': 1, 'rank': 2, 'parserank': 1, 'data': 'Source B'}
          ]
      }

      grouped_data = group_sources(data)
      # grouped_data will be:
      # [
      #   {'_id': 1, '_rank': 2, '_parserank': 0, 'OtherSourceDate': '2020-01-01', 'OtherSourceName': 'Source A'},
      #   {'_id': 1, '_rank': 2, '_parserank': 1, 'OtherSourceDate': '2020-01-02', 'OtherSourceName': 'Source B'}
      # ]
  """
   # Create a dictionary to store entries by (id) with rank = 0 and parserank = 0
  base_dict = {}
  grouped_dict = {}

  # First pass: Group items by (id) where rank and parserank are both 0
  for source_name, items in data.items():
      for item in items:
          if item['rank'] == 0 and item['parserank'] == 0:
              key = item['id']
              if key not in base_dict:
                  base_dict[key] = {'_id': item['id'], '_rank': 0, '_parserank': 0}
              if source_name not in base_dict[key]:
                  base_dict[key][source_name] = []
              base_dict[key][source_name].append(item['data'])

  # Second pass: Loop over items where rank > 0, clone the base item, update the data and the rank, and add the new item
  for source_name, items in data.items():
      for item in items:
          if item['rank'] > 0:
              base_key = item['id']
              new_key = (item['id'], item['rank'], 0)

              if base_key in base_dict:
                  if new_key not in grouped_dict:
                      grouped_dict[new_key] = base_dict[base_key].copy()
                  grouped_dict[new_key]['_rank'] = item['rank']
                  if source_name not in grouped_dict[new_key]:
                      grouped_dict[new_key][source_name] = []
                  grouped_dict[new_key][source_name] = [item['data']]
              else:
                  # If there is no base item, initialize new entry
                  grouped_dict[new_key] = {
                      '_id': item['id'],
                      '_rank': item['rank'],
                      '_parserank': 0,
                      source_name: [item['data']]
                  }

  # Third pass: Group items by (id, rank) where parserank is 0
  for source_name, items in data.items():
      for item in items:
          if item['parserank'] == 0:
              key = (item['id'], item['rank'], 0)
              if key not in grouped_dict:
                  grouped_dict[key] = {'_id': item['id'], '_rank': item['rank'], '_parserank': 0}
              if source_name not in grouped_dict[key]:
                  grouped_dict[key][source_name] = []
              grouped_dict[key][source_name] = [item['data']]

  # Fourth pass: Loop over items where rank > 0 and parserank > 0, clone the base item, update the data and the parserank, and add the new item
  for source_name, items in data.items():
      for item in items:
          if item['rank'] > 0 and item['parserank'] > 0:
              base_key = (item['id'], item['rank'], 0)
              new_key = (item['id'], item['rank'], item['parserank'])

              if base_key in grouped_dict:
                  grouped_dict[new_key] = grouped_dict[base_key].copy()
                  grouped_dict[new_key]['_parserank'] = item['parserank']
                  if source_name not in grouped_dict[new_key]:
                      grouped_dict[new_key][source_name] = []
                  grouped_dict[new_key][source_name] = [item['data']]
              else:
                  # If there is no base item, initialize new entry
                  grouped_dict[new_key] = {
                      '_id': item['id'],
                      '_rank': item['rank'],
                      '_parserank': item['parserank'],
                      source_name: [item['data']]
                  }

  # Create the final grouped list directly from grouped_dict
  grouped_list = []
  for key, sources in grouped_dict.items():
      entry = {
          '_id': sources['_id'],
          '_rank': sources['_rank'],
          '_parserank': sources['_parserank']
      }
      for source_name, data_list in sources.items():
          if source_name not in ['_id', '_rank', '_parserank']:
              if len(data_list) == 1:
                  entry[source_name] = data_list[0]
              else:
                  entry[source_name] = data_list
      grouped_list.append(entry)

  return grouped_list



def map_parsed_data(parsing_spec, parsing_data, main_task, main_progress):
  """map an already parsed dataset according to a spec

  Args:

  Returns:
    Boolean: True if the mapping is successful, False otherwise
  """
  # try to load plugins
  plugin_category = 'mapping'

  # try to load plugins
  loader  = get_plugins_loader(plugin_category)

  # exit early if we failed to get the interface of the loader
  if loader is None: return False

  # get the nested dictionary of plugins
  plugins = loader.plugins

  # first pass: 'source_targets'
  # loop over datasets and documents
  file_id = 0
  document_id = 0
  for dataset_info in parsing_data['datasets']:
    main_progress.update(main_task, advance=1)
    # loop over parsed documents
    for document in dataset_info['documents']:
      document_key_rank_id = {}
      # 'source_targets': loop over key-values
      for key, value in document:
        # loop over key mappings
        # TODO(martinec) lint check if key exists before outer loops
        for mapping in parsing_spec['spec']['mapping']['source_targets'][key]:
          # key to create
          map_key = mapping['target']

          # check if the rank key is defined by the current mapping key
          # or if it depends on a key referenced by the 'rank' attribute
          rank_key = mapping['rank'] if 'rank' in mapping else map_key

          # check if we need to initialize the rank id counter for this key
          if not rank_key in document_key_rank_id:
            document_key_rank_id[rank_key] = 0
          # increase the rank id counter for this key
          elif map_key == rank_key:
            document_key_rank_id[rank_key] = document_key_rank_id[rank_key] + 1

          # get the current rank id
          rank_id = document_key_rank_id[rank_key]

          # check if we need to initialize the mappings for this key
          if not map_key in parsing_data['mappings']:
            parsing_data['mappings'][map_key] = []

          # create a list of nodes with a default node row
          nodes = [
            {
              'file'       : dataset_info['shortname'],
              'id'         : document_id,
              'rank'       : rank_id,
              'parserank'  : 0,
              'data'       : value
            }
          ]

          # call requested plugins
          plugin_group = 'mapping'
          if 'plugins' in mapping and mapping['plugins'] is not None:
            for plugin_call in mapping['plugins']:
              plugin_category  = list(plugin_call.keys())[0]
              plugin_name   = list(plugin_call.values())[0]
              plugin_id = "{}.{}.{}".format(plugin_group,plugin_category,plugin_name)
              plugin = plugins[plugin_group][plugin_id]
              # call the process function of each plugin
              log.debug("Calling plugin '[green]{}[/green]' for key '{}' in " \
                        "document {}".format(plugin_id, key, document_id))
              params = plugin_call['params'] if 'params' in plugin_call and plugin_call['params'] else {}
              if not 'enabled' in params or params['enabled'] == True:
                if not plugin.process(parsing_spec, parsing_data, nodes, **params):
                  log.warn("Plugin '{}' finished with issues for key '{}' and nodes: {}".format(
                            plugin_id, key, nodes))
              else:
                log.debug("Ignoring plugin '[green]{}[/green]'".format(plugin_id))

          # filter nodes to include only those where 'data' is not None
          filtered_nodes = [node for node in nodes if node['data'] is not None]

          # add the mapped nodes for the current key
          parsing_data['mappings'][map_key].extend(filtered_nodes)

      # increase the document_id
      document_id = document_id + 1

    # increase file id
    file_id = file_id + 1

  # return early if not 'target_template' are needed
  if 'target_template' not in parsing_spec['spec']['mapping']:
    return True

  target_template = parsing_spec['spec']['mapping']['target_template']
  env = jinja2.Environment()

  # check if the required key mappings exists
  for map_key, mapping in target_template.items():
    # check if the target_template can be resolved using the mapping keys
    ast = env.parse(mapping['template'])
    template_variables = meta.find_undeclared_variables(ast)

    # loop over each variable and check if there is a mapping key for it
    for template_variable in template_variables:
      if template_variable not in parsing_data['mappings']:
        log.warn("target_template requieres the mapping '{}'", template_variable)
        return False

  # second pass: 'target_template'
  # loop over datasets and documents
  file_id = 0
  document_id = 0
  for dataset_info in parsing_data['datasets']:
    # loop over parsed documents
    for document in dataset_info['documents']:
      document_key_rank_id = {}
      for map_key, mapping in target_template.items():

        # check if the rank key is defined by the current mapping key
        # or if it depends on a key referenced by the 'rank' attribute
        rank_key = mapping['rank'] if 'rank' in mapping else map_key

        # check if we need to initialize the rank id counter for this key
        if not rank_key in document_key_rank_id:
          document_key_rank_id[rank_key] = 0
        # increase the rank id counter for this key
        elif map_key == rank_key:
          document_key_rank_id[rank_key] = document_key_rank_id[rank_key] + 1

        # get the current rank id
        rank_id = document_key_rank_id[rank_key]

        # check if we need to initialize the mappings for this key
        if not map_key in parsing_data['mappings']:
          parsing_data['mappings'][map_key] = []

        # get the template string
        template_string = mapping['template']

        # get the template variables
        ast = env.parse(template_string)
        template_variables = meta.find_undeclared_variables(ast)

        try:
          # prepare a template for the expected output value
          template_context_nodes = {}
          template = jinja2.Template(template_string)

          # we loop over the keys needed to resolve the context
          for key_name in template_variables:
            # find the mapped data for a document key
            document_key_nodes = data_binary_search_id(
                                           parsing_data['mappings'][key_name],
                                           document_id)
            for document_key_node in document_key_nodes:
              if not key_name in template_context_nodes:
                template_context_nodes[key_name] = [ document_key_node ]
              else:
                template_context_nodes[key_name].append(document_key_node)

          # group template_context_nodes items by 'id', 'rank', and 'parserank',
          group_template_context = group_mapping_nodes(template_context_nodes)

          # default settings if the template is not using variables
          if not group_template_context:
            group_template_context.append({
              '_id'         : document_id,
              '_rank'       : rank_id,
              '_parserank'  : 0,
            })

          for template_context in group_template_context:
            resolved_template =  template.render(template_context)

            # if the expand template is empty, we do not need to add a new node
            if not resolved_template:
              continue

            # create a list of nodes with a default node row
            nodes = [
              {
                'file'       : dataset_info['shortname'],
                'id'         : template_context['_id'],
                'rank'       : template_context['_rank'],
                'parserank'  : template_context['_parserank'],
                'data'       : resolved_template
              }
            ]

            # call requested plugins
            plugin_group = 'mapping'
            if 'plugins' in mapping and mapping['plugins'] is not None:
              for plugin_call in mapping['plugins']:
                plugin_category  = list(plugin_call.keys())[0]
                plugin_name   = list(plugin_call.values())[0]
                plugin_id = "{}.{}.{}".format(plugin_group,plugin_category,plugin_name)
                plugin = plugins[plugin_group][plugin_id]
                # call the process function of each plugin
                log.debug("Calling plugin '[green]{}[/green]' for key '{}' in " \
                          "document {}".format(plugin_id, key, document_id))
                params = plugin_call['params'] if 'params' in plugin_call and plugin_call['params'] else {}
                if not 'enabled' in params or params['enabled'] == True:
                  if not plugin.process(parsing_spec, parsing_data, nodes, **params):
                    log.warn("Plugin '{}' finished with issues for key '{}' and nodes: {}".format(
                              plugin_id, key, nodes))
                else:
                  log.debug("Ignoring plugin '[green]{}[/green]'".format(plugin_id))

            # filter nodes to include only those where 'data' is not None
            filtered_nodes = [node for node in nodes if node['data'] is not None]

            # add the mapped nodes for the current key
            parsing_data['mappings'][map_key].extend(filtered_nodes)

        except Exception as e:
          log.warning("Unknown error while resolving '{}' template: {} - {}".format(
                            map_key, type(e).__name__, e.__doc__))
          return False

      # increase the document_id
      document_id = document_id + 1

    # increase file id
    file_id = file_id + 1

  return True

def curate_data(process_stage, parsing_spec, parsing_data, main_task, main_progress):
  """curate data according to a spec

  Args:

  Returns:
    Boolean: True if the process is successful, False otherwise
  """

  # check if there are curating tasks to be performed
  if not 'curating' in parsing_spec['spec']:
    return True

  # check if there are curating tasks for this stage
  if not process_stage in parsing_spec['spec']['curating'] or \
    parsing_spec['spec']['curating'][process_stage] is None:
    return True

  # try to load plugins
  plugin_group = 'curating'
  loader  = get_plugins_loader(plugin_group)
  # exit early if we failed to get the interface of the loader
  if loader is None: return False

  # get the nested dictionary of plugins
  plugins = loader.plugins

  # check if there are plugings to call for this processing stage
  if not ('plugins' in parsing_spec['spec'][plugin_group][process_stage] and
      parsing_spec['spec'][plugin_group][process_stage]['plugins'] is not None):
    return False

  # now loop calling the requested plugins
  for plugin_call in parsing_spec['spec'][plugin_group][process_stage]['plugins']:
    main_progress.update(main_task, advance=1)
    # get the group and name of the requested plugin
    plugin_type   = list(plugin_call.keys())[0]
    plugin_name   = list(plugin_call.values())[0]
    plugin_id = "{}.{}.{}".format(plugin_group,plugin_type,plugin_name)

    if not plugin_id in plugins[plugin_group]:
      log.error("Plugin '[green]{}[/green]' not found".format(plugin_id))
      return False

    # get the request plugin
    plugin = plugins[plugin_group][plugin_id]

    # call the process function of this plugin
    log.debug("Calling plugin '[green]{}[/green]'".format(plugin_id))
    params = plugin_call['params'] if 'params' in plugin_call and plugin_call['params'] else {}
    if not 'enabled' in params or params['enabled'] == True:
      if plugin.process(parsing_spec, parsing_data, **params):
        log.debug("The execution of '{}' was successful".format(plugin_id))
      else:
        log.error("Plugin '{}' finished with errors".format(plugin_id))
        return False
    else:
      log.debug("Ignoring plugin '[green]{}[/green]'".format(plugin_id))

  return True

def store_parsed_data(parsing_spec,
                          parsing_data,
                          output_info,
                          main_task,
                          main_progress):
  """store parsed data

  Args:

  Returns:
    Boolean: True if the store is successful, False otherwise
  """
  try:
    # try to load plugins
    plugin_group = 'storing'
    loader  = get_plugins_loader(plugin_group)

    # exit early if we failed to get the interface of the loader
    if loader is None: return False

    # get the nested dictionary of plugins
    plugins = loader.plugins

    # first loop to check if the requested plugins are available
    store_type = output_info['type']
    for plugin_call in parsing_spec['spec'][plugin_group][store_type]['plugins']:
      plugin_category  = list(plugin_call.keys())[0]
      plugin_name   = list(plugin_call.values())[0]
      plugin_id = "{}.{}.{}".format(plugin_group,plugin_category,plugin_name)

      # test if plugin exists
      if plugin_group not in plugins or plugin_id not in plugins[plugin_group]:
        log.error("Calling undefined plugin '{}' while processing output of type '{}'".format(
                  plugin_id, store_type))
        return False

    # now we call each plugin following the declaration order
    log.info("Processing output of type '[green]{}[/green]'".format(store_type))
    for plugin_call in parsing_spec['spec'][plugin_group][store_type]['plugins']:
      main_progress.update(main_task, advance=1)
      plugin_category  = list(plugin_call.keys())[0]
      plugin_name   = list(plugin_call.values())[0]
      plugin_id = "{}.{}.{}".format(plugin_group,plugin_category,plugin_name)
      plugin = plugins[plugin_group][plugin_id]
      params = plugin_call['params'] if 'params' in plugin_call and plugin_call['params'] else {}
      if not 'enabled' in params or params['enabled'] == True:
        # call the process function of each plugin
        log.debug("Calling plugin '[green]{}[/green]'".format(plugin_id))
        if plugin.process(parsing_spec, parsing_data, output_info, **params):
          log.debug("The execution of '{}' was successful".format(plugin_id))
        else:
          log.error("Plugin '{}' finished with errors".format(plugin_id))
          return False
      else:
        log.debug("Ignoring plugin '[green]{}[/green]'".format(plugin_id))

  except pluginlib.PluginImportError as e:
      if e.friendly:
        log.error("{}".format(e))
      else:
        log.error("Unexpected error loading %s plugins", plugin_group)
      return False

  return True

def load_parsing_plugin(parsing_spec):
  # Load parsing plugins
  plugin_group = 'parsing'
  try:
    loader  = get_plugins_loader(plugin_group)

    # exit early if we failed to get the interface of the loader
    if loader is None: return False

    # get the nested dictionary of plugins
    plugins = loader.plugins

  except pluginlib.PluginImportError as e:
      if e.friendly:
        log.error("{}".format(e))
      else:
        log.error("Unexpected error loading %s plugins", plugin_group)
      return False

  parser_category = parsing_spec['category']
  parser_type = parsing_spec['type']
  plugin_id = "{}.{}.{}".format(plugin_group,parser_category,parser_type)

  # test if parsing plugin exists
  if plugin_group not in plugins or plugin_id not in plugins[plugin_group]:
    log.error("Requesting to use an unknown parsing plugin '{}'".format(
              plugin_id))
    return False

  # get the requested parser plugin
  parsing_spec['parser'] = plugins[plugin_group][plugin_id]

  # call the parser initialization routine
  log.info("Parsing plugin '{}' - Initializing...".format(plugin_id))
  if not parsing_spec['parser'].init(parsing_spec):
    log.error("Parsing plugin '{}' - Initialization error".format(
              plugin_id))
    return False
  log.info("Parsing plugin '{}' - Initialization done!".format(plugin_id))

  return True

def process_datasets(file_parsing_spec, file_output, file_datasets):
  """Parscival parse files

  Args:

  Returns:
    Boolean: True if data was parsed, False otherwise
  """
  # initial dictionary to seed the hdf5 parsing_data
  parsing_data_init_dict  = {
    'files' : file_datasets,
    'datasets' : [],
    'mappings' :  {},
    'transient' : {
      'files': [],
      'directories': []
    },
    'stats' : {
      'total'    : 0,
      'parsed'    : 0,
      'missed'   : 0,
      'lines'    : 0,
      'files'    : 0
    },
    'status': {
      'processed' : False
    }
  }

  # first get the specification
  parsing_spec = get_parsing_spec(file_parsing_spec)
  if parsing_spec['valid'] == False or not 'spec' in parsing_spec:
    log.critical("The parscival specification is not valid")
    return parsing_data_init_dict

  # check the type of the output to create
  # /path/to/foo.bar.zaz
  # foo
  output_name  = file_output.with_suffix('').stem
  # bar.zaz
  output_extension = file_output.name[len(output_name)+1:]

  # keep track about the requested output
  output_info  = {
    'type' : None,
    'file': file_output
  }

  # by default we need to create a hdf5
  parsing_data_output_file = str(Path.joinpath(file_output.parent, output_name + '.hdf5'))
  log.info("Storing parsing data on [yellow]{}[/yellow]".format(parsing_data_output_file))

  # only .hdf5 and spec tranforms format types are valid
  if output_extension != 'hdf5':
    if not 'storing' in parsing_spec['spec']:
      log.critical("No 'storing' key found on the parscival specification")
      return parsing_data_init_dict

    # eg. cortext.json or cortext.db
    output_info['type'] = output_extension
    if not output_extension in parsing_spec['spec']['storing']:
      log.critical("A valid output type is required to continue")
      log.critical("Requested output type: [yellow].{}[/yellow]"
                   .format(output_extension))
      log.critical("The known output types are: [yellow][.hdf5; .{}][/yellow]"
                   .format('; .'.join(parsing_spec['spec']['storing'])))
      return parsing_data_init_dict

  # ensure to have an empty output file
  open(parsing_data_output_file, 'w').close()

  # initialize a dictionary with a single hdf5 file archive backend
  parsing_data = klepto.archives.hdf_archive(
                  parsing_data_output_file,
                  dict = parsing_data_init_dict,
                  cached = True,
                  meta = True)

  # only continues if we have a valid specification
  if not parsing_spec['valid']:
    log.critical("A valid specification is required to continue")
    return parsing_data

  # visualize progress on the console
  with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    TimeRemainingColumn(),
    TimeElapsedColumn(),
    console=console,
    transient=True,
  ) as progress:
    # before_ingesting: curate raw input data according to the spec
    if 'before_ingesting' in parsing_spec['spec']['curating']:
      log.info("[green]<Curating>[/green] raw input data... ([yellow]before_ingesting[/yellow])")
      curating_before_ingesting_mapping_task = progress.add_task("[green]Curating raw input data",
                              total=len(parsing_spec['spec']['curating']['before_ingesting']))
      if not curate_data('before_ingesting', parsing_spec, parsing_data, curating_before_ingesting_mapping_task, progress):
        log.error("Unexpected error curating raw input data")
        return parsing_data
      progress.update(curating_before_ingesting_mapping_task,
                      advance=len(parsing_spec['spec']['curating']['before_ingesting']))

    # then get information about the datasets to process
    if not load_datasets_info(parsing_spec, parsing_data):
      log.critical("It was not possible to obtain any information about the datasets")
      return parsing_data

    # after_ingesting: curate ingested data according to the spec
    if 'after_ingesting' in parsing_spec['spec']['curating']:
      log.info("[green]<Curating>[/green] ingested data... ([yellow]after_ingesting[/yellow])")
      curating_after_ingesting_mapping_task = progress.add_task("[green]Curating ingested data",
                              total=len(parsing_spec['spec']['curating']['after_ingesting']))
      if not curate_data('after_ingesting', parsing_spec, parsing_data, curating_after_ingesting_mapping_task, progress):
        log.error("Unexpected error curating ingested data")
        return parsing_data
      progress.update(curating_after_ingesting_mapping_task,
                      advance=len(parsing_spec['spec']['curating']['after_ingesting']))

    # before_parsing: curate ingested data according to the spec
    if 'before_parsing' in parsing_spec['spec']['curating']:
      log.info("[green]<Curating>[/green] ingested data... ([yellow]before_parsing[/yellow])")
      curating_before_parsing_mapping_task = progress.add_task("[green]Curating ingested data",
                              total=len(parsing_spec['spec']['curating']['before_parsing']))
      if not curate_data('before_parsing', parsing_spec, parsing_data, curating_before_parsing_mapping_task, progress):
        log.error("Unexpected error curating ingested data")
        return parsing_data
      progress.update(curating_before_parsing_mapping_task,
                      advance=len(parsing_spec['spec']['curating']['before_parsing']))

    log.info("Starting parsing process...")
    log.info("Using [yellow]{}-{}-{}-{}[/yellow] specification".format(
             parsing_spec['spec']['source'],
             parsing_spec['spec']['schema'],
             parsing_spec['spec']['format'],
             parsing_spec['spec']['version']))

    log.info("Parser category: [yellow]{}[/yellow]".format(
             parsing_spec['category']))

    log.info("Parser type: [yellow]{}[/yellow]".format(
             parsing_spec['type']))

    dataset_parsing_task = progress.add_task("[green]Parsing files",
                           total=parsing_data['stats']['total'])

    # load parsing plugins
    if not load_parsing_plugin(parsing_spec):
      log.critical("It was not possible to initialize the parser plugin")
      return parsing_data

    log.info("[green]<Parsing>[/green] data...")
    # parse each dataset
    for dataset_info in parsing_data['datasets']:
      if parse_dataset(parsing_spec, dataset_info, dataset_parsing_task, progress):
        # update stats
        parsing_data['stats']['parsed']  += dataset_info['stats']['parsed']
        parsing_data['stats']['missed'] += dataset_info['stats']['missed']
        parsing_data['stats']['lines']  += dataset_info['stats']['lines']

    # check if there is at least 1 parsed document
    if parsing_data['stats']['parsed'] <= 0:
      log.error("No documents parsed. Nothing to do!")
      return parsing_data

    # log global stats if multiple files
    if parsing_data['stats']['files'] > 1:
      # total parsed
      log.info("{} of {} documents were parsed".format(parsing_data['stats']['parsed'],
                                                       parsing_data['stats']['total']))
      # total missed
      if parsing_data['stats']['missed'] > 1:
        log.info("{} malformed documents were missing".format(parsing_data['stats']['missed']))

      # lines scanned
      log.info("{} lines scanned".format(parsing_data['stats']['lines']))

    # after_parsing: curate parsed data according to the spec
    if 'after_parsing' in parsing_spec['spec']['curating']:
      log.info("[green]<Curating>[/green] parsed data... ([yellow]after_parsing[/yellow])")
      curating_after_parsing_mapping_task = progress.add_task("[green]Curating parsed data",
                              total=len(parsing_spec['spec']['curating']['after_parsing']))
      if not curate_data('after_parsing', parsing_spec, parsing_data, curating_after_parsing_mapping_task, progress):
        log.error("Unexpected error curating parsed data")
        return parsing_data
      progress.update(curating_after_parsing_mapping_task,
                      advance=len(parsing_spec['spec']['curating']['after_parsing']))

    # before_mapping: curate parsed data according to the spec
    if 'before_mapping' in parsing_spec['spec']['curating']:
      log.info("[green]<Curating>[/green] parsed data... ([yellow]before_mapping[/yellow])")
      curating_before_mapping_mapping_task = progress.add_task("[green]Curating parsed data",
                              total=len(parsing_spec['spec']['curating']['before_mapping']))
      if not curate_data('before_mapping', parsing_spec, parsing_data, curating_before_mapping_mapping_task, progress):
        log.error("Unexpected error curating parsed data")
        return parsing_data
      progress.update(curating_before_mapping_mapping_task,
                      advance=len(parsing_spec['spec']['curating']['before_mapping']))

    # map whole parsed data according to the spec
    log.info("[green]<Mapping>[/green] parsed data...")
    dataset_mapping_task = progress.add_task("[green]Mapping parse data",
                           total=len(parsing_data['datasets']))
    if not map_parsed_data(parsing_spec, parsing_data, dataset_mapping_task, progress):
      log.error("Unexpected error mapping parsed data")
      return parsing_data
    progress.update(dataset_mapping_task, advance=len(parsing_data['datasets']))

    # after_mapping: curate mapped data according to the spec
    if 'after_mapping' in parsing_spec['spec']['curating']:
      log.info("[green]<Curating>[/green] mapped data... ([yellow]after_mapping[/yellow])")
      curating_after_mapping_mapping_task = progress.add_task("[green]Curating mapped data",
                              total=len(parsing_spec['spec']['curating']['after_mapping']))
      if not curate_data('after_mapping', parsing_spec, parsing_data, curating_after_mapping_mapping_task, progress):
        log.error("Unexpected error curating mapped data")
        return parsing_data
      progress.update(curating_after_mapping_mapping_task,
                      advance=len(parsing_spec['spec']['curating']['after_mapping']))

    # before_storing: curate mapped data according to the spec
    if 'before_storing' in parsing_spec['spec']['curating']:
      log.info("[green]<Curating>[/green] mapped data... ([yellow]before_storing[/yellow])")
      curating_before_storing_mapping_task = progress.add_task("[green]Curating mapped data",
                              total=len(parsing_spec['spec']['curating']['before_storing']))
      if not curate_data('before_storing', parsing_spec, parsing_data, curating_before_storing_mapping_task, progress):
        log.error("Unexpected error curating mapped data")
        return parsing_data
      progress.update(curating_before_storing_mapping_task,
                      advance=len(parsing_spec['spec']['curating']['before_storing']))

    # dump from the cache to the archive representing the parsed data
    parsing_data.dump()

    # store whole parsed data according to the requested output type
    log.info("[green]<Storing>[/green] mapped data...")
    store_type = output_info['type']

    dataset_storing_task = progress.add_task("[green]Storing mapped data",
              total=len(parsing_spec['spec']['storing'][store_type]['plugins']))
    if not store_parsed_data(parsing_spec,
                                parsing_data,
                                output_info,
                                dataset_storing_task,
                                progress):
      log.error("Unexpected error storing mapped data")
      return parsing_data
    progress.update(dataset_storing_task,
            advance=len(parsing_spec['spec']['storing'][store_type]['plugins']))

    if not progress.finished:
      log.error("Unexpected error")
      return parsing_data

    documents_duplicated = parsing_data['stats'].get('duplicated', '?')
    document_unique = (
        parsing_data['stats']['parsed'] - documents_duplicated
        if documents_duplicated != '?'
        else parsing_data['stats']['parsed']
    )
    log.info("Process successfully completed...")
    log.info("Files: {}, Lines: {}, Documents: {}, Parsed: {}, Missed: {}, Duplicated: {}, Unique: {}".format(
             parsing_data['stats']['files'],
             parsing_data['stats']['lines'],
             parsing_data['stats']['total'],
             parsing_data['stats']['parsed'],
             parsing_data['stats']['missed'],
             documents_duplicated,
             document_unique))

    parsing_data['status']['processed'] = True
    return parsing_data

# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.

def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="""
    A modular framework for ingesting, parsing, mapping, curating, validating and storing data
    """)
    parser.add_argument(
        "--job-id",
        dest="job_id",
        help="job identifier for logging",
        type=str,
        default=None
    )
    parser.add_argument(
        "--version",
        action="version",
        version="parscival {ver}".format(ver=__version__),
    )
    parser.add_argument(
        dest="file_parsing_spec",
        help="parscival specification",
        type=argparse.FileType('r'),
        metavar="FILE_PARSER_SPEC")
    parser.add_argument(
        dest="file_output",
        help="processed data output",
        type=lambda p: Path(p).absolute(),
        metavar="FILE_OUTPUT")
    parser.add_argument(
        dest="file_datasets",
        help="input dataset",
        type=argparse.FileType('r+b'),
        metavar="FILE_DATASET",
        nargs='+')
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
        default=logging.INFO
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)

def get_log_directory():
    """Return the log directory, prioritizing the PARSCIVAL_LOG_PATH environment variable."""
    log_path = os.getenv('PARSCIVAL_LOG_PATH')

    if log_path:
        os.makedirs(log_path, exist_ok=True)
        if os.access(log_path, os.W_OK):
            return log_path

    # Fallback to a user-writable directory
    home_dir = os.path.expanduser('~')
    fallback_log_path = os.path.join(home_dir, '.parscival', 'log')
    os.makedirs(fallback_log_path, exist_ok=True)

    if not os.access(fallback_log_path, os.W_OK):
      return None

    return fallback_log_path

class JobIDFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, style='%', job_id_name=None):
        super().__init__(fmt, datefmt, style)
        self.job_id_name = job_id_name

    def format(self, record):
        record.job_id_name = self.job_id_name
        return super().format(record)

def setup_logging(loglevel, job_id=None):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    # setup the logger rich handler
    rh = RichHandler(
        console=console,
        enable_link_path=False,
        markup=True,
        omit_repeated_times=False,
        rich_tracebacks=True,
        show_level=False,
        show_path=False,
        show_time=False
      )

    # get the log directory
    log_dir = get_log_directory()

    # determine the global log file
    log_global_path = os.path.normpath(os.path.join(log_dir, 'parscival.log'))

    # determine the current job name
    job_id_name = job_id if job_id and job_id.strip() else os.getpid()

    # Setup the global rotating file handler
    gfh = RotatingFileHandler(log_global_path, maxBytes=10**6, backupCount=5)
    gfh.setLevel(loglevel)
    global_file_formatter = JobIDFormatter("%(asctime)s [%(job_id_name)s] %(levelname)s %(message)s",
                                     datefmt="[%X]", job_id_name=job_id_name)
    gfh.setFormatter(global_file_formatter)

    # Setup the logger
    logging.basicConfig(
        level=loglevel,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="[%X]",
        handlers=[rh, gfh]
    )

    # Ensure log handlers are properly closed on exit
    atexit.register(close_log_handlers, log)

    if job_id is None:
      return [log_global_path]

    # Determine the log file name
    log_job_file_name = f'parscival_{job_id_name}.log'
    log_job_file_path = os.path.normpath(os.path.join(log_dir, log_job_file_name))

    # Setup the job file handler
    jfh = logging.FileHandler(log_job_file_path, mode='w')
    jfh.setLevel(loglevel)
    job_file_formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s", datefmt="[%X]")
    jfh.setFormatter(job_file_formatter)

    log.parent.addHandler(jfh)

    return [log_global_path, log_job_file_path]

def close_log_handlers(logger):
  """Clean up the log handlers by closing them."""
  handlers = logger.parent.handlers[:]
  for handler in handlers:
    handler.close()
    logger.removeHandler(handler)

def check_open_file_descriptors(whitelist_files=[]):
    """
    Check and return the list of open file descriptors for the
    current process.

    Returns:
        list of dict: A list of dictionaries containing path
                      and file descriptor.
    """
    # Get the current process
    process = psutil.Process(os.getpid())

    # List all open file descriptors
    open_files = process.open_files()

    # Prepare the list of open files
    open_files_list = []
    for open_file in open_files:
      if os.path.normpath(open_file.path) not in whitelist_files:
        open_files_list.append({
          'path': open_file.path,
          'fd': open_file.fd
        })

    return open_files_list

def is_whitelisted_path(path, whitelist_keywords):
  """
  Check if the given path contains any of the whitelist keywords.

  Parameters:
    path (str): The path to check.
    whitelist_keywords (list): A list of keywords to whitelist.

  Returns:
    bool: True if the path contains any of the whitelist keywords, False otherwise.
  """
  return any(keyword in str(path) for keyword in whitelist_keywords)

def clean_transient_files(files, whitelist_keywords):
  """
  Safely delete files listed in the provided list.

  Parameters:
    files (list): A list of file paths to delete.
    whitelist_keywords (list): A list of keywords that must be in the path to allow deletion.
  """
  for file_path in files:
    try:
      if file_path.exists() and file_path.is_file():
        if is_whitelisted_path(file_path, whitelist_keywords):
          log.debug(f"Deleting file: {file_path}")
          file_path.unlink()
        else:
          log.warning(f"File not whitelisted for deletion: {file_path}")
      else:
        log.warning(f"File not found or is not a file: {file_path}")
    except Exception as e:
      log.error(f"Error deleting file {file_path}: {e}")

def clean_transient_directories(directories, whitelist=None, blacklist=None, whitelist_keywords=None):
  """
  Safely delete directories listed in the provided list.

  Parameters:
    directories (list): A list of directory paths to delete.
    whitelist (list): Directories allowed to be removed.
    blacklist (list): Directories not allowed to be removed.
    whitelist_keywords (list): A list of keywords that must be in the path to allow deletion.

  Raises:
    ValueError: If an attempt is made to delete a protected or root directory.
  """
  # set default whitelists and blacklists if not provided
  if whitelist is None:
    whitelist = []
  if blacklist is None:
    blacklist = ["/", "/bin", "/boot", "/dev", "/etc", "/lib", "/proc", "/root", "/sys", "/usr", "/var"]
  if whitelist_keywords is None:
    whitelist_keywords = []

  for dir_path in directories:
    try:
      # normalize the path to avoid issues with trailing slashes
      path = Path(os.path.normpath(dir_path))

      # ensure the directory is not root
      if path == Path("/"):
        raise ValueError("Attempt to delete root directory is not allowed.")

      # check if path is in the blacklist
      if path in [Path(p) for p in blacklist]:
        raise ValueError(f"Attempt to delete a protected directory is not allowed: {path}")

      # if a whitelist is provided, ensure the path is within the whitelist
      if whitelist and path not in [Path(p) for p in whitelist]:
        raise ValueError(f"Attempt to delete a directory not in the whitelist: {path}")

      # check if the path contains any of the whitelist keywords
      if not is_whitelisted_path(path, whitelist_keywords):
        raise ValueError(f"Directory not whitelisted for deletion: {path}")

      # check if the directory exists before attempting to delete
      if path.exists() and path.is_dir():
        log.debug(f"Deleting directory: {path}")
        shutil.rmtree(path)
      else:
        log.warning(f"Directory not found or is not a directory: {path}")
    except Exception as e:
      log.error(f"{e}")

def clean_transient(transient):
  """
  Safely delete files and directories listed in the transient dictionary.

  Parameters:
    transient (dict): A dictionary containing 'files' and 'directories' keys with lists of paths to delete.
  """
  whitelist_keywords = ['/parscival-']

  # Delete files
  clean_transient_files(transient.get('files', []), whitelist_keywords)

  # Delete directories
  clean_transient_directories(transient.get('directories', []), whitelist_keywords=whitelist_keywords)

def main(args):
    """Wrapper allowing :func:`parse` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`parse`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    # take environment variables from .env
    load_dotenv()
    # parse arguments
    args = parse_args(args)
    # setup logging at level
    log_files = setup_logging(args.loglevel, args.job_id)

    if not log_files:
      raise RuntimeError("Unable to create a logging files. Use PARSCIVAL_LOG_PATH")
      return

    log.info("Parscival [cyan]v{}[/cyan]".format(get_version_major_minor_patch(__version__)))

    global engine_version
    engine_version = get_custom_metadata('engine', 'version')
    log.info("Using Parscival Engine [cyan]v{}[/cyan]".format(engine_version))

    log.info(f"Logging global activity in {log_files[0]}")
    if len(log_files) > 1:
      for log_file in log_files[1:]:
        log.info(f"Logging activity in {log_file}")

    log.info("Starting the worker...")

    parsing_data = None
    # process_datasets
    try:
      parsing_data = process_datasets(args.file_parsing_spec,
                                      args.file_output,
                                      args.file_datasets)
    finally:
      # ensure file_parsing_spec is closed
      args.file_parsing_spec.close()
      # ensure all file objects in file_datasets are closed
      for file_obj in args.file_datasets:
        try:
          file_obj.close()
        except Exception as e:
          log.error(f"Error closing file: {file_obj.name}, {e}")

    # get the open file descriptors
    open_files = check_open_file_descriptors(log_files)
    if open_files:
      log.warning("A plugin or module has opened one or more file descriptors without closing them:")
      for file in open_files:
        log.warning(f"File Descriptor: {file['fd']}, Path: {file['path']}")

    # clean transient directories and files
    clean_transient(parsing_data['transient'])

    # final logging message
    if ('status' in parsing_data and
        'processed' in parsing_data['status'] and
        parsing_data['status']['processed']):
      log.info("Worker finished without errors")
    else:
      log.critical("Worker finished with errors")

def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function is used as entry point to create a console script with setuptools.
    """
    main(sys.argv[1:])

if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run this Python
    # module as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m parscival.worker PARAMS...
    #
    run()
