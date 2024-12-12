from model_utils.models import TimeStampedModel


class BaseModel(TimeStampedModel):
    ORDERING = ("-created",)

    class Meta:
        abstract = True