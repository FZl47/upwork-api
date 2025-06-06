from rest_framework.generics import (
    CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
)

from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import APIException

from apps.core.swagger import SwaggerViewMixin
from apps.account.permissions import UserRolePermission

from . import serializers, models


class ProjectCreate(SwaggerViewMixin, CreateAPIView):
    """
        create project
    """

    swagger_title = 'Create project'
    swagger_tags = ['Project']
    swagger_response_code = 201
    serializer = serializers.ProjectCreateSerializer
    serializer_class = serializer
    permission_classes = (UserRolePermission('client'),)

    def perform_create(self, serializer):
        additional_data = {
            'client': self.request.user
        }
        serializer.save(**additional_data)


class ProjectList(SwaggerViewMixin, ListAPIView):
    """
        list project
    """

    class Pagination(PageNumberPagination):
        page_size = 20

    swagger_title = 'List project'
    swagger_tags = ['Project']
    serializer_response = serializers.ProjectListSerializer
    serializer_class = serializers.ProjectDetailListSerializer
    pagination_class = Pagination
    queryset = models.Project.objects.all()


class ProjectProposalList(SwaggerViewMixin, ListAPIView):
    """
        list project proposal
    """

    class Pagination(PageNumberPagination):
        page_size = 20

    swagger_title = 'List project proposal'
    swagger_tags = ['Project']
    serializer_response = serializers.ProposalListSerializer
    serializer_class = serializers.ProposalDetailListSerializer
    pagination_class = Pagination
    permission_classes = (UserRolePermission('client'),)

    def get_queryset(self):
        project_id = self.kwargs['project_pk']
        user = self.request.user
        try:
            project = user.get_projects().get(id=project_id)
        except models.Project.DoesNotExist:
            raise APIException('Project does not exists', code=404)

        return project.get_proposals()


class ProjectProposalStatus(SwaggerViewMixin, UpdateAPIView):
    """
        status project proposal
    """

    swagger_title = 'Status project proposal'
    swagger_tags = ['Project']
    serializer = serializers.ProposalStatusSerializer
    serializer_class = serializer
    permission_classes = (UserRolePermission('client'),)

    def get_object(self):
        project_id = self.kwargs['project_pk']
        proposal_id = self.kwargs['proposal_pk']
        user = self.request.user
        try:
            project = user.get_projects().get(id=project_id)
        except models.Project.DoesNotExist:
            raise APIException('Project does not exists', code=404)

        if project.accepted_proposal:
            raise APIException('Currently there is a approved proposal', code=400)

        try:
            proposal = project.get_proposals().get(id=proposal_id)
        except models.Proposal.DoesNotExist:
            raise APIException('Proposal does not exists', code=404)

        return proposal


class ProjectDetail(SwaggerViewMixin, RetrieveAPIView):
    """
        detail project
    """

    swagger_title = 'Detail project'
    swagger_tags = ['Project']
    serializer_response = serializers.ProjectDetailSerializer
    serializer_class = serializer_response
    queryset = models.Project.objects.all()


class ProposalCreate(SwaggerViewMixin, CreateAPIView):
    """
        create proposal
    """

    swagger_title = 'Create proposal'
    swagger_tags = ['Proposal']
    swagger_response_code = 201
    serializer = serializers.ProposalCreateSerializer
    serializer_class = serializer
    permission_classes = (UserRolePermission('freelancer'),)

    def perform_create(self, serializer):
        additional_data = {
            'freelancer': self.request.user
        }
        serializer.save(**additional_data)


class ProposalList(SwaggerViewMixin, ListAPIView):
    """
        list proposal
    """

    class Pagination(PageNumberPagination):
        page_size = 20

    swagger_title = 'List proposal'
    swagger_tags = ['Proposal']
    serializer_response = serializers.ProposalListSerializer
    serializer_class = serializers.ProposalDetailListSerializer
    pagination_class = Pagination
    permission_classes = (UserRolePermission('freelancer'),)

    def get_queryset(self):
        return self.request.user.get_proposals()


class ProposalDetail(SwaggerViewMixin, RetrieveAPIView):
    """
        detail proposal
    """

    swagger_title = 'Detail proposal'
    swagger_tags = ['Proposal']
    serializer_response = serializers.ProposalDetailSerializer
    serializer_class = serializer_response

    def get_object(self):
        """
            get object by user role
        """
        obj = None
        pk = self.kwargs['pk']
        user = self.request.user
        try:
            if user.role == 'client':
                obj = models.Proposal.objects.get(id=pk, project__client=user)
            elif user.role == 'freelancer':
                obj = user.get_proposals().get(id=pk)
            else:
                obj = models.Proposal.objects.get(id=pk)
        except models.Proposal.DoesNotExist:
            raise APIException('Proposal does not exists', code=404)
        return obj
