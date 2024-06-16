from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample, OpenApiResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Transaction
from .serializers import TransactionSerializer

# Create your views here.
@extend_schema_view(
        get=extend_schema(
            operation_id='Get All Transactions',
            description='Get a list of all transactions',
            summary='Get a list of all transactions',
            responses={
                200: OpenApiResponse(
                    response=TransactionSerializer(many=True),
                    description='Returns a list of transactions'
            )  
        }
    ) 
)


@extend_schema_view(
    post=extend_schema(
        operation_id='Create a Transaction',
        summary='Create one Transaction',
        responses={
            200: OpenApiResponse(
                response=TransactionSerializer(many=True),
                description="Creates a Transaction"
            ),
            400: OpenApiResponse(
                response={'Transaction Not Created'},
                description='Null value in required field',
                examples=[
                    OpenApiExample('Serializer Error: Transaction Type',
                    description='Null value provided for required transaction_type field',
                    value={'transaction_type': "['This field is required.']"}
                    )
                ]
            )
        }
    )
)    

class TransactionListApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    # List all transactions
    def get(self, request, *args, **kwargs):
        """
        List all transactions
        """
        transactions = Transaction.objects.filter()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Create a transaction
    def post(self, request, *args, **kwargs):
        """
        Create a new transaction
        """
        data = {
            'transaction_type': request.data.get('transaction_type'),
            'credit_from': request.data.get('credit_from'),
            'debit_to': request.data.get('debit_to'),
            'amount': request.data.get('amount'),
            'currency': request.data.get('currency'),
            'date': request.data.get('date'),
            'status': request.data.get('status')
        }
        serializer = TransactionSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
                            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@extend_schema_view(
    get=extend_schema(
        operation_id='Get a Transaction',
        summary='Get a single transaction based on the provided ID',
        responses={
            200: TransactionSerializer(many=True),
            400: OpenApiResponse(
                response={'Transaction Not Found'},
                description='Object does not exist',
                examples=[
                OpenApiExample(
                    'Transaction does not exist',
                    description='Object with transaction id does not exist',
                    value={ 
                        'res':'Object with transaction id does not exist'})
                ]
            )
        }
    )
) 

@extend_schema_view(
    put=extend_schema(
        operation_id='Update a Transaction',
        summary='Update a single transaction based on the provided ID',
        responses={
            200: OpenApiResponse(
                response=TransactionSerializer
            ),
            400: OpenApiResponse(
                response={'Currency must be a 3 character ISO code'},
                examples=[
                    OpenApiExample(
                        'Currency code Bad Request',
                        description='Currency code validation fails',
                        value={'detail': 'Currency must be a 3 character ISO code'}
                    )
                ]
            )
        }
    )
)

@extend_schema_view(
    delete=extend_schema(
        operation_id='Delete a Transaction',
        summary='Delete a transaction based on the provided ID',
        responses={
            200: OpenApiResponse(
                response={'Success'},
                examples=[
                    OpenApiExample(
                        'Deletion Success',
                        description='Custom delete response for Transaction',
                        value={'res': 'Transaction deleted'}
                    )
                ]
            ),
            400: OpenApiResponse(
                response={'Transaction Not Found'},
                examples=[
                    OpenApiExample(
                        'Transaction does not exist',
                        description='Custom delete bad request response for Transaction',
                        value={'res': 'Object with given transaction id does not exist'}
                    )
                ]
            )
        }
    )
)

class TransactionDetailApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id):
        """
        Helper method to retrieve the object with a given id
        """
        try:
            return Transaction.objects.get(id=id) 
        except Transaction.DoesNotExist:
            return None

    # Get a single transaction
    def get(self, request, id, *args, **kwargs):
        """
        Retrieves the Transaction with the given id
        """

        transaction_instance = self.get_object(id)
        if not transaction_instance:
            return Response(
                {"res": "Object with transaction id does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = TransactionSerializer(transaction_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Update a single transaction
    def put(self, request, id, *args, **kwargs):
        """
        Updates the transaction with the given id if it exists
        """
        transaction_instance = self.get_object(id)
        if not transaction_instance:
            return Response(
                {"res": "Object with given transaction id does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )
        
        data = {
            'transaction_type': request.data.get('transaction_type'),
            'credit_from': request.data.get('credit_from'),
            'debit_to': request.data.get('debit_to'),
            'amount': request.data.get('amount'),
            'currency': request.data.get('currency'),
            'date': request.data.get('date'),
            'status': request.data.get('status')
        }
        serializer = TransactionSerializer(instance=transaction_instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Delete a single transaction
    def delete(self, request, id, *args, **kwargs):
        """
        Deletes the transaction with the given id if it exists
        """
        transaction_instance = self.get_object(id)
        if not transaction_instance:
            return Response(
                {"res": "Object with given transaction id does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )
        
        transaction_instance.delete()
        return Response(
            {"res": "Transaction deleted"},
            status=status.HTTP_200_OK
        )    