import mistletoe as markdowner
from pygments_renderer import PygmentsRenderer

def mdToHtml(md: str) -> str:
    html: str = markdowner.markdown(md, renderer=PygmentsRenderer)
    return html