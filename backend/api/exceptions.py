from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException

class UserNotFoundException(APIException):
    status_code = 404
    default_detail = "User not found"
    default_code = "user_not_found"

class AnnouncementNotFoundException(APIException):
    status_code = 404
    default_detail = "Announcement not found"
    default_code = "announcement_not_found"

class UnauthorizedAccessException(APIException):
    status_code = 403
    default_detail = "You do not have permission to perform this action"
    default_code = "unauthorized_access"

class ValidationErrorException(APIException):
    status_code = 400
    default_detail = "Validation error"
    default_code = "validation_error"

def custom_exception_handler(exc, context):
    # Wywołaj domyślny handler DRF, aby uzyskać standardową odpowiedź
    response = exception_handler(exc, context)

    # Jeśli odpowiedź istnieje, dostosuj ją do ustrukturyzowanego formatu JSON
    if response is not None:
        return Response(
            {
                "error": response.data.get("detail", "An error occurred"),
                "status": response.status_code,
            },
            status=response.status_code,
        )

    # Jeśli odpowiedź nie istnieje (np. błąd serwera), zwróć ogólny błąd
    return Response(
        {
            "error": "Internal server error",
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )