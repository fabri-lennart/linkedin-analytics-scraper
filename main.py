from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import pandas as pd
from datetime import datetime
import time
import knime.scripting.io as knio

# =============================================================================
# CONFIG
# =============================================================================

LINKEDIN_EMAIL = ""        # optional
LINKEDIN_PASSWORD = ""     # optional
ANALYTICS_URL = "https://www.linkedin.com/analytics/demographic-detail/urn:li:fsd_profile:profile/?metricType=MEMBER_FOLLOWERS"

# =============================================================================
# FUNCTIONS
# =============================================================================

def login_linkedin(page, email=None, password=None):
    page.goto("https://www.linkedin.com/login", wait_until="domcontentloaded")
    time.sleep(2)
    
    if email and password:
        try:
            page.fill("#username", email)
            page.fill("#password", password)
            page.click('button[type="submit"]')
            time.sleep(5)
        except:
            pass
    # Manual login if needed

def extract_simple_data(page):
    time.sleep(3)
    
    # Smooth scroll
    for i in range(5):
        page.evaluate(f"window.scrollTo(0, {i * 300})")
        time.sleep(0.5)
    
    page.evaluate("window.scrollTo(0, 0)")
    time.sleep(2)
    
    data = []
    body_text = page.locator("body").inner_text()
    lines = body_text.split("\n")
    current_section = None
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        if line in [
            "Cargo", "Ubicación", "Sector",
            "Nivel de responsabilidad", "Antigüedad",
            "Tamaño de empresa", "Función"
        ]:
            current_section = line
            continue
        
        if "%" in line and current_section:
            name = None
            percentage = None
            
            if i > 0 and "%" not in lines[i - 1]:
                name = lines[i - 1].strip()
                percentage = line
            else:
                parts = line.rsplit(" ", 1)
                if len(parts) == 2:
                    name, percentage = parts
            
            if name and percentage:
                data.append({
                    "section": current_section,
                    "name": name,
                    "percentage": percentage,
                    "extraction_date": datetime.now()
                })
    
    return data

# =============================================================================
# MAIN
# =============================================================================

rows = []

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        slow_mo=500,
        args=["--disable-blink-features=AutomationControlled"]
    )
    
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="es-ES"
    )
    
    page = context.new_page()
    page.set_default_timeout(60000)
    
    login_linkedin(page, LINKEDIN_EMAIL, LINKEDIN_PASSWORD)
    
    try:
        page.goto(ANALYTICS_URL, wait_until="domcontentloaded", timeout=30000)
    except PlaywrightTimeout:
        pass
    
    time.sleep(5)
    rows = extract_simple_data(page)
    
    browser.close()

# =============================================================================
# KNIME OUTPUT
# =============================================================================

if rows:
    df = pd.DataFrame(rows)
else:
    df = pd.DataFrame(
        columns=["section", "name", "percentage", "extraction_date"]
    )

knio.output_tables[0] = knio.Table.from_pandas(df)
