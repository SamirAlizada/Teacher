from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Group, Student
from .forms import GroupForm, StudentForm
from django.contrib import messages
from datetime import datetime, date, timedelta
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.db.models import Q

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
        print("POST request received")
        form = StudentForm(request.POST)
        if form.is_valid():
            print("Form düzgündür")
            form.save()
            messages.success(request, 'Tələbə uğurla əlavə edildi.')
            return redirect('add_student') 
        else:
            print("Form düzgün deyil")
            print(form.errors)
    else:
        form = StudentForm()
    return render(request, 'student/add_student.html', {'form': form})

def group_detail(request, group_id):
    group = Group.objects.get(id=group_id)
    students = Student.objects.filter(group=group)
    return render(request, 'group/group_detail.html', {'group': group, 'students': students})

def update_student(request, pk, group_id):
    student = get_object_or_404(Student, pk=pk)
    group = get_object_or_404(Group, pk=group_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('group_detail', group_id=group.id)
    else:
        form = StudentForm(instance=student)
    return render(request, 'student/update_student.html', {'form': form, 'group': group})

def update_student_pay(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(instance=student)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('pay_day')
    return render(request, 'student/update_student_pay.html', {'form': form})

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

def pay_day(request):
    now = datetime.now()
    today = now.date()
    end_date_range = today - timedelta(days=27)
    
    expired_students = Student.objects.filter(
        Q(end_date=today) | Q(end_date__range=(end_date_range, today))
    )
    return render(request, 'student/pay_day.html', {'expired_students': expired_students})

def renew_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    # Update the student's records
    student.add_date = student.end_date
    student.end_date = student.add_date + relativedelta(months=1)
    student.save()
    return redirect('pay_day')

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