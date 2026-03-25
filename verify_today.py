from playwright.sync_api import sync_playwright
from pathlib import Path

USER_DATA_DIR = Path("user_data").resolve()
with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(user_data_dir=str(USER_DATA_DIR), headless=True)
    page = context.pages[0] if context.pages else context.new_page()
    page.goto("https://marketing-prod.i17game.com/i17GameMarketing_Backend/i17GameMarketing/MarketingDailyReport/DailyMediaDetail")
    # Wait for grid to load if it's already on the page from the active session
    # Actually, the user's browser state says we are on the page.
    page.wait_for_timeout(5000)
    
    # Try to find the values in the ag-grid Total row
    data = page.evaluate('''
        () => {
            const viewport = document.querySelector('.ag-body-viewport, .ag-center-cols-viewport');
            if (!viewport) return "Grid not found";
            
            // Scroll to find columns
            const totalRow = document.querySelector('.ag-row-total, .ag-floating-bottom .ag-row');
            if (!totalRow) return "Total row not found";
            
            const results = {};
            const cells = totalRow.querySelectorAll('.ag-cell');
            cells.forEach(c => {
                const colId = c.getAttribute('col-id');
                if (colId) results[colId] = c.innerText.trim();
            });
            return results;
        }
    ''')
    print(data)
    context.close()
