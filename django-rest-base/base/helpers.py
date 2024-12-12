from django.shortcuts import _get_queryset


def get_or_none(cls, *args, **kwargs):
    qs = _get_queryset(cls)
    try:
        obj = qs.get(*args, **kwargs)
    except qs.model.DoesNotExist:
        obj = None
    return obj


def get_response_message(data, model, action="create"):
    obj_response_message = data.get("response_message", None)
    response_message = f"{obj_response_message} {action}d successfully"
    return response_message
