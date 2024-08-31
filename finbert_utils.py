from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import Tuple 
import warnings
import time

#warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=UserWarning)
if torch.cuda.is_available():
    device = "cuda:0"
else:
    device = "cpu"



tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert").to(device)
labels = ["positive", "negative", "neutral"]

def estimate_sentiment(news):
    #start_time = time.time()
    if news:
        tokens = tokenizer(news, return_tensors="pt", padding=True).to(device)

        result = model(tokens["input_ids"], attention_mask=tokens["attention_mask"])[
            "logits"
        ]
        result = torch.nn.functional.softmax(torch.sum(result, 0), dim=-1)
        probability = result[torch.argmax(result)]
        sentiment = labels[torch.argmax(result)]
        end_time = time.time()
        #print("Time elapsed: ")
        #print(end_time-start_time)
        return probability, sentiment
    else:
        #print("Time elapsed: ")
        #print(end_time-start_time)
        return 0, labels[-1]
    


if __name__ == "__main__":
    tensor, sentiment = estimate_sentiment(['markets responded positively to the news!','traders were thrilled!'])
    
    print(tensor, sentiment)
    print(torch.cuda.is_available())