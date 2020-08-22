from django.urls import reverse_lazy


def get_admin_urls(prefix, obj):
    return (
        reverse_lazy(f"{prefix}_changelist"),
        reverse_lazy(f"{prefix}_add"),
        reverse_lazy(f"{prefix}_history", args=(obj.id,)),
        reverse_lazy(f"{prefix}_delete", args=(obj.id,)),
        reverse_lazy(f"{prefix}_change", args=(obj.id,)),
    )
