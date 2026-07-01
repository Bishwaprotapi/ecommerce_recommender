import torch
import torch.nn as nn

class ScalableRecommender(nn.Module):
    def __init__(self, num_users, num_products):
        super().__init__()
        self.user_emb = nn.Embedding(num_users, 64)
        self.prod_emb = nn.Embedding(num_products, 64)

        self.fc = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

    def forward(self, user, product):
        u = self.user_emb(user)
        p = self.prod_emb(product)
        x = torch.cat([u, p], dim=1)
        return torch.sigmoid(self.fc(x))