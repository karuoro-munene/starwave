from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("profile/<slug:username>", views.profile, name="profile"),
    path("passwords/change", views.change_password, name="change_password"),
    path("employees/add", views.new_employee, name="new_employee"),
    path("employees/delete", views.delete_employee, name="delete_employee"),
    path("loans", views.loans, name="loans"),
    path("loans/new", views.new_loan, name="new_loan"),
    path("loans/<slug:loan_id>", views.loan, name="loan"),
    path("loan/pay", views.pay_loan, name="pay_loan"),
    path("loan/paid", views.paid_loans, name="paid_loans"),
    path("loan/defaults", views.defaulted_loans, name="defaulted_loans"),
    path("loan/defaults/new", views.default_loan, name="default_loan"),
    path("loan/extend", views.extend_loan, name="extend_loan"),
    path("collaterals", views.collaterals, name="collaterals"),
    path("collateral/collected", views.collected_collaterals, name="collected_collaterals"),
    path("collateral/confiscated", views.confiscated_collaterals, name="confiscated_collaterals"),
    path("collaterals/<slug:id>", views.collateral_details, name="collateral"),
    path("reports", views.reports, name="reports"),
    path("activity/log", views.activity_log, name="activity_log"),
]
