from django.shortcuts import render, get_object_or_404, redirect

# Home page view
def home(request):
    return render(request, "home.html")
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Destination, DestinationImage
from .forms import DestinationForm, DestinationImageFormSet
from rest_framework import viewsets, permissions
from .serializers import DestinationSerializer
from django.views.decorators.http import require_http_methods
from django.template import RequestContext

# REST API Views
class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

# Template Views
class DestinationListView(ListView):
    model = Destination
    template_name = 'destinations/destination_list.html'
    context_object_name = 'destinations'
    paginate_by = 10

class DestinationDetailView(DetailView):
    model = Destination
    template_name = 'destinations/destination_detail.html'
    context_object_name = 'destination'
    slug_url_kwarg = 'slug'

class DestinationCreateView(LoginRequiredMixin, CreateView):
    model = Destination
    form_class = DestinationForm
    template_name = 'destinations/destination_form.html'
    success_url = reverse_lazy('destination-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        formset = DestinationImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        if formset.is_valid():
            formset.save()
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = DestinationImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['formset'] = DestinationImageFormSet()
        return context

class DestinationUpdateView(LoginRequiredMixin, UpdateView):
    model = Destination
    form_class = DestinationForm
    template_name = 'destinations/destination_form.html'
    slug_url_kwarg = 'slug'

    def get_success_url(self):
        return reverse_lazy('destination-detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = DestinationImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['formset'] = DestinationImageFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.get_success_url())
        return self.render_to_response(self.get_context_data(form=form))

@login_required
@require_http_methods(['POST'])
def delete_destination_image(request, pk):
    image = get_object_or_404(DestinationImage, pk=pk)
    destination_slug = image.destination.slug
    image.delete()
    messages.success(request, 'Image deleted successfully.')
    return redirect('destination-update', slug=destination_slug)

@login_required
def destination_delete(request, slug):
    destination = get_object_or_404(Destination, slug=slug)
    if request.method == 'POST':
        destination.delete()
        messages.success(request, 'Destination deleted successfully.')
        return redirect('destination-list')
    return render(request, 'destinations/destination_confirm_delete.html', {'destination': destination})

def handler404(request, exception, template_name='404.html'):
    response = render(request, template_name)
    response.status_code = 404
    return response

def handler500(request, template_name='500.html'):
    response = render(request, template_name)
    response.status_code = 500
    return response