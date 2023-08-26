from multiprocessing.connection import wait
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .blockchain import *
from .models import WaitBlock
from .forms import WaitBlockForm
from account.models import User
from datetime import datetime
from hashlib import sha512

# Create your views here.
@login_required(login_url='account_app:login')
def home(request):
    user = request.user
    if user.is_teacher == False:
        student_code = user.student_code
        list_cert = get_cert_list_by_student_code("cert/ledger.json", str(student_code))
        wait_blocks = WaitBlock.objects.filter(student_id=user.id)
        print("Y"*10)
        print(list_cert)
        context = {
            "list_cert":list_cert,
            "wait_blocks":wait_blocks,
            "student":user
        }
        return render(request, 'cert/student_home.html', context)
    else:
        wait_blocks = WaitBlock.objects.filter(teacher_id=user.id)
        list_cert = get_cert_list_by_teacher_id("cert/ledger.json", str(user.id))
        context = {
            "wait_blocks":wait_blocks,
            "teacher":user,
            "list_cert":list_cert,
        }
        return render(request, 'cert/teacher_home.html', context)

@login_required(login_url='account_app:login')
def add_wait_block(request):
    context ={}
    if request.method == 'POST':
        form = WaitBlockForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.student_id = request.user.id
            obj.student_name = request.user.full_name
            obj.save()
            return redirect('cert_app:home')
    else:
        form = WaitBlockForm()
        context['form']= form
    return render(request, "cert/add_wait_block.html", context)

# Teacher Sign The Cert
@login_required(login_url='account_app:login')
def teacher_sign(request, pk):
    cert = WaitBlock.objects.get(id=pk)
    student_ = User.objects.get(id=cert.student_id)

    student_name = student_.full_name
    student_code = student_.student_code
    teacher_name = request.user.full_name
    teacher_id = request.user.id
    course_name = cert.course_name
    mark = cert.final_mark
    date = datetime.now().strftime("%d/%m/%Y")

    data_for_sign = bytes(str(student_name)+str(student_code)+str(teacher_name)+str(teacher_id)+str(course_name)+str(mark)+str(date), 'utf-8')
    hash = int.from_bytes(sha512(data_for_sign).digest(), byteorder='big')
    signature = pow(hash, int(request.user.d_key, 16), int(request.user.n_key, 16))

    data_to_mine = {
        "student_name":str(student_name),
        "student_code":str(student_code),
        "teacher_name":str(teacher_name),
        "teacher_id":str(teacher_id),
        "course_name":str(course_name),
        "mark":str(mark),
        "date":str(date),
        "signature":signature,
    }

    # Mining (Add Block To Chain)
    data = get_data('cert/ledger.json')
    mine(data, Block(data_to_mine))

    cert.delete()

    return redirect('cert_app:home')

# Teacher Sign The Cert
@login_required(login_url='account_app:login')
def teacher_delete_wait_block(request, pk):
    cert = WaitBlock.objects.get(id=pk)
    cert.delete()
    return redirect('cert_app:home')


@login_required(login_url='account_app:login')
def delete_cert_in_blockchain(request, pk):
    data_to_mine = {
        "target_block_id":int(pk),
        "method":"delete",
        "new_block_id":""
    } 
    # Mining (Add Block To Chain)
    data = get_data('cert/ledger.json')
    mine(data, Block(data_to_mine))
    return redirect('cert_app:home')

@login_required(login_url='account_app:login')
def get_cert(request, pk):
    cert = get_cert_by_id("cert/ledger.json", pk)
    teacher = User.objects.get(id=int(cert["teacher_id"]))
    is_valid = check_block_isValid("cert/ledger.json", pk, teacher.e_key, teacher.n_key)
    context = {
        "cert":cert,
        "is_valid":is_valid
    }
    return render(request, 'cert/cert.html', context)