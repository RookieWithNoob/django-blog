# Generated by Django 2.1 on 2020-06-23 14:47

from django.db import migrations, models
import django.db.models.deletion
import mdeditor.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('title', models.CharField(help_text='标题', max_length=150, verbose_name='标题')),
                ('summary', models.TextField(default='文章摘要等同于网页description内容，请务必填写...', help_text='摘要', max_length=230, verbose_name='文章摘要')),
                ('content', mdeditor.fields.MDTextField(help_text='内容', verbose_name='内容')),
                ('views', models.IntegerField(default=0, help_text='浏览量', verbose_name='阅览量')),
                ('attributes', models.SmallIntegerField(choices=[(0, '转载'), (1, '原创')], default=1, verbose_name='是否原创')),
                ('image_url', models.ImageField(upload_to='article/%Y%m%d/', verbose_name='文章图片')),
            ],
            options={
                'verbose_name': '博客文章',
                'verbose_name_plural': '博客文章',
                'db_table': 'tb_articles',
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('content', models.TextField(help_text='内容', verbose_name='内容')),
                ('articles', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.Article', verbose_name='所属文章')),
            ],
            options={
                'verbose_name': '评论',
                'verbose_name_plural': '评论',
                'db_table': 'tb_comments',
            },
        ),
        migrations.CreateModel(
            name='FriendLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('name', models.CharField(max_length=50, verbose_name='网站名称')),
                ('description', models.CharField(blank=True, max_length=100, verbose_name='网站描述')),
                ('link', models.URLField(help_text='请填写http或https开头的完整形式地址', verbose_name='友链地址')),
                ('logo', models.URLField(blank=True, help_text='请填写http或https开头的完整形式地址', verbose_name='网站LOGO')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('is_active', models.SmallIntegerField(choices=[(0, '无效'), (1, '有效')], default=1, verbose_name='是否有效')),
                ('is_show', models.BooleanField(default=False, verbose_name='是否首页展示')),
            ],
            options={
                'verbose_name': '友情链接',
                'verbose_name_plural': '友情链接',
                'db_table': 'tb_FriendLink',
            },
        ),
        migrations.CreateModel(
            name='HotArticles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('priority', models.IntegerField(help_text='首页热门文章优先级', verbose_name='优先级')),
                ('news', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='article.Article', verbose_name='文章')),
            ],
            options={
                'verbose_name': '热门文章',
                'verbose_name_plural': '热门文章',
                'db_table': 'tb_hot_articles',
            },
        ),
        migrations.CreateModel(
            name='RecommendRead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('recommend_title', models.CharField(help_text='标题', max_length=150, verbose_name='标题')),
                ('recommend_url', models.URLField(help_text='请填写推荐文章的地址', verbose_name='文章地址')),
            ],
            options={
                'verbose_name': '推荐阅读',
                'verbose_name_plural': '推荐阅读',
                'db_table': 'tb_recommend_read',
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('name', models.CharField(help_text='标签名', max_length=64, verbose_name='标签名')),
            ],
            options={
                'verbose_name': '文章标签',
                'verbose_name_plural': '文章标签',
                'db_table': 'tb_tag',
            },
        ),
    ]
