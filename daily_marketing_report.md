---
description: 每日行銷日報自動提取工作流
---

---
name: Daily Marketing Report Workflow
description: Handle user requests for marketing backend data extraction and direct reporting.
triggers: "get [project] data", "fetch marketing report", "抓[專案]數據"
---

# Workflow: Daily Marketing Report

## 1. Parsing & Validation
- **Extract**: Identify `project`, `region` (default: All), and `date_range` from the prompt.
- **Auth Check**: Verify active browser session for the marketing backend.

## 2. Execution
- **Call Skill**: Execute `.agent/skills/marketing_scraper.md`.
- **Pass Parameters**: Provide the extracted `project`, `region`, and `date_range` to the skill. 
- *(Note: Rely entirely on the skill file for DOM navigation, selectors, and JS injection. Do not redefine them here.)*

## 3. Formatting & Output
- **Clean Data**: Apply the cleaning logic (remove $, %, commas) defined in the skill file.
- **Markdown Output**: Return a concise summary directly in the chat containing: Project, Region, Period, Impressions, Clicks, Installs, Cost(USD). Do NOT export or save to any files.