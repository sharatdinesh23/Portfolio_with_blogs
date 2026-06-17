"""Reusable navbar component."""
import reflex as rx
from portfolio.state import State


def nav_link(text: str, href: str) -> rx.Component:
    return rx.link(
        text,
        href=href,
        class_name="nav-link",
    )


def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            # Logo
            rx.link(
                rx.box(
                    rx.text("DA", class_name="logo-text"),
                    class_name="logo-box",
                ),
                href="/",
            ),
            # Desktop nav links
            rx.hstack(
                nav_link("Home", "/"),
                nav_link("Skills", "/#skills"),
                nav_link("Projects", "/#projects"),
                nav_link("Experience", "/#experience"),
                nav_link("Blog", "/blog"),
                nav_link("Contact", "/contact"),
                spacing="6",
                class_name="desktop-nav",
            ),
            # Theme toggle + mobile menu
            rx.hstack(
                rx.el.button(
                    rx.box(
                        rx.text("🌙"),
                        rx.text("☀️"),
                        class_name="theme-toggle-icon",
                    ),
                    on_click=State.toggle_theme,
                    class_name="theme-toggle",
                ),
                # Mobile hamburger
                rx.el.button(
                    rx.text("☰", font_size="1.3rem"),
                    on_click=State.toggle_menu,
                    class_name="mobile-menu-btn desktop-hidden",
                ),
                spacing="3",
                align="center",
            ),
            align="center",
            justify="between",
            width="100%",
        ),
        # Mobile dropdown menu
        rx.cond(
            State.menu_open,
            rx.vstack(
                nav_link("Home", "/"),
                nav_link("Skills", "/#skills"),
                nav_link("Projects", "/#projects"),
                nav_link("Experience", "/#experience"),
                nav_link("Blog", "/blog"),
                nav_link("Contact", "/contact"),
                class_name="mobile-nav",
                spacing="4",
                align="start",
                width="100%",
            ),
            rx.fragment(),
        ),
        class_name="navbar",
        id="top",
    )
