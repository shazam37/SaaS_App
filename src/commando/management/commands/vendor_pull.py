import helpers

from django.core.management.base import BaseCommand
from django.conf import settings
from typing import Any

VENDOR_STATICFILES = {
    "flowbite.min.css": "https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.css",
    "flowbite.min.js": "https://cdn.js.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.js",
}

STATICFILES_VENDOR_DIRS = getattr(settings, 'STATICFILES_VENDOR_DIR')

class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any):
        self.stdout.write("Dowloading vendor static files")
        completed_urls = []
        for name,url in VENDOR_STATICFILES.items():
            out_path = STATICFILES_VENDOR_DIRS / name
            dl_success = helpers.download_to_local(url, out_path)
            if dl_success:
                completed_urls.append(url)
            else:
                self.stdout.write(
                    self.style.ERROR(f'failed to download {url}')
                )
            print(name, url, out_path)
        
        if set(completed_urls) == set(VENDOR_STATICFILES.values()):
            self.stdout.write(
                self.style.SUCCESS('Successfully updated all vendor static files')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Some files were not updated')
            )