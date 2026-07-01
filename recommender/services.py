import torch
from datetime import date, timedelta
from .models import Product, Sale
from .ml_model import ScalableRecommender

# Load trained model
checkpoint = torch.load("model.pth")

user_map = checkpoint["user_map"]
product_map = checkpoint["product_map"]

model = ScalableRecommender(len(user_map), len(product_map))
model.load_state_dict(checkpoint["model"])
model.eval()

def recommend(user_id, purchased_product_name, top_k=10):

    try:
        purchased_product = Product.objects.get(name=purchased_product_name)
    except:
        return []

    category = purchased_product.category

    candidates = Product.objects.filter(category=category)

    user_history = Sale.objects.filter(user_id=user_id)

    recommendations = []

    for product in candidates:

        if product.name == purchased_product_name:
            continue

        reason = "Similar category recommendation."

        previous = user_history.filter(product=product).first()

        if previous:
            replace_date = previous.purchase_date + timedelta(days=365*product.lifecycle_years)
            if replace_date <= date.today():
                reason = "Previous product expired. Replacement suggested."
            else:
                continue

        if user_id in user_map and product.id in product_map:
            user_tensor = torch.tensor([user_map[user_id]])
            product_tensor = torch.tensor([product_map[product.id]])
            score = model(user_tensor, product_tensor).item()
        else:
            score = 0.5

        recommendations.append({
            "product": product.name,
            "score": round(score,3),
            "reason": reason
        })

    recommendations.sort(key=lambda x: x["score"], reverse=True)

    return recommendations[:top_k]