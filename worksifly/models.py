from django.db import models, migrations
from django.contrib.auth.models import User
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from cloudinary.models import CloudinaryField
from .validators import textfield_not_empty

STATUS = ((0, "Save for later"), (1, "Publish Now"))


class SecurityFeature(models.Model):
    """Model for security feature"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_security_features")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    description = models.TextField()
    method = models.TextField(validators=[textfield_not_empty])
    image = CloudinaryField('image', default='placeholder')
    status = models.IntegerField(choices=STATUS, default=1)
    bookmarks = models.ManyToManyField(
        User, related_name='bookmarks', blank=True)
    likes = models.ManyToManyField(
        User, related_name='blog_security_features_like', blank=True)
    # Added default value for the excerpt field
    excerpt = models.CharField(max_length=255, default='')


    class Meta:
        """To display the security features by created_on in ascending order"""
        ordering = ['-created_on']

    def get_absolute_url(self):
        """Return the url to access a particular security feature"""
        return reverse('securityfeature_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f"{self.title}"


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
        User, on_delete=models.CASCADE, related_name="tech_security")
    security_feature = models.ForeignKey(
        SecurityFeature, on_delete=models.CASCADE, related_name="tech_security_item")
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now=True)

    class Meta:
        """To display the comments by created_on in ascending order"""
        ordering = ['created_on']

    def __str__(self):
        return f"Comment {self.body} by {self.user.username}"


    # class Migration(migrations.Migration):

    #     dependencies = [
    #         ('worksifly', '0001_initial'),
    #     ]

    #     operations = [
    #         migrations.RunSQL(
    #             'DROP TABLE worksifly_securityfeature_bookmarks;',
    #             reverse_sql='CREATE TABLE worksifly_securityfeature_bookmarks(...);'
    #         ),
    #     ]