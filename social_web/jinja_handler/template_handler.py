from jinja2 import Environment, FileSystemLoader, select_autoescape


template_env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', ])
)


def render_template(template_name: str, context: dict = None):
    template = template_env.get_template(template_name)
    return template.render(context)