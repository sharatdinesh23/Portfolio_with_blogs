"""Main Reflex application — registers all pages."""
import reflex as rx

from portfolio.pages.index import index
from portfolio.pages.blog import blog
from portfolio.pages.blog_post import blog_post
from portfolio.pages.contact import contact

app = rx.App(
    stylesheets=["/site.css"],
    style={
        "font_family": "Inter, sans-serif",
    },
)

app.add_page(index, route="/", title="Sharath Dinesh | Data Analyst & FastAPI Developer")
app.add_page(blog, route="/blog", title="Blog | Sharath Dinesh")
app.add_page(blog_post, route="/blog/[id]", title="Blog Post | Sharath Dinesh")
app.add_page(contact, route="/contact", title="Contact | Sharath Dinesh")
