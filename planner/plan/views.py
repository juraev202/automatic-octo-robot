from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Plan, Category
from .forms import RegForm, PlanForm
 # Your Telegram bot helper




def plan_detail(request, pk):
    plan = get_object_or_404(Plan, pk=pk)
    return render(request, 'plan_detail.html', {'plan': plan})


def home_page(request):
    plans = Plan.objects.all()
    categories = Category.objects.all()
    return render(request, 'home.html', {'plans': plans, 'categories': categories})


def category_page(request, pk):
    category = get_object_or_404(Category, pk=pk)
    plans = Plan.objects.filter(category=category)
    return render(request, 'category.html', {'category': category, 'plans': plans})


def plan_page(request, pk):
    plan = get_object_or_404(Plan, pk=pk)
    return render(request, 'plan.html', {'plan': plan})


def search(request):
    if request.method == "POST":
        query = request.POST.get('search_product')
        searched_plans = Plan.objects.filter(title__iregex=query)
        return render(request, 'result.html', {'plans': searched_plans, 'query': query})
    return redirect('home')


class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        return render(request, self.template_name, {'form': RegForm()})

    def post(self, request):
        form = RegForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password2']
            )
            login(request, user)
            return redirect('home')
        return render(request, self.template_name, {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def create_plan(request):
    if request.method == 'POST':
        form = PlanForm(request.POST, request.FILES)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.user = request.user
            plan.save()

            # Redirect to your Telegram bot after plan creation
            return redirect('home')
    else:
        form = PlanForm()
    return render(request, 'plan_form.html', {'form': form})


def edit_plan(request, pk):
    plan = get_object_or_404(Plan, pk=pk)

    if request.method == 'POST':
        form = PlanForm(request.POST, request.FILES, instance=plan)
        if form.is_valid():
            form.save()
            return redirect('plan_detail', pk=plan.pk)
    else:
        form = PlanForm(instance=plan)

    return render(request, 'plan_form.html', {'form': form})


def delete_plan(request, pk):
    plan = get_object_or_404(Plan, pk=pk)
    if request.method == 'POST':
        plan.delete()
        return redirect('home')
    return redirect('plan_detail', pk=pk)

