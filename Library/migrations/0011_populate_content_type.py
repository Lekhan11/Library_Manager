from django.db import migrations
from django.contrib.contenttypes.models import ContentType

def populate_content_type(apps, schema_editor):
    IssuedBooks = apps.get_model('Library', 'IssuedBooks')
    Students = apps.get_model('Library', 'Students')
    student_type = ContentType.objects.get_for_model(Students)
    
    for ib in IssuedBooks.objects.all():
        ib.content_type = student_type
        ib.object_id = ib.user.id  # assuming 'user' was previously a FK to Students
        ib.save()

class Migration(migrations.Migration):

    dependencies = [
        ('Library', '0010_setting_students_fine_teacher_fine'),
    ]

    operations = [
        migrations.RunPython(populate_content_type),
    ]
