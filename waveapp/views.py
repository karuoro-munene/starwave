from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Exists, OuterRef
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from waveapp.models import Loans, Collaterals, Activities
from waveapp.utilities import generate_loan_id, generate_collateral_id


@login_required(login_url='/accounts/login')
def dashboard(request):
    all_loans = Loans.objects.all()
    paid_loans = Loans.objects.filter(loan_status="Paid")
    unpaid_loans = Loans.objects.filter(loan_status="Unpaid")
    defaulted_loans = Loans.objects.filter(default_status=True)
    today = timezone.now().today()
    jan_loans = Loans.objects.filter(issue_date__year=today.year, issue_date__month='1')
    feb_loans = Loans.objects.filter(issue_date__year=today.year, issue_date__month='2')
    mar_loans = Loans.objects.filter(issue_date__year=today.year, issue_date__month='3')
    apr_loans = Loans.objects.filter(issue_date__year=today.year, issue_date__month='4')
    may_loans = Loans.objects.filter(issue_date__year=today.year, issue_date__month='5')
    jun_loans = Loans.objects.filter(issue_date__year=today.year, issue_date__month='6')
    jul_loans = Loans.objects.filter(issue_date__year=today.year, issue_date__month='7')
    aug_loans = Loans.objects.filter(issue_date__year=today.year, issue_date__month='8')
    sep_loans = Loans.objects.filter(issue_date__year=today.year, issue_date__month='9')
    oct_loans = Loans.objects.filter(issue_date__year=today.year, issue_date__month='10')
    nov_loans = Loans.objects.filter(issue_date__year=today.year, issue_date__month='11')
    dec_loans = Loans.objects.filter(issue_date__year=today.year, issue_date__month='12')
    return render(request, "index.html", locals())


@login_required(login_url='/accounts/login')
def profile(request, username):
    user = request.user
    if User.objects.get(username=username) == request.user:
        employees = User.objects.filter(is_active=True).exclude(username='admin')
        return render(request, "profile.html", locals())
    else:
        return render(request, "forbidden.html", locals())


@login_required(login_url='/accounts/login')
def change_password(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.POST.get("username"))
        password = request.POST.get("password").strip()
        user.set_password(password)
        user.save()
    return JsonResponse({"success": "success!"})


@login_required(login_url='/accounts/login')
def new_employee(request):
    if request.method == 'POST':
        username = request.POST.get("username").strip()
        password = request.POST.get("password").strip()
        user = User.objects.create_superuser(username=username, password=password)
        user.save()
        print(user)
    return JsonResponse({"success": "success!"})


@login_required(login_url='/accounts/login')
def delete_employee(request):
    if request.method == 'POST':
        username = request.POST.get("username").strip()
        user = User.objects.get(username=username)
        user.is_active = False
        user.save()
    return JsonResponse({"success": "success!"})


@login_required(login_url='/accounts/login')
def loans(request):
    for loan in Loans.objects.filter(loan_status="Unpaid"):
        if (loan.repayment_date - timezone.now()).days < 0:
            loan.overdue = True
            loan.save()
    loans = Loans.objects.filter(loan_status="Unpaid", default_status=False).order_by("-created_on")
    return render(request, "loans.html", locals())


@login_required(login_url='/accounts/login')
def paid_loans(request):
    loans = Loans.objects.filter(loan_status="Paid")
    return render(request, "paid_loans.html", locals())


@login_required(login_url='/accounts/login')
def collected_collaterals(request):
    collaterals = Collaterals.objects.filter(status="Collected")
    return render(request, "collected_collaterals.html", locals())


@login_required(login_url='/accounts/login')
def confiscated_collaterals(request):
    collaterals = Collaterals.objects.filter(confiscated=True)
    return render(request, "collected_collaterals.html", locals())


@login_required(login_url='/accounts/login')
def loan(request, loan_id):
    loan = Loans.objects.get(loan_id=loan_id)
    health = {}
    current_interest = loan.repayment_amount - loan.loan_amount
    difference = loan.repayment_date - timezone.now()
    delta = difference.days
    if delta > 2:
        health["remark"] = "safe"
        health["days"] = delta
    elif (delta < 2) and (delta > -1):
        health["remark"] = "safe"
        health["days"] = delta
    else:
        health["remark"] = "unsafe"
        health["days"] = abs(delta)
    return render(request, "loan.html", locals())


@login_required(login_url='/accounts/login')
def pay_loan(request):
    if request.method == 'POST':
        loan = Loans.objects.get(loan_id=request.POST.get("loan_id"))
        loan.loan_status = "Paid"
        loan.paid_on = timezone.now()
        loan.paid = True
        loan.default_status = False
        loan.save()
        activity = Activities.objects.create(type="Loan Repayment", initiator=request.user,
                                             initiated_on=timezone.now(), loan=loan)
        activity.save()
        collateral = Collaterals.objects.get(collateral_id=loan.collateral_id)
        collateral.status = "Collected"
        collateral.confiscated = False
        collateral.collected_on = timezone.now()
        collateral.save()
    return JsonResponse({"success": "success!"})


@login_required(login_url='/accounts/login')
def default_loan(request):
    if request.method == 'POST':
        loan = Loans.objects.get(loan_id=request.POST.get("loan_id"))
        loan.default_status = True
        loan.defaulted_on = timezone.now()
        loan.save()
        activity = Activities.objects.create(type="Loan Defaulted", initiator=request.user,
                                             initiated_on=timezone.now(), loan=loan)
        activity.save()
        collateral = Collaterals.objects.get(collateral_id=loan.collateral_id)
        collateral.confiscated = True
        collateral.confiscated_on = timezone.now()
        collateral.save()
    return JsonResponse({"success": "success!"})


@login_required(login_url='/accounts/login')
def extend_loan(request):
    if request.method == 'POST':
        loan = Loans.objects.get(loan_id=request.POST.get("loan_id"))
        new_period = request.POST.get("days_to_extend")
        loan.repayment_date = loan.repayment_date + timedelta(days=int(new_period))
        paid_interest = request.POST.get("paid_interest")
        if paid_interest == 'Yes':
            new_repayment_amount = ((loan.loan_amount * 0.3) * (int(new_period) / 7)) + loan.loan_amount
            loan.repayment_amount = new_repayment_amount
        else:
            new_repayment_amount = ((loan.loan_amount * 0.3) * (int(new_period) / 7)) + loan.repayment_amount
            loan.repayment_amount = new_repayment_amount
        loan.loan_period = loan.loan_period + int(new_period)
        loan.loan_extended = True
        loan.loan_extensions = loan.loan_extensions + 1
        if loan.extended_on == None:
            loan.extended_on = [timezone.now()]
        else:
            loan.extended_on = loan.extended_on.append(timezone.now())
        loan.save()
        activity = Activities.objects.create(type="Loan Extension", initiator=request.user,
                                             initiated_on=timezone.now(), loan=loan)
        activity.save()
    return JsonResponse({"success": "success!"})


@login_required(login_url='/accounts/login')
def defaulted_loans(request):
    loans = Loans.objects.filter(default_status=True)
    return render(request, "defaulted_loans.html", locals())


@login_required(login_url='/accounts/login')
def collaterals(request):
    collaterals = Collaterals.objects.filter(status="Not Collected", confiscated=False).order_by("-held_on")
    return render(request, "collaterals.html", locals())


@login_required(login_url='/accounts/login')
def collateral_details(request, id):
    col = Collaterals.objects.get(collateral_id=id)
    return render(request, "collateral.html", locals())


@login_required(login_url='/accounts/login')
def reports(request):
    collected_cols = Collaterals.objects.filter(status="Collected").order_by("-collected_on")
    confiscated_cols = Collaterals.objects.filter(confiscated=True).order_by("-confiscated_on")
    paid_loans = Loans.objects.filter(loan_status="Paid").order_by("-paid_on")
    defaulted_loans = Loans.objects.filter(default_status=True).order_by("-paid_on")
    return render(request, "reports.html", locals())


@login_required(login_url='/accounts/login')
def new_loan(request):
    if request.method == 'POST':
        loan_id = generate_loan_id()
        collateral_id = generate_collateral_id()
        client_name = request.POST.get("full_names"),
        client_id_no = request.POST.get("id_number"),
        client_phone_no = request.POST.get("phone_number"),
        collateral_name = request.POST.get("collateral_name"),
        loan_amount = float(request.POST.get("loan_amount")),
        loan_period = request.POST.get("loan_period")
        repayment_date = timezone.now() + timedelta(days=int(loan_period))
        interest_rate = float(0.3)
        print(loan_amount[0])
        print(interest_rate)
        repayment_amount = ((loan_amount[0] * interest_rate) * (int(loan_period) / 7)) + loan_amount[0]
        loan_status = "Unpaid"
        issued_by = request.user
        created_on = timezone.now()
        paid_on = None

        new_loan_item = Loans.objects.create(
            loan_id=loan_id,
            client_name=client_name[0],
            client_id_no=client_id_no[0],
            client_phone_no=client_phone_no[0],
            collateral_name=collateral_name[0],
            collateral_id=collateral_id,
            loan_amount=loan_amount[0],
            loan_period=loan_period,
            repayment_date=repayment_date,
            repayment_amount=repayment_amount,
            interest_rate=interest_rate,
            loan_status=loan_status,
            issued_by=issued_by,
            created_on=created_on,
            paid_on=paid_on
        )

        new_loan_item.save()
        activity = Activities.objects.create(type="New Loan", initiator=request.user,
                                             initiated_on=timezone.now(), loan=new_loan_item)
        activity.save()
        return JsonResponse({"message": "success!"})


@login_required(login_url='/accounts/login')
def activity_log(request):
    activities = Activities.objects.all().order_by("-initiated_on")
    return render(request, "activity_log.html", locals())
