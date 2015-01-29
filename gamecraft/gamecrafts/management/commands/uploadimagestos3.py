"""Refetch images and place into S3

"""

from django.core.management.base import BaseCommand

from gamecraft.gamecrafts import models


class Command(BaseCommand):
    help = "Refetch images from filepicker.io and upload to S3 (creating thumbnails)"

    def handle(self, *args, **options):
        import logging
        logging.basicConfig(level=logging.INFO)
        for sponsor in models.Sponsor.objects.all():
            self.stderr.write("{sponsor.slug} {sponsor.name} {sponsor.url} {sponsor.logo_url}\n".format(sponsor=sponsor))

            models.update_image_from_url(sponsor, sponsor.slug, "logo_url", "logo", save=True)
