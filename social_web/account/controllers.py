from aiohttp_jinja2 import render_template_async


async def index(request):
    context = {'foo': 'bar'}
    return await render_template_async(
        'account/detail.html',
        request,
        context,
    )
