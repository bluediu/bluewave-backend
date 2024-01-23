from rest_framework import serializers


class Serializer(serializers.Serializer):
    """
    Define API base serializer.

    The `create` and `update` methods of DRF serializers are
    overridden to exclude business logic, which should reside
    in the models for simple cases or services for more complex
    scenarios.
    """

    def create(self, validated_data):
        """Invalidate serializer instance creation."""
        raise NotImplementedError()

    def update(self, instance, validated_data):
        """Invalidate serializer instance update."""
        raise NotImplementedError()

    def check_data(self) -> None:
        """Check data validity and raise an exception if not."""
        self.is_valid(raise_exception=True)


def inline_serializer(
    *,
    name: str,
    base: type[Serializer] = Serializer,
    fields: dict,
    **kwargs,
):
    """Return a nested inlined serializer."""
    return type(name, (base,), fields)(**kwargs)
