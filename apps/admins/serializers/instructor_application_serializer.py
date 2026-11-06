from rest_framework import serializers

from apps.instructors.models import InstructorApplication


class AdminInstructorApplicationListSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    categories = serializers.SerializerMethodField()
    experience_years = serializers.IntegerField(read_only=True)
    experience_months = serializers.IntegerField(read_only=True)

    class Meta:
        model = InstructorApplication
        fields = (
            "id",
            "full_name",
            "email",
            "profile_image",
            "occupation",
            "experience_years",
            "experience_months",
            "status",
            "submitted_at",
            "categories",
        )

    def get_categories(self, obj):
        return list(obj.categories_to_teach.values_list("name", flat=True))


class AdminInstructorApplicationDetailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        source="user.email",
        read_only=True,
    )
    experience_years = serializers.IntegerField(read_only=True)
    experience_months = serializers.IntegerField(read_only=True)
    categories = serializers.SerializerMethodField()
    resume_url = serializers.SerializerMethodField()
    resume_name = serializers.SerializerMethodField()
    supporting_files = serializers.SerializerMethodField()

    class Meta:
        model = InstructorApplication
        fields = (
            "id",
            "full_name",
            "email",
            "profile_image",
            "phone_number",
            "location",
            "occupation",
            "education",
            "experience_years",
            "experience_months",
            "professional_bio",
            "motivation",
            "categories",
            "portfolio_url",
            "linkedin_url",
            "github_url",
            "submitted_at",
            "status",
            "resume_name",
            "resume_url",
            "supporting_files",
            "admin_message",
            "reviewed_at",
        )

    def get_categories(self, obj):
        return list(obj.categories_to_teach.values_list("name", flat=True))

    def get_resume_url(self, obj):
        if not obj.resume:
            return None

        url = obj.resume.url
        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(url)

        return url

    def get_resume_name(self, obj):
        if not obj.resume:
            return None

        return obj.resume.name.rsplit("/", 1)[-1]

    def get_supporting_files(self, obj):
        request = self.context.get("request")
        files = []

        for document in obj.supporting_documents.all():
            url = document.document.url

            if request:
                url = request.build_absolute_uri(url)

            files.append(
                {
                    "id": document.id,
                    "name": document.document.name.rsplit("/", 1)[-1],
                    "url": url,
                }
            )

        return files


class AdminInstructorApplicationRejectSerializer(serializers.Serializer):
    admin_message = serializers.CharField(
        required=True,
        allow_blank=False,
        trim_whitespace=True,
        max_length=2000,
    )


class AdminInstructorApplicationApproveSerializer(serializers.Serializer):
    admin_message = serializers.CharField(
        required=True,
        allow_blank=False,
        trim_whitespace=True,
        max_length=2000,
    )
