from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from cloudinary.models import CloudinaryField
from .validators import textfield_not_empty

# Define choices for the 'status' field
STATUS_CHOICES = (
    (0, "Save for later"),
    (1, "Publish Now")
)


class SecurityFeature(models.Model):
    """Model for security feature"""
    title = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from='title', unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="security_features")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    setup_time = models.CharField(max_length=10, default='0')  # Ensure default value is string
    search_time = models.CharField(max_length=10, default='0')  # Ensure default value is string
    description = models.TextField()
    method = models.TextField(validators=[textfield_not_empty])
    image = CloudinaryField('image', default='placeholder')
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    bookmarks = models.ManyToManyField(User, related_name='bookmarks', blank=True)  # Default can be blank
    likes = models.ManyToManyField(User, related_name='liked_security_features', blank=True)  # Default can be blank

    class Meta:
        """Meta options"""
        ordering = ['-created_on']
        verbose_name = "Security Feature"
        verbose_name_plural = "Security Features"

    def get_absolute_url(self):
        """Return the absolute URL for a security feature"""
        return reverse('securityfeature_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    def number_of_likes(self):
        """Return the number of likes for this security feature"""
        return self.likes.count()


class TechSecurityItem(models.Model):
    """Model for tech security item"""
    DAY_CHOICES = [
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tech_security_items")
    security_feature = models.ForeignKey(SecurityFeature, on_delete=models.CASCADE, related_name="tech_security_items")
    day = models.IntegerField(choices=DAY_CHOICES, default=0)

    class Meta:
        """Meta options"""
        ordering = ['day']
        verbose_name = "Tech Security Item"
        verbose_name_plural = "Tech Security Items"

    def __str__(self):
        return f"{self.get_day_display()} Tech Security by {self.user}"


class Comment(models.Model):
    """Model for Comment"""
    security_feature = models.ForeignKey(SecurityFeature, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta options"""
        ordering = ['-created_on']
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return f"Comment by {self.name}"
