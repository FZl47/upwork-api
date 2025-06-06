from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Project(BaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    client = models.ForeignKey('account.ClientUser', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    @property
    def accepted_proposal(self):
        return self.get_proposals().filter(status='accepted').first()

    def get_proposals(self):
        return self.proposal_set.all()


class Proposal(BaseModel):
    STATUS_TYPES = (
        ('accepted', _('Accepted')),
        ('rejected', _('Rejected')),
        ('pending', _('Pending')),
    )

    status = models.CharField(max_length=12, choices=STATUS_TYPES, default='pending')
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    freelancer = models.ForeignKey('account.FreelancerUser', on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True)
    proposed_price = models.DecimalField(max_digits=20, decimal_places=0)

    def __str__(self):
        return f'{self.project} / {self.freelancer.get_full_name()}({self.status})'
