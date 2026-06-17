"""Contact page."""
import reflex as rx
from portfolio.state import State
from portfolio.data import PERSONAL
from portfolio.components.navbar import navbar
from portfolio.components.footer import footer


def contact() -> rx.Component:
    return rx.box(
        rx.box(
            rx.box(class_name="orb orb-1"),
            rx.box(class_name="orb orb-3"),
            class_name="bg-orbs",
        ),
        rx.box(
            navbar(),
            # Hero content
            rx.box(
                rx.heading(
                    "Start a",
                    rx.el.br(),
                    rx.el.span("Conversation", style={"color": "var(--accent)"}),
                    class_name="section-title",
                    as_="h1",
                ),
                rx.text(
                    "Ready to optimize your backend architecture or derive insights from your data? "
                    "Reach out for collaborations or technical consulting.",
                    class_name="section-subtitle",
                    style={"margin-top": "1rem", "font-size": "1.1rem"},
                ),
                class_name="contact-hero",
                style={"padding-bottom": "2rem"},
            ),
            
            # Contact Grid: Left Form, Right Details + Map
            rx.box(
                # LEFT SIDE: FORM (Image 2)
                rx.box(
                    rx.cond(
                        State.form_submitted,
                        rx.box("Message sent successfully! I'll get back to you soon.", class_name="success-box"),
                    ),
                    rx.cond(
                        State.form_error,
                        rx.text(State.form_error, class_name="form-error", margin_bottom="1rem"),
                    ),
                    rx.form(
                        rx.vstack(
                            rx.hstack(
                                rx.box(
                                    rx.text("FULL NAME", class_name="img2-label"),
                                    rx.input(placeholder="John Doe", id="name", class_name="img2-input", on_blur=State.set_contact_name, required=True),
                                    width="100%"
                                ),
                                rx.box(
                                    rx.text("WORK EMAIL", class_name="img2-label"),
                                    rx.input(placeholder="john@company.com", id="email", type="email", class_name="img2-input", on_blur=State.set_contact_email, required=True),
                                    width="100%"
                                ),
                                spacing="4", width="100%", class_name="form-row-mobile"
                            ),
                            rx.box(
                                rx.text("INQUIRY SUBJECT", class_name="img2-label"),
                                rx.select(
                                    ["Backend Development (FastAPI)", "Data Analysis","Reconciliation Analysis", "Consulting", "Other"],
                                    placeholder="Select a subject...",
                                    class_name="img2-input",
                                    on_change=State.set_contact_subject,
                                ),
                                width="100%"
                            ),
                            rx.box(
                                rx.text("MESSAGE", class_name="img2-label"),
                                rx.text_area(placeholder="Tell me about your project requirements...", id="message", class_name="img2-input img2-textarea", on_blur=State.set_contact_message, required=True),
                                width="100%"
                            ),
                            rx.el.button("Send Message ▷", type="submit", class_name="img2-submit"),
                            spacing="5", width="100%", align="start"
                        ),
                        on_submit=State.submit_contact,
                        reset_on_submit=True,
                    ),
                    class_name="img2-form-card"
                ),
                
                # RIGHT SIDE: DETAILS & MAP (Images 1 & 3)
                rx.vstack(
                    # Email Card (Image 3 Top)
                    rx.box(
                        rx.hstack(
                            rx.box(
                                rx.icon(tag="mail", size=24, color="#0284c7"),
                                class_name="img3-icon-box"
                            ),
                            rx.vstack(
                                rx.text("Professional Email", class_name="img3-title"),
                                rx.text("Expect a response within 24 hours.", class_name="img3-subtitle"),
                                rx.link(PERSONAL["email"], href=f"mailto:{PERSONAL['email']}", class_name="img3-link"),
                                spacing="1", align="start"
                            ),
                            spacing="4", align="center"
                        ),
                        class_name="img3-card"
                    ),
                    
                    # Digital Footprint Card (Image 3 Bottom)
                    rx.box(
                        rx.text("Digital Footprint", class_name="img3-title", margin_bottom="1.25rem"),
                        rx.vstack(
                            rx.link(
                                rx.hstack(
                                    rx.icon(tag="link", size=18, color="#64748b"),
                                    rx.text("LinkedIn Profile", class_name="img3-footprint-text"),
                                    spacing="3", align="center"
                                ),
                                href=PERSONAL["linkedin"], is_external=True, class_name="img3-footprint-link"
                            ),
                            rx.link(
                                rx.hstack(
                                    rx.icon(tag="code", size=18, color="#64748b"),
                                    rx.text("GitHub Repository", class_name="img3-footprint-text"),
                                    spacing="3", align="center"
                                ),
                                href=PERSONAL["github"], is_external=True, class_name="img3-footprint-link"
                            ),
                            spacing="3", width="100%"
                        ),
                        class_name="img3-card"
                    ),
                    
                    # Map (Image 1)
                    rx.box(
                        rx.box(
                            rx.hstack(
                                rx.icon(tag="map-pin", color="#38bdf8", size=20),
                                rx.text("Remote / Mumbai, India", font_weight="700", color="#ffffff", font_size="1.15rem"),
                                spacing="2", align="center", margin_bottom="0.25rem"
                            ),
                            rx.text("Available for global timezones.", color="#94a3b8", font_size="0.85rem", padding_left="1.75rem"),
                            class_name="img1-map-overlay"
                        ),
                        class_name="img1-map-card"
                    ),
                    
                    spacing="5", width="100%"
                ),
                class_name="contact-grid",
                style={"grid-template-columns": "repeat(auto-fit, minmax(350px, 1fr))", "gap": "3rem"}
            ),
            
            footer(),
            class_name="page-wrapper",
        ),
        class_name=rx.cond(State.is_dark, "theme-wrapper", "theme-wrapper light"),
        style={"min-height": "100vh"},
    )
