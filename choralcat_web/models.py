import logging

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.shortcuts import reverse

from choralcat_core.consts import VARCHAR_LENGTH
from choralcat_core.fields import AutoSlugField
from choralcat_core.models import UserModel

logger = logging.getLogger(__name__)


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    timezone = models.CharField(max_length=VARCHAR_LENGTH, default=settings.TIME_ZONE)


class Person(UserModel):
    first_name = models.CharField(max_length=VARCHAR_LENGTH)
    slug = AutoSlugField(populated_from="first_name")
    last_name = models.CharField(max_length=VARCHAR_LENGTH, blank=True)
    birth = models.DateField(null=True, blank=True)
    death = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)
    poc = models.BooleanField(default=False)
    non_male_identifying = models.BooleanField(default=False)

    class Meta:
        ordering = ["last_name", "first_name"]
        verbose_name_plural = "People"

    def __str__(self):
        if self.last_name:
            return f"{self.last_name}, {self.first_name} "
        return self.first_name

    @property
    def name(self):
        if self.last_name:
            return f"{self.last_name}, {self.first_name} "
        return self.first_name

    def get_absolute_url(self):
        return reverse("person_detail", kwargs={"slug": self.slug})


class SimpleModel(UserModel):
    value = models.CharField(
        max_length=VARCHAR_LENGTH, blank=True, unique=True, null=True
    )

    class Meta:
        ordering = ["value", "user"]
        abstract = True

    def __str__(self):
        return self.value


class Category(SimpleModel):
    class Meta:
        verbose_name_plural = "Categories"


class Instrument(SimpleModel):
    pass


class Topic(SimpleModel):
    pass


class Tag(SimpleModel):
    value = models.CharField(max_length=VARCHAR_LENGTH, blank=True, null=True)

    class Meta:
        unique_together = ("user", "value")


class Composition(UserModel):
    title = models.CharField(max_length=VARCHAR_LENGTH)
    slug = AutoSlugField(populated_from="title")
    composers = models.ManyToManyField(Person, related_name="composers", blank=True)
    arrangers = models.ManyToManyField(Person, related_name="arrangers", blank=True)
    duration = models.DurationField(null=True, blank=True)
    starting_key = models.CharField(max_length=VARCHAR_LENGTH, blank=True)
    ending_key = models.CharField(max_length=VARCHAR_LENGTH, blank=True)
    time_period = models.CharField(max_length=VARCHAR_LENGTH, blank=True)
    language = models.CharField(max_length=VARCHAR_LENGTH, blank=True)
    number_of_voices = models.IntegerField(
        validators=[MinValueValidator(1)], blank=True, null=True
    )
    voicing = models.CharField(max_length=VARCHAR_LENGTH, blank=True)
    categories = models.ManyToManyField(Category, blank=True)
    accompaniment = models.ManyToManyField(Instrument, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    topics = models.ManyToManyField(Topic, blank=True)

    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True, null=True
    )
    score_link = models.CharField(max_length=VARCHAR_LENGTH, blank=True)
    notes = models.TextField(blank=True)
    edition_notes = models.TextField(blank=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

    @property
    def duration_mmss(self):
        if not self.duration:
            return ""
        sec = self.duration.total_seconds()
        return f"{int(sec / 60) % 60:02d}:{int(sec % 60):02d}"

    @property
    def stars(self):
        return range(self.rating)

    def get_absolute_url(self):
        return reverse("composition_detail", kwargs={"slug": self.slug})


class Program(UserModel):
    title = models.CharField(max_length=VARCHAR_LENGTH)
    slug = AutoSlugField(populated_from="title")
    compositions = models.ManyToManyField(Composition, blank=True)
    ordering = models.JSONField(default=dict, blank=True)
    season = models.CharField(max_length=VARCHAR_LENGTH, blank=True)
    topics = models.ManyToManyField(Topic, blank=True)

    class Meta:
        ordering = ["season", "title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("program_detail", kwargs={"slug": self.slug})

    @property
    def duration(self):
        return self.compositions.aggregate(models.Sum("duration"))["duration__sum"]

    @property
    def compositions_ordered(self):
        if self.ordering.get("compositions") is None:
            logger.warning(f"No composition ordering was found for {self}")

        slug_to_comp = {c.slug: c for c in self.compositions.all()}
        slugs = list(slug_to_comp.keys())
        ordering = self.ordering.get("compositions", [])
        if set(slugs) - set(ordering):
            logger.warning(
                f"Not all compositions were found in ordering for program {self}, defaulting to alphabetical order"
            )
            ordering = sorted(slugs)
            self.ordering["compositions"] = ordering
            self.save()
        return [slug_to_comp[slug] for slug in ordering]

    def add(self, composition: Composition):
        logger.debug(f"Adding {composition} to program {self}")
        self.compositions.add(composition)
        if "compositions" not in self.ordering:
            logger.warning("Composition ordering was uninstantiated")
            self.ordering["compositions"] = [composition.slug]
        else:
            self.ordering["compositions"].append(composition.slug)

    def remove(self, composition: Composition):
        logger.debug(f"Removing {composition} from program {self}")
        self.compositions.remove(composition)
        self.ordering["compositions"] = [
            c for c in self.ordering["compositions"] if c != composition.slug
        ]

    def reorder(self, new_order: list[str]):
        logger.debug(f"Reordering program {self} to {new_order}")
        self.ordering["compositions"] = new_order
