from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp_community.models import Community

from djangoldp_tzcld.permissions import RegionalReferentPermissions


#############################
# Page Suivi du territoire => Synthèse
#############################
class TzcldTerritorySynthesisFollowed(Model):
    questions = models.TextField(blank=True, null=True, verbose_name="Questions")
    needs = models.TextField(blank=True, null=True, verbose_name="Needs, Actions")
    targetdate = models.DateField(verbose_name="Target date", blank=True, null=True)
    community = models.OneToOneField(
        Community,
        on_delete=models.CASCADE,
        related_name="tzcld_community_synthesis_followed",
        blank=True,
        null=True,
    )
    date = models.DateField(verbose_name="Date", auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        if self.id:
            return "{} ({})".format(self.id, self.urlid)
        else:
            return self.urlid

    class Meta(Model.Meta):
        auto_author = "author"
        verbose_name = _("TZCLD Territory Synthesis Followed")
        verbose_name_plural = _("TZCLD Territories Synthesis Followed")

        container_path = "tzcld-territory-synthesis-followed/"
        serializer_fields = [
            "@id",
            "questions",
            "needs",
            "targetdate",
            "community",
            "tzcld_referents_community_shared_notes",
            "date",
            "author",
            "tzcld_referents_community_shared_files",
        ]
        nested_fields = [
            "community",
            "tzcld_referents_community_shared_notes",
            "tzcld_referents_community_shared_files",
        ]
        rdf_type = "tzcld:territorySynthesisFollowed"
        permission_classes = [RegionalReferentPermissions]
        community_path = "community"
