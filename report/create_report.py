from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_BREAK
from pathlib import Path


# ============================================================
# UAC SYSTEM CAPACITY & CARE LOAD ANALYTICS
# Professional Project Report Generator
# ============================================================


# ------------------------------------------------------------
# 1. CREATE DOCUMENT
# ------------------------------------------------------------

doc = Document()

# Page setup
section = doc.sections[0]
section.top_margin = Inches(0.75)
section.bottom_margin = Inches(0.75)
section.left_margin = Inches(0.85)
section.right_margin = Inches(0.85)


# ------------------------------------------------------------
# 2. DOCUMENT STYLES
# ------------------------------------------------------------

styles = doc.styles

# Normal text
normal = styles["Normal"]
normal.font.name = "Arial"
normal.font.size = Pt(10.5)

# Title
title_style = styles["Title"]
title_style.font.name = "Arial"
title_style.font.size = Pt(26)
title_style.font.bold = True

# Heading 1
h1 = styles["Heading 1"]
h1.font.name = "Arial"
h1.font.size = Pt(18)
h1.font.bold = True

# Heading 2
h2 = styles["Heading 2"]
h2.font.name = "Arial"
h2.font.size = Pt(14)
h2.font.bold = True

# Heading 3
h3 = styles["Heading 3"]
h3.font.name = "Arial"
h3.font.size = Pt(12)
h3.font.bold = True


# ------------------------------------------------------------
# 3. HELPER FUNCTIONS
# ------------------------------------------------------------

def add_page_number(paragraph):
    """Add page number field to a paragraph."""
    run = paragraph.add_run()

    fldChar1 = OxmlElement("w:fldChar")
    fldChar1.set(qn("w:fldCharType"), "begin")

    instrText = OxmlElement("w:instrText")
    instrText.set(qn("xml:space"), "preserve")
    instrText.text = "PAGE"

    fldChar2 = OxmlElement("w:fldChar")
    fldChar2.set(qn("w:fldCharType"), "end")

    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)


def set_cell_text(cell, text, bold=False):
    cell.text = ""
    paragraph = cell.paragraphs[0]
    paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT

    run = paragraph.add_run(str(text))
    run.bold = bold
    run.font.name = "Arial"
    run.font.size = Pt(9)

    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER


def shade_cell(cell, fill="D9EAF7"):
    """Apply background shading to a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tcPr.append(shd)


def add_table(headers, rows, widths=None):
    """Create a formatted table."""
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"

    # Header
    for i, header in enumerate(headers):
        cell = table.rows[0].cells[i]
        set_cell_text(cell, header, bold=True)
        shade_cell(cell)

    # Rows
    for row_data in rows:
        row = table.add_row()

        for i, value in enumerate(row_data):
            set_cell_text(row.cells[i], value)

    # Optional widths
    if widths:
        for row in table.rows:
            for i, width in enumerate(widths):
                row.cells[i].width = Inches(width)

    doc.add_paragraph()

    return table


def add_bullet(text):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(3)
    p.add_run(text)


def add_number(text):
    p = doc.add_paragraph(style="List Number")
    p.paragraph_format.space_after = Pt(3)
    p.add_run(text)


def add_code_block(text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.3)
    p.paragraph_format.right_indent = Inches(0.3)

    run = p.add_run(text)
    run.font.name = "Courier New"
    run.font.size = Pt(9)


def add_paragraph(text, bold_start=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(7)
    p.paragraph_format.line_spacing = 1.15

    if bold_start and text.startswith(bold_start):
        r1 = p.add_run(bold_start)
        r1.bold = True
        p.add_run(text[len(bold_start):])
    else:
        p.add_run(text)

    return p


def add_section_heading(text):
    doc.add_heading(text, level=1)


def add_subheading(text):
    doc.add_heading(text, level=2)


def add_small_heading(text):
    doc.add_heading(text, level=3)


# ------------------------------------------------------------
# 4. HEADER AND FOOTER
# ------------------------------------------------------------

header = section.header
header_para = header.paragraphs[0]
header_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

header_run = header_para.add_run(
    "UAC System Capacity & Care Load Analytics"
)
header_run.font.name = "Arial"
header_run.font.size = Pt(9)
header_run.bold = True


footer = section.footer
footer_para = footer.paragraphs[0]
footer_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

footer_run = footer_para.add_run("Page ")
footer_run.font.name = "Arial"
footer_run.font.size = Pt(9)

add_page_number(footer_para)


# ------------------------------------------------------------
# 5. TITLE PAGE
# ------------------------------------------------------------

title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
title.paragraph_format.space_before = Inches(1.5)

run = title.add_run("UAC SYSTEM CAPACITY &\nCARE LOAD ANALYTICS")
run.bold = True
run.font.name = "Arial"
run.font.size = Pt(26)

subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
subtitle.paragraph_format.space_before = Inches(0.4)

run = subtitle.add_run(
    "Data Analytics, Capacity Monitoring and Interactive Dashboard"
)
run.font.name = "Arial"
run.font.size = Pt(14)
run.bold = True

doc.add_paragraph()

info = doc.add_paragraph()
info.alignment = WD_ALIGN_PARAGRAPH.CENTER
info.paragraph_format.space_before = Inches(1)

run = info.add_run(
    "Project Report\n\n"
    "Project: UAC System Capacity & Care Load Analytics\n"
    "Technology: Python, Pandas, Matplotlib, Jupyter Notebook and Streamlit\n"
    "Deliverables: Analytical Dataset, Analysis Notebook and Interactive Dashboard"
)
run.font.name = "Arial"
run.font.size = Pt(11)

doc.add_paragraph()

date_para = doc.add_paragraph()
date_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
date_run = date_para.add_run("September 2026")
date_run.font.name = "Arial"
date_run.font.size = Pt(11)

doc.add_page_break()


# ------------------------------------------------------------
# 6. EXECUTIVE SUMMARY
# ------------------------------------------------------------

add_section_heading("1. Executive Summary")

add_paragraph(
    "This project analyzes system capacity and care load within the "
    "Unaccompanied Children (UAC) care pipeline. The analysis focuses on "
    "children moving through the care process from U.S. Customs and Border "
    "Protection (CBP) custody to the U.S. Department of Health and Human "
    "Services (HHS) care system and eventual discharge."
)

add_paragraph(
    "Historical UAC data was analyzed to understand system load, children "
    "in CBP custody, children in HHS care, transfers, discharges, intake "
    "pressure and periods of relatively high system demand."
)

add_paragraph(
    "The project combines data cleaning, exploratory data analysis, "
    "feature engineering, statistical analysis, time-series analysis and "
    "interactive visualization through a Streamlit dashboard."
)

add_paragraph(
    "The final analytical dataset contains the original measurements "
    "together with derived metrics such as Total System Load, Net Intake "
    "Pressure, Care Load Growth Rate, Discharge Offset Ratio, rolling "
    "averages, cumulative intake and high-load indicators."
)


# ------------------------------------------------------------
# 7. PROJECT OVERVIEW
# ------------------------------------------------------------

add_section_heading("2. Project Overview")

add_paragraph(
    "The UAC care pipeline involves multiple stages through which "
    "unaccompanied children move from initial custody toward care and "
    "eventual discharge. Monitoring the number of children within these "
    "stages can provide a quantitative view of changes in system demand."
)

add_paragraph(
    "This project develops an analytical framework for examining "
    "historical system-level UAC data. The framework focuses on the "
    "relationship between children in CBP custody, children in HHS care, "
    "transfers from CBP custody, and HHS discharges."
)

add_paragraph(
    "The project also provides an interactive dashboard so that users "
    "can examine selected metrics and time periods without directly "
    "working with the underlying Python analysis."
)


# ------------------------------------------------------------
# 8. PROBLEM STATEMENT
# ------------------------------------------------------------

add_section_heading("3. Problem Statement")

add_paragraph(
    "The UAC care system can experience changes in the number of children "
    "moving through custody, care and discharge stages. Understanding these "
    "changes requires systematic analysis of historical observations."
)

add_paragraph(
    "The project therefore addresses the need for a structured analytical "
    "approach to measure system load, compare transfers and discharges, "
    "identify changes in intake pressure, and highlight observations "
    "with relatively high system load."
)


# ------------------------------------------------------------
# 9. OBJECTIVES
# ------------------------------------------------------------

add_section_heading("4. Project Objectives")

objectives = [
    "Analyze the overall UAC system load over time.",
    "Compare children in CBP custody with children in HHS care.",
    "Examine transfers from CBP custody into HHS care.",
    "Analyze HHS discharges.",
    "Measure daily net intake pressure.",
    "Identify periods of relatively high system load.",
    "Study changes and trends in system capacity indicators.",
    "Develop analytical metrics that summarize system pressure.",
    "Create an interactive dashboard for exploring the data.",
    "Create a reusable analytical dataset for further analysis."
]

for item in objectives:
    add_number(item)


# ------------------------------------------------------------
# 10. PROJECT WORKFLOW
# ------------------------------------------------------------

add_section_heading("5. Project Workflow")

add_code_block(
    "Raw UAC Dataset\n"
    "       |\n"
    "       v\n"
    "Data Loading\n"
    "       |\n"
    "       v\n"
    "Data Cleaning & Validation\n"
    "       |\n"
    "       v\n"
    "Exploratory Data Analysis\n"
    "       |\n"
    "       v\n"
    "Feature Engineering\n"
    "       |\n"
    "       v\n"
    "Statistical & Trend Analysis\n"
    "       |\n"
    "       v\n"
    "High-Load Identification\n"
    "       |\n"
    "       v\n"
    "Monthly & Time-Based Analysis\n"
    "       |\n"
    "       v\n"
    "Final Analytical Dataset\n"
    "       |\n"
    "       v\n"
    "Streamlit Dashboard\n"
    "       |\n"
    "       v\n"
    "Insights & Reporting"
)


# ------------------------------------------------------------
# 11. DATASET
# ------------------------------------------------------------

add_section_heading("6. Dataset Description")

add_paragraph(
    "The project uses historical UAC data containing measurements related "
    "to custody, transfers, HHS care and discharges."
)

add_table(
    ["Field", "Description"],
    [
        ["Date", "Observation date."],
        [
            "Children apprehended and placed in CBP custody*",
            "Number of children apprehended and placed in CBP custody."
        ],
        [
            "Children in CBP custody",
            "Number of children recorded in CBP custody."
        ],
        [
            "Children transferred out of CBP custody",
            "Number of children transferred out of CBP custody."
        ],
        [
            "Children in HHS Care",
            "Number of children recorded in HHS care."
        ],
        [
            "Children discharged from HHS Care",
            "Number of children discharged from HHS care."
        ]
    ]
)

add_paragraph(
    "The original dataset contains 720 observations and 14 original "
    "columns. Additional analytical columns were created during the "
    "feature engineering stage."
)


# ------------------------------------------------------------
# 12. DATA PREPARATION
# ------------------------------------------------------------

add_section_heading("7. Data Preparation")

add_subheading("7.1 Data Loading")

add_paragraph(
    "The original CSV dataset was loaded into Python using the Pandas "
    "library. The primary analysis notebook is stored at:"
)

add_code_block("analysis/uac_analysis.ipynb")


add_subheading("7.2 Column Cleaning")

add_paragraph(
    "Column names were reviewed and cleaned to make them easier to use "
    "during analysis and feature engineering."
)


add_subheading("7.3 Date Conversion")

add_paragraph(
    "The Date field was converted into a datetime format so that the "
    "observations could be sorted chronologically and analyzed as a "
    "time series."
)


add_subheading("7.4 Numeric Data Cleaning")

add_paragraph(
    "The relevant numerical fields were checked and converted into "
    "appropriate numeric data types."
)


add_subheading("7.5 Missing-Value Check")

add_paragraph(
    "The dataset was examined for missing values in the primary "
    "analytical fields."
)


add_subheading("7.6 Duplicate-Date Check")

add_paragraph(
    "Dates were checked for duplicate observations to ensure that the "
    "time-series analysis was not affected by unintended duplicate records."
)


add_subheading("7.7 Negative-Value Check")

add_paragraph(
    "The original numerical fields were checked for negative values "
    "because the primary count variables represent numbers of children."
)


add_subheading("7.8 Chronological Sorting")

add_paragraph(
    "The observations were sorted by date so that sequential calculations, "
    "rolling averages and cumulative measures could be calculated correctly."
)


# ------------------------------------------------------------
# 13. TIME SERIES
# ------------------------------------------------------------

add_section_heading("8. Time-Series Observation Analysis")

add_paragraph(
    "The dataset does not contain an observation for every calendar day. "
    "The average gap between observations was approximately 1.49 days, "
    "while the largest observed gap was 10 days."
)

add_paragraph(
    "Because of these gaps, rolling averages were defined using the "
    "number of observations rather than exact calendar-day windows."
)


# ------------------------------------------------------------
# 14. FEATURE ENGINEERING
# ------------------------------------------------------------

add_section_heading("9. Feature Engineering")

add_paragraph(
    "Additional analytical variables were created from the original "
    "fields. These variables provide a more detailed representation of "
    "system load, intake pressure and time-based trends."
)

features = [
    "transfer_gt_cbp_flag",
    "discharge_gt_hhs_flag",
    "Total System Load",
    "Net Intake Pressure",
    "Care Load Growth Rate",
    "Discharge Offset Ratio",
    "7_Observation_Load_Avg",
    "14_Observation_Load_Avg",
    "Month",
    "Week",
    "High_Load_Flag",
    "High_Load_Group",
    "Cumulative Net Intake",
    "7_Observation_Intake_Avg",
    "14_Observation_Intake_Avg"
]

for feature in features:
    add_bullet(feature)


# ------------------------------------------------------------
# 15. ANALYTICAL METRICS
# ------------------------------------------------------------

add_section_heading("10. Key Analytical Metrics")

add_subheading("10.1 Total System Load")

add_paragraph(
    "Total System Load represents the combined number of children in "
    "CBP custody and HHS care."
)

add_code_block(
    "Total System Load = Children in CBP custody + Children in HHS Care"
)


add_subheading("10.2 Net Intake Pressure")

add_paragraph(
    "Net Intake Pressure compares transfers from CBP custody with "
    "HHS discharges."
)

add_code_block(
    "Net Intake Pressure = Children transferred out of CBP custody "
    "- Children discharged from HHS Care"
)

add_paragraph(
    "A positive value indicates that transfers were greater than "
    "discharges for that observation. A negative value indicates that "
    "discharges were greater than transfers."
)


add_subheading("10.3 Care Load Growth Rate")

add_paragraph(
    "Care Load Growth Rate measures the percentage change in Total "
    "System Load from one observation to the next."
)


add_subheading("10.4 Discharge Offset Ratio")

add_paragraph(
    "Discharge Offset Ratio compares HHS discharges with transfers "
    "from CBP custody."
)

add_code_block(
    "Discharge Offset Ratio = Children discharged from HHS Care "
    "/ Children transferred out of CBP custody"
)


add_subheading("10.5 Rolling Averages")

add_paragraph(
    "The project calculates four observation-based rolling averages:"
)

for item in [
    "7-observation Total System Load average",
    "14-observation Total System Load average",
    "7-observation Net Intake Pressure average",
    "14-observation Net Intake Pressure average"
]:
    add_bullet(item)


add_subheading("10.6 High-Load Flag")

add_paragraph(
    "A high-load observation is identified using the 75th percentile "
    "of Total System Load. Observations at or above this threshold are "
    "classified as High Load, while other observations are classified "
    "as Normal Load."
)

add_paragraph(
    "This classification is a statistical indicator created for the "
    "analysis and is not an official facility capacity threshold."
)


# ------------------------------------------------------------
# 16. EXPLORATORY DATA ANALYSIS
# ------------------------------------------------------------

add_section_heading("11. Exploratory Data Analysis")

add_paragraph(
    "Exploratory Data Analysis was performed to understand patterns "
    "and relationships within the dataset."
)

eda_items = [
    "Total System Load trends",
    "CBP custody trends",
    "HHS care trends",
    "Transfers into HHS care",
    "HHS discharge patterns",
    "Net Intake Pressure",
    "Cumulative Net Intake",
    "Rolling averages",
    "High-load observations",
    "Monthly trends"
]

for item in eda_items:
    add_bullet(item)


# ------------------------------------------------------------
# 17. KEY FINDINGS
# ------------------------------------------------------------

add_section_heading("12. Key Project Findings")


add_subheading("12.1 Highest System Load")

add_table(
    ["Metric", "Value"],
    [
        ["Date", "December 20, 2023"],
        ["Total System Load", "11,762"],
        ["Children in CBP custody", "246"],
        ["Children in HHS Care", "11,516"]
    ]
)


add_subheading("12.2 Lowest System Load")

add_table(
    ["Metric", "Value"],
    [
        ["Date", "August 24, 2025"],
        ["Total System Load", "2,002"],
        ["Children in CBP custody", "21"],
        ["Children in HHS Care", "1,981"]
    ]
)


add_subheading("12.3 Highest Positive Net Intake Pressure")

add_table(
    ["Metric", "Value"],
    [
        ["Date", "February 12, 2024"],
        ["Net Intake Pressure", "206"],
        ["Transfers", "440"],
        ["Discharges", "234"]
    ]
)

add_paragraph(
    "For this observation, transfers exceeded discharges by 206."
)


add_subheading("12.4 Most Negative Net Intake Pressure")

add_table(
    ["Metric", "Value"],
    [
        ["Date", "January 11, 2024"],
        ["Net Intake Pressure", "-465"],
        ["Transfers", "11"],
        ["Discharges", "476"]
    ]
)

add_paragraph(
    "For this observation, discharges exceeded transfers by 465."
)


add_subheading("12.5 Net Intake Pressure Distribution")

add_table(
    ["Category", "Number of Observations"],
    [
        ["Positive", "238"],
        ["Zero", "7"],
        ["Negative", "475"]
    ]
)


add_subheading("12.6 Average Care Load")

add_table(
    ["Metric", "Average"],
    [
        ["CBP custody", "171.49"],
        ["HHS care", "6,061.28"],
        ["Total System Load", "6,232.77"]
    ]
)


add_subheading("12.7 Overall Transfers and Discharges")

add_table(
    ["Metric", "Value"],
    [
        ["Total transfers", "92,641"],
        ["Total discharges", "124,853"],
        ["Overall discharge-to-transfer ratio", "1.348"]
    ]
)


add_subheading("12.8 High-Load Observations")

add_table(
    ["Metric", "Value"],
    [
        ["High-load observations", "180"],
        ["Share of observations", "25.0%"]
    ]
)


add_subheading("12.9 Highest HHS Care Observation")

add_table(
    ["Metric", "Value"],
    [
        ["Date", "December 20, 2023"],
        ["HHS care", "11,516"]
    ]
)


add_subheading("12.10 Highest CBP Custody Observation")

add_table(
    ["Metric", "Value"],
    [
        ["Date", "February 4, 2024"],
        ["CBP custody", "531"]
    ]
)


# ------------------------------------------------------------
# 18. CBP / HHS SHARE
# ------------------------------------------------------------

add_section_heading("13. CBP and HHS System Share")

add_paragraph(
    "The analysis also examined the relative contribution of CBP custody "
    "and HHS care to the overall system-load measure."
)

add_table(
    ["Component", "Share"],
    [
        ["CBP", "2.75%"],
        ["HHS", "97.25%"]
    ]
)

add_paragraph(
    "These percentages describe the analyzed dataset and should not be "
    "interpreted as an official allocation of organizational responsibility "
    "or capacity."
)


# ------------------------------------------------------------
# 19. DASHBOARD
# ------------------------------------------------------------

add_section_heading("14. Dashboard Development")

add_paragraph(
    "The project includes an interactive dashboard developed using "
    "Streamlit. The dashboard provides a user-friendly interface for "
    "exploring the analytical dataset."
)

add_code_block("dashboard/app.py")


add_subheading("14.1 Dashboard Features")

dashboard_features = [
    "System Load Overview",
    "CBP vs HHS Care Load Comparison",
    "Net Intake and Backlog Trends",
    "Cumulative Net Intake",
    "Transfers vs Discharges",
    "Selected Metric Analysis",
    "Analytical Summary",
    "High Load Periods",
    "Monthly Summary",
    "Dataset Explorer",
    "Filtered CSV Download"
]

for item in dashboard_features:
    add_bullet(item)


add_subheading("14.2 Dashboard Controls")

add_paragraph(
    "Users can select a date range to focus on a particular period "
    "of the dataset."
)

add_paragraph(
    "The dashboard also allows users to select analytical metrics."
)

metrics = [
    "Total System Load",
    "Children in CBP custody",
    "Children in HHS Care",
    "Net Intake Pressure",
    "Children transferred out of CBP custody",
    "Children discharged from HHS Care"
]

for item in metrics:
    add_bullet(item)


# ------------------------------------------------------------
# 20. ANALYTICAL DATASET
# ------------------------------------------------------------

add_section_heading("15. Final Analytical Dataset")

add_paragraph(
    "The final analytical dataset was created after completing the "
    "data preparation and feature engineering process."
)

add_paragraph("File location:")

add_code_block("data/uac_final_analysis.csv")

add_paragraph(
    "The final dataset contains the original UAC measurements together "
    "with derived system-load metrics, intake and discharge indicators, "
    "rolling averages, cumulative measures, high-load classifications "
    "and time-based features."
)


# ------------------------------------------------------------
# 21. MONTHLY SUMMARY
# ------------------------------------------------------------

add_section_heading("16. Monthly Summary")

add_paragraph(
    "A monthly summary dataset was created to support higher-level "
    "trend analysis and monthly comparisons."
)

add_code_block("data/uac_monthly_summary.csv")


# ------------------------------------------------------------
# 22. TECHNOLOGIES
# ------------------------------------------------------------

add_section_heading("17. Technologies Used")

add_table(
    ["Technology", "Purpose"],
    [
        ["Python", "Data processing, feature engineering and analysis."],
        ["Pandas", "Data loading, cleaning, transformation and aggregation."],
        ["Matplotlib", "Data visualization and exploratory analysis."],
        ["Streamlit", "Interactive dashboard development."],
        ["Jupyter Notebook", "Exploratory analysis and development."],
        ["Visual Studio Code", "Project development and file management."]
    ]
)


# ------------------------------------------------------------
# 23. PROJECT STRUCTURE
# ------------------------------------------------------------

add_section_heading("18. Project Structure")

add_code_block(
    "C:\\UAC_Project\n"
    "│\n"
    "├── README.md\n"
    "│\n"
    "├── data\n"
    "│   ├── uac_data.csv\n"
    "│   ├── uac_final_analysis.csv\n"
    "│   └── uac_monthly_summary.csv\n"
    "│\n"
    "├── analysis\n"
    "│   └── uac_analysis.ipynb\n"
    "│\n"
    "├── dashboard\n"
    "│   └── app.py\n"
    "│\n"
    "└── report\n"
    "    ├── README.md\n"
    "    ├── create_report.py\n"
    "    └── UAC_System_Capacity_Report.docx"
)


# ------------------------------------------------------------
# 24. LIMITATIONS
# ------------------------------------------------------------

add_section_heading("19. Limitations")

add_subheading("19.1 Historical Data")

add_paragraph(
    "The analysis is based on historical observations and therefore "
    "describes patterns in the available dataset."
)


add_subheading("19.2 Observation Gaps")

add_paragraph(
    "The dataset does not contain an observation for every calendar day. "
    "The average gap between observations was approximately 1.49 days, "
    "with a maximum observed gap of 10 days."
)


add_subheading("19.3 Statistical High-Load Threshold")

add_paragraph(
    "The High Load classification is based on the 75th percentile of "
    "Total System Load. It is an analytical classification and does not "
    "represent an official operational capacity threshold."
)


add_subheading("19.4 Aggregate-Level Analysis")

add_paragraph(
    "The analysis focuses on aggregate system-level measures available "
    "in the dataset. It does not provide facility-level capacity, "
    "staffing-level capacity, geographic-level capacity or individual "
    "case-level analysis."
)


add_subheading("19.5 Interpretation of Net Intake Pressure")

add_paragraph(
    "Net Intake Pressure is an analytical indicator based on transfers "
    "and discharges. It should not be interpreted as a complete measure "
    "of actual physical capacity or available beds."
)


# ------------------------------------------------------------
# 25. FUTURE ENHANCEMENTS
# ------------------------------------------------------------

add_section_heading("20. Future Enhancements")

future_items = [
    (
        "Forecasting",
        "Time-series forecasting models could be added to estimate "
        "future system load and intake pressure."
    ),
    (
        "Automated Alerts",
        "The dashboard could include automated alerts when selected "
        "analytical thresholds are reached."
    ),
    (
        "Facility-Level Analysis",
        "If facility-level data becomes available, the analysis could "
        "be extended to compare workload and capacity across facilities."
    ),
    (
        "Geographic Analysis",
        "Geographic information could be incorporated to examine "
        "regional differences in care demand."
    ),
    (
        "Real-Time Data Integration",
        "The dashboard could be connected to regularly updated data "
        "sources for more current monitoring."
    ),
    (
        "Advanced Predictive Analytics",
        "Machine learning and statistical forecasting techniques could "
        "be explored to identify factors associated with changes in "
        "system load."
    )
]

for title_text, description in future_items:
    add_small_heading(title_text)
    add_paragraph(description)


# ------------------------------------------------------------
# 26. CONCLUSION
# ------------------------------------------------------------

add_section_heading("21. Conclusion")

add_paragraph(
    "The UAC System Capacity & Care Load Analytics project provides "
    "a structured analytical approach for examining system load and "
    "movement patterns within the UAC care pipeline."
)

add_paragraph(
    "The project combines data preparation, exploratory analysis, "
    "feature engineering, statistical indicators, rolling averages, "
    "high-load classification and interactive visualization."
)

add_paragraph(
    "The analysis transforms historical system-level data into "
    "quantitative indicators such as Total System Load, Net Intake "
    "Pressure, Care Load Growth Rate, Discharge Offset Ratio, "
    "cumulative intake and rolling averages."
)

add_paragraph(
    "The Streamlit dashboard improves accessibility by allowing users "
    "to interactively examine metrics and time periods."
)

add_paragraph(
    "The resulting analytical framework provides a foundation for "
    "future enhancements such as forecasting, automated alerts, "
    "facility-level analysis and integration with additional data sources."
)


# ------------------------------------------------------------
# 27. DELIVERABLES
# ------------------------------------------------------------

add_section_heading("22. Project Deliverables")

add_table(
    ["Deliverable", "Location"],
    [
        ["Analysis Notebook", "analysis/uac_analysis.ipynb"],
        ["Original Dataset", "data/uac_data.csv"],
        ["Final Analytical Dataset", "data/uac_final_analysis.csv"],
        ["Monthly Summary Dataset", "data/uac_monthly_summary.csv"],
        ["Streamlit Dashboard", "dashboard/app.py"],
        ["Project Documentation", "report/README.md"],
        ["Project Report", "report/UAC_System_Capacity_Report.docx"]
    ]
)


# ------------------------------------------------------------
# 28. FINAL SUMMARY
# ------------------------------------------------------------

add_section_heading("23. Project Summary")

add_paragraph(
    "The project demonstrates an end-to-end data analytics workflow "
    "from raw data preparation to interactive visualization."
)

add_code_block(
    "Data Collection\n"
    "      ↓\n"
    "Data Cleaning\n"
    "      ↓\n"
    "Data Validation\n"
    "      ↓\n"
    "Exploratory Data Analysis\n"
    "      ↓\n"
    "Feature Engineering\n"
    "      ↓\n"
    "Statistical Analysis\n"
    "      ↓\n"
    "Trend Analysis\n"
    "      ↓\n"
    "High-Load Identification\n"
    "      ↓\n"
    "Dashboard Development\n"
    "      ↓\n"
    "Analytical Insights"
)


# ------------------------------------------------------------
# 29. SAVE DOCUMENT
# ------------------------------------------------------------

output_path = Path(__file__).parent / "UAC_System_Capacity_Report.docx"

doc.save(output_path)

print()
print("=" * 60)
print("REPORT CREATED SUCCESSFULLY!")
print("=" * 60)
print(f"File: {output_path}")
print("=" * 60)
print()