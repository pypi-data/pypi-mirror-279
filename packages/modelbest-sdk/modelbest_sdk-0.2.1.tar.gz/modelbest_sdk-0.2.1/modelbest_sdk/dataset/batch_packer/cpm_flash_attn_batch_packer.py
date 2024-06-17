
from collections import defaultdict, deque
import hashlib
from typing import Dict, Generator, List, Tuple

import numpy as np
import torch
from modelbest_sdk.dataset.batch_packer.batch_packer import BatchPacker
from modelbest_sdk.dataset.thrift_wrapper.base_doc import DetailedDoc
from modelbest_sdk.dataset.thrift_wrapper.dataset_checkpoint import Chunk


class CpmFlashAttnBatchPacker(BatchPacker):
    def __init__(self, batch_size: int, max_len: int, dataset_cnt: int):
        super().__init__()
        self.buffer = deque()
        self.current_length = 0
        self.max_total_length = batch_size * max_len
        self.batch_size = 1
        self.dataset_cnt = dataset_cnt

    def put(self, data: DetailedDoc):
        self.buffer.append(data)
        # TODO: 只适配megatron segment
        self.current_length += (len(data.base_doc.token_ids) - 1)
        
    def pop(self) -> DetailedDoc:
        lengths = []
        indexes: List[Tuple[int, Dict[Chunk, List[int]]]] = []
        inputs = torch.zeros((self.batch_size, self.max_total_length), dtype=torch.int32)
        targets = torch.full((self.batch_size, self.max_total_length), dtype=torch.int32, fill_value=-100)
        dataset_ids = torch.full((self.batch_size, self.max_total_length), dtype=torch.int32, fill_value=-1)
        position_ids = torch.zeros((self.batch_size, self.max_total_length), dtype=torch.int32)
        tags = torch.full((self.batch_size, self.max_total_length), dtype=torch.int64, fill_value=-1)

        span_begin = 0
        while self.buffer:
            data: DetailedDoc = self.buffer.pop()
            base_doc = data.base_doc
            dataset_idx = data.dataset_idx
            token_ids = base_doc.token_ids
            mask = base_doc.mask
            tag = base_doc.tag[0] # TODO: support multiple tags
            span_end = span_begin + len(token_ids) - 1
            inputs[0, span_begin:span_end] = torch.tensor(token_ids[:-1], dtype=torch.int32)
            target_ids = np.where(mask[:-1], -100, token_ids[1:]).tolist()
            targets[0, span_begin:span_end] = torch.tensor(target_ids, dtype=torch.int32)
            dataset_ids[0, span_begin:span_end] = torch.tensor(dataset_idx, dtype=torch.int32)
            tags[0, span_begin:span_end] = self.encode_tags(token_ids[:-1], tag)
            indexes.append((dataset_idx, data.indexes_dict))

            # reset position ids
            cu_seqlens, inner_span_begin = [0], span_begin
            for i, position in enumerate(data.positions):
                if len(data.positions) - 1 == i:
                    instance_length = position.length - 1
                    if instance_length == 0:
                        continue
                else:     
                    instance_length = position.length
                lengths.append(instance_length)
                position_ids[0, inner_span_begin:inner_span_begin + instance_length] = torch.from_numpy(np.arange(instance_length, dtype=np.int32))
                inner_span_begin += instance_length
            assert inner_span_begin == span_end
            cu_seqlens = torch.tensor([0] + lengths).cumsum(dim=-1)
            if cu_seqlens[-1].item() != self.max_total_length: 
                cu_seqlens = torch.cat(
                    [cu_seqlens, torch.tensor([self.max_total_length], dtype=torch.int32)],
                    dim=0,
                )
            cu_seqlens = cu_seqlens.int()
            span_begin = span_end

        batch = {
            "input_ids": inputs,
            "target_ids": targets,
            "dataset_ids": dataset_ids,
            "indexes": indexes,
            "cu_seqlens": cu_seqlens,
            "max_seqlen": int(torch.max(cu_seqlens[1:] - cu_seqlens[:-1])),
            "lengths": torch.tensor(sum(lengths)).int(),
            "position_ids": position_ids,
            "tags": tags,
            "hash_to_tag": self.hash_to_tag
        }
        self.current_length = 0
        return batch
    
    
    def will_exceed(self, data: DetailedDoc):
        if data is None:
            return False
        # TODO: 只适配megatron segment
        cur_base_doc_length = len(data.base_doc.token_ids) - 1
        return self.current_length + cur_base_doc_length > self.max_total_length

    def too_long(self, data: DetailedDoc):
        if len(data.base_doc.token_ids) > self.max_total_length:
            # logger.warning(f"Document {data.base_doc.docid} is too long, length {len(data.base_doc.token_ids)} > {self.max_total_length}, truncate it.")
            return True
        return False
    
    @staticmethod
    def collate_fn(batch):
        return batch[0]

    def __call__(self, detailed_doc: DetailedDoc=None, pop_last=False) -> Generator[DetailedDoc, None, None]:
        if (pop_last and self.buffer):
            yield self.pop()
        if detailed_doc is not None:
            if self.will_exceed(detailed_doc):
                yield self.pop()
            self.put(detailed_doc)