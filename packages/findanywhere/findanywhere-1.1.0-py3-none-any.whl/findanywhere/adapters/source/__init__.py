from typing import Any

from findanywhere.adapters.source.text import load_text_source_using
from findanywhere.adapters.source.tabular import load_tabular_source_using
from findanywhere.ports.source import SourceAdapter
from findanywhere.types.factory import FactoryMap

SOURCE_FACTORIES: FactoryMap[SourceAdapter[Any, Any, Any]] = FactoryMap(
    (load_text_source_using, load_tabular_source_using)
)
