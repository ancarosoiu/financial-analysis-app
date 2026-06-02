from django.utils import timezone

def company_directory_path(instance, filename):
    now = timezone.now()
    owner_id = instance.company.owner.id

    clean_filename = filename.replace(" ", "_")
    new_filename = f"{now.strftime('%Y%m%d_%H%M%S')}_{clean_filename}"

    return f'uploads/owner_{owner_id}/{now.year}/{now.month}/{new_filename}'