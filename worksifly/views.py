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
    This view is used to display all securityfeatures in the browse securityfeatures page
    """
    model = SecurityFeature
    queryset = SecurityFeature.objects.filter(status=1).order_by('-created_on')
    template_name = 'browse_securityfeatures.html'
    paginate_by = 8


class SecurityFeatureDetail(View):
    """
    This view is used to display the full securityfeature details including comments.
    It also includes the comment form and add to tech security form
    """
    def get(self, request, slug):
        """
        Retrives the securityfeature and related comments from the database
        """
        queryset = SecurityFeature.objects.all()
        securityfeature = get_object_or_404(queryset, slug=slug)
        comments = securityfeature.comments.order_by('created_on')
        bookmarked = False
        if securityfeature.bookmarks.filter(id=self.request.user.id).exists():
            bookmarked = True

        return render(
            request,
            "securityfeature_detail.html",
            {
                "securityfeature": securityfeature,
                "comments": comments,
                "comment_form": CommentForm(),
                "techsecurity_form": TechSecurityForm(),
                "bookmarked": bookmarked
            },
        )

    def post(self, request, slug):
        """
        This method is called when a POST request is made to the view
        via the comment form or the tech security form.
        """
        queryset = SecurityFeature.objects.filter(status=1)
        securityfeature = get_object_or_404(queryset, slug=slug)
        comments = securityfeature.comments.order_by('created_on')
        bookmarked = False
        if securityfeature.bookmarks.filter(id=self.request.user.id).exists():
            bookmarked = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.securityfeature = securityfeature
            comment.save()
            messages.success(self.request, 'Comment successfully added')
        else:
            comment_form = CommentForm()

        techsecurity_form = TechSecurityForm(data=request.POST)

        if techsecurity_form.is_valid():
            # get existing mpi record for user / day
            queryset = TechSecurityItem.objects.filter(
                user=request.user, day=request.POST['day'])
            techsecurity_item = queryset.first()

            # if a techsecurity item already exists for that day
            if techsecurity_item:
                # over write existing techsecurity item
                techsecurity_item.securityfeature = securityfeature
                messages.success(self.request, 'TechSecurity successfully updated')
            else:
                techsecurity_item = techsecurity_form.save(commit=False)
                techsecurity_item.user = request.user
                techsecurity_item.securityfeature = securityfeature
                messages.success(self.request, 'SecurityFeature added to techsecurity')

            techsecurity_item.save()

        else:
            techsecurity_form = TechSecurityForm()

        return render(
            request,
            "securityfeature_detail.html",
            {
                "securityfeature": securityfeature,
                "comments": comments,
                "comment_form": CommentForm(),
                "techsecurity_form": TechSecurityForm(),
                "bookmarked": bookmarked
            },
        )
        
        context['messages'] = messages.get_messages(request)

        return render(request, "securityfeature_detail.html", context)


class AddSecurityFeature(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    """This view is used to allow logged in users to create a securityfeature"""
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
        the securityfeature title into the success message.
        source: https://docs.djangoproject.com/en/4.0/ref/contrib/messages/
        """
        return self.success_message % dict(
            cleaned_data,
            calculated_field=self.object.title,
        )


class MySecurityFeatures(LoginRequiredMixin, generic.ListView):
    """
    This view is used to display a list of securityfeatures created by the logged in
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
        Prevent another user from updating other's securityfeature
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
            request, 'my_techsecurity.html', {'techsecurity': techsecurity})


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
        """ Return to securityfeature detail view when comment deleted sucessfully"""
        securityfeature = self.object.securityfeature
        return reverse_lazy('securityfeature_detail', kwargs={'slug': securityfeature.slug})