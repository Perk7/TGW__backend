# Generated by Django 3.2.5 on 2021-07-02 15:46

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Default country', max_length=20)),
                ('identify', models.CharField(blank=True, default='empire', max_length=50)),
                ('education_quality', models.FloatField(default=0.6)),
                ('education_avail', models.FloatField(default=0.6)),
                ('alchemy', models.FloatField(default=0.6)),
                ('magic', models.FloatField(default=0.6)),
                ('science', models.FloatField(default=0.6)),
                ('technology', models.FloatField(default=0.6)),
                ('export_trash', models.FloatField(default=0.6)),
                ('support', models.FloatField(default=0.6)),
                ('stability', models.FloatField(default=0.6)),
                ('government', models.CharField(default='m,t,a,p', max_length=7)),
                ('area_format', models.CharField(default='c,p,l,e', max_length=7)),
                ('army_salary', models.CharField(default='2,1600,2500', max_length=13)),
                ('army_maintain', models.CharField(default='2,1,3', max_length=5)),
                ('army_equip', models.CharField(default='4,3,1', max_length=5)),
                ('maternal_capital', models.IntegerField(default=5000)),
                ('avg_pension', models.IntegerField(default=1500)),
                ('allowance_unemploy', models.IntegerField(default=500)),
                ('allowance_disability', models.IntegerField(default=500)),
                ('pension_m', models.CharField(default='3', max_length=1)),
                ('pension_w', models.CharField(default='2', max_length=1)),
                ('inflation', models.FloatField(default=5.5)),
                ('law_equal_rights', models.BooleanField(default=True)),
                ('law_torture', models.BooleanField(default=True)),
                ('law_speech', models.BooleanField(default=True)),
                ('law_demonstration', models.BooleanField(default=True)),
                ('law_property', models.BooleanField(default=True)),
                ('law_creation', models.BooleanField(default=True)),
                ('law_rasism', models.BooleanField(default=True)),
                ('law_heritage', models.BooleanField(default=True)),
                ('law_slavery', models.BooleanField(default=True)),
                ('law_court', models.BooleanField(default=True)),
                ('law_child_labour', models.BooleanField(default=True)),
                ('law_monopoly', models.BooleanField(default=True)),
                ('law_free_enterspire', models.BooleanField(default=True)),
                ('law_work_day_limit', models.BooleanField(default=True)),
                ('law_death_penalty', models.BooleanField(default=True)),
                ('tax_physic', models.CharField(default='d z', max_length=7)),
                ('tax_jurid', models.CharField(default='p i g e', max_length=7)),
            ],
            options={
                'verbose_name': 'Default Страна',
                'verbose_name_plural': 'Default Страны',
            },
        ),
        migrations.CreateModel(
            name='Regions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Default region', max_length=20)),
                ('capital', models.CharField(default='Default city', max_length=20)),
                ('population', models.IntegerField(default=500000)),
                ('area', models.IntegerField(default=100)),
                ('universities', models.IntegerField(default=5)),
                ('schools', models.IntegerField(default=15)),
                ('aqueducs', models.IntegerField(default=30)),
                ('stone_road', models.FloatField(default=0.4)),
                ('pave_road', models.FloatField(default=0.1)),
                ('poverty', models.FloatField(default=0.2)),
                ('unemployment', models.FloatField(default=0.08)),
                ('avg_salary', models.IntegerField(default=2500)),
                ('seaside', models.BooleanField(default=False)),
                ('infrastructure', models.FloatField(default=0.5)),
                ('port', models.FloatField(blank=True, default=0.6)),
                ('cargo_ship', models.FloatField(default=0.6)),
                ('people_ship', models.FloatField(default=0.6)),
                ('industry_blackmetall', models.IntegerField(default=700000000)),
                ('industry_colormetall', models.IntegerField(default=400000000)),
                ('industry_coal', models.IntegerField(default=200000000)),
                ('industry_hunting', models.IntegerField(default=300000000)),
                ('industry_fishing', models.IntegerField(default=300000000)),
                ('industry_forestry', models.IntegerField(default=500000000)),
                ('industry_blacksmith', models.IntegerField(default=1000000000)),
                ('industry_animals', models.IntegerField(default=100000000)),
                ('industry_vegetable', models.IntegerField(default=200000000)),
                ('industry_wheat', models.IntegerField(default=300000000)),
                ('industry_typography', models.IntegerField(default=50000000)),
                ('industry_light', models.IntegerField(default=300000000)),
                ('industry_eating', models.IntegerField(default=200000000)),
                ('industry_jewelry', models.IntegerField(default=100000000)),
                ('industry_transport', models.IntegerField(default=200000000)),
                ('industry_alchemy', models.IntegerField(default=50000000)),
                ('industry_hiring', models.IntegerField(default=300000000)),
                ('industry_culture', models.IntegerField(default=100000000)),
                ('industry_other', models.IntegerField(default=300000000)),
                ('needs_blackmetall', models.IntegerField(default=700000000)),
                ('needs_colormetall', models.IntegerField(default=400000000)),
                ('needs_coal', models.IntegerField(default=200000000)),
                ('needs_hunting', models.IntegerField(default=300000000)),
                ('needs_fishing', models.IntegerField(default=300000000)),
                ('needs_forestry', models.IntegerField(default=500000000)),
                ('needs_blacksmith', models.IntegerField(default=1000000000)),
                ('needs_animals', models.IntegerField(default=100000000)),
                ('needs_vegetable', models.IntegerField(default=200000000)),
                ('needs_wheat', models.IntegerField(default=300000000)),
                ('needs_typography', models.IntegerField(default=50000000)),
                ('needs_light', models.IntegerField(default=300000000)),
                ('needs_eating', models.IntegerField(default=200000000)),
                ('needs_jewelry', models.IntegerField(default=100000000)),
                ('needs_transport', models.IntegerField(default=200000000)),
                ('needs_alchemy', models.IntegerField(default=50000000)),
                ('needs_hiring', models.IntegerField(default=300000000)),
                ('needs_culture', models.IntegerField(default=100000000)),
                ('needs_other', models.IntegerField(default=300000000)),
            ],
            options={
                'verbose_name': 'Default Регион',
                'verbose_name_plural': 'Default Регионы',
            },
        ),
        migrations.CreateModel(
            name='SaveContracts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('con_type', models.CharField(choices=[('AL', 'Alliance'), ('CM', 'Common market'), ('CT', 'Culture transfer'), ('SH', 'Social help'), ('EH', 'Economic help'), ('PA', 'Passage of army'), ('ES', 'Economic sanctions'), ('DW', 'Declare war'), ('CP', 'Contract of Peace'), ('FW', 'Finish war')], default='EH', max_length=2)),
            ],
            options={
                'verbose_name': 'Save Договор',
                'verbose_name_plural': 'Save Договора',
            },
        ),
        migrations.CreateModel(
            name='SaveCountry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Default country', max_length=20)),
                ('identify', models.CharField(blank=True, default='empire', max_length=50)),
                ('education_quality', models.FloatField(default=0.6)),
                ('education_avail', models.FloatField(default=0.6)),
                ('alchemy', models.FloatField(default=0.6)),
                ('magic', models.FloatField(default=0.6)),
                ('science', models.FloatField(default=0.6)),
                ('technology', models.FloatField(default=0.6)),
                ('export_trash', models.FloatField(default=0.6)),
                ('support', models.FloatField(default=0.6)),
                ('stability', models.FloatField(default=0.6)),
                ('government', models.CharField(default='m,t,a,p', max_length=7)),
                ('area_format', models.CharField(default='c,p,l,e', max_length=7)),
                ('army_salary', models.CharField(default='2,1600,2500', max_length=13)),
                ('army_maintain', models.CharField(default='2,1,3', max_length=5)),
                ('army_equip', models.CharField(default='4,3,1', max_length=5)),
                ('maternal_capital', models.IntegerField(default=5000)),
                ('avg_pension', models.IntegerField(default=1500)),
                ('allowance_unemploy', models.IntegerField(default=500)),
                ('allowance_disability', models.IntegerField(default=500)),
                ('pension_m', models.CharField(default='3', max_length=1)),
                ('pension_w', models.CharField(default='2', max_length=1)),
                ('inflation', models.FloatField(default=5.5)),
                ('law_equal_rights', models.BooleanField(default=True)),
                ('law_torture', models.BooleanField(default=True)),
                ('law_speech', models.BooleanField(default=True)),
                ('law_demonstration', models.BooleanField(default=True)),
                ('law_property', models.BooleanField(default=True)),
                ('law_creation', models.BooleanField(default=True)),
                ('law_rasism', models.BooleanField(default=True)),
                ('law_heritage', models.BooleanField(default=True)),
                ('law_slavery', models.BooleanField(default=True)),
                ('law_court', models.BooleanField(default=True)),
                ('law_child_labour', models.BooleanField(default=True)),
                ('law_monopoly', models.BooleanField(default=True)),
                ('law_free_enterspire', models.BooleanField(default=True)),
                ('law_work_day_limit', models.BooleanField(default=True)),
                ('law_death_penalty', models.BooleanField(default=True)),
                ('tax_physic', models.CharField(default='d z', max_length=7)),
                ('tax_jurid', models.CharField(default='p i g e', max_length=7)),
            ],
            options={
                'verbose_name': 'Save Страна',
                'verbose_name_plural': 'Save Страны',
            },
        ),
        migrations.CreateModel(
            name='SaveCountryAI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Default country', max_length=20)),
                ('identify', models.CharField(blank=True, default='empire', max_length=50)),
                ('education_quality', models.FloatField(default=0.6)),
                ('support', models.FloatField(default=0.6)),
                ('stability', models.FloatField(default=0.6)),
                ('government', models.CharField(default='m,t,a,p', max_length=7)),
                ('area_format', models.CharField(default='c,p,l,e', max_length=7)),
                ('army_quality', models.FloatField(default=0.5)),
                ('tax_physic', models.CharField(default='d,z', max_length=7)),
                ('tax_jurid', models.CharField(default='p,i,g,e', max_length=7)),
            ],
            options={
                'verbose_name': 'Save ИИ_Страна',
                'verbose_name_plural': 'Save ИИ_Страны',
            },
        ),
        migrations.CreateModel(
            name='SaveRegions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Default region', max_length=20)),
                ('capital', models.CharField(default='Default city', max_length=20)),
                ('population', models.IntegerField(default=500000)),
                ('area', models.IntegerField(default=100)),
                ('universities', models.IntegerField(default=5)),
                ('schools', models.IntegerField(default=15)),
                ('aqueducs', models.IntegerField(default=30)),
                ('stone_road', models.FloatField(default=0.4)),
                ('pave_road', models.FloatField(default=0.1)),
                ('poverty', models.FloatField(default=0.2)),
                ('unemployment', models.FloatField(default=0.08)),
                ('avg_salary', models.IntegerField(default=2500)),
                ('seaside', models.BooleanField(default=False)),
                ('infrastructure', models.FloatField(default=0.5)),
                ('port', models.FloatField(blank=True, default=0.6)),
                ('cargo_ship', models.FloatField(default=0.6)),
                ('people_ship', models.FloatField(default=0.6)),
                ('industry_blackmetall', models.IntegerField(default=700000000)),
                ('industry_colormetall', models.IntegerField(default=400000000)),
                ('industry_coal', models.IntegerField(default=200000000)),
                ('industry_hunting', models.IntegerField(default=300000000)),
                ('industry_fishing', models.IntegerField(default=300000000)),
                ('industry_forestry', models.IntegerField(default=500000000)),
                ('industry_blacksmith', models.IntegerField(default=1000000000)),
                ('industry_animals', models.IntegerField(default=100000000)),
                ('industry_vegetable', models.IntegerField(default=200000000)),
                ('industry_wheat', models.IntegerField(default=300000000)),
                ('industry_typography', models.IntegerField(default=50000000)),
                ('industry_light', models.IntegerField(default=300000000)),
                ('industry_eating', models.IntegerField(default=200000000)),
                ('industry_jewelry', models.IntegerField(default=100000000)),
                ('industry_transport', models.IntegerField(default=200000000)),
                ('industry_alchemy', models.IntegerField(default=50000000)),
                ('industry_hiring', models.IntegerField(default=300000000)),
                ('industry_culture', models.IntegerField(default=100000000)),
                ('industry_other', models.IntegerField(default=300000000)),
                ('needs_blackmetall', models.IntegerField(default=700000000)),
                ('needs_colormetall', models.IntegerField(default=400000000)),
                ('needs_coal', models.IntegerField(default=200000000)),
                ('needs_hunting', models.IntegerField(default=300000000)),
                ('needs_fishing', models.IntegerField(default=300000000)),
                ('needs_forestry', models.IntegerField(default=500000000)),
                ('needs_blacksmith', models.IntegerField(default=1000000000)),
                ('needs_animals', models.IntegerField(default=100000000)),
                ('needs_vegetable', models.IntegerField(default=200000000)),
                ('needs_wheat', models.IntegerField(default=300000000)),
                ('needs_typography', models.IntegerField(default=50000000)),
                ('needs_light', models.IntegerField(default=300000000)),
                ('needs_eating', models.IntegerField(default=200000000)),
                ('needs_jewelry', models.IntegerField(default=100000000)),
                ('needs_transport', models.IntegerField(default=200000000)),
                ('needs_alchemy', models.IntegerField(default=50000000)),
                ('needs_hiring', models.IntegerField(default=300000000)),
                ('needs_culture', models.IntegerField(default=100000000)),
                ('needs_other', models.IntegerField(default=300000000)),
            ],
            options={
                'verbose_name': 'Save Регион',
                'verbose_name_plural': 'Save Регионы',
            },
        ),
        migrations.CreateModel(
            name='SaveRelations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(default=0)),
                ('pair', models.ManyToManyField(to='App.SaveCountryAI')),
                ('uniq', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.savecountry')),
            ],
            options={
                'verbose_name': 'Save Отношение',
                'verbose_name_plural': 'Save Отношения',
            },
        ),
        migrations.CreateModel(
            name='SaveSquad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pechot_quan', models.IntegerField(default=100)),
                ('archer_quan', models.IntegerField(default=100)),
                ('cavallery_quan', models.IntegerField(default=100)),
                ('catapult_quan', models.IntegerField(default=10)),
                ('place_type', models.CharField(choices=[('G', 'Ground'), ('S', 'Sea')], default='G', max_length=1)),
                ('status', models.CharField(choices=[('R', 'Ready'), ('Q', 'Quartered')], default='Q', max_length=1)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.savecountry')),
            ],
            options={
                'verbose_name': 'Save Отряд',
                'verbose_name_plural': 'Save Отряды',
            },
        ),
        migrations.CreateModel(
            name='SaveSquadAI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pechot_quan', models.IntegerField(default=100)),
                ('archer_quan', models.IntegerField(default=100)),
                ('cavallery_quan', models.IntegerField(default=100)),
                ('catapult_quan', models.IntegerField(default=10)),
                ('place_type', models.CharField(choices=[('G', 'Ground'), ('S', 'Sea')], default='G', max_length=1)),
                ('status', models.CharField(choices=[('R', 'Ready'), ('Q', 'Quartered')], default='Q', max_length=1)),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='App.savecountryai')),
            ],
            options={
                'verbose_name': 'Save ИИ_Отряд',
                'verbose_name_plural': 'Save ИИ_Отряды',
            },
        ),
        migrations.CreateModel(
            name='StartGame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('save_date', models.DateTimeField(auto_now=True)),
                ('contracts', models.ManyToManyField(to='App.SaveContracts')),
                ('country', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='App.savecountry')),
                ('country_ai', models.ManyToManyField(to='App.SaveCountryAI')),
                ('regions', models.ManyToManyField(to='App.SaveRegions')),
                ('relations', models.ManyToManyField(to='App.SaveRelations')),
                ('squad', models.ManyToManyField(to='App.SaveSquad')),
                ('squad_ai', models.ManyToManyField(to='App.SaveSquadAI')),
            ],
            options={
                'verbose_name': 'Save',
                'verbose_name_plural': 'Saves',
            },
        ),
        migrations.CreateModel(
            name='CustomAuth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('active_save', models.IntegerField(default=0)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('saves', models.ManyToManyField(blank=True, to='App.StartGame')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Squad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pechot_quan', models.IntegerField(default=100)),
                ('archer_quan', models.IntegerField(default=100)),
                ('cavallery_quan', models.IntegerField(default=100)),
                ('catapult_quan', models.IntegerField(default=10)),
                ('place_type', models.CharField(choices=[('G', 'Ground'), ('S', 'Sea')], default='G', max_length=1)),
                ('status', models.CharField(choices=[('R', 'Ready'), ('Q', 'Quartered')], default='Q', max_length=1)),
                ('country', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='App.country')),
            ],
            options={
                'verbose_name': 'Default Отряд',
                'verbose_name_plural': 'Default Отряды',
            },
        ),
        migrations.AddField(
            model_name='savecountryai',
            name='capital',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='AI_region_capital', to='App.saveregions'),
        ),
        migrations.AddField(
            model_name='savecountryai',
            name='regions',
            field=models.ManyToManyField(to='App.SaveRegions'),
        ),
        migrations.AddField(
            model_name='savecountry',
            name='capital',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='region_capital', to='App.saveregions'),
        ),
        migrations.AddField(
            model_name='savecountry',
            name='regions',
            field=models.ManyToManyField(to='App.SaveRegions'),
        ),
        migrations.AddField(
            model_name='savecontracts',
            name='pair',
            field=models.ManyToManyField(to='App.SaveCountryAI'),
        ),
        migrations.AddField(
            model_name='savecontracts',
            name='uniq',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.savecountry'),
        ),
        migrations.CreateModel(
            name='Relations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(default=0)),
                ('pair', models.ManyToManyField(to='App.Country')),
            ],
            options={
                'verbose_name': 'Default Отношение',
                'verbose_name_plural': 'Default Отношения',
            },
        ),
        migrations.AddField(
            model_name='country',
            name='capital',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='region_capital', to='App.regions'),
        ),
        migrations.AddField(
            model_name='country',
            name='regions',
            field=models.ManyToManyField(to='App.Regions'),
        ),
        migrations.CreateModel(
            name='Contracts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('con_type', models.CharField(choices=[('AL', 'Alliance'), ('CM', 'Common market'), ('CT', 'Culture transfer'), ('SH', 'Social help'), ('EH', 'Economic help'), ('PA', 'Passage of army'), ('ES', 'Economic sanctions'), ('DW', 'Declare war'), ('CP', 'Contract of Peace'), ('FW', 'Finish war')], default='EH', max_length=2)),
                ('pair', models.ManyToManyField(to='App.Country')),
            ],
            options={
                'verbose_name': 'Default Договор',
                'verbose_name_plural': 'Default Договора',
            },
        ),
    ]
