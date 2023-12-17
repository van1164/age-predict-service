import torch
import torch.nn as nn
import torch.nn.functional as F
class EnsembleModel(nn.Module):
    def __init__(self, modelA, modelB,num_features):
        super().__init__()
        self.modelA = modelA
        self.modelB = modelB
        self.classifier = nn.Linear(3*num_features, num_features)

    def forward(self, x):
        x1 = self.modelA(x)
        x2 = self.modelB(x)
        x = torch.cat((x1,x2,x2), dim=-1)
        x = self.classifier(F.relu(x))
        return x