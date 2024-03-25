from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from cloudinary.models import CloudinaryField
from .validators import textfield_not_empty

STATUS = ((0, "Save for later"), (1, "Publish Now"))


class SecurityFeature(models.Model):
    """Model for security feature"""
    title = models.CharField(max_length=50, unique=True)
    slug = AutoSlugField(populate_from='title', unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="security_features")
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now=True)
    setup_time = models.CharField(max_length=10, default=0)
    search_time = models.CharField(max_length=10, default=0)
    description = models.TextField()
    method = models.TextField(validators=[textfield_not_empty])
    image = CloudinaryField('image', default='placeholder')
    status = models.IntegerField(choices=STATUS, default=1)
    bookmarks = models.ManyToManyField(
        User, related_name='bookmarks', default=None, blank=True)
    likes = models.ManyToManyField(
        User, related_name='liked_security_features', blank=True)

    class Meta:
        """To display the security features by created_on in descending order"""
        ordering = ['-created_on']

    def get_absolute_url(self):
        """Return the url to access a particular security feature"""
        return reverse('securityfeature_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f"{self.title}"

    def number_of_likes(self):
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

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tech_security_items")
    security_feature = models.ForeignKey(
        SecurityFeature, on_delete=models.CASCADE, related_name="tech_security_items")
    day = models.IntegerField(choices=DAY_CHOICES, default=0)

    class Meta:
        """To display the tech security items by day in ascending order"""
        ordering = ['day']

    def __str__(self):
        return f"Tech Security for {self.day} by {self.user}"


class Comment(models.Model):
    """Model for Comment"""
    security_feature = models.ForeignKey(
        SecurityFeature, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now=True)

    class Meta:
        """To display the comments by created_on in descending order"""
        ordering = ['-created_on']

    def __str__(self):
        return f"Comment {self.body} by {self.name}"
