from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from gait_integration.persmissions import HasRole
from gait_integration.utils import get_user_id, get_user_role


class WhoAmIView(APIView):
    """
    Simple debug view to confirm auth integration.
    Requires a valid JWT and returns your user claims.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "user_id": get_user_id(request),
            "role": get_user_role(request),
            "claims": request.user_claims,
        })


class AdminOnlyView(APIView):
    """
    Example of role-protected endpoint.
    Only accessible to users with role='admin'.
    """
    permission_classes = [HasRole("admin")]

    def get(self, request):
        return Response({"message": "You are an admin. Access granted!"})
