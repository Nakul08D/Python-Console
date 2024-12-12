import django_filters

from src.user import models
from base import filters


class UserFilter(filters.BaseFilter):
    name = django_filters.CharFilter(lookup_expr="icontains", field_name="name")
    mobile_number = django_filters.CharFilter(
        lookup_expr="icontains", field_name="mobile_number"
    )
    email = django_filters.CharFilter(lookup_expr="icontains", field_name="email")

    class Meta:
        model = models.User
        fields = ("is_active",)

    ordering = filters.BaseOrderingFilter(fields=(("id", "id"),))