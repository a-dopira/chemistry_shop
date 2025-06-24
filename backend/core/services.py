import os
import hashlib
from io import BytesIO
from PIL import Image
from django.core.cache import cache
import redis


class ImageCacheService:
    """service for caching images in redis and django cache"""

    SIZE_PRESETS = {
        "mini": (50, 50),
        "small": (150, 150),
        "medium": (300, 300),
        "large": (600, 600),
    }

    def __init__(self):
        self.redis_client = None
        try:
            self.redis_client = redis.Redis(host="127.0.0.1", port=6379, db=1)
        except Exception:
            raise Exception("Redis connection failed")

    def _get_image_hash(self, image_field, updated_at=None):
        """generates image hash"""
        if not image_field:
            return "no_image"

        try:
            content = f"{image_field.name}"
            if updated_at:
                content += f"_{updated_at.timestamp()}"

            if hasattr(image_field, "path") and os.path.exists(image_field.path):
                file_size = os.path.getsize(image_field.path)
                content += f"_{file_size}"

            return hashlib.md5(content.encode()).hexdigest()[:8]
        except Exception:
            if updated_at:
                return str(int(updated_at.timestamp()))[:8]
            return "default"

    def _generate_thumbnail(self, image_field, width, height):
        """generates thumbnail image and caches it in redis"""
        try:
            if not hasattr(image_field, "path") or not os.path.exists(image_field.path):
                return None

            with Image.open(image_field.path) as img:
                if img.mode in ["RGBA", "P"]:
                    img = img.convert("RGB")

                img.thumbnail((width, height), Image.Resampling.LANCZOS)

                buffer = BytesIO()
                img.save(buffer, format="JPEG", quality=85, optimize=True)

                return buffer.getvalue()

        except Exception as e:
            raise Exception(f"Error generating thumbnail: {e}")

    def get_cached_image_url(
        self, model_name, instance_id, image_field, size="medium", updated_at=None
    ):
        """returns cached image url"""
        if not image_field:
            return None

        width, height = self.SIZE_PRESETS.get(size, (300, 300))
        image_hash = self._get_image_hash(image_field, updated_at)

        cache_key = f"{model_name}_{instance_id}_{width}x{height}_{image_hash}"

        cached_data = cache.get(cache_key)
        if cached_data:
            return f"/{model_name}_image/{cache_key}/"

        thumbnail_data = self._generate_thumbnail(image_field, width, height)
        if thumbnail_data:
            cache.set(cache_key, thumbnail_data, timeout=60 * 60 * 24 * 30)
            return f"/{model_name}_image/{cache_key}/"

        return image_field.url

    def invalidate_cache(self, model_name, instance_id):
        """invalidates cache for model instance"""
        try:
            if self.redis_client:
                pattern = f"*{model_name}_{instance_id}_*"
                keys = self.redis_client.keys(pattern)
                if keys:
                    self.redis_client.delete(*keys)
            else:
                for size_name in self.SIZE_PRESETS.keys():
                    width, height = self.SIZE_PRESETS[size_name]
                    for i in range(10):
                        cache_key = f"{model_name}_{instance_id}_{width}x{height}_*"
                        cache.delete(cache_key)

        except Exception as e:
            raise Exception(f"Error invalidating cache: {e}")


image_cache_service = ImageCacheService()
