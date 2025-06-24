from django.db import models

from core.services import image_cache_service


class ImageCacheMixin(models.Model):
    """mixin for caching images"""

    class Meta:
        abstract = True

    def get_cached_image_url(self, image_field_name, size="medium"):
        """get cached image url"""
        image_field = getattr(self, image_field_name, None)
        if not image_field:
            return None

        updated_at = getattr(self, "time_update", None) or getattr(
            self, "updated_at", None
        )

        return image_cache_service.get_cached_image_url(
            model_name=self.__class__.__name__.lower(),
            instance_id=self.pk,
            image_field=image_field,
            size=size,
            updated_at=updated_at,
        )

    def invalidate_image_cache(self):
        """flush image cache for this instance"""
        image_cache_service.invalidate_cache(
            model_name=self.__class__.__name__.lower(), instance_id=self.pk
        )
