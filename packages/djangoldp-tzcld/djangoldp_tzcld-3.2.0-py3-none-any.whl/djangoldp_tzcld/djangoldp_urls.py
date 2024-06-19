from django.urls import path
from djangoldp_community.models import Community

from .views import MemberOfCommunitiesView, MyTerritoriesView

urlpatterns = [
    path(
        "myterritories/",
        MyTerritoriesView.as_view({"get": "list"}, model=Community),
        name="myterritories",
    ),
    path(
        "memberofcommunities/",
        MemberOfCommunitiesView.as_view({"get": "list"}, model=Community),
        name="memberofcommunities",
    ),
]
