"""Reusable footer component."""
import reflex as rx
from portfolio.data import PERSONAL


def footer() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.link("Home", href="/", class_name="footer-link"),
                rx.link("Blog", href="/blog", class_name="footer-link"),
                rx.link("Contact", href="/contact", class_name="footer-link"),
                rx.link("GitHub", href=PERSONAL["github"], class_name="footer-link", is_external=True),
                rx.link("LinkedIn", href=PERSONAL["linkedin"], class_name="footer-link", is_external=True),
                spacing="6",
                wrap="wrap",
                justify="center",
            ),
            rx.divider(class_name="footer-divider"),
            rx.text(
                f"© 2024 {PERSONAL['name']}. Built with Reflex Python.",
                class_name="footer-copy",
            ),
            spacing="4",
            align="center",
            width="100%",
        ),
        class_name="footer",
    )
