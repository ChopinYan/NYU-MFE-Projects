import numpy as np

import torch
import torch.nn as nn
from torch.optim import Adam, AdamW
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm, trange

from transformers import (
    BertModel,
    BertTokenizer,
    get_scheduler
)

from sklearn.metrics import (
    precision_score,
    accuracy_score,
    recall_score
)

from loader.text_preprocessing import SimpleProcessor
from loader.data_loader import NewsDataset


INPUT_DIM = 768
HIDDEN_DIM = 256
OUTPUT_DIM = 2


# TODO: NEED FURTHER MODIFICATION
class FeedForwardNet(nn.Module):
    def __init__(self, lr, total_steps):
        super(FeedForwardNet, self).__init__()
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = nn.Sequential(
            nn.Linear(384, 256),
            nn.ReLU(),
            nn.Linear(256, 2),
            nn.Dropout(p=0.05),
            nn.Sigmoid()
        )
        self.model = self.model.to(self.device)
        self.optimizer = AdamW(self.model.parameters(), lr=lr, eps=1e-8)
        self.scheduler = get_scheduler(
            name='linear',
            optimizer=self.optimizer,
            num_warmup_steps=0,
            num_training_steps=total_steps
        )

    def forward(self, x):
        return self.model(x)


class EmbeddingClassifier(nn.Module):
    """
    Classification using LSTM
    """
    def __init__(self, pre_trained='bert-base-uncased', lstm_layers=2, lr=1e-3):
        super().__init__()

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.bert = BertModel.from_pretrained(pre_trained)
        self.bert.requires_grad_(False)  # frozen parameters
        self.hidden_size = self.bert.config.hidden_size

        self.lstm_layers = lstm_layers
        self.LSTM = nn.LSTM(input_size=self.hidden_size, hidden_size=256, num_layers=lstm_layers, dropout=0.2)

        self.bn1 = nn.BatchNorm1d(256)
        self.bn2 = nn.BatchNorm1d(64)

        self.fc1 = nn.Linear(in_features=256, out_features=64)
        self.fc2 = nn.Linear(in_features=64, out_features=1)

        self.optimizer = Adam(self.parameters(), lr=lr)
        self.criterion = nn.BCELoss(reduction='sum')

    def forward(self, input_id, mask):
        h = torch.zeros((self.lstm_layers, input_id.size(0), 256)).to(self.device)
        c = torch.zeros((self.lstm_layers, input_id.size(0), 256)).to(self.device)
        torch.nn.init.xavier_normal_(h)
        torch.nn.init.xavier_normal_(c)

        encoded_layers = self.bert(input_ids=input_id, attention_mask=mask)[0]
        encoded_layers = encoded_layers.permute(1, 0, 2)

        out, (hn, cn) = self.LSTM(encoded_layers, (h, c))
        out = out[-1, :, :].view(-1, 256)
        out = self.bn1(out)

        out = torch.relu_(self.fc1(out))
        out = self.bn2(out)

        out = torch.sigmoid(self.fc2(out))

        return out


def trainer(model, train_loader, valid_loader, epochs):
    # epochs 
    train_loss = []
    valid_loss = []

    model = model.to(model.device)
    print(model.device)
    for _ in trange(epochs):

        # set model to training model
        model.train()

        total_loss = 0
        total_num = 0
        for train_inputs, train_labels in train_loader:
            train_labels = train_labels.float()
            train_labels = train_labels.to(model.device)
            mask = train_inputs['attention_mask'].to(model.device)
            input_id = train_inputs['input_ids'].squeeze(1).to(model.device)

            model.optimizer.zero_grad()

            output = model(input_id, mask)

            loss = model.criterion(output, train_labels.unsqueeze(1))
            loss.backward()

            model.optimizer.step()
            total_loss += loss.item()

            total_num += input_id.size(0)

        # Validation
        model.eval()

        total_loss_val = 0
        total_num_val = 0
        preds = []
        trues = []
        with torch.no_grad():

            for valid_inputs, valid_labels in valid_loader:
                valid_labels = valid_labels.float()
                valid_labels = valid_labels.to(model.device)
                mask = valid_inputs['attention_mask'].to(model.device)
                input_id = valid_inputs['input_ids'].squeeze(1).to(model.device)

                output = model(input_id, mask)

                loss = model.criterion(output, valid_labels.unsqueeze(1))

                total_loss_val += loss.item()
                total_num_val += input_id.size(0)

                probs = output.detach().cpu().numpy()
                predictions = [1 if p > 0.5 else 0 for p in probs]

                labels = valid_labels.detach().cpu().numpy().flatten()

                preds += list(predictions)
                trues += list(labels)

        train_loss.append(total_loss / total_num)
        valid_loss.append(total_loss_val / total_num_val)
        print('\n\t - Train loss : {:.4f}'.format(total_loss / total_num))
        print('\t - Validation loss : {:.4f}'.format(total_loss_val / total_num_val))
        print('\t - Validation accuracy : {:.4f}'.format(accuracy_score(trues, preds)))
        print('\t - Validation precision : {:.4f}'.format(precision_score(trues, preds)))
        print('\t - Validation recall : {:.4f}'.format(recall_score(trues, preds)))

    return train_loss, valid_loss


def evaluate(model, test_loader):
    model = model.to(model.device)
    preds = []
    with torch.no_grad():
        for test_inputs, test_labels in test_loader:
            test_labels = test_labels.float()
            test_labels = test_labels.to(model.device)
            mask = test_inputs['attention_mask'].to(model.device)
            input_id = test_inputs['input_ids'].squeeze(1).to(model.device)

            output = model(input_id, mask)

            probs = output.detach().cpu().numpy()
            predictions = [1 if p > 0.5 else 0 for p in probs]

            preds += list(predictions)
    return preds


if __name__ == "__main__":
    sp = SimpleProcessor(
        r"../data/btc_eth.csv",
        r"../data/price_vol.csv",
        "BTC", "close")
    data = sp.get_data()

    # train valid test split
    percent = 0.8
    n = data.shape[0]
    trainData, testData = data.iloc[0: int(n * percent)], data.iloc[int(n * percent):]
    m = trainData.shape[0]
    trainData, validData = trainData.iloc[0: int(m * percent)], trainData.iloc[int(m * percent):]

    # load pre-trained model
    # TODO: UNMATCHED DATATYPE should be tensorflow "Dataset"
    BERT_NAME = 'bert-base-uncased'
    tokenizer = BertTokenizer.from_pretrained(BERT_NAME)
    trainDataLoader = DataLoader(NewsDataset(trainData, tokenizer), batch_size=32, drop_last = True)
    validDataLoader = DataLoader(NewsDataset(validData, tokenizer), batch_size=32, drop_last = True)
    testDataLoader = DataLoader(NewsDataset(testData, tokenizer), batch_size=32)

    # Model training / fine-tuning
    num_epochs = 5
    clf = EmbeddingClassifier(lr=1e-4)
    trainloss, validloss = trainer(clf, trainDataLoader, validDataLoader, num_epochs)


