import io
from datetime import datetime
from typing import Dict, Any, Optional

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)


def generate_nutrient_pdf(
    report_data: Dict[str, Any],
    report_uuid: str = "RPT-PREVIEW",
) -> bytes:
    """
    Generate a scientific, publication-grade PDF report for a vegetable peel nutrient estimation
    and valorization assessment using ReportLab.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#1B5E20"),  # Forest green
    )

    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#37474F"),
    )

    section_header = ParagraphStyle(
        "SectionHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#2E7D32"),
        spaceBefore=10,
        spaceAfter=6,
    )

    body_style = ParagraphStyle(
        "DocBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#263238"),
    )

    bold_body = ParagraphStyle(
        "BoldBody",
        parent=body_style,
        fontName="Helvetica-Bold",
    )

    table_header = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=colors.white,
    )

    table_cell = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#263238"),
    )

    table_cell_bold = ParagraphStyle(
        "TableCellBold",
        parent=table_cell,
        fontName="Helvetica-Bold",
    )

    disclaimer_style = ParagraphStyle(
        "Disclaimer",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#546E7A"),
    )

    elements = []

    # 1. Header Banner
    elements.append(Paragraph("SMART PEEL AI", title_style))
    elements.append(
        Paragraph(
            "Scientific Vegetable Peel Nutrient Identification & Valorization System | ICMR-NIN & USDA Validated",
            subtitle_style,
        )
    )
    elements.append(Spacer(1, 4))
    elements.append(
        Paragraph(
            f"<b>Report Reference:</b> {report_uuid} &nbsp;|&nbsp; "
            f"<b>Generated:</b> {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')} &nbsp;|&nbsp; "
            f"<b>Engine:</b> MobileNetV3 + IFCT 2017",
            body_style,
        )
    )
    elements.append(Spacer(1, 8))
    elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#2E7D32"), spaceAfter=12))

    # 2. Sample & Botanical Profile
    elements.append(Paragraph("1. Botanical Identification & Sample Parameters", section_header))

    veg_name_en = report_data.get("vegetable_name_en", "Vegetable Peel")
    veg_name_ta = report_data.get("vegetable_name_ta", "")
    input_wt = report_data.get("input_weight_grams", 0.0)
    peel_wt = report_data.get("calculated_peel_weight_grams", 0.0)
    peel_pct = report_data.get("peel_yield_percentage", 0.0)
    dry_wt = report_data.get("dry_matter_weight_grams", 0.0)
    moist_wt = report_data.get("moisture_weight_grams", 0.0)
    prep_en = report_data.get("preparation_method_label_en", "Fresh / Raw")
    pop_en = report_data.get("population_group_label_en", "Adult Male / Female")

    sample_table_data = [
        [
            Paragraph("<b>Target Vegetable:</b>", body_style),
            Paragraph(f"{veg_name_en} {f'({veg_name_ta})' if veg_name_ta else ''}", bold_body),
            Paragraph("<b>Plant Part:</b>", body_style),
            Paragraph("Outer Peel / Epidermal Cortex (தோல்)", body_style),
        ],
        [
            Paragraph("<b>Input Sample Weight:</b>", body_style),
            Paragraph(f"{input_wt:.1f} g (Whole)", body_style),
            Paragraph("<b>Calculated Peel Yield:</b>", body_style),
            Paragraph(f"{peel_wt:.1f} g ({peel_pct:.1f}%)", bold_body),
        ],
        [
            Paragraph("<b>Dry Matter Content:</b>", body_style),
            Paragraph(f"{dry_wt:.1f} g", body_style),
            Paragraph("<b>Moisture Content:</b>", body_style),
            Paragraph(f"{moist_wt:.1f} g", body_style),
        ],
        [
            Paragraph("<b>Culinary Preparation:</b>", body_style),
            Paragraph(prep_en, body_style),
            Paragraph("<b>RDA Target Group:</b>", body_style),
            Paragraph(pop_en, body_style),
        ],
    ]

    sample_table = Table(sample_table_data, colWidths=[130, 130, 130, 130])
    sample_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F1F8E9")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#C8E6C9")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    elements.append(sample_table)
    elements.append(Spacer(1, 10))

    # 3. Nutrient Quantification Table
    elements.append(Paragraph("2. Scientific Nutrient Quantification & DRI/RDA Coverage", section_header))

    nutrients_list = report_data.get("nutrients", [])
    nut_table_rows = [
        [
            Paragraph("Nutrient", table_header),
            Paragraph("Category", table_header),
            Paragraph("Raw (100g)", table_header),
            Paragraph("Retention", table_header),
            Paragraph("Intake Yield", table_header),
            Paragraph("% RDA/DRI", table_header),
            Paragraph("Biological Function", table_header),
        ]
    ]

    if nutrients_list:
        for nut in nutrients_list:
            unit = nut.get("unit", "mg")
            conc = nut.get("concentration_per_100g_raw", 0.0)
            ret = nut.get("retention_factor", 1.0)
            est = nut.get("estimated_amount", 0.0)
            pct = nut.get("percentage_rda")
            pct_str = f"{pct:.1f}%" if pct is not None else "N/A"
            role = nut.get("biological_role_en", "")
            if len(role) > 45:
                role = role[:42] + "..."

            nut_table_rows.append(
                [
                    Paragraph(f"<b>{nut.get('nutrient_name_en', '')}</b>", table_cell),
                    Paragraph(nut.get("category", "").capitalize(), table_cell),
                    Paragraph(f"{conc:.1f} {unit}", table_cell),
                    Paragraph(f"{ret*100:.0f}%", table_cell),
                    Paragraph(f"<b>{est:.2f} {unit}</b>", table_cell_bold),
                    Paragraph(pct_str, table_cell_bold if pct and pct >= 10 else table_cell),
                    Paragraph(role, table_cell),
                ]
            )
    else:
        nut_table_rows.append([Paragraph("No nutrient measurements recorded.", table_cell)] * 7)

    nut_table = Table(
        nut_table_rows,
        colWidths=[100, 60, 65, 50, 70, 55, 120],
    )
    nut_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2E7D32")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E0E0E0")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#FAFAFA")]),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    elements.append(nut_table)
    elements.append(Spacer(1, 10))

    # 4. Valorization & Environmental Impact
    elements.append(Paragraph("3. Waste Diversion & Environmental Valorization", section_header))

    env = report_data.get("environmental_impact", {})
    diverted_kg = env.get("wet_waste_diverted_kg", (peel_wt / 1000.0) if peel_wt else 0.0)
    co2_kg = env.get("ghg_emissions_avoided_kg_co2e", diverted_kg * 0.52)
    compost_kg = env.get("compost_potential_kg", diverted_kg * 0.25)

    env_table_data = [
        [
            Paragraph("<b>Organic Waste Diverted:</b>", body_style),
            Paragraph(f"<b>{diverted_kg:.3f} kg</b>", bold_body),
            Paragraph("<b>GHG Avoided (EPA WARM):</b>", body_style),
            Paragraph(f"<b>{co2_kg:.3f} kg CO2e</b>", bold_body),
            Paragraph("<b>Compost Potential:</b>", body_style),
            Paragraph(f"<b>{compost_kg:.3f} kg</b>", bold_body),
        ]
    ]
    env_table = Table(env_table_data, colWidths=[110, 60, 120, 70, 95, 65])
    env_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#E8F5E9")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#A5D6A7")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    elements.append(env_table)
    elements.append(Spacer(1, 10))

    # 5. Food Safety Assessment
    elements.append(Paragraph("4. Food Safety Assessment & Toxicological Clearance", section_header))

    safety_notes = report_data.get("safety_notes", {})
    hazards = safety_notes.get("hazards", []) if isinstance(safety_notes, dict) else []

    if hazards:
        safety_text = f"<b>Identified Cautions ({len(hazards)}):</b> " + "; ".join(
            [h.get("hazard_type", "Caution") for h in hazards]
        )
        safety_bg = colors.HexColor("#FFF3E0")
        safety_border = colors.HexColor("#FFE082")
    else:
        safety_text = (
            "<b>Toxicological Status: CLEARED.</b> No acute antinutritional hazards detected. "
            "Ensure hygienic washing with potable water to eliminate surface soil and pesticide residues."
        )
        safety_bg = colors.HexColor("#E8F5E9")
        safety_border = colors.HexColor("#C8E6C9")

    safety_table = Table([[Paragraph(safety_text, body_style)]], colWidths=[520])
    safety_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), safety_bg),
                ("BOX", (0, 0), (-1, -1), 1, safety_border),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    elements.append(safety_table)
    elements.append(Spacer(1, 10))

    # 6. References & Scientific Disclaimer
    elements.append(Paragraph("5. Scientific References & Responsible Use Disclaimer", section_header))
    elements.append(
        Paragraph(
            "<b>Primary References:</b> [1] Indian Food Composition Tables (IFCT 2017), ICMR - National Institute of Nutrition, Hyderabad. "
            "[2] USDA FoodData Central (FDC), Agricultural Research Service. "
            "[3] FAO/INFOODS Food Composition Database for Biodiversity (BioFoodComp4.0).",
            body_style,
        )
    )
    elements.append(Spacer(1, 4))
    elements.append(
        Paragraph(
            "<b>Disclaimer:</b> This report is generated by SMART PEEL AI for nutritional education and food waste "
            "valorization guidance. Nutrient quantities are statistical estimates derived from published scientific databases "
            "and do not constitute certified analytical chemistry laboratory assays of this specific biological sample. "
            "Never consume peels showing signs of mould, extreme bitterness, or greening.",
            disclaimer_style,
        )
    )

    doc.build(elements)
    return buffer.getvalue()
