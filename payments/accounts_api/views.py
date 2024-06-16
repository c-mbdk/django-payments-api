from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample, OpenApiResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Account
from .serializers import AccountSerializer

# Create your views here.
@extend_schema_view(
        get=extend_schema(
            operation_id='Get All Accounts',
            summary='Get a list of all accounts',
            responses={
                200: OpenApiResponse(
                    response=AccountSerializer(many=True),
                    description='Returns a list of accounts'
            )  
        }
    ) 
)

@extend_schema_view(
    post=extend_schema(
        operation_id='Create an Account',
        summary='Create one Account',
        responses={
            200: OpenApiResponse(
                response=AccountSerializer(many=True),
                description="Creates an account"
            ),
            400: OpenApiResponse(
                response={'Serializer Error: Status'},
                description='Null value in required field',
                examples=[
                    OpenApiExample('Serializer Error: Account Name',
                    description='Null value provided for required account_name field',
                    value={'account_name': "['This field is required.']"}
                    )
                ]
            )
        }
    )
) 

class AccountListApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    # List all
    def get(self, request, *args, **kwargs):
        """
        List all the accounts
        """
        accounts = Account.objects.filter()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Create
    def post(self, request, *args, **kwargs):
        """
        Create an account with the given account data
        """
        data = {
            'account_name': request.data.get('account_name'),
            'status': request.data.get('status'),
            'balance': request.data.get('balance'),
            'currency': request.data.get('currency')
        }
        serializer = AccountSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
                            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@extend_schema_view(
    get=extend_schema(
        operation_id='Get an Account',
        summary='Get a single account based on the provided ID',
        responses={
            200: AccountSerializer(many=True),
            400: OpenApiResponse(
                response={'Object with account id does not exist'},
                description='Object does not exist',
                examples=[
                OpenApiExample(
                    'Account does not exist',
                    description='Object with account id does not exist',
                    value={ 
                        'res':'Object with account id does not exist'})
                ]
            )
        }
    )
)    

@extend_schema_view(
    put=extend_schema(
        operation_id='Update an Account',
        summary='Update a single Account based on the provided ID',
        responses={
            200: OpenApiResponse(
                response=AccountSerializer
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
        operation_id='Delete an Account',
        summary='Delete an account based on the provided ID',
        responses={
            200: OpenApiResponse(
                response={'Success'},
                examples=[
                    OpenApiExample(
                        'Deletion Success',
                        description='Custom delete response for Account',
                        value={'res': 'Account deleted'}
                    )
                ]
            ),
            400: OpenApiResponse(
                response={'Account Not Found'},
                examples=[
                    OpenApiExample(
                        'Account does not exist',
                        description='Custom delete bad request response for Transaction',
                        value={'res': 'Object with given account id does not exist'}
                    )
                ]
            )
        }
    )
)

class AccountDetailApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]  

    def get_object(self, id):
        """
        Helper method to retrieve the object with a given id
        """

        try:
            return Account.objects.get(id=id)
        except Account.DoesNotExist:
            return None

    # Get a single account
    def get(self, request, id, *args, **kwargs):
        """
        Retrieves the Account with the given id
        """

        account_instance = self.get_object(id)
        if not account_instance:
            return Response(
                {"res": "Object with account id does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = AccountSerializer(account_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Update a single account
    def put(self, request, id, *args, **kwargs):
        """
        Updates the account with the given id if it exists
        """
        account_instance = self.get_object(id)
        if not account_instance:
            return Response(
                {"res": "Object with given account id does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'account_name': request.data.get('account_name'),
            'status': request.data.get('status'),
            'status_valid_to': request.data.get('status_valid_to'),
            'balance': request.data.get('balance'),
            'currency': request.data.get('currency')
        }
        serializer = AccountSerializer(instance=account_instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Delete a single account
    def delete(self, request, id, *args, **kwargs):
        """
        Deletes the account with the given id if it exists
        """
        account_instance = self.get_object(id)
        if not account_instance:
            return Response(
                {"res": "Object with given account id does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )
        
        account_instance.delete()
        return Response(
            {"res": "Account deleted"},
            status=status.HTTP_200_OK
        )