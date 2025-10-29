"""
Swagger/OpenAPI schema definitions for bank app endpoints.
Keeps views clean by separating API documentation.
"""
from drf_yasg import openapi
from .serializers import TransactionSerializer


# Query parameters for TransactionListApiView
transaction_list_params = [
    openapi.Parameter(
        'deposit',
        openapi.IN_QUERY,
        description="Filter deposit transactions (true/false)",
        type=openapi.TYPE_BOOLEAN,
        required=False,
        default=True
    ),
    openapi.Parameter(
        'withdrawal',
        openapi.IN_QUERY,
        description="Filter withdrawal transactions (true/false)",
        type=openapi.TYPE_BOOLEAN,
        required=False,
        default=True
    ),
]

# Responses for TransactionListApiView
transaction_list_responses = {
    200: TransactionSerializer(many=True),
    400: 'Bad Request - Invalid bank account or not yours'
}

transaction_list_description = "Get transactions for a specific bank account with optional filters"
