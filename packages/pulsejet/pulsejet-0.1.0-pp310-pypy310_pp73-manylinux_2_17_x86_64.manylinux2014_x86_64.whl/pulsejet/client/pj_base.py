from ..pulsejet import *
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple, Union


class PulsejetBase:
    def __init__(self, **kwargs: Any):
        pass

    def close(self, **kwargs: Any) -> None:
        pass

    def create_collection(
            self,
            collection_name: str,
            vector_config: VectorParams,
            **kwargs: Any,
    ) -> bool:
        raise NotImplementedError()

    def update_collection(
            self,
            existing_name: str,
            vector_config: VectorParams,
            new_name: Optional[str] = None,
            **kwargs: Any,
    ) -> bool:
        raise NotImplementedError()

    def delete_collection(self, collection_name: str, **kwargs: Any) -> bool:
        raise NotImplementedError()

    def list_collections(self, filter: Optional[str], **kwargs: Any) -> bool:
        raise NotImplementedError()

    def insert_single(self, collection_name: str, vector: [float], meta: Dict[str, str]) -> bool:
        raise NotImplementedError()

    def insert_multi(self, collection_name: str, embeds: [RawEmbed]) -> bool:
        raise NotImplementedError()

    def delete(self, collection_name: str, embed_ids: [int]) -> bool:
        raise NotImplementedError()

    def update(self, collection_name: str, embeds: [Embed]) -> bool:
        raise NotImplementedError()

    def search_single(self, collection_name: str, vector: [float], limit: int, filter: Optional[PayloadFilter]) -> bool:
        raise NotImplementedError()

    def search_multi(self, searches: [OpSearchEmbed]) -> bool:
        raise NotImplementedError()