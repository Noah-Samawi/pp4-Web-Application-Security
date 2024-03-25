"""Views"""

from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views import generic, View
from .models import SecurityFeature, TechSecurityItem, Comment
from .forms import CommentForm, SecurityFeatureForm, TechSecurityForm


class Home(generic.TemplateView):
    """This view is used to display the home page"""
    template_name = "index.html"


class SecurityFeatureList(generic.ListView):
    """
    This view is used to display all security
    features in the browse securityfeatures page
    """
    model = SecurityFeature
    queryset = SecurityFeature.objects.filter(status=1).order_by("-created_on")
    template_name = "browse_securityfeatures.html"
    paginate_by = 8


class SecurityFeatureDetail(View):
    """Full SecurityFeature View, Single SecurityFeature per page"""

    def get(self, request, slug, *args, **kwargs):
        """Get function to obtain all information for securityfeature detail page"""
        queryset = SecurityFeature.objects.filter(status=1, slug=slug)
        securityfeature = get_object_or_404(queryset, slug=slug)
        comments = securityfeature.comments.order_by('created_on')  # Fix applied here
        liked = False
        bookmarked = False

        if securityfeature.likes.filter(id=self.request.user.id).exists():
            liked = True

        if securityfeature.bookmarks.filter(id=self.request.user.id).exists():
            bookmarked = True

        return render(
            request,
            "securityfeature_detail.html",
            {
                "securityfeature": securityfeature,
                "comments": comments,
                "bookmarked": bookmarked,
                "liked": liked,
                "comment_form": CommentForm(),
            },
        )

    def post(self, request, slug, *args, **kwargs):
        """Post function for comment form on securityfeature detailed page"""
        queryset = SecurityFeature.objects.filter(status=1, slug=slug)
        securityfeature = get_object_or_404(queryset, slug=slug)
        comments = securityfeature.comments.order_by('created_on')  # Fix applied here
        liked = False
        bookmarked = False

        if securityfeature.likes.filter(id=self.request.user.id).exists():
            liked = True

        if securityfeature.bookmarks.filter(id=self.request.user.id).exists():
            bookmarked = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user  # Assign the current user to the comment's user field
            comment.security_feature = securityfeature  # Associate the comment with the security feature
            comment.save()
            messages.success(request, 'Comment Successfully Added')
        else:
            comment_form = CommentForm()

        return render(
            request,
            "securityfeature_detail.html",
            {
                "securityfeature": securityfeature,
                "comments": comments,
                "liked": liked,
                "bookmarked": bookmarked,
                "comment_form": CommentForm(),
            },
        )


class SecurityFeatureLike(View):
    """Add a like to a securityfeature"""

    def post(self, request, slug):
        """
        Find securityfeature and post like (user-id) to model
        See Credit 9. in README
        """
        securityfeature = get_object_or_404(SecurityFeature, slug=slug)
        origin = request.META.get("HTTP_REFERER")

        if securityfeature.likes.filter(id=request.user.id).exists():
            securityfeature.likes.remove(request.user)
            messages.success(request, 'Like successfully removed')
        else:
            securityfeature.likes.add(request.user)
            messages.success(request, 'Like successfully added')
        return redirect(origin)


class AddSecurityFeature(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    """This view is used to allow logged in users to create a security feature"""
    form_class = SecurityFeatureForm
    template_name = 'add_securityfeature.html'
    success_message = "%(calculated_field)s was created successfully"

    def form_valid(self, form):
        """
        This method is called when valid form data has been posted.
        The signed in user is set as the author of the securityfeature.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        """
        This function overrides the get_success_message() method to add
        the security feature title into the success message.
        source: https://docs.djangoproject.com/en/4.0/ref/contrib/messages/
        """
        return self.success_message % dict(
            cleaned_data,
            calculated_field=self.object.title,
        )


class MySecurityFeatures(LoginRequiredMixin, generic.ListView):
    """
    This view is used to display a list of security features created by the logged in
    user.
    """
    model = SecurityFeature
    template_name = 'my_securityfeatures.html'
    paginate_by = 8

    def get_queryset(self):
        """Override get_queryset to filter by user"""
        return SecurityFeature.objects.filter(author=self.request.user)


class UpdateSecurityFeature(
        LoginRequiredMixin, UserPassesTestMixin,
        SuccessMessageMixin, generic.UpdateView
        ):

    """
    This view is used to allow logged in users to edit their own securityfeatures
    """
    model = SecurityFeature
    form_class = SecurityFeatureForm
    template_name = 'update_securityfeature.html'
    success_message = "%(calculated_field)s was edited successfully"

    def form_valid(self, form):
        """
        This method is called when valid form data has been posted.
        The signed in user is set as the author of the securityfeature.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """
        Prevent another user from updating other's securityfeatures
        """
        securityfeature = self.get_object()
        return securityfeature.author == self.request.user

    def get_success_message(self, cleaned_data):
        """
        Override the get_success_message() method to add the securityfeature title
        into the success message.
        source: https://docs.djangoproject.com/en/4.0/ref/contrib/messages/
        """
        return self.success_message % dict(
            cleaned_data,
            calculated_field=self.object.title,
        )


class DeleteSecurityFeature(
        LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    """
    This view is used to allow logged in users to delete their own securityfeatures
    """
    model = SecurityFeature
    template_name = 'delete_securityfeature.html'
    success_message = "SecurityFeature deleted successfully"
    success_url = reverse_lazy('my_securityfeatures')

    def test_func(self):
        """
        Prevent another user from deleting other's securityfeatures
        """
        securityfeature = self.get_object()
        return securityfeature.author == self.request.user

    def delete(self, request, *args, **kwargs):
        """
        This function is used to display sucess message given
        SucessMessageMixin cannot be used in generic.DeleteView.
        Credit: https://stackoverflow.com/questions/24822509/
        success-message-in-deleteview-not-shown
        """
        messages.success(self.request, self.success_message)
        return super(DeleteSecurityFeature, self).delete(request, *args, **kwargs)


class BookmarkSecurityFeature(LoginRequiredMixin, View):
    """
    This view allows a logged in user to bookmark securityfeatures.
    """
    def post(self, request, slug):
        """
        Checks if user id already exists in the favourites
        field in the SecurityFeature database.
        If they exist then remove them from the database.
        If they don't exist then add them to the database.
        """
        securityfeature = get_object_or_404(SecurityFeature, slug=slug)
        if securityfeature.bookmarks.filter(id=request.user.id).exists():
            securityfeature.bookmarks.remove(request.user)
            messages.success(self.request, 'SecurityFeature removed from bookmarks')
        else:
            securityfeature.bookmarks.add(request.user)
            messages.success(self.request, 'SecurityFeature added to bookmarks')

        return HttpResponseRedirect(reverse('securityfeature_detail', args=[slug]))


class MyBookmarks(LoginRequiredMixin, generic.ListView):
    """
    This view allows a logged in user to view their bookmarked securityfeatures.
    """
    model = SecurityFeature
    template_name = 'my_bookmarks.html'
    paginate_by = 8

    def get_queryset(self):
        """Override get_queryset to filter by user favourites"""
        return SecurityFeature.objects.filter(bookmarks=self.request.user.id)


class TechSecurity(LoginRequiredMixin, View):
    """This view renders the logged in user's Tech Security"""

    def get(self, request):
        """
        Filters the TechSecurityItems table by user and creates a dictionary with
        day and tech security item as a key, value pair.
        """
        user_tech_security_items = TechSecurityItem.objects.filter(user=request.user)

        days = {
            0: 'Monday',
            1: 'Tuesday',
            2: 'Wednesday',
            3: 'Thursday',
            4: 'Friday',
            5: 'Saturday',
            6: 'Sunday'
        }
        techsecurity = {}

        for ind, day in days.items():
            # Retrive tech security item based on day
            day_tech_security_item = user_tech_security_items.filter(day=ind).first()
            # Add to tech security if it exists
            techsecurity[day] = day_tech_security_item or None

        return render(
            request, 'techsecurity.html', {'techsecurity': techsecurity})


class UpdateComment(
        LoginRequiredMixin, UserPassesTestMixin,
        SuccessMessageMixin, generic.UpdateView):

    """
    This view is used to allow logged in users to edit their own comments
    """
    model = Comment
    form_class = CommentForm
    template_name = 'update_comment.html'
    success_message = "Comment edited successfully"

    def form_valid(self, form):
        """
        This method is called when valid form data has been posted.
        The signed in user is set as the author of the comment.
        """
        form.instance.name = self.request.user.username
        return super().form_valid(form)

    def test_func(self):
        """
        Prevent another user from editing user's comments
        """
        comment = self.get_object()
        return comment.name == self.request.user.username

    def get_success_url(self):
        """ Return to securityfeature detail view when comment updated sucessfully"""
        securityfeature = self.object.securityfeature
        return reverse_lazy('securityfeature_detail', kwargs={'slug': securityfeature.slug})


class DeleteComment(
        LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):

    """
    This view is used to allow logged in users to delete their own comments
    """
    model = Comment
    template_name = 'delete_comment.html'
    success_message = "Comment deleted successfully"

    def test_func(self):
        """
        Prevent another user from deleting user's comments
        """
        comment = self.get_object()
        return comment.name == self.request.user.username

    def delete(self, request, *args, **kwargs):
        """
        This function is used to display success message given
        SuccessMessageMixin cannot be used in generic.DeleteView.
        Credit: https://stackoverflow.com/questions/24822509/
        success-message-in-deleteview-not-shown
        """
        messages.success(self.request, self.success_message)
        return super(DeleteComment, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        """ Return to securityfeature detail view when comment deleted successfully"""
        securityfeature = self.object.securityfeature
        return reverse_lazy('securityfeature_detail', kwargs={'slug': securityfeature.slug})

