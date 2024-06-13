from django.db import models


class DomainPack(models.Model):
    date = models.DateField(unique=True)

    def __str__(self):
        return str(self.date)


class Domain(models.Model):
    pack = models.ForeignKey(
        DomainPack,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='domains',
        related_query_name='domain',
    )
    name = models.CharField(max_length=255, primary_key=True)

    def __str__(self):
        return str(self.name)
