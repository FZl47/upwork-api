from rest_framework import serializers

from apps.core import serializers as core_serializers

from . import models


class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        exclude = ('client',)


class ProjectDetailListSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.get_full_name')

    class Meta:
        model = models.Project
        exclude = ('description',)


class ProjectListSerializer(core_serializers.ListSerializer):
    results = ProjectDetailListSerializer(many=True)


class ProjectDetailSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.get_full_name')

    class Meta:
        model = models.Project
        fields = '__all__'


class ProposalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Proposal
        exclude = ('freelancer', 'status')


class ProposalDetailListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Proposal
        exclude = ('message',)


class ProposalListSerializer(core_serializers.ListSerializer):
    results = ProposalDetailListSerializer(many=True)


class ProposalDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Proposal
        fields = '__all__'


class ProposalStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Proposal
        fields = ('status',)
