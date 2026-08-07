from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitudsocio',
            name='fecha_nacimiento',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de nacimiento'),
        ),
    ]
