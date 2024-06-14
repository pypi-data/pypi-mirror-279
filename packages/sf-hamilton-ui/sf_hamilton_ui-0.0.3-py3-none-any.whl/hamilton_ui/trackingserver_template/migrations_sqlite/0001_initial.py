# Generated by Django 4.2.6 on 2024-06-08 00:00

import django.core.validators
import django.db.models.deletion
import trackingserver_base.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("trackingserver_projects", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CodeArtifact",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=1024)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("p_function", "Function"),
                            ("p_class", "Class"),
                            ("p_module", "Module"),
                            ("p_unknown", "Unknown"),
                        ],
                        max_length=15,
                    ),
                ),
                ("path", models.CharField(max_length=1024)),
                ("start", models.IntegerField()),
                ("end", models.IntegerField()),
                ("url", models.CharField(max_length=255)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="CodeVersion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="DAGTemplate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255)),
                (
                    "template_type",
                    models.CharField(choices=[("HAMILTON", "Hamilton")], max_length=255),
                ),
                ("config", models.JSONField(null=True)),
                (
                    "dag_hash",
                    models.CharField(
                        max_length=64, validators=[django.core.validators.MinLengthValidator(64)]
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("tags", models.JSONField(null=True)),
                ("code_hash", models.CharField(max_length=1024)),
                (
                    "code_version_info_type",
                    models.CharField(
                        choices=[("git", "Git"), ("ad_hoc", "Ad hoc")], max_length=1024
                    ),
                ),
                ("code_version_info", models.JSONField(null=True)),
                ("code_version_info_schema", models.IntegerField(null=True)),
                (
                    "code_log_store",
                    models.CharField(
                        choices=[("s3", "S3"), ("local", "Local"), ("none", "None")],
                        max_length=1024,
                    ),
                ),
                ("code_log_url", models.CharField(default=None, max_length=1024, null=True)),
                ("code_log_schema_version", models.IntegerField(null=True)),
                (
                    "project",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="trackingserver_projects.project",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="NodeTemplate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(db_index=True, max_length=1024)),
                (
                    "dependencies",
                    trackingserver_base.models.ArrayField(models.CharField(), null=True),
                ),
                (
                    "dependency_specs",
                    trackingserver_base.models.ArrayField(models.JSONField(), null=True),
                ),
                ("dependency_specs_type", models.CharField(max_length=63, null=True)),
                ("dependency_specs_schema_version", models.IntegerField(null=True)),
                ("output", models.JSONField(null=True)),
                ("output_type", models.CharField(max_length=1024, null=True)),
                ("output_schema_version", models.IntegerField(null=True)),
                ("documentation", models.TextField(null=True)),
                ("tags", models.JSONField(null=True)),
                (
                    "classifications",
                    trackingserver_base.models.ArrayField(
                        models.CharField(
                            choices=[
                                ("transform", "Transform"),
                                ("data_saver", "DataSaver"),
                                ("data_loader", "DataLoader"),
                                ("input", "Input"),
                                ("placeholder", "Placeholder"),
                            ]
                        )
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="NodeTemplateCodeArtifactRelation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_primary", models.BooleanField(default=False)),
                (
                    "code_artifact",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="trackingserver_template.codeartifact",
                    ),
                ),
                (
                    "node_template",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="trackingserver_template.nodetemplate",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="nodetemplate",
            name="code_artifacts",
            field=models.ManyToManyField(
                related_name="code_artifacts",
                through="trackingserver_template.NodeTemplateCodeArtifactRelation",
                to="trackingserver_template.codeartifact",
            ),
        ),
        migrations.AddField(
            model_name="nodetemplate",
            name="dag_template",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="trackingserver_template.dagtemplate",
            ),
        ),
        migrations.CreateModel(
            name="DAGTemplateAttribute",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=63)),
                ("type", models.CharField(max_length=63)),
                ("schema_version", models.IntegerField()),
                ("value", models.JSONField()),
                (
                    "dag_template",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="trackingserver_template.dagtemplate",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="codeartifact",
            name="dag_template",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="trackingserver_template.dagtemplate",
            ),
        ),
        migrations.AddConstraint(
            model_name="nodetemplatecodeartifactrelation",
            constraint=models.UniqueConstraint(
                condition=models.Q(("is_primary", True)),
                fields=("node_template", "is_primary"),
                name="unique_primary",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="nodetemplate",
            unique_together={("name", "dag_template")},
        ),
        migrations.AlterUniqueTogether(
            name="dagtemplateattribute",
            unique_together={("name", "dag_template")},
        ),
        migrations.AlterUniqueTogether(
            name="dagtemplate",
            unique_together={("dag_hash", "code_hash", "name", "project")},
        ),
    ]
