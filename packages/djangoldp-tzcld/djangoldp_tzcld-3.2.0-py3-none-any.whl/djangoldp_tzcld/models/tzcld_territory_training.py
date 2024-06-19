from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp.permissions import InheritPermissions

from djangoldp_tzcld.models.tzcld_community_identity import \
    TzcldCommunityIdentity
from djangoldp_tzcld.models.tzcld_territories_training_course import \
    TzcldTerritoriesTrainingCourse
from djangoldp_tzcld.models.tzcld_territories_training_promotion import \
    TzcldTerritoriesTrainingPromotion


#############################
# Page Etat d'avancement => Carte d’identité du territoire => Participation aux formations TZCLD
#############################
class TzcldTerritoryTraining(Model):
    training_course = models.ForeignKey(
        TzcldTerritoriesTrainingCourse,
        on_delete=models.DO_NOTHING,
        related_name="territory_training_course",
        blank=True,
        null=True,
    )
    training_promotion = models.ForeignKey(
        TzcldTerritoriesTrainingPromotion,
        on_delete=models.DO_NOTHING,
        related_name="territory_training_promotion",
        blank=True,
        null=True,
    )
    training_person = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )
    community_identity = models.ForeignKey(
        TzcldCommunityIdentity,
        on_delete=models.CASCADE,
        related_name="territories_trainings",
        blank=True,
        null=True,
    )

    def __str__(self):
        if self.community_identity:
            return "{} ({})".format(self.community_identity.urlid, self.urlid)
        else:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _("TZCLD Territory Training")
        verbose_name_plural = _("TZCLD Territories Trainings")

        container_path = "tzcld-territories-training/"
        serializer_fields = [
            "@id",
            "training_course",
            "training_promotion",
            "training_person",
            "community_identity",
        ]
        nested_fields = ["community_identity"]
        rdf_type = "tzcld:territoryTraining"
        permission_classes = [InheritPermissions]
        inherit_permissions = ["community_identity"]
