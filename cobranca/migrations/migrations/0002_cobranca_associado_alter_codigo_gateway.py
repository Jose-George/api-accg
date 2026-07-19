from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        (
            "associados",
            "0004_associado_data_ultimo_aviso",
        ),
        (
            "cobranca",
            "0001_initial",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="cobranca",
            name="associado",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=(
                    django.db.models.deletion.PROTECT
                ),
                related_name="cobrancas",
                to="associados.associado",
            ),
        ),
        migrations.AlterField(
            model_name="cobranca",
            name="codigo_gateway",
            field=models.CharField(
                blank=True,
                max_length=100,
                null=True,
                unique=True,
            ),
        ),
    ]