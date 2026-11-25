from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm
from .models import Request

def home(request):
    done_requests = Request.objects.filter(status='done').order_by('-created_at')
    context = {
        'done_requests': done_requests,
    }
    return render(request, 'portal/home.html', context)

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


from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Request, Category
from .forms import ChangeStatusToInProgressForm, ChangeStatusToDoneForm


@staff_member_required
def admin_requests(request):
    all_requests = Request.objects.all().order_by('-created_at')
    return render(request, 'admin/admin_requests.html', {'requests': all_requests})

@staff_member_required
def change_status(request, pk):
    req = get_object_or_404(Request, pk=pk)

    if req.status == 'done':
        messages.error(request, 'Смена статуса невозможна: заявка уже выполнена.')
        return redirect('admin_requests')

    if request.method == 'POST':
        if 'to_in_progress' in request.POST:
            if req.status == 'in_progress':
                messages.warning(request, 'Заявка уже находится в работе.')
                return redirect('admin_requests')

            form = ChangeStatusToInProgressForm(request.POST)
            if form.is_valid():
                req.status = 'in_progress'
                req.comment = form.cleaned_data['comment']
                req.save()
                messages.success(request, 'Заявка переведена в статус «Принято в работу».')
                return redirect('admin_requests')

        elif 'to_done' in request.POST:
            form = ChangeStatusToDoneForm(request.POST, request.FILES)
            if form.is_valid():
                req.status = 'done'
                req.design_image = form.cleaned_data['design_image']
                req.save()
                messages.success(request, 'Заявка выполнена! Изображение дизайна сохранено.')
                return redirect('admin_requests')
    else:
        form_in_progress = ChangeStatusToInProgressForm()
        form_done = ChangeStatusToDoneForm()

        return render(request, 'admin/change_status.html', {
            'req': req,
            'form_in_progress': form_in_progress,
            'form_done': form_done,
        })


from .forms import CategoryForm

@staff_member_required
def manage_categories(request):
    categories = Category.objects.all()
    return render(request, 'admin/manage_categories.html', {'categories': categories})

@staff_member_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категория успешно добавлена.')
            return redirect('manage_categories')
    else:
        form = CategoryForm()
    return render(request, 'admin/add_category.html', {'form': form})

@staff_member_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Категория "{category.name}" и все её заявки удалены.')
        return redirect('manage_categories')

    return render(request, 'admin/confirm_delete_category.html', {'category': category})