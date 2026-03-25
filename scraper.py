import json
import logging
import csv
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def main():
    USER_DATA_DIR = Path("user_data").resolve()
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(USER_DATA_DIR),
            headless=True,
            viewport={"width": 1920, "height": 1080},
        )
        page = context.pages[0] if context.pages else context.new_page()
        page.on("console", lambda msg: logger.info(f"BROWSER: {msg.text}"))
        
        try:
            logger.info("Navigate to 行銷日報")
            page.goto("https://marketing-prod.i17game.com/i17GameMarketing_Backend/Home/WelcomePage", wait_until="networkidle")
            page.locator("text=營銷分析").first.click()
            page.wait_for_timeout(1000)
            page.locator("text=行銷日報").first.click()
            page.wait_for_timeout(3000)

            logger.info("Select Project")
            page.locator("select").first.select_option(label="明星三缺一")
            page.wait_for_timeout(2000)

            logger.info("Set Date - Manual & JS robust")
            # Try to find date input by value or name
            page.evaluate('''
                () => {
                    const findPicker = () => {
                        let p = $('input[name="daterangepicker"]').data('daterangepicker');
                        if (p) return p;
                        p = $('.form-control').filter(function() { return $(this).data('daterangepicker'); }).data('daterangepicker');
                        if (p) return p;
                        // deeper search
                        const all = $('*').filter(function() { return $(this).data('daterangepicker'); });
                        if (all.length > 0) return all.data('daterangepicker');
                        return null;
                    };
                    const drp = findPicker();
                    if (drp) {
                        drp.setStartDate('2026/02/01');
                        drp.setEndDate('2026/02/28');
                        drp.clickApply();
                        console.log("Date set successfully to Feb 2026");
                    } else {
                        console.error("Daterangepicker not found anywhere");
                    }
                }
            ''')
            page.wait_for_timeout(2000)

            logger.info("Click Tab: 每日媒體明細")
            page.locator("text=每日媒體明細").first.click()
            page.wait_for_timeout(5000)

            logger.info("Open Column Selector and enable Target Columns")
            page.evaluate('''
                () => {
                    // Find and click the button that opens column choice
                    const btn = $('button:contains("選擇"), button:contains("欄位選取")').first();
                    if (btn.length > 0) {
                        btn.click();
                        console.log("Opened column selector");
                        // Timeout to wait for dropdown
                        setTimeout(() => {
                            ['新進人數', '回流人數'].forEach(name => {
                                const chk = $('label:contains("' + name + '") input');
                                if (chk.length > 0 && !chk.prop('checked')) {
                                    chk.click();
                                    console.log("Checked " + name);
                                }
                            });
                        }, 500);
                    }
                }
            ''')
            page.wait_for_timeout(2000)
            page.keyboard.press("Escape")
            page.wait_for_timeout(1000)


            
            logger.info("Scraping grid with Horizontal + Vertical Scroll")
            # We will scroll in steps to capture all cells
            grid_data = page.evaluate('''
                async () => {
                    const viewport = document.querySelector('.ag-body-viewport, .ag-center-cols-viewport');
                    const headers = Array.from(document.querySelectorAll('.ag-header-cell-text, th')).map(el => el.innerText.trim()).filter(t => t);
                    
                    if (!viewport) return {headers, rows: []};

                    const container = document.querySelector('.ag-center-cols-container');
                    const totalHeight = container ? container.offsetHeight : 5000;
                    const totalWidth = container ? container.offsetWidth : 5000;
                    const vh = viewport.offsetHeight;
                    const vw = viewport.offsetWidth;
                    
                    let masterRows = new Map();
                    
                    // Vertical Scroll
                    for (let y = 0; y < totalHeight; y += vh * 0.8) {
                        viewport.scrollTop = y;
                        await new Promise(r => setTimeout(r, 400));
                        
                        // Horizontal Scroll within each vertical step to capture all cells
                        for (let x = 0; x < totalWidth; x += vw * 0.8) {
                            viewport.scrollLeft = x;
                            await new Promise(r => setTimeout(r, 400));
                            
                            const rows = document.querySelectorAll('.ag-row');
                            rows.forEach(row => {
                                const id = row.getAttribute('row-index') || row.innerText.slice(0,30);
                                if (!masterRows.has(id)) masterRows.set(id, {});
                                const data = masterRows.get(id);
                                
                                // Map cells by column-id or index if possible, 
                                // but simpler: just merge what's visible
                                row.querySelectorAll('.ag-cell').forEach(cell => {
                                    const colId = cell.getAttribute('col-id');
                                    if (colId) data[colId] = cell.innerText.trim();
                                });
                            });
                        }
                    }
                    
                    // Convert Map of objects to list of lists based on column-ids or common headers
                    // For now, let's just return the raw map
                    return {headers, data: Array.from(masterRows.values())};
                }
            ''')
            
            # Since data is a list of dicts {colId: val}, we need to flatten it
            data_list = grid_data['data']
            if data_list:
                # Get all unique col-ids found
                all_col_ids = set()
                for d in data_list:
                    all_col_ids.update(d.keys())
                
                # Sort col-ids (optional, but try to match headers if possible)
                sorted_cols = sorted(list(all_col_ids))
                
                with open("feb_final_scraped.csv", "w", newline="", encoding="utf-8-sig") as f:
                    writer = csv.DictWriter(f, fieldnames=sorted_cols)
                    writer.writeheader()
                    writer.writerows(data_list)
                logger.info(f"Successfully saved {len(data_list)} rows to feb_final_scraped.csv")
            else:
                logger.warning("No data found")
                page.screenshot(path="empty_final.png")

        except Exception as e:
            logger.error(f"Error: {e}")
            page.screenshot(path="crash_final.png")
        finally:
            context.close()

if __name__ == "__main__":
    main()
