from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import SecurityFeature


class SecurityFeatureList(generic.ListView):
    model = SecurityFeature
    queryset = SecurityFeature.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 6



class SecurityFeatureDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = SecurityFeature.objects.filter(status=1)
        securityfeature = get_object_or_404(queryset, slug=slug)
        comments = securityfeature.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if securityfeature.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "securityfeature_detail.html",
            {
                "securityfeature": securityfeature,
                "comments": comments,
                "liked": liked
            },
        )