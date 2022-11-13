import attr
import warnings
from typing import List

import numpy as np
import pandas as pd

import torch

from embeddings.sentence_embeddings import (
    load_model_and_tokenizer,
    get_sentence_embeddings
)


@attr.s
class Dataset(object):
    """
    version:
    sentence bert from AutoModel deepset sbert
    """
    # These are the text (news articles, product descriptions, etc.)
    examples: List[str] = attr.ib()
    # Labels associated with each example
    labels: List[int] = attr.ib()
    # embeddings for each example and each category
    _embeddings = attr.ib(default=None)

    def calc_sbert_embeddings(self):
        model, tokenizer = load_model_and_tokenizer()
        self._embeddings = get_sentence_embeddings(
            self.examples, model, tokenizer
        )

    @property
    def embeddings(self):
        if not hasattr(self, "_embeddings") or self._embeddings is None:
            warnings.warn(
                "Should run dataset.calc_sbert_embeddings() first.  In the future this will fail."
            )
            self.calc_sbert_embeddings()
            # raise Exception("Run dataset.calc_sbert_embeddings() first.")
        return self._embeddings


def create_dataset_from_df(df: pd.DataFrame, text_column: str) -> Dataset:
    dataset = Dataset(
        examples=df[text_column].tolist(),
        labels=df.label.tolist(),
    )
    return dataset


class NewsDataset(Dataset):
    """
    Version:
    from transformers import BertModel
    BERT_NAME = 'bert-base-uncased'
    tokenizer = BertTokenizer.from_pretrained(BERT_NAME)
    """
    def __init__(self, df, tokenizer):
        self.labels = [i for i in df['class']]
        self.texts = [tokenizer(
            str(text),
            padding='max_length',
            truncation=True,
            return_tensors='pt')
            for text in df['text']
        ]

    def __len__(self):
        return len(self.labels)

    def get_batch_labels(self, idx):
        return np.array(self.labels[idx])

    def get_batch_text(self, idx):
        return self.texts[idx]

    def __getitem__(self, idx):
        batch_texts = self.get_batch_text(idx)
        batch_labels = self.get_batch_labels(idx)
        return batch_texts, batch_labels

