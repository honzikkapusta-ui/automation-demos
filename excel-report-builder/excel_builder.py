"""
Excel Report Builder — creates a formatted workbook with formulas, tables,
and a dashboard sheet. Replaces manual VBA/macro workflows with Python.
"""
from pathlib import Path
from datetime import date
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, numbers
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, Reference

OUT = Path(__file__).parent / "monthly_sales_report.xlsx"

# Style constants
HDR_FONT = Font(bold=True, color="FFFFFF", size=11)
HDR_FILL = PatternFill(start_color="4F46E5", end_color="4F46E5", fill_type="solid")
SUB_FILL = PatternFill(start_color="F3F4F6", end_color="F3F4F6", fill_type="solid")
THIN_BORDER = Border(
    left=Side(style="thin"), right=Side(style="thin"),
    top=Side(style="thin"), bottom=Side(style="thin"),
)
MONEY_FMT = '#,##0.00'

def build() -> None:
    wb = Workbook()

    # ---------- Sheet 1: Raw Data ----------
    ws_data = wb.active
    ws_data.title = "Sales Data"

    headers = ["Date", "Product", "Category", "Region", "Qty", "Unit Price", "Revenue"]
    rows = [
        [date(2024,1,5),  "Widget Pro",      "Electronics", "West",   3,  149.99],
        [date(2024,1,7),  "Gadget Basic",    "Electronics", "East",   7,   49.99],
        [date(2024,1,10), "Service Plan A",  "Services",    "North",  1,  299.00],
        [date(2024,1,12), "Widget Pro",      "Electronics", "West",   2,  149.99],
        [date(2024,1,15), "Part X-100",      "Parts",       "South",  10,   9.99],
        [date(2024,1,18), "Gadget Basic",    "Electronics", "East",   7,   49.99],
        [date(2024,1,22), "Service Plan B",  "Services",    "North",  1,  199.00],
        [date(2024,1,25), "Widget Standard", "Electronics", "West",   5,   89.99],
        [date(2024,1,28), "Part X-100",      "Parts",       "South",  20,   9.99],
        [date(2024,2,1),  "Gadget Basic",    "Electronics", "East",   3,   54.99],
        [date(2024,2,4),  "Service Plan A",  "Services",    "Central",1,  299.00],
        [date(2024,2,8),  "Widget Pro",      "Electronics", "West",   4,  149.99],
        [date(2024,2,12), "Part Y-200",      "Parts",       "South",  8,  19.99],
        [date(2024,2,15), "Gadget Basic",    "Electronics", "East",   2,   49.99],
        [date(2024,2,20), "Service Plan C",  "Services",    "North",  1,  499.00],
        [date(2024,2,23), "Widget Standard", "Electronics", "Central",3,   89.99],
    ]

    # Write headers
    for col, h in enumerate(headers, 1):
        c = ws_data.cell(row=1, column=col, value=h)
        c.font = HDR_FONT; c.fill = HDR_FILL; c.alignment = Alignment(horizontal="center")
        c.border = THIN_BORDER

    # Write data + revenue formula
    for r_idx, row in enumerate(rows, 2):
        for c_idx, val in enumerate(row, 1):
            c = ws_data.cell(row=r_idx, column=c_idx, value=val)
            c.border = THIN_BORDER
            if c_idx in (5, 6): c.number_format = MONEY_FMT
            if c_idx == 1: c.number_format = 'YYYY-MM-DD'

        # Revenue formula in column G: =E*F
        c = ws_data.cell(row=r_idx, column=7)
        c.value = f"=E{r_idx}*F{r_idx}"
        c.number_format = MONEY_FMT
        c.border = THIN_BORDER

    # Auto-filter
    ws_data.auto_filter.ref = f"A1:G{len(rows)+1}"

    # Column widths
    widths = [12, 18, 14, 10, 8, 12, 14]
    for i, w in enumerate(widths, 1):
        ws_data.column_dimensions[get_column_letter(i)].width = w

    # ---------- Sheet 2: Pivot by Category ----------
    ws_cat = wb.create_sheet("By Category")
    cat_headers = ["Category", "Total Revenue", "Total Qty", "Avg Price", "Order Count"]
    for col, h in enumerate(cat_headers, 1):
        c = ws_cat.cell(row=1, column=col, value=h)
        c.font = HDR_FONT; c.fill = HDR_FILL; c.alignment = Alignment(horizontal="center")
        c.border = THIN_BORDER

    # Pivot formulas (SUMIFS, COUNTIFS)
    data_ref = "'Sales Data'"
    cats = ["Electronics", "Services", "Parts"]
    for i, cat in enumerate(cats, 2):
        r = i
        ws_cat.cell(row=r, column=1, value=cat).border = THIN_BORDER
        # Total Revenue = SUMIFS(Sales Data!G:G, Sales Data!C:C, cat)
        c = ws_cat.cell(row=r, column=2)
        c.value = f"=SUMIFS({data_ref}!G:G,{data_ref}!C:C,A{r})"
        c.number_format = MONEY_FMT
        # Total Qty
        c = ws_cat.cell(row=r, column=3)
        c.value = f"=SUMIFS({data_ref}!E:E,{data_ref}!C:C,A{r})"
        c.number_format = '#,##0'
        # Avg Price
        c = ws_cat.cell(row=r, column=4)
        c.value = f"=IF(B{r}=0,0,B{r}/C{r})"
        c.number_format = MONEY_FMT
        # Order Count
        c = ws_cat.cell(row=r, column=5)
        c.value = f"=COUNTIFS({data_ref}!C:C,A{r})"
        c.number_format = '#,##0'

        for c in range(1, 6):
            ws_cat.cell(row=r, column=c).border = THIN_BORDER
            if c in (2, 4): ws_cat.cell(row=r, column=c).number_format = MONEY_FMT

    # Totals row
    tot_row = len(cats) + 2
    for col in range(2, 6):
        c = ws_cat.cell(row=tot_row, column=col)
        c.value = f"=SUM({get_column_letter(col)}2:{get_column_letter(col)}{tot_row-1})"
        c.font = Font(bold=True)
        c.fill = SUB_FILL
        c.border = THIN_BORDER
        if col in (2, 4): c.number_format = MONEY_FMT

    ws_cat.column_dimensions["A"].width = 16
    for c in "BCDE":
        ws_cat.column_dimensions[c].width = 16

    # ---------- Sheet 3: Dashboard ----------
    ws_dash = wb.create_sheet("Dashboard")

    # Title
    ws_dash.merge_cells("A1:F1")
    t = ws_dash.cell(row=1, column=1, value="Monthly Sales Dashboard")
    t.font = Font(size=16, bold=True, color="1F2937")
    t.alignment = Alignment(horizontal="center")

    # KPI cards
    kpis = [
        ("Total Revenue", "=SUM('Sales Data'!G:G)", MONEY_FMT),
        ("Total Orders", "=COUNTA('Sales Data'!A:A)-1", '#,##0'),
        ("Avg Order Value", "=IFERROR(B2/B3,0)", MONEY_FMT),
        ("Top Category", "=INDEX('By Category'!A2:A4,MATCH(MAX('By Category'!B2:B4),'By Category'!B2:B4,0))", "@"),
    ]
    for i, (label, formula, fmt) in enumerate(kpis, 2):
        ws_dash.cell(row=i, column=1, value=label).font = Font(bold=True, size=11)
        c = ws_dash.cell(row=i, column=2, value=formula)
        c.number_format = fmt
        c.font = Font(size=13, color="4F46E5", bold=True)

    # Bar chart embedded in dashboard
    chart = BarChart()
    chart.type = "col"
    chart.title = "Revenue by Category"
    chart.y_axis.title = "Revenue ($)"
    chart.x_axis.title = "Category"
    chart.style = 2
    data = Reference(ws_cat, min_col=2, min_row=1, max_row=len(cats)+1, max_col=2)
    cats_ref = Reference(ws_cat, min_col=1, min_row=2, max_row=len(cats)+1)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats_ref)
    chart.shape = 4
    ws_dash.add_chart(chart, "A6")

    wb.save(OUT)
    print(f"Workbook saved -> {OUT}")

if __name__ == "__main__":
    build()
