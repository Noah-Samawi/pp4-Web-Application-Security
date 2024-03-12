from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from autoslug import AutoSlugField
from django.urls import reverse
from .validators import textfield_not_empty
from django.utils.text import slugify


STATUS = ((0, "Save for later"), (1, "Publish Now"))


class SecurityFeature(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_security_features")
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now=True)
    description = models.TextField()
    method = models.TextField(validators=[textfield_not_empty])
    image = CloudinaryField('image', default='placeholder')
    status = models.IntegerField(choices=STATUS, default=1)
    bookmarks = models.ManyToManyField(
        User, related_name='bookmarks', blank=True)
    likes = models.ManyToManyField(
        User, related_name='blog_security_features_like', blank=True)    

    class Meta:
        """To display the security features by created_on in descending order"""
        ordering = ['-created_on']

    def get_absolute_url(self):
        """Get URL after the user adds/edits a security feature"""
        return reverse('securityfeature_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f"{self.title}"


class TechSecurityItem(models.Model):
    """Model for Tech Secur Item"""
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
        User, on_delete=models.CASCADE, related_name="tech_security")
    security_feature = models.ForeignKey(
        SecurityFeature, on_delete=models.CASCADE, related_name="tech_security_items")
    day = models.IntegerField(choices=DAY_CHOICES, default=0)

    class Meta:
        """To display the Tech Security Items by day in ascending order"""
        ordering = ['day']

    def __str__(self):
        return f"Tech Security for {self.day} by {self.user}"


class Comment(models.Model):
    """Model for Comment"""
    security_feature = models.ForeignKey(
        SecurityFeature, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)

    class Meta:
        """To display the comments by created_on in ascending order"""
        ordering = ['created_on']

    def __str__(self):
        return f"Comment {self.body} by {self.user.username}"
