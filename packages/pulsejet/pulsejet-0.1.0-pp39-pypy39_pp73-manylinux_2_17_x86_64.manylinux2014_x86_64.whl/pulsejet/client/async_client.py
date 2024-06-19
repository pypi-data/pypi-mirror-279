import warnings
import logging
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Union,
)
from ..pulsejet import *
from ..client.async_pj_base import *
from ..client.async_pj_remote import *
import tomllib

class AsyncPulsejetClient(AsyncPulsejetBase):
    def __init__(self,
                 location: Optional[str] = "local",
                 https: Optional[bool] = None,
                 host: Optional[str] = "127.0.0.1",
                 port: Optional[int] = 47044,
                 grpc_port: int = 47045,
                 prefer_grpc: bool = True,
                 timeout: Optional[int] = None,
                 grpc_options: Optional[Dict[str, Any]] = None,
                 prod_name: Optional[str] = "pulsejetdb",
                 shard_id: Optional[int] = 0,
                 basedir: Optional[str] = ".database",
                 hot_storage_size: Optional[int] = 10000000,
                 bloom_fp_rate: Optional[float] = 0.001,
                 bloom_size: Optional[int] = 1000000,
                 flush_size: Optional[int] = 52428800,
                 bufferpool_to_resident_ratio: Optional[float] = 0.2,
                 resident_writeback_interval_ms: Optional[int] = 50000,
                 txn_timeout_ms: Optional[int] = 500,
                 max_background_jobs: Optional[int] = 10,
                 config_path: Optional[str] = None,
                 **kwargs: Any,
                 ):
        if config_path:
            with open(config_path, "rb") as f:
                d = tomllib.load(f)
                storage = d['storage']
                hotcfg = storage['hot_config']
                warmcfg = storage['warm_config']
                self.options: Options = Options(
                    rest_api_port=d['rest_api_port'],
                    grpc_api_port=d['grpc_api_port'],
                    prod_name=storage['prod_name'],
                    shard_id=storage['shard_id'],
                    basedir=storage['basedir'],
                    hot_storage_size=hotcfg['hot_storage_size'],
                    bloom_fp_rate=hotcfg['bloom_fp_rate'],
                    bloom_size=hotcfg['bloom_size'],
                    flush_size=hotcfg['flush_size'],
                    bufferpool_to_resident_ratio=hotcfg['bufferpool_to_resident_ratio'],
                    resident_writeback_interval_ms=hotcfg['resident_writeback_interval_ms'],
                    txn_timeout_ms=hotcfg['txn_timeout_ms'],
                    max_background_jobs=warmcfg['max_background_jobs'],
                )
        else:
            self.options: Options = Options(
                rest_api_port=port,
                grpc_api_port=grpc_port,
                prod_name=prod_name,
                shard_id=shard_id,
                basedir=basedir,
                hot_storage_size=hot_storage_size,
                bloom_fp_rate=bloom_fp_rate,
                bloom_size=bloom_size,
                flush_size=flush_size,
                bufferpool_to_resident_ratio=bufferpool_to_resident_ratio,
                resident_writeback_interval_ms=resident_writeback_interval_ms,
                txn_timeout_ms=txn_timeout_ms,
                max_background_jobs=max_background_jobs,
            )

        if https:
            self.grpc_address = "https://{}.{}".format(host, self.options.grpc_api_port)
            self.http_address = "https://{}.{}".format(host, self.options.rest_api_port)
        else:
            self.grpc_address = "http://{}.{}".format(host, self.options.grpc_api_port)
            self.http_address = "http://{}.{}".format(host, self.options.rest_api_port)

        # PulseJet Base
        self._client: PulsejetBase

        # XXX: Doing the launch here with options.
        if location == "inmem":
            raise NotImplementedError
        elif location == "remote":
            logging.info(f"PulseJet™ DB - Connecting remote instance on '{host}' and port: '{grpc_port}'.")
            self._client = AsyncPulsejetRemote(
                host=host,
                port=port,
                grpc_port=grpc_port,
                prefer_grpc=prefer_grpc,
                https=https,
                timeout=timeout,
                grpc_options=grpc_options,
                **kwargs,
            )
        else:
            logging.info(f"PulseJet™ DB - Unknown server launch style is given: {location}.")

    def __del__(self) -> None:
        self.close()

    async def close(self, grpc_grace: Optional[float] = None, **kwargs: Any) -> None:
        """Closes the connection to PulseJet

        Args:
            grpc_grace: Grace period for gRPC connection close. Default: None
        """
        if hasattr(self, "_client"):
            self._client.close(grpc_grace=grpc_grace, **kwargs)

    async def create_collection(self, collection_name: str, vector_config: VectorParams, **kwargs: Any) -> bool:
        assert len(kwargs) == 0, f"Unknown arguments: {list(kwargs.keys())}"
        return await self._client.create_collection(
            collection_name=collection_name,
            vector_config=vector_config,
            **kwargs
        )

    async def update_collection(self, existing_name: str, vector_config: VectorParams, new_name: Optional[str] = None,
                          **kwargs: Any) -> bool:
        assert len(kwargs) == 0, f"Unknown arguments: {list(kwargs.keys())}"
        return await self._client.update_collection(
            existing_name=existing_name,
            vector_config=vector_config,
            new_name=new_name,
            **kwargs
        )

    async def delete_collection(self, collection_name: str, **kwargs: Any) -> bool:
        assert len(kwargs) == 0, f"Unknown arguments: {list(kwargs.keys())}"
        return await self._client.delete_collection(
            collection_name=collection_name,
            **kwargs
        )

    async def list_collections(self, filter: Optional[str], **kwargs: Any) -> bool:
        assert len(kwargs) == 0, f"Unknown arguments: {list(kwargs.keys())}"
        return await self._client.list_collections(
            filter=filter,
            **kwargs
        )

    async def insert_single(self, collection_name: str, vector: [float], meta: Dict[str, str]) -> bool:
        return await self._client.insert_single(
            collection_name=collection_name,
            vector=vector,
            meta=meta
        )

    async def insert_multi(self, collection_name: str, embeds: [RawEmbed], num_workers: int = 1) -> bool:
        return await self._client.insert_multi(
            collection_name=collection_name,
            embeds=embeds,
            num_workers=num_workers
        )

    async def delete(self, collection_name: str, embed_ids: [int]) -> bool:
        return await self._client.delete(
            collection_name=collection_name,
            embed_ids=embed_ids
        )

    async def update(self, collection_name: str, embeds: [Embed]) -> bool:
        return await self._client.update(
            collection_name=collection_name,
            embeds=embeds
        )

    async def search_single(self, collection_name: str, vector: [float], limit: int, filter: Optional[PayloadFilter]) -> bool:
        return await self._client.search_single(
            collection_name=collection_name,
            vector=vector,
            limit=limit,
            filter=filter
        )

    async def search_multi(self, searches: [OpSearchEmbed]) -> bool:
        return await self._client.search_multi(
            searches=searches
        )
