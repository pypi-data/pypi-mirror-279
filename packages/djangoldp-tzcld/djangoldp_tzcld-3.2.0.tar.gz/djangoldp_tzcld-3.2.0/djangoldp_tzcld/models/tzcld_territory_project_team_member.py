from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp.permissions import InheritPermissions

from djangoldp_tzcld.models.tzcld_community_identity import \
    TzcldCommunityIdentity
from djangoldp_tzcld.models.tzcld_territories_team_user_state import \
    TzcldTerritoriesTeamUserState
from djangoldp_tzcld.permissions import RegionalReferentPermissions


#############################
# Page Etat d'avancement => Carte d’identité du territoire => Equipe projet
#############################
class TzcldTerritoryProjectTeamMember(Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )
    user_state = models.ForeignKey(
        TzcldTerritoriesTeamUserState,
        on_delete=models.DO_NOTHING,
        related_name="team_member_state",
        blank=True,
        null=True,
    )
    etp = models.CharField(max_length=255, blank=True, null=True, default="")
    attachment_structure = models.CharField(
        max_length=255, blank=True, null=True, default=""
    )
    community_identity = models.ForeignKey(
        TzcldCommunityIdentity,
        on_delete=models.CASCADE,
        related_name="territories_project_team_members",
        blank=True,
        null=True,
    )

    def __str__(self):
        if self.community_identity:
            return "{} ({})".format(self.community_identity.urlid, self.urlid)
        else:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _("TZCLD Territory Project Team Member")
        verbose_name_plural = _("TZCLD Territories Project Team Members")

        container_path = "tzcld-territories-project-team-member/"
        serializer_fields = [
            "@id",
            "user",
            "user_state",
            "etp",
            "attachment_structure",
            "community_identity",
        ]
        nested_fields = ["community_identity"]
        rdf_type = "tzcld:territoryProjectTeamMember"
        permission_classes = [InheritPermissions | RegionalReferentPermissions]
        inherit_permissions = ["community_identity"]
        community_path = "community_identity.community"
