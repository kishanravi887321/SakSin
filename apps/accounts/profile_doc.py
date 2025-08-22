from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

profile_image_upload_doc = swagger_auto_schema(
    operation_description="Upload profile image",
    manual_parameters=[
        openapi.Parameter(
            name="profile_image",
            in_=openapi.IN_FORM,
            type=openapi.TYPE_FILE,
            description="Image to upload",
            required=True
        )
    ]
)
