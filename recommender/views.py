from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import recommend

@api_view(["POST"])
def get_recommendation(request):

    user_id = request.data.get("user_id")
    purchased_product = request.data.get("purchased_product")

    recs = recommend(user_id, purchased_product)

    return Response(recs)