import asyncio
import os
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client, ClientOptions
import httpx
from datetime import datetime
from portfolio.data import PERSONAL
import reflex as rx

load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_SCHEMA = os.getenv("SCHEMA", "portfolio")
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Initialize supabase client with custom schema
supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(
        SUPABASE_URL, 
        SUPABASE_KEY,
        options=ClientOptions(schema=SUPABASE_SCHEMA)
    )


def _run_automation_script(script_name: str, content: str) -> str:
    """Run a local helper script and return stdout or raise a readable error."""
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / script_name)],
        input=content,
        capture_output=True,
        encoding="utf-8",
        text=True,
        cwd=PROJECT_ROOT,
        check=False,
        env={
            **os.environ,
            "PYTHONUTF8": "1",
            "PYTHONIOENCODING": "utf-8",
        },
    )

    if result.returncode != 0:
        error_message = result.stderr.strip() or result.stdout.strip() or f"{script_name} failed."
        raise RuntimeError(error_message)

    return result.stdout.rstrip("\r\n")


class BlogPost(rx.Base):
    id: str = ""
    title: str = ""
    content: str = ""
    excerpt: str = ""
    display_date: str = ""
    read_time: str = ""
    tags: list[str] = []
    published_at: str = ""


class State(rx.State):
    """The app state."""
    
    is_dark: bool = True
    menu_open: bool = False
    
    # Contact form
    contact_name: str = ""
    contact_email: str = ""
    contact_subject: str = ""
    contact_message: str = ""
    form_submitted: bool = False
    form_error: str = ""
    
    # Blog state – using strongly typed BlogPost list
    blogs: list[BlogPost] = []
    selected_blog: BlogPost = BlogPost()
    current_blog_id: str = ""
    current_blog_title: str = ""
    current_blog_content: str = ""
    current_blog_excerpt: str = ""
    current_blog_tags: str = ""
    is_creating_blog: bool = False

    def toggle_theme(self):
        """Toggle between dark and light mode."""
        self.is_dark = not self.is_dark
    
    def toggle_menu(self):
        """Toggle mobile menu."""
        self.menu_open = not self.menu_open
    
    def close_menu(self):
        """Close mobile menu."""
        self.menu_open = False
        
    # --- ADMIN AUTH ---
    is_admin: bool = False
    login_password: str = ""
    login_error: str = ""

    def check_login(self):
        """Verify admin password from env."""
        admin_pass = os.getenv("ADMIN_PASSWORD", "sharath@2024")
        if self.login_password == admin_pass:
            self.is_admin = True
            self.login_password = ""
            self.login_error = ""
            return rx.toast.info("Logged in as Admin")
        else:
            self.login_error = "Invalid password."
            return rx.toast.error("Invalid Credentials")
            
    def logout(self):
        """Log out the admin."""
        self.is_admin = False
        return rx.toast.info("Logged out")
    
    async def fetch_blog_id(self):
        """Fetch a single blog by its dynamic route ID."""
        blog_id = self.router.page.params.get("id")
        if not blog_id or not supabase:
            return
            
        try:
            response = supabase.table("blogs").select("*").eq("id", blog_id).execute()
            if response.data:
                blog = response.data[0]
                # Format date
                try:
                    dt = datetime.fromisoformat(blog["published_at"].replace("Z", "+00:00"))
                    display_date = dt.strftime("%b %d, %Y")
                except:
                    display_date = blog.get("published_at", "Just now")
                
                self.selected_blog = BlogPost(
                    id=str(blog["id"]),
                    title=blog.get("title", "Untitled"),
                    content=blog.get("content", ""),
                    excerpt=blog.get("excerpt", ""),
                    display_date=display_date,
                    read_time=str(blog.get("read_time", 5)),
                    tags=blog.get("tags", []),
                    published_at=blog.get("published_at", "")
                )
        except Exception as e:
            print(f"Error fetching blog details: {e}")

    async def fetch_blogs(self):
        """Fetch all blogs from Supabase and format them."""
        if not supabase:
            return
        
        try:
            # Query the portfolio.blogs table
            response = supabase.table("blogs").select("*").order("published_at", desc=True).execute()
            raw_blogs = response.data
            
            # Pre-format for the frontend (avoiding Var attribute errors)
            formatted_blogs = []
            for blog in raw_blogs:
                # 1. Format published_at
                try:
                    dt = datetime.fromisoformat(blog["published_at"].replace("Z", "+00:00"))
                    display_date = dt.strftime("%b %d, %Y")
                except:
                    display_date = blog.get("published_at", "Just now")
                
                # 2. Ensure read_time is a safe string or integer
                read_time = str(blog.get("read_time", 5))
                
                # 3. Ensure excerpt exists and is a string
                excerpt = blog.get("excerpt")
                if not excerpt:
                    excerpt = (blog.get("content", "")[:180] + "...") if blog.get("content") else ""
                
                # 4. Ensure tags is a list
                tags = blog.get("tags")
                if not isinstance(tags, list):
                    tags = []

                # Convert to BlogPost object (this is what enables deep foreach iteration)
                formatted_blogs.append(
                    BlogPost(
                        id=str(blog["id"]),
                        title=blog.get("title", "Untitled"),
                        content=blog.get("content", ""),
                        excerpt=excerpt,
                        display_date=display_date,
                        read_time=read_time,
                        tags=tags,
                        published_at=blog.get("published_at", "")
                    )
                )
                
            self.blogs = formatted_blogs
        except Exception as e:
            print(f"Error fetching blogs: {e}")
            self.blogs = []

    def insert_markdown(self, tag: str):
        """Append markdown snippet to current article content."""
        snippets = {
            "h1": "\n# Main Title\n",
            "h2": "\n## Section Heading\n",
            "h3": "\n### Subsection Heading\n",
            "bold": "**Bold Text**",
            "italic": "_Italic Text_",
            "code": " `Code Snippet` ",
            "link": "[Link Text](https://)",
            "image": "\n![Image Description](https://)\n",
            "list": "\n- List Item\n",
            "quote": "\n> Quote here\n",
            "divider": "\n---\n"
        }
        if tag in snippets:
            # We just append for now, more complex insertion would require component refs
            self.current_blog_content = self.current_blog_content + snippets[tag]

    def _find_blog(self, blog_id: str) -> BlogPost | None:
        if self.selected_blog.id == blog_id:
            return self.selected_blog

        for blog in self.blogs:
            if blog.id == blog_id:
                return blog

        return None

    async def delete_blog(self, blog_id: str):
        """Delete a blog from Supabase."""
        if not supabase or not self.is_admin:
            return
            
        try:
            supabase.table("blogs").delete().eq("id", blog_id).execute()
            await self.fetch_blogs()
            return rx.toast.info("Blog deleted successfully")
        except Exception as e:
            print(f"Error deleting blog: {e}")
            return rx.toast.error("Deletion failed")

    def load_blog_for_edit(self, blog: BlogPost):
        """Load blog data into the form for editing."""
        self.current_blog_id = blog.id
        self.current_blog_title = blog.title
        self.current_blog_content = blog.content
        self.current_blog_excerpt = blog.excerpt
        self.current_blog_tags = ", ".join(blog.tags)
        self.is_creating_blog = True # Reuse the same modal state

    async def post_blog_to_linkedin(self, blog_id: str):
        """Convert a blog post to LinkedIn format and publish it."""
        if not self.is_admin:
            return rx.toast.error("Admin access required")

        blog = self._find_blog(blog_id)
        if blog is None:
            return rx.toast.error("Blog post not found")

        if not blog.content.strip():
            return rx.toast.error("This blog post is empty")

        try:
            linkedin_post = await asyncio.to_thread(
                _run_automation_script,
                "markdown_to_linkedin.py",
                blog.content,
            )
            await asyncio.to_thread(
                _run_automation_script,
                "playwright_config.py",
                linkedin_post,
            )
            return rx.toast.success("Posted to LinkedIn successfully")
        except RuntimeError as err:
            print(f"Error posting to LinkedIn: {err}")
            return rx.toast.error(str(err))
        except Exception as err:
            print(f"Error posting to LinkedIn: {err}")
            return rx.toast.error("LinkedIn posting failed")

    async def create_blog(self):
        """Create or Update a blog in Supabase."""
        if not supabase or not self.is_admin:
            return
        
        if not self.current_blog_title or not self.current_blog_content:
            return
            
        try:
            tags = [t.strip() for t in self.current_blog_tags.split(",") if t.strip()]
            # Cleanly handle excerpt
            excerpt = self.current_blog_excerpt.strip()
            if not excerpt:
                # Create a clean excerpt from content
                excerpt = self.current_blog_content[:180].strip() + "..."

            blog_data = {
                "title": self.current_blog_title,
                "content": self.current_blog_content,
                "excerpt": excerpt,
                "tags": tags,
                "author": PERSONAL["name"],
                "read_time": max(1, len(self.current_blog_content.split()) // 200)
            }
            
            if self.current_blog_id:
                # Update existing blog
                supabase.table("blogs").update(blog_data).eq("id", self.current_blog_id).execute()
                msg = "Blog updated successfully"
            else:
                # Create new blog
                blog_data["published_at"] = datetime.utcnow().isoformat()
                supabase.table("blogs").insert(blog_data).execute()
                msg = "Blog published successfully"
            
            # Reset fields and refresh
            self.current_blog_id = ""
            self.current_blog_title = ""
            self.current_blog_content = ""
            self.current_blog_excerpt = ""
            self.current_blog_tags = ""
            self.is_creating_blog = False
            
            await self.fetch_blogs()
            return rx.toast.success(msg)
        except Exception as e:
            print(f"Error publishing/updating blog: {e}")
            return rx.toast.error("Action failed")

    def open_new_blog_editor(self):
        """Open the editor for a fresh new post."""
        self.current_blog_id = ""
        self.current_blog_title = ""
        self.current_blog_content = ""
        self.current_blog_excerpt = ""
        self.current_blog_tags = ""
        self.is_creating_blog = True

    async def submit_contact(self):
        """Handle contact form submission automatically."""
        if not self.contact_name or not self.contact_email or not self.contact_message:
            self.form_error = "Please fill in all required fields."
            return
        if "@" not in self.contact_email:
            self.form_error = "Please enter a valid email address."
            return

        # Prepare details for the automated message
        details = {
            "name": self.contact_name,
            "email": self.contact_email,
            "subject": self.contact_subject or "General Inquiry",
            "message": self.contact_message
        }
        
        # --- AUTOMATION: Sending via Webhook ---
        # This will push the details to the webhook URL specified in data.py
        import httpx
        webhook_url = PERSONAL.get("contact_webhook")
        
        if webhook_url:
            try:
                # We use an async call to keep the UI responsive
                async with httpx.AsyncClient() as client:
                    response = await client.post(webhook_url, json=details)
                    if response.status_code not in (200, 201, 204):
                        print(f"Webhook error: {response.text}")
            except Exception as e:
                print(f"Error sending message to webhook: {e}")
        else:
            print("No webhook URL configured in data.py. Printing details to console for now:")
            print(details)

        # Reset form locally
        self.form_submitted = True
        self.form_error = ""
        self.contact_name = ""
        self.contact_email = ""
        self.contact_subject = ""
        self.contact_message = ""
        
        # Return None to stay on the page (the success message will be shown via rx.cond in the UI)
        return None
    
    def reset_form(self):
        """Reset form submission state."""
        self.form_submitted = False
