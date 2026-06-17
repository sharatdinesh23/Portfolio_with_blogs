"""Home page — the main portfolio landing page."""
import reflex as rx
from portfolio.state import State
from portfolio.data import (
    PERSONAL, TECH_SKILLS, PROJECTS, EXPERIENCE,
    EDUCATION, TESTIMONIALS
)
from portfolio.components.navbar import navbar
from portfolio.components.footer import footer


# ── Hero Section ─────────────────────────────────────────────────────────────
def hero_code_block() -> rx.Component:
    return rx.box(
        rx.box(
            rx.hstack(
                rx.box(class_name="code-dot code-dot-red"),
                rx.box(class_name="code-dot code-dot-yellow"),
                rx.box(class_name="code-dot code-dot-green"),
                rx.text("main.py", class_name="code-title"),
                spacing="2",
                align="center",
            ),
            class_name="code-header",
        ),
        rx.box(
            rx.html(
                '<span class="code-keyword">from</span> fastapi <span class="code-keyword">import</span> FastAPI\n'
                '<span class="code-keyword">from</span> uuid <span class="code-keyword">import</span> UUID\n\n'
                'app = FastAPI()\n\n'
                '<span class="code-keyword">@app</span>.get(<span class="code-string">"/v1/insights"</span>)\n'
                '<span class="code-keyword">async def</span> <span class="code-function">get_analytics</span>(\n'
                '    <span class="code-param">user_id</span>: UUID\n'
                '):\n'
                '    data = <span class="code-keyword">await</span> db.query(user_id)\n'
                '    <span class="code-comment"># Run predictive model</span>\n'
                '    result = model.predict(data)\n'
                '    <span class="code-keyword">return</span> {\n'
                '        <span class="code-string">"status"</span>: <span class="code-string">"success"</span>,\n'
                '        <span class="code-string">"latency"</span>: <span class="code-string">"12ms"</span>,\n'
                '        <span class="code-string">"data"</span>: result\n'
                '    }',
            ),
            class_name="code-content",
        ),
        class_name="code-block",
    )


def hero_section() -> rx.Component:
    return rx.box(
        rx.hstack(
            # Left: Text content
            rx.vstack(
                rx.box(
                    rx.hstack(
                        rx.box(class_name="hero-badge-dot"),
                        rx.text("Available for new projects"),
                        spacing="2",
                        align="center",
                    ),
                    class_name="hero-badge",
                ),
                rx.heading(
                    PERSONAL["title"].split(" & ")[0] + " &",
                    rx.el.br(),
                    rx.el.span(PERSONAL["title"].split(" & ")[1], class_name="hero-title-accent"),
                    class_name="hero-title",
                    as_="h1",
                ),
                rx.text(
                    PERSONAL["tagline"] + " " + PERSONAL["bio"],
                    class_name="hero-desc",
                ),
                rx.hstack(
                    rx.link(
                        "View Projects →",
                        href="/#projects",
                        class_name="btn-primary",
                    ),
                    rx.link(
                        "Contact Me",
                        href="/contact",
                        class_name="btn-secondary",
                    ),
                    spacing="4",
                    wrap="wrap",
                ),
                align="start",
                spacing="5",
                class_name="hero-left",
            ),
            # Right: Code block
            rx.box(
                hero_code_block(),
                class_name="hero-right",
            ),
            align="center",
            spacing="8",
        ),
        class_name="hero",
        id="home",
    )


# ── Skills Section ────────────────────────────────────────────────────────────
def skill_card(skill: dict) -> rx.Component:
    return rx.box(
        rx.text(skill["icon"], class_name="skill-icon"),
        rx.text(skill["name"], class_name="skill-name"),
        rx.text(skill["level"], class_name="skill-level"),
        class_name="skill-card",
    )


def skills_section() -> rx.Component:
    return rx.box(
        rx.text("TECHNICAL ARSENAL", class_name="section-label"),
        rx.heading("Technologies & Tools", class_name="section-title", as_="h2"),
        rx.text(
            "The technologies and tools powering precision-driven solutions.",
            class_name="section-subtitle",
        ),
        rx.box(
            *[skill_card(skill) for skill in TECH_SKILLS],
            class_name="skills-grid",
        ),
        class_name="section",
        id="skills",
    )


# ── Projects Section ──────────────────────────────────────────────────────────
def project_card(project: dict) -> rx.Component:
    return rx.box(
        rx.box(
            rx.text("⚡ " + project["highlight"], class_name="project-highlight"),
        ),
        rx.heading(project["title"], class_name="project-title", as_="h3"),
        rx.text(project["description"], class_name="project-desc"),
        rx.box(
            *[rx.text(tag, class_name="tag") for tag in project["tags"]],
            class_name="tags-row",
        ),
        rx.hstack(
            rx.link("↗ GitHub", href=project["github"], class_name="project-link", is_external=True),
            rx.link("→ Demo", href=project["demo"], class_name="project-link"),
            spacing="4",
        ),
        class_name="project-card",
    )


def projects_section() -> rx.Component:
    return rx.box(
        rx.text("SELECTED WORKS", class_name="section-label"),
        rx.heading("End-to-End Data Products", class_name="section-title", as_="h2"),
        rx.text(
            "High-performance APIs and data pipelines built for production scale.",
            class_name="section-subtitle",
        ),
        rx.box(
            *[project_card(p) for p in PROJECTS],
            class_name="projects-grid",
        ),
        class_name="section",
        id="projects",
    )


# ── Experience Section ────────────────────────────────────────────────────────
def exp_entry(exp: dict) -> rx.Component:
    return rx.box(
        rx.box(class_name="exp-dot"),
        rx.text(exp["period"], class_name="exp-period"),
        rx.heading(exp["role"], class_name="exp-role", as_="h3"),
        rx.text(exp["company"], class_name="exp-company"),
        rx.text(exp["description"], class_name="exp-desc"),
        rx.box(
            *[rx.text(a, class_name="exp-badge") for a in exp["achievements"]],
            class_name="exp-achievements",
        ),
        class_name="exp-entry",
    )


def experience_section() -> rx.Component:
    return rx.box(
        rx.text("PROFESSIONAL PATH", class_name="section-label"),
        rx.heading("Work Experience", class_name="section-title", as_="h2"),
        rx.text(
            "Building data systems and APIs that drive measurable results.",
            class_name="section-subtitle",
        ),
        rx.box(
            *[exp_entry(e) for e in EXPERIENCE],
            class_name="experience-timeline",
        ),
        class_name="section",
        id="experience",
    )


# ── Education Section ─────────────────────────────────────────────────────────
def education_section() -> rx.Component:
    edu = EDUCATION
    return rx.box(
        rx.text("EDUCATION", class_name="section-label"),
        rx.heading("Academic Background", class_name="section-title", as_="h2"),
        rx.box(
            rx.heading(edu["degree"], class_name="edu-degree", as_="h3"),
            rx.text(edu["school"], class_name="edu-school"),
            rx.text(edu["period"], class_name="edu-period"),
            rx.text(edu["description"], class_name="edu-desc"),
            rx.text(f'Thesis: "{edu["thesis"]}"', class_name="edu-thesis"),
            rx.text("Certifications", class_name="certs-title"),
            *[
                rx.box(
                    rx.text("🏆", class_name="cert-icon"),
                    rx.vstack(
                        rx.text(c["name"], class_name="cert-name"),
                        rx.text(c["issuer"], class_name="cert-issuer"),
                        spacing="0",
                        align="start",
                    ),
                    class_name="cert-item",
                )
                for c in edu["certifications"]
            ],
            class_name="edu-card",
        ),
        class_name="section",
        id="education",
    )


# ── Testimonials Section ──────────────────────────────────────────────────────
def testimonial_card(t: dict) -> rx.Component:
    return rx.box(
        rx.text('"', class_name="quote-mark"),
        rx.text(t["quote"], class_name="testimonial-text"),
        rx.box(
            rx.box(t["avatar"], class_name="author-avatar"),
            rx.vstack(
                rx.text(t["name"], class_name="author-name"),
                rx.text(t["role"], class_name="author-role"),
                spacing="0",
                align="start",
            ),
            class_name="testimonial-author",
        ),
        class_name="testimonial-card",
    )


def testimonials_section() -> rx.Component:
    return rx.box(
        rx.text("VOICES OF TRUST", class_name="section-label"),
        rx.heading("What Collaborators Say", class_name="section-title", as_="h2"),
        rx.text(
            "Collaborations that drove real impact and technical excellence.",
            class_name="section-subtitle",
        ),
        rx.box(
            *[testimonial_card(t) for t in TESTIMONIALS],
            class_name="testimonials-grid",
        ),
        class_name="section",
        id="testimonials",
    )


# ── Connect Section ───────────────────────────────────────────────────────────
def connect_section() -> rx.Component:
    return rx.box(
        rx.box(
            rx.text("START A CONNECTION", class_name="section-label", style={"text-align": "center"}),
            rx.heading(
                "Let's Build Something", rx.el.br(),
                rx.el.span("Remarkable Together", class_name="gradient-text"),
                class_name="section-title",
                as_="h2",
                style={"text-align": "center"},
            ),
            rx.text(
                "Have a technical challenge or a data pipeline that needs scaling? Let's discuss how I can help.",
                class_name="section-subtitle",
                style={"text-align": "center", "margin": "0 auto"},
            ),
            rx.box(
                rx.link("🔗 LinkedIn", href=PERSONAL["linkedin"], class_name="contact-link-btn", is_external=True),
                rx.link("🐙 GitHub", href=PERSONAL["github"], class_name="contact-link-btn", is_external=True),
                rx.link("✉️ Email Me", href=f"mailto:{PERSONAL['email']}", class_name="contact-link-btn"),
                rx.link("📋 Contact Form →", href="/contact", class_name="btn-primary"),
                class_name="contact-links",
            ),
            class_name="contact-connect",
        ),
        class_name="section",
        id="contact",
    )


# ── Main Page ─────────────────────────────────────────────────────────────────
def index() -> rx.Component:
    return rx.box(
        # Animated background orbs
        rx.box(
            rx.box(class_name="orb orb-1"),
            rx.box(class_name="orb orb-2"),
            rx.box(class_name="orb orb-3"),
            class_name="bg-orbs",
        ),
        rx.box(
            navbar(),
            hero_section(),
            rx.box(class_name="divider", style={"margin": "0 3rem"}),
            skills_section(),
            rx.box(class_name="divider", style={"margin": "0 3rem"}),
            projects_section(),
            rx.box(class_name="divider", style={"margin": "0 3rem"}),
            experience_section(),
            rx.box(class_name="divider", style={"margin": "0 3rem"}),
            education_section(),
            rx.box(class_name="divider", style={"margin": "0 3rem"}),
            testimonials_section(),
            rx.box(class_name="divider", style={"margin": "0 3rem"}),
            connect_section(),
            footer(),
            class_name="page-wrapper",
        ),
        class_name=rx.cond(State.is_dark, "theme-wrapper", "theme-wrapper light"),
        style={"min-height": "100vh"},
    )
