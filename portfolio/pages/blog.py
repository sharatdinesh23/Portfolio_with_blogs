"""Blog page."""
import reflex as rx

from portfolio.components.footer import footer
from portfolio.components.navbar import navbar
from portfolio.state import BlogPost, State


def post_meta_row(post: BlogPost) -> rx.Component:
    return rx.hstack(
        rx.text(post.display_date, class_name="post-meta"),
        rx.text("\u00b7", class_name="post-meta post-meta-sep"),
        rx.text(f"{post.read_time} min read", class_name="post-meta"),
        spacing="2",
        align="center",
    )


def blog_card_component(post: BlogPost) -> rx.Component:
    return rx.box(
        rx.hstack(
            post_meta_row(post),
            rx.spacer(),
            rx.cond(
                State.is_admin,
                rx.hstack(
                    rx.tooltip(
                        rx.box(
                            rx.icon(tag="pencil", size=16),
                            on_click=lambda: State.load_blog_for_edit(post),
                            class_name="admin-icon-btn edit",
                        ),
                        content="Edit Post",
                    ),
                    rx.tooltip(
                        rx.box(
                            rx.icon(tag="send", size=16),
                            on_click=lambda: State.post_blog_to_linkedin(post.id),
                            class_name="admin-icon-btn linkedin",
                        ),
                        content="Post to LinkedIn",
                    ),
                    rx.tooltip(
                        rx.box(
                            rx.icon(tag="trash-2", size=16),
                            on_click=lambda: State.delete_blog(post.id),
                            class_name="admin-icon-btn delete",
                        ),
                        content="Delete Post",
                    ),
                    spacing="2",
                ),
            ),
            width="100%",
            align="center",
        ),
        rx.heading(post.title, class_name="blog-card-title", as_="h3"),
        rx.text(post.excerpt, class_name="blog-card-desc"),
        rx.box(
            rx.foreach(
                post.tags,
                lambda tag: rx.text(tag, class_name="tag tag-neutral"),
            ),
            class_name="tags-row",
        ),
        rx.link("Read More \u2192", href=f"/blog/{post.id}", class_name="read-more"),
        class_name="blog-card",
    )


def markdown_toolbar_item(icon: str, tag: str, label: str) -> rx.Component:
    return rx.tooltip(
        rx.box(
            rx.icon(tag=icon, size=18),
            on_click=lambda: State.insert_markdown(tag),
            class_name="toolbar-item",
        ),
        content=label,
    )


def markdown_toolbar() -> rx.Component:
    return rx.hstack(
        markdown_toolbar_item("heading-1", "h1", "Main Heading"),
        markdown_toolbar_item("heading-2", "h2", "Side Heading"),
        markdown_toolbar_item("heading-3", "h3", "Sub Heading"),
        markdown_toolbar_item("bold", "bold", "Bold"),
        markdown_toolbar_item("italic", "italic", "Italic"),
        markdown_toolbar_item("code", "code", "Inline Code"),
        markdown_toolbar_item("link", "link", "Insert Link"),
        markdown_toolbar_item("image", "image", "Insert Image"),
        markdown_toolbar_item("list", "list", "Bullet List"),
        markdown_toolbar_item("quote", "quote", "Blockquote"),
        markdown_toolbar_item("minus", "divider", "Horizontal Rule"),
        spacing="1",
        class_name="markdown-toolbar",
    )


def blog_editor_modal() -> rx.Component:
    """A modal to create or edit blog posts."""
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                "+ New Post",
                on_click=State.open_new_blog_editor,
                class_name="btn-primary",
                style={
                    "position": "fixed",
                    "bottom": "2rem",
                    "right": "2rem",
                    "z-index": "1000",
                    "box-shadow": "0 10px 25px rgba(0,0,0,0.3)",
                    "border-radius": "100px",
                    "padding": "0.75rem 1.5rem",
                },
            ),
        ),
        rx.dialog.content(
            rx.dialog.title(
                rx.cond(State.current_blog_id, "Edit Insight", "Compose New Insight"),
            ),
            rx.dialog.description("Update your technical thoughts for the world."),
            rx.vstack(
                rx.text("Title", class_name="img2-label"),
                rx.input(
                    placeholder="Enter post title...",
                    on_change=State.set_current_blog_title,
                    value=State.current_blog_title,
                    class_name="img2-input",
                    width="100%",
                ),
                rx.text("Excerpt (Optional)", class_name="img2-label"),
                rx.input(
                    placeholder="Short summary for the card...",
                    on_change=State.set_current_blog_excerpt,
                    value=State.current_blog_excerpt,
                    class_name="img2-input",
                    width="100%",
                ),
                rx.text("Tags (comma separated)", class_name="img2-label"),
                rx.input(
                    placeholder="FastAPI, Python, Data Engineering",
                    on_change=State.set_current_blog_tags,
                    value=State.current_blog_tags,
                    class_name="img2-input",
                    width="100%",
                ),
                rx.text("Content (Markdown supported)", class_name="img2-label"),
                markdown_toolbar(),
                rx.text_area(
                    placeholder="Write your article here...",
                    on_change=State.set_current_blog_content,
                    value=State.current_blog_content,
                    class_name="img2-input img2-input-no-top",
                    style={"min-height": "300px", "margin-top": "0"},
                    width="100%",
                ),
                rx.hstack(
                    rx.dialog.close(
                        rx.button("Cancel", variant="soft", color_scheme="gray"),
                    ),
                    rx.button(
                        rx.cond(State.current_blog_id, "Update Post", "Publish Post"),
                        on_click=State.create_blog,
                        class_name="btn-primary",
                    ),
                    spacing="3",
                    width="100%",
                    justify="end",
                    margin_top="1rem",
                ),
                spacing="4",
                width="100%",
                align="start",
            ),
            style={
                "max-width": "700px",
                "background": "var(--bg-card)",
                "border": "1px solid var(--border)",
            },
        ),
        open=State.is_creating_blog,
        on_open_change=State.set_is_creating_blog,
    )


def admin_login_modal() -> rx.Component:
    """A hidden or small modal to login as admin."""
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon(tag="lock", size=14),
                rx.cond(State.is_admin, "Admin Panel", "Admin Login"),
                variant="ghost",
                size="1",
                color_scheme="gray",
                style={
                    "opacity": "0.3",
                    "&:hover": {"opacity": "1"},
                    "margin-top": "1.5rem",
                },
            ),
        ),
        rx.dialog.content(
            rx.dialog.title("Admin Access"),
            rx.dialog.description("Enter your administrative password."),
            rx.cond(
                State.is_admin,
                rx.vstack(
                    rx.text("You are currently logged in as admin."),
                    rx.button("Logout", on_click=State.logout, color_scheme="red", width="100%"),
                    width="100%",
                    align="center",
                    spacing="4",
                    padding_top="1rem",
                ),
                rx.vstack(
                    rx.input(
                        type="password",
                        placeholder="Enter password...",
                        on_change=State.set_login_password,
                        value=State.login_password,
                        width="100%",
                    ),
                    rx.text(State.login_error, color="red", size="2"),
                    rx.button(
                        "Login",
                        on_click=State.check_login,
                        width="100%",
                        class_name="btn-primary",
                    ),
                    width="100%",
                    spacing="3",
                    padding_top="1rem",
                ),
            ),
            style={
                "max-width": "400px",
                "background": "var(--bg-card)",
                "border": "1px solid var(--border)",
            },
        ),
    )


def blog() -> rx.Component:
    return rx.box(
        rx.box(
            rx.box(class_name="orb orb-1"),
            rx.box(class_name="orb orb-2"),
            class_name="bg-orbs",
        ),
        rx.box(
            navbar(),
            rx.box(
                rx.text("DATA INSIGHTS", class_name="section-label"),
                rx.heading(
                    "Data Insights &",
                    rx.el.br(),
                    rx.el.span("Technical Musings", style={"color": "var(--accent)"}),
                    class_name="section-title",
                    as_="h1",
                ),
                rx.text(
                    "Exploring the intersection of high-performance backend architecture and analytical storytelling. "
                    "From FastAPI optimization to complex data visualizations.",
                    class_name="section-subtitle",
                ),
                admin_login_modal(),
                class_name="blog-hero",
            ),
            rx.cond(
                State.blogs.length() > 0,
                rx.box(
                    rx.foreach(State.blogs, blog_card_component),
                    class_name="blog-grid",
                ),
                rx.vstack(
                    rx.text("No posts yet. Be the first to share an insight!", class_name="section-subtitle"),
                    spacing="4",
                    padding="5rem",
                    align="center",
                ),
            ),
            rx.cond(
                State.is_admin,
                blog_editor_modal(),
            ),
            footer(),
            class_name="page-wrapper",
        ),
        class_name=rx.cond(State.is_dark, "theme-wrapper", "theme-wrapper light"),
        style={"min-height": "100vh"},
        on_mount=State.fetch_blogs,
    )
