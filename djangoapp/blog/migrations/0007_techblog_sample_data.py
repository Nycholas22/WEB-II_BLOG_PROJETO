from django.conf import settings
from django.db import migrations


def create_techblog_sample_data(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Category = apps.get_model('blog', 'Category')
    Tag = apps.get_model('blog', 'Tag')
    Post = apps.get_model('blog', 'Post')
    SiteSetup = apps.get_model('site_setup', 'SiteSetup')
    MenuLink = apps.get_model('site_setup', 'MenuLink')

    author, _ = User.objects.get_or_create(
        username='ithalo',
        defaults={
            'first_name': 'Ithalo',
            'email': 'ithalo@example.com',
        },
    )

    site_setup, _ = SiteSetup.objects.update_or_create(
        id=1,
        defaults={
            'title': 'TechBlog Escolar',
            'description': (
                'Noticias e curiosidades sobre tecnologia para estudantes.'
            ),
            'show_header': True,
            'show_search': True,
            'show_menu': True,
            'show_description': True,
            'show_pagination': True,
            'show_footer': True,
        },
    )

    menu_links = [
        ('Inicio', '/'),
        ('Inteligencia Artificial', '/tag/inteligencia-artificial/'),
        ('Seguranca Digital', '/tag/seguranca-digital/'),
    ]

    for text, url_or_path in menu_links:
        MenuLink.objects.get_or_create(
            site_setup=site_setup,
            text=text,
            defaults={'url_or_path': url_or_path},
        )

    category, _ = Category.objects.get_or_create(
        slug='tecnologia',
        defaults={'name': 'Tecnologia'},
    )

    tags = {}
    for name, slug in [
        ('Inteligencia Artificial', 'inteligencia-artificial'),
        ('Seguranca Digital', 'seguranca-digital'),
        ('Programacao', 'programacao'),
        ('Inovacao', 'inovacao'),
    ]:
        tags[slug], _ = Tag.objects.get_or_create(
            slug=slug,
            defaults={'name': name},
        )

    posts = [
        {
            'title': 'Como a inteligencia artificial aparece no dia a dia',
            'slug': 'inteligencia-artificial-no-dia-a-dia',
            'excerpt': (
                'Assistentes virtuais, recomendacoes e tradutores mostram como '
                'a IA ja faz parte da rotina.'
            ),
            'content': (
                '<p>A inteligencia artificial ajuda computadores a reconhecer '
                'padroes e apoiar tarefas simples. Ela aparece em pesquisas, '
                'aplicativos de estudo, mapas e plataformas de video.</p>'
            ),
            'tags': ['inteligencia-artificial', 'inovacao'],
        },
        {
            'title': 'Dicas basicas de seguranca digital para estudantes',
            'slug': 'seguranca-digital-para-estudantes',
            'excerpt': (
                'Senhas fortes, verificacao em duas etapas e cuidado com links '
                'suspeitos protegem contas pessoais.'
            ),
            'content': (
                '<p>Boas praticas de seguranca digital comecam com senhas '
                'diferentes para cada servico, atencao a mensagens falsas e '
                'uso de autenticacao em duas etapas sempre que possivel.</p>'
            ),
            'tags': ['seguranca-digital'],
        },
        {
            'title': 'Por que aprender programacao na escola',
            'slug': 'por-que-aprender-programacao-na-escola',
            'excerpt': (
                'Programar desenvolve raciocinio logico e ajuda a entender '
                'melhor os sistemas usados todos os dias.'
            ),
            'content': (
                '<p>A programacao permite criar sites, aplicativos e automacoes. '
                'Mesmo projetos pequenos ajudam a praticar solucao de problemas '
                'e organizacao de ideias.</p>'
            ),
            'tags': ['programacao'],
        },
        {
            'title': 'Tecnologias sustentaveis e inovacao',
            'slug': 'tecnologias-sustentaveis-e-inovacao',
            'excerpt': (
                'Novas solucoes tecnologicas podem reduzir desperdicios e apoiar '
                'o uso consciente de energia.'
            ),
            'content': (
                '<p>Sensores, sistemas inteligentes e analise de dados ajudam '
                'empresas e escolas a consumir menos recursos e acompanhar '
                'melhor seus resultados.</p>'
            ),
            'tags': ['inovacao'],
        },
    ]

    for post_data in posts:
        tag_slugs = post_data.pop('tags')
        post, _ = Post.objects.update_or_create(
            slug=post_data['slug'],
            defaults={
                **post_data,
                'is_published': True,
                'cover_in_post_content': False,
                'created_by': author,
                'updated_by': author,
                'category': category,
            },
        )
        post.tags.set([tags[tag_slug] for tag_slug in tag_slugs])


def remove_techblog_sample_data(apps, schema_editor):
    Post = apps.get_model('blog', 'Post')

    Post.objects.filter(slug__in=[
        'inteligencia-artificial-no-dia-a-dia',
        'seguranca-digital-para-estudantes',
        'por-que-aprender-programacao-na-escola',
        'tecnologias-sustentaveis-e-inovacao',
    ]).delete()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('site_setup', '0006_alter_menulink_site_setup'),
        ('blog', '0006_postattachment'),
    ]

    operations = [
        migrations.RunPython(
            create_techblog_sample_data,
            remove_techblog_sample_data,
        ),
    ]
