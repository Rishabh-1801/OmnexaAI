"""
Views for about page — both SSR template and REST API.
"""

from django.shortcuts import render, get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import TeamMember, CompanyValue, CompanyMilestone, AboutPageContent
from .serializers import (
    TeamMemberSerializer, CompanyValueSerializer,
    CompanyMilestoneSerializer, AboutPageContentSerializer
)


# --- Template Views (SSR) ---
def about_page(request):
    """
    Renders about.html with all about page content.
    """
    # Get active about page content
    about_content = AboutPageContent.objects.filter(is_active=True).first()

    # Get all active related content
    team_members = TeamMember.objects.filter(is_active=True).order_by('order')
    company_values = CompanyValue.objects.filter(is_active=True).order_by('order')
    company_milestones = CompanyMilestone.objects.filter(is_active=True).order_by('order')

    context = {
        'about_content': about_content,
        'team_members': team_members,
        'company_values': company_values,
        'company_milestones': company_milestones,
    }

    return render(request, 'about.html', context)


def team_member_detail(request, slug):
    """
    Individual team member detail page.
    """
    team_member = get_object_or_404(TeamMember, slug=slug, is_active=True)
    return render(request, 'about/team_member_detail.html', {'team_member': team_member})


# --- REST API Views ---
class AboutPageContentAPIView(RetrieveAPIView):
    """
    GET /api/v1/about/
    Returns the active about page content with all related data.
    """
    queryset = AboutPageContent.objects.filter(is_active=True)
    serializer_class = AboutPageContentSerializer

    def get_object(self):
        # Return the first active about page content
        return get_object_or_404(self.queryset)


class TeamMemberListAPIView(ListAPIView):
    """
    GET /api/v1/about/team/
    Returns all active team members.
    """
    queryset = TeamMember.objects.filter(is_active=True).order_by('order')
    serializer_class = TeamMemberSerializer


class TeamMemberDetailAPIView(RetrieveAPIView):
    """
    GET /api/v1/about/team/<slug>/
    Returns a single team member's detail.
    """
    queryset = TeamMember.objects.filter(is_active=True)
    serializer_class = TeamMemberSerializer
    lookup_field = 'slug'


class CompanyValueListAPIView(ListAPIView):
    """
    GET /api/v1/about/values/
    Returns all active company values.
    """
    queryset = CompanyValue.objects.filter(is_active=True).order_by('order')
    serializer_class = CompanyValueSerializer


class CompanyMilestoneListAPIView(ListAPIView):
    """
    GET /api/v1/about/milestones/
    Returns all active company milestones.
    """
    queryset = CompanyMilestone.objects.filter(is_active=True).order_by('order')
    serializer_class = CompanyMilestoneSerializer


class AboutStatsAPIView(APIView):
    """
    GET /api/v1/about/stats/
    Returns about page statistics.
    """

    def get(self, request):
        about_content = AboutPageContent.objects.filter(is_active=True).first()

        if about_content:
            stats = {
                'clients': about_content.stats_clients,
                'projects': about_content.stats_projects,
                'years': about_content.stats_years,
                'team': about_content.stats_team,
            }
        else:
            stats = {
                'clients': 0,
                'projects': 0,
                'years': 0,
                'team': 0,
            }

        return Response(stats)
