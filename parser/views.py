from django.shortcuts import render
from rest_framework.views import APIView, status
from rest_framework.generics import ListAPIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from .models import Transaction, Type
from .serializers import TransactionSerializer, UploadSerializer, StoreSerializer


# Create your views here.
class CreateCNAB(APIView):
    serializer_class = UploadSerializer

    def post(self, request):
        file = request.FILES["file"]
        myArray = []
        for line in file:

            myArray.append(
                {
                    "type": Type.objects.filter(id=int(line[0:1])).first(),
                    "date": f"${line[1:5]}-{line[5:7]}-{line[7:9]}".replace("$b'", "")
                    .replace("b'", "")
                    .replace("'", ""),
                    "value": float(str(line[9:19]).lstrip("b'0")[:-1]) / 100,
                    "cpf": str(line[19:30]).strip("b'"),
                    "cardNum": str(line[30:42]).strip("b'"),
                    "hour": f"{line[42:44]}:{line[44:46]}:{line[46:48]}".replace(
                        "$b'", ""
                    )
                    .replace("b'", "")
                    .replace("'", ""),
                    "owner": line[48:62].decode("utf-8").strip(" "),
                    "store": line[62:81].decode("utf-8").strip(" \n"),
                }
            )
        returnArray = []
        for transaction in myArray:

            serializer = TransactionSerializer(data=transaction)
            serializer.is_valid(raise_exception=True)
            serializer.save(type=transaction["type"])
            returnArray.append(serializer.data)

        return Response(returnArray, status.HTTP_200_OK)


class ListOperations(APIView):
    def get(self, request, store_name):
        transactions = Transaction.objects.filter(store__icontains=store_name)
        total = sum(
            [
                item.value if item.type.nature == "Entrada" else -item.value
                for item in transactions
            ]
        )

        transactions = TransactionSerializer(transactions, many=True)

        return Response(
            {
                "store": store_name,
                "saldo": total,
                "transactions": transactions.data,
            },
            status.HTTP_200_OK,
        )
