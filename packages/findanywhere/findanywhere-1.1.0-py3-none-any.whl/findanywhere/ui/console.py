from argparse import ArgumentParser, Namespace
from functools import partial
from json import dump
from multiprocessing import cpu_count
from pathlib import Path
from typing import cast

from findanywhere.ports.source import SourceAdapter
from findanywhere.schema import load_schema, SearchSchema
from findanywhere.search.base import Search, search, SearchPattern
from findanywhere.search.parallel import parallel_search
from findanywhere.search.sequential import sequential_search
from findanywhere.types.input_data import InputData


def main() -> None:
    """
    Main method for searching data in a data set using a schema.
    """
    parser: ArgumentParser = ArgumentParser('Search for data in a data set using a schema')
    parser.add_argument('schema', type=Path, help='Schema to use for search.')
    parser.add_argument('input_data', type=Path, help='JSON file with input data')
    parser.add_argument('--processes', type=int, default=cpu_count())
    parser.add_argument('--out', type=Path, default=Path('schema.yml'))
    parser.add_argument('--sequential', type=bool, default=False, help='Do not use parallel search. (False)')
    primary_args: Namespace = parser.parse_known_args()[0]

    schema: SearchSchema = load_schema(primary_args.schema)
    parser.add_argument('location', type=schema.source.config.location_type())
    args: Namespace = parser.parse_args()

    search_: Search = partial(search, schema.evaluation_adapter(), schema.create_deduction(), schema.create_threshold())

    source_adapter: SourceAdapter = schema.source_adapter()

    search_style: SearchPattern = cast(SearchPattern, partial(
        parallel_search, processes=args.processes
    )) if not primary_args.sequential else sequential_search

    with open(args.out, 'w', encoding='utf-8', errors='surrogateescape') as out:
        for result in search_style(InputData.from_json(args.input_data), search_, source_adapter(args.location)):
            dump(result, out, ensure_ascii=False, default=str)
            out.write('\n')
