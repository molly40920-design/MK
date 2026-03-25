---
name: Marketing Scraper Skill
description: Navigate and scrape i17Game marketing backend (DOM, Selectors, JS date injection, data cleaning).
---

# Marketing Scraper Skill

## 1. Target URL
`https://marketing-prod.i17game.com/i17GameMarketing_Backend/Home/WelcomePage`

## 2. Execution Steps

1. **導航 (Navigate)**：點擊主選單 -> 進入目標子選單「行銷日報」。
2. **篩選器設定 (Filters)**：
   - 專案：透過 `select#dp_ProjectList` 選擇。
   - 日期範圍 (JS 注入)：使用 `page.evaluate` 執行 daterangepicker 設定。
3. **切換頁籤 (Switch Tab)**：點擊「每日媒體明細」。
4. **欄位選取 (Column Selection)**：在右側工具列勾選「新進人數」與「回流人數」。**勾選後數據會自動反應式更新，不需再次點擊「查詢」按鈕。**
5. **數據擷取 (Extract)**：等待 `ag-grid` 渲染完成，執行雙軸滾動以擷取完整數據（含日期、媒體、投放地區、新進人數與回流人數）。


## 3. Data Cleaning
Remove currency, percentage, commas, and spaces before output:
`value.replace(/[$%,\s]/g, "")`