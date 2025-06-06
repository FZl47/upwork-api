from django.urls import path

from . import views

app_name = 'apps.public'

urlpatterns = [
    path('project/create', views.ProjectCreate.as_view(), name='project__create'),
    path('project/list', views.ProjectList.as_view(), name='project__list'),
    path('project/<int:project_pk>/proposal/list', views.ProjectProposalList.as_view(), name='project_proposal__list'),
    path('project/<int:pk>/detail', views.ProjectDetail.as_view(), name='project__detail'),

    path('proposal/create', views.ProposalCreate.as_view(), name='proposal__create'),
    path('proposal/list', views.ProposalList.as_view(), name='proposal__list'),
    path('proposal/<int:pk>/detail', views.ProposalDetail.as_view(), name='proposal__detail'),
    path('proposal/<int:project_pk>/<int:proposal_pk>/status', views.ProjectProposalStatus.as_view(), name='proposal__status'),

]
