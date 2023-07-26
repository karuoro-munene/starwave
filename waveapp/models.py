from datetime import timedelta

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User

loan_statuses = (
    ("Paid", "Paid"),
    ("Unpaid", "Unpaid"),
)

collaterals_statuses = (
    ("Collected", "Collected"),
    ("Not Collected", "Not Collected"),
)

activity_types = (
    ("New Loan", "New Loan"),
    ("Loan Repayment", "Loan Repayment"),
    ("Loan Extension", "Loan Extension"),
    ("Loan Defaulted", "Loan Defaulted")
)


class Loans(models.Model):
    loan_id = models.CharField(max_length=100, unique=True, blank=True, null=False)
    client_name = models.CharField(max_length=300, null=False)
    client_id_no = models.CharField(max_length=10, null=False)
    client_phone_no = models.CharField(max_length=10, null=False)
    collateral_name = models.CharField(max_length=200, null=False)
    issue_date = models.DateTimeField(default=timezone.now)
    loan_period = models.IntegerField(default=7)
    repayment_date = models.DateTimeField(default=(timezone.now() + timedelta(days=7)))
    loan_amount = models.FloatField()
    interest_rate = models.FloatField(default=0.3)
    repayment_amount = models.FloatField()
    loan_status = models.CharField(max_length=100, choices=loan_statuses)
    issued_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Users")
    created_on = models.DateTimeField(default=timezone.now)
    paid_on = models.DateTimeField(default=timezone.now, null=True)
    collateral_id = models.CharField(max_length=100, unique=True, blank=True, null=False)
    default_status = models.BooleanField(default=False)
    defaulted_on = models.DateTimeField(default=timezone.now)
    overdue = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    paid_amount = models.FloatField(null=True)
    remaining_amount = models.FloatField(null=True)
    loan_extended = models.BooleanField(default=False)
    loan_extensions = models.IntegerField(default=0)
    extended_on = ArrayField(models.DateTimeField(default=timezone.now), null=True)

    def __str__(self):
        return self.client_id_no

    class Meta:
        get_latest_by = ['created_on']


class Collaterals(models.Model):
    collateral_id = models.CharField(max_length=100, unique=True, blank=True, null=False)
    collateral_name = models.CharField(max_length=200, null=False)
    loan = models.OneToOneField(Loans, on_delete=models.CASCADE)
    held_on = models.DateTimeField(default=timezone.now)
    collection_date = models.DateTimeField(default=timezone.now)
    collected_on = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=100, choices=collaterals_statuses)
    confiscated = models.BooleanField(default=False)
    confiscated_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.collateral_name

    class Meta:
        get_latest_by = ['held_on']


@receiver(post_save, sender=Loans)
def create_collateral(sender, instance, created, **kwargs):
    if created:
        collateral = Collaterals.objects.create(
            loan=instance,
            collateral_name=instance.collateral_name,
            collateral_id=instance.collateral_id,
            held_on=instance.created_on,
            collection_date=instance.repayment_date,
            status="Not Collected"
        )
        collateral.save()


class Activities(models.Model):
    type = models.CharField(max_length=100, choices=activity_types)
    initiator = models.ForeignKey(User, on_delete=models.CASCADE)
    initiated_on = models.DateTimeField(default=timezone.now)
    loan = models.ForeignKey(Loans, on_delete=models.CASCADE)

    def __str__(self):
        return self.type + " - " + self.loan.loan_id
