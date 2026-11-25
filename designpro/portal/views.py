from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm

def home(request):
    return render(request, 'portal/home.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = RegistrationForm()
    return render(request, 'registration/registration.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'portal/profile.html')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm, RequestForm
from .models import Request

@login_required
def profile(request):
    user_requests = Request.objects.filter(user=request.user)
    return render(request, 'portal/profile.html', {'requests': user_requests})

@login_required
def create_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST, request.FILES)
        if form.is_valid():
            req = form.save(commit=False)
            req.user = request.user
            req.status = 'new'
            req.save()
            messages.success(request, 'Заявка успешно создана!')
            return redirect('profile')
    else:
        form = RequestForm()
    return render(request, 'portal/cr_request.html', {'form': form})


@login_required
def delete_request(request, pk):
    req = get_object_or_404(Request, pk=pk, user=request.user)

    if req.status != 'new':
        messages.error(request, 'Простите, мы не можем удалить заявку, которую уже взяли в работу(')
        return redirect('profile')

    if request.method == 'POST':
        req.delete()
        messages.success(request, 'Заявка была удалена.')
        return redirect('profile')

    return render(request, 'portal/confirm_request_delete.html', {'req': req})