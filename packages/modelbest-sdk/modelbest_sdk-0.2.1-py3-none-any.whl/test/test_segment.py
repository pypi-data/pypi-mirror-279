import unittest

from modelbest_sdk.dataset.segment.segment_factory import CONDITIONAL_FIXED_LENGTH_SEGMENT
from modelbest_sdk.dataset.segment_dataset import SegmentDataset
from modelbest_sdk.dataset.thrift_wrapper.base_doc import BaseDoc
from modelbest_sdk.dataset.thrift_wrapper.dataset_context import DatasetContext
from modelbest_sdk.file_format.mbtable_builder import MbTableBuilder


class TestSegment(unittest.TestCase):
    def test_segment(self):
        builder = MbTableBuilder('example/mbtable_data/chat.mbt')
        for j in range(10):
            doc = BaseDoc()
            doc.token_ids = [-1, 1, 2, 3, 4, -2]
            doc.mask = [True, True, False, False, False, True]
            doc_str = doc.serialize()
            builder.write(doc_str)
        builder.flush()
        
        builder = MbTableBuilder('/tmp/text.mbt')
        for j in range(10):
            doc = BaseDoc()
            doc.token_ids = [-1, 1, 2, 3, 4, -2]
            doc.mask = [False, False, False, False, False, True]
            doc_str = doc.serialize()
            builder.write(doc_str)
        builder.flush()
        
        context = DatasetContext()
        dataset = SegmentDataset(
            context,
            '/tmp/chat.mbt',
            max_epoch=2,
            segment_type=CONDITIONAL_FIXED_LENGTH_SEGMENT,
            max_len = 9
        )
        dataset.worker_init()
        for data in dataset:
            print(data)

if __name__ == '__main__':
    unittest.main()