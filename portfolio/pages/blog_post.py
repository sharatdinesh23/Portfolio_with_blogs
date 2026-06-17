"""Individual blog post detail page."""
import reflex as rx

from portfolio.components.footer import footer
from portfolio.components.navbar import navbar
from portfolio.state import State


def blog_post() -> rx.Component:
    """The blog post detail page."""
    return rx.box(
        rx.box(
            rx.box(class_name="orb orb-1"),
            rx.box(class_name="orb orb-3"),
            class_name="bg-orbs",
        ),
        rx.box(
            navbar(),
            rx.container(
                rx.vstack(
                    rx.link(
                        rx.hstack(
                            rx.icon(tag="arrow-left", size=18),
                            rx.text("Back to Blogs"),
                            spacing="2",
                            align="center",
                        ),
                        href="/blog",
                        class_name="back-link",
                        margin_bottom="2rem",
                    ),
                    rx.hstack(
                        rx.text(State.selected_blog.display_date, class_name="post-meta"),
                        rx.text("\u00b7", class_name="post-meta post-meta-sep"),
                        rx.text(f"{State.selected_blog.read_time} min read", class_name="post-meta"),
                        spacing="2",
                        align="center",
                    ),
                    rx.heading(
                        State.selected_blog.title,
                        class_name="post-detail-title",
                        as_="h1",
                        size="9",
                    ),
                    rx.box(
                        rx.foreach(
                            State.selected_blog.tags,
                            lambda tag: rx.text(tag, class_name="tag"),
                        ),
                        class_name="tags-row",
                        margin_bottom="2rem",
                    ),
                    rx.cond(
                        State.is_admin,
                        rx.hstack(
                            rx.button(
                                rx.icon(tag="send", size=16),
                                "Post to LinkedIn",
                                on_click=lambda: State.post_blog_to_linkedin(State.selected_blog.id),
                                class_name="btn-secondary linkedin-post-btn",
                            ),
                            class_name="post-admin-actions",
                            margin_bottom="0.5rem",
                        ),
                    ),
                    rx.box(
                        rx.markdown(
                            State.selected_blog.content,
                            class_name="post-content-markdown",
                        ),
                        width="100%",
                        padding_top="2rem",
                        border_top="1px solid var(--border)",
                    ),
                    spacing="4",
                    width="100%",
                    align="start",
                    padding_y="4rem",
                ),
                size="3",
            ),
            footer(),
            class_name="page-wrapper",
        ),
        class_name=rx.cond(State.is_dark, "theme-wrapper", "theme-wrapper light"),
        style={"min-height": "100vh"},
        on_mount=State.fetch_blog_id,
    )
