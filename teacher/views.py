from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Group, Student
from .forms import GroupForm, StudentForm
from django.contrib import messages


def add_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('group_list')
    else:
        form = GroupForm()
    return render(request, 'group/add_group.html', {'form': form})

def group_list(request):
    groups = Group.objects.all()
    return render(request, 'group/group_list.html', {'groups': groups})

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tələbə uğurla əlavə edildi.')
            return redirect('add_student') 
    else:
        form = StudentForm()
    return render(request, 'student/add_student.html', {'form': form})

def group_detail(request, group_id):
    group = Group.objects.get(id=group_id)
    students = Student.objects.filter(group=group)
    return render(request, 'group/group_detail.html', {'group': group, 'students': students})

def update_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(instance=student)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('group_list')
    return render(request, 'student/update_student.html', {'form': form})

def update_group(request, pk):
    group = get_object_or_404(Group, pk=pk)
    form = GroupForm(instance=group)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('group_list')
    return render(request, 'group/update_group.html', {'form': form})

# Delete
def delete_group(request, pk):
    group = Group.objects.get(pk=pk)
    group.delete()
    return redirect('group_list')

def delete_student(request, pk):
    student = Student.objects.get(pk=pk)
    student.delete()
    return redirect('group_list')

# User
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('group_list')
        else:
            messages.error(request, 'İstifadəçi adı və ya parol səhvdir.')
    return render(request, 'account/login.html')

def user_logout(request):
    logout(request)
    return redirect('group_list')