from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from .forms import *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse


@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
        return redirect('task:Home')
    return redirect('task:Home')  # In case it's not POST, just redirect to home



@login_required(login_url='user:login')
def Home(request):
    tasks = Task.objects.filter(user=request.user)
    form = TaskForm()
    context = {'tasks': tasks, 'form': form}
    return render(request, 'task/home.html', context)


def remove_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        task = Task.objects.get(pk = task_id)
        task.delete()
    return redirect('task:Home')



@csrf_exempt
def done(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            task_id = data.get('task_id')
            status = data.get('status')
            task = get_object_or_404(Task, pk=task_id)
            task.status = status
            task.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})