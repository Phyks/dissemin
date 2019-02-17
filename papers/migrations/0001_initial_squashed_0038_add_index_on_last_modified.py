# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-25 22:20


import caching.base
from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import papers.baremodels
import papers.models


class Migration(migrations.Migration):

    replaces = [(b'papers', '0001_initial'), (b'papers', '0002_remove_disambiguation_models'), (b'papers', '0003_author_position'), (b'papers', '0004_strip_latex'), (b'papers', '0005_researcher_orcid'), (b'papers', '0006_uploadedpdf_instead_of_file_for_depositrecord'), (b'papers', '0007_rename_identifer_to_identifier'), (b'papers', '0008_publication_abstract'), (b'papers', '0009_empty'), (b'papers', '0010_remove_departments'), (b'papers', '0011_researcher_fetch_status'), (b'papers', '0012_add_empty_orcid_profile_to_researcher'), (b'papers', '0013_researchers_have_users'), (b'papers', '0014_paperworld'), (b'papers', '0015_add_paper_task'), (b'papers', '0016_cleaner_doctypes'), (b'papers', '0017_add_departments_and_institutions'), (b'papers', '0018_add_uniqueness_constraints'), (b'papers', '0019_alter_email'), (b'papers', '0020_publication_pdf_url'), (b'papers', '0021_change_department_field_on_researcher'), (b'papers', '0022_department'), (b'papers', '0023_fingerprint_unique'), (b'papers', '0024_publication_to_oairecord'), (b'papers', '0025_migrate_publis'), (b'papers', '0026_delete_publication'), (b'papers', '0027_paper_authors_list'), (b'papers', '0028_migrate_authors'), (b'papers', '0029_delete_authors'), (b'papers', '0030_paper_researchers'), (b'papers', '0031_remove_annotation_simplify_visibility'), (b'papers', '0032_doi_not_unique'), (b'papers', '0033_remove_oairecord_abstract'), (b'papers', '0027_alter_paperworld'), (b'papers', '0034_merge'), (b'papers', '0035_index_doi'), (b'papers', '0036_paper_temp'), (b'papers', '0037_remove_paper_last_modified'), (b'papers', '0038_add_index_on_last_modified')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('statistics', '0001_initial'),
        ('publishers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('stats', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='statistics.AccessStatistics')),
            ],
        ),
        migrations.CreateModel(
            name='Name',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first', models.CharField(max_length=256)),
                ('last', models.CharField(max_length=256)),
                ('full', models.CharField(db_index=True, max_length=513)),
                ('best_confidence', models.FloatField(default=0.0)),
            ],
            options={
                'ordering': ['last', 'first'],
            },
            bases=(models.Model, papers.baremodels.BareName),
        ),
        migrations.CreateModel(
            name='NameVariant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confidence', models.FloatField(default=1.0)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='papers.Name')),
            ],
        ),
        migrations.CreateModel(
            name='OaiRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=512, unique=True)),
                ('splash_url', models.URLField(blank=True, max_length=1024, null=True)),
                ('pdf_url', models.URLField(blank=True, max_length=1024, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('keywords', models.TextField(blank=True, null=True)),
                ('contributors', models.CharField(blank=True, max_length=4096, null=True)),
                ('pubtype', models.CharField(blank=True, choices=[('journal-article', 'Journal article'), ('proceedings-article', 'Proceedings article'), ('book-chapter', 'Book chapter'), ('book', 'Book'), ('journal-issue', 'Journal issue'), ('proceedings', 'Proceedings'), ('reference-entry', 'Entry'), ('poster', 'Poster'), ('report', 'Report'), ('thesis', 'Thesis'), ('dataset', 'Dataset'), ('preprint', 'Preprint'), ('other', 'Other document')], max_length=64, null=True)),
                ('journal_title', models.CharField(blank=True, max_length=512, null=True)),
                ('container', models.CharField(blank=True, max_length=512, null=True)),
                ('publisher_name', models.CharField(blank=True, max_length=512, null=True)),
                ('issue', models.CharField(blank=True, max_length=64, null=True)),
                ('volume', models.CharField(blank=True, max_length=64, null=True)),
                ('pages', models.CharField(blank=True, max_length=64, null=True)),
                ('pubdate', models.DateField(blank=True, null=True)),
                ('doi', models.CharField(blank=True, db_index=True, max_length=1024, null=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('priority', models.IntegerField(default=1)),
            ],
            options={
                'verbose_name': 'OAI record',
            },
            bases=(models.Model, papers.baremodels.BareOaiRecord),
        ),
        migrations.CreateModel(
            name='OaiSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=300, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('oa', models.BooleanField(default=False)),
                ('priority', models.IntegerField(default=1)),
                ('default_pubtype', models.CharField(choices=[('journal-article', 'Journal article'), ('proceedings-article', 'Proceedings article'), ('book-chapter', 'Book chapter'), ('book', 'Book'), ('journal-issue', 'Journal issue'), ('proceedings', 'Proceedings'), ('reference-entry', 'Entry'), ('poster', 'Poster'), ('report', 'Report'), ('thesis', 'Thesis'), ('dataset', 'Dataset'), ('preprint', 'Preprint'), ('other', 'Other document')], max_length=64)),
                ('last_status_update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'OAI source',
            },
            bases=(caching.base.CachingMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1024)),
                ('fingerprint', models.CharField(max_length=64, unique=True)),
                ('date_last_ask', models.DateField(null=True)),
                ('pubdate', models.DateField()),
                ('authors_list', django.contrib.postgres.fields.jsonb.JSONField(default=list)),
                ('last_modified', models.DateTimeField(auto_now=True, db_index=True)),
                ('visible', models.BooleanField(default=True)),
                ('last_annotation', models.CharField(blank=True, max_length=32, null=True)),
                ('doctype', models.CharField(blank=True, choices=[('journal-article', 'Journal article'), ('proceedings-article', 'Proceedings article'), ('book-chapter', 'Book chapter'), ('book', 'Book'), ('journal-issue', 'Journal issue'), ('proceedings', 'Proceedings'), ('reference-entry', 'Entry'), ('poster', 'Poster'), ('report', 'Report'), ('thesis', 'Thesis'), ('dataset', 'Dataset'), ('preprint', 'Preprint'), ('other', 'Other document')], max_length=64, null=True)),
                ('oa_status', models.CharField(blank=True, default='UNK', max_length=32, null=True)),
                ('pdf_url', models.URLField(blank=True, max_length=2048, null=True)),
                ('task', models.CharField(blank=True, max_length=512, null=True)),
            ],
            bases=(models.Model, papers.baremodels.BarePaper),
        ),
        migrations.CreateModel(
            name='PaperWorld',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stats', models.ForeignKey(default=papers.models.create_default_stats, on_delete=django.db.models.deletion.CASCADE, to='statistics.AccessStatistics')),
            ],
            options={
                'verbose_name': 'Paper World',
            },
        ),
        migrations.CreateModel(
            name='Researcher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('homepage', models.URLField(blank=True, null=True)),
                ('role', models.CharField(blank=True, max_length=128, null=True)),
                ('orcid', models.CharField(blank=True, max_length=32, null=True, unique=True)),
                ('empty_orcid_profile', models.NullBooleanField()),
                ('last_harvest', models.DateTimeField(blank=True, null=True)),
                ('harvester', models.CharField(blank=True, max_length=512, null=True)),
                ('current_task', models.CharField(blank=True, choices=[('init', 'Preparing profile'), ('orcid', 'Fetching publications from ORCID'), ('crossref', 'Fetching publications from CrossRef'), ('base', 'Fetching publications from BASE'), ('core', 'Fetching publications from CORE'), ('oai', 'Fetching publications from OAI-PMH'), ('clustering', 'Clustering publications'), ('stats', 'Updating statistics')], max_length=64, null=True)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='papers.Department')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='papers.Name')),
                ('stats', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='statistics.AccessStatistics')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='paper',
            name='researchers',
            field=models.ManyToManyField(to='papers.Researcher'),
        ),
        migrations.AddField(
            model_name='oairecord',
            name='about',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='papers.Paper'),
        ),
        migrations.AddField(
            model_name='oairecord',
            name='journal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='publishers.Journal'),
        ),
        migrations.AddField(
            model_name='oairecord',
            name='publisher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='publishers.Publisher'),
        ),
        migrations.AddField(
            model_name='oairecord',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='papers.OaiSource'),
        ),
        migrations.AddField(
            model_name='namevariant',
            name='researcher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='papers.Researcher'),
        ),
        migrations.AlterUniqueTogether(
            name='name',
            unique_together=set([('first', 'last')]),
        ),
        migrations.AddField(
            model_name='department',
            name='institution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='papers.Institution'),
        ),
        migrations.AddField(
            model_name='department',
            name='stats',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='statistics.AccessStatistics'),
        ),
        migrations.AlterUniqueTogether(
            name='namevariant',
            unique_together=set([('name', 'researcher')]),
        ),
    ]


