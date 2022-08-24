#!/usr/bin/env python3
"""
Validate beacon data files against beacon schema.
"""
import argparse
import json
import logging
import sys
from urllib.request import urlopen

from jsonschema import validate, RefResolver

logging.basicConfig(level=logging.INFO)

LOGGER = logging.getLogger(__name__)
DEFAULT_SCHEMA_BASEURI = ('https://raw.githubusercontent.com/ga4gh-beacon/'
                          'beacon-v2/main/models/json/beacon-v2-default-model')
SCHEMA_NAMES = ['individuals', 'biosamples', 'runs', 'analyses',
                'genomicVariations', 'cohorts', 'datasets']


def get_schemata(baseuri):
    """
    Return a dict mapping schema name to (schema, resolver).

    Args:
        baseuri: schema base URI
    """
    schemata = {}
    for name in SCHEMA_NAMES:
        location = f'{baseuri}/{name}/defaultSchema.json'
        with urlopen(location) as uh:
            schema = json.load(uh)
        schemata[name] = (schema, RefResolver(location, schema))
    return schemata


def parse_cmdargs(args):
    """
    Returns: Parsed arguments
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('schema',
                        choices=SCHEMA_NAMES,
                        help='Schema entity type to validate.')
    parser.add_argument('data',
                        type=argparse.FileType(mode='rb'),
                        help=('JSON data file containing an array of '
                              'instances of the schema entity.'))
    parser.add_argument('--baseuri',
                        default=DEFAULT_SCHEMA_BASEURI,
                        help=('Base URI for the schema documents. '
                              f'(default={DEFAULT_SCHEMA_BASEURI}) '
                              'i.e. latest from github.'))
    return parser.parse_args(args)


if __name__ == '__main__':

    args = parse_cmdargs(sys.argv[1:])
    LOGGER.info(f'validating {args.data.name} against {args.schema}')
    schemata = get_schemata(args.baseuri)
    instances = json.load(args.data)
    schema, resolver = schemata[args.schema]
    for instance in instances:
        validate(instance, schema=schema, resolver=resolver)
