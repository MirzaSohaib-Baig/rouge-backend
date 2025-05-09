from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, get_object_or_404, DestroyAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .exceptions import *
from .serializers import *
from .utils import *


class JWTTokenView(TokenObtainPairView):
    pass

# LogIn / LogOut JWT
class LoginView(APIView):

    @staticmethod
    def post(request):
        serializer = LoginSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            return create_200_response("Login successful", serializer.validated_data)
        return create_400_response(message=list(serializer.errors.values())[0][0])

class LogoutView(APIView):

    @staticmethod
    def post(request):
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return create_400_response(message="Refresh token is required")
        token = RefreshToken(refresh_token)
        token.blacklist()
        return create_205_response(message="Logout successful")


# Users All

class UserListActiveView(ListAPIView):

    serializer_class = UserSerializer
    permission_classes = []
    authentication_classes = []
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_queryset(self):
        """Return all users active"""
        return UserModel.objects.filter(is_active=True)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        if serializer:
            return create_200_response(message="Users Fetched Successfully", data=serializer.data)
        return create_400_response(message=list(serializer.errors.values())[0][0])

class UserListInActiveView(ListAPIView):

    serializer_class = UserSerializer
    permission_classes = []
    authentication_classes = []
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_queryset(self):
        """Return all users inactive"""
        return UserModel.objects.filter(is_active=False)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        if serializer:
            return create_200_response(message="Users Fetched Successfully", data=serializer.data)
        return create_400_response(message=list(serializer.errors.values())[0][0])

class UserListIdView(ListAPIView):

    serializer_class = UserSerializer
    permission_classes = []
    authentication_classes = []

    def list(self, request, *args, **kwargs):
        with transaction.atomic():
            user = request.user
            if not user:
                return create_404_response(message="User Not Found", data={})
            serializer = self.get_serializer(user)
            if serializer:
                return create_200_response(message="User Fetched Successfully", data=serializer.data)
            return create_400_response(message=list(serializer.errors.values())[0][0])

class UserRegisterView(CreateAPIView):

    serializer_class = UserSerializer
    permission_classes = []
    authentication_classes = []
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save(is_active=False, is_verified=False)
                # send_verification_email(user)
                return create_200_response(message="User registered successfully.")
            return create_400_response(message=list(serializer.errors.values())[0][0])

class UserVerifyView(APIView):

    queryset = UserModel.objects.none()
    pagination_class = None

    def get(self, request, *args, **kwargs):
        token = self.kwargs.get('token')
        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            user = UserModel.objects.get(id=user_id)
            if not user.is_active:
                user.is_active = True
                user.is_verified = True
                user.save()
            return create_200_response(message=f"Dear {user.first_name} {user.last_name}, your account is Successfully activated")
        except Exception as e:
            return create_400_response(message="Invalid or expired token")

class UserUpdateView(UpdateAPIView):

    serializer_class = UserSerializer
    permission_classes = []
    authentication_classes = []
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    lookup_field = "id"

    def get_queryset(self):
        """Get all users linked to the authenticated client."""
        return UserModel.objects.all()

    def update(self, request, *args, **kwargs):
        """Handle both PUT (full update) and PATCH (partial update)."""
        partial = request.method == "PATCH"
        user_id = self.kwargs.get("id")
        user = get_object_or_404(self.get_queryset(), id=user_id)
        serializer = self.get_serializer(user, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save(is_active=True)
            return create_200_response(message="User Updated Successfully", data=serializer.data)
        return create_400_response(message=list(serializer.errors.values())[0][0])

class UserDeleteView(DestroyAPIView):

    serializer_class = UserSerializer
    permission_classes = []
    authentication_classes = []
    lookup_field = "id"

    def get_queryset(self):
        """Return all users linked to the authenticated client"""
        return UserModel.objects.all()

    def destroy(self, request, *args, **kwargs):
        """Soft delete the user by deactivating the account"""
        user_id = self.kwargs.get("id")
        user = get_object_or_404(self.get_queryset(), id=user_id)
        user.is_active = False
        user.save()
        return create_200_response(message="User Deleted Successfully")


# Passwords
class PasswordResetView(UpdateAPIView):

    serializer_class = UserSerializer
    permission_classes = []
    authentication_classes = []
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def patch(self, request, *args, **kwargs):

        with transaction.atomic():
            password = request.data.get("password")
            confirm_password = request.data.get("confirmPassword")
            print(request.data)
            if not password or not confirm_password:
                return create_400_response(message="Password fields are required.")

            if password != confirm_password:
                return create_400_response(message="Passwords do not match.")

            try:
                validate_password(password)
            except ValidationError as e:
                return create_400_response(message=e.detail)

            user = self.request.user
            user.set_password(confirm_password)
            user.save()

            return create_200_response(message="Password updated successfully.")

class ForgotPassword(APIView):

    serializer_class = UserSerializer
    permission_classes = []
    authentication_classes = []
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            user_data = self.request.data
            if 'phone' in user_data:
               user = UserModel.objects.get(phone=user_data['phone'])
            if 'email' in user_data:
                user = UserModel.objects.get(email=user_data['email'])

            new_password = secrets.token_urlsafe(8)
            user.set_password(new_password)
            user.save()

            send_password_reset_email(user, new_password)

            return create_200_response(message="New Password Send to your Email")
#______________________________________________________________________________________________________________________


class GroupDetailView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific group.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = []

class PermissionListView(ListAPIView):
    """
    List all available permissions.
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = []

# dropdowns______________________________________________________________________________________________________________________
class Countries(ListAPIView):

    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        if serializer:
            return create_200_response(message="Countries Fetched Successfully", data=serializer.data)
        return create_400_response(message=list(serializer.errors.values())[0][0])

class Regions(ListAPIView):

    queryset = Region.objects.all()
    serializer_class = RegionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        if serializer:
            return create_200_response(message="Regions Fetched Successfully", data=serializer.data)
        return create_400_response(message=list(serializer.errors.values())[0][0])

class Cities(ListAPIView):

    queryset = City.objects.all()
    serializer_class = CitySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        if serializer:
            return create_200_response(message="Cities Fetched Successfully", data=serializer.data)
        return create_400_response(message=list(serializer.errors.values())[0][0])