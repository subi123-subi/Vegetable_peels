from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app.models.vegetable import Vegetable, PlantPart
from app.models.nutrient import (
    Nutrient,
    NutrientProfile,
    NutrientMeasurement,
    PeelYieldRatio,
    DailyReferenceIntake,
)
from app.schemas.estimation import (
    EstimationInput,
    EstimationResponse,
    NutrientIntakeDetail,
    EnvironmentalImpact,
    NutritionalSuperiorityHighlight,
    PeelYieldRatioResponse,
    DailyReferenceIntakeResponse,
)

POPULATION_GROUP_LABELS = {
    "adult_male": {
        "en": "Adult Male (19-59 yrs, Sedentary/Moderate)",
        "ta": "வயது வந்த ஆண் (19-59 வயது)",
    },
    "adult_female": {
        "en": "Adult Female (19-59 yrs, Sedentary/Moderate)",
        "ta": "வயது வந்த பெண் (19-59 வயது)",
    },
    "pregnant_woman": {
        "en": "Pregnant Woman (2nd & 3rd Trimester)",
        "ta": "கர்ப்பிணிப் பெண் (2 மற்றும் 3-ம் பருவம்)",
    },
    "lactating_mother": {
        "en": "Lactating Mother (0-12 months postpartum)",
        "ta": "தாய்ப்பால் அளிக்கும் தாய்",
    },
    "children_7_9y": {
        "en": "Children (7-9 years of age)",
        "ta": "வளரும் குழந்தைகள் (7-9 வயது)",
    },
}

PREPARATION_METHOD_CONFIG = {
    "fresh_raw": {
        "label_en": "Fresh / Raw Preparation (Chutney / Salad)",
        "label_ta": "புதிய / பச்சையான பயன்பாடு (துவையல் / சாலட்)",
        "retention_multipliers": {},
        "default_retention": 1.00,
    },
    "sauteed": {
        "label_en": "Sautéed / Stir-Fried (Poriyal / Thuvaiyal)",
        "label_ta": "வறுவல் / துவையல் / பொரியல்",
        "retention_multipliers": {
            "vit_c": 0.80,
            "vit_b9": 0.80,
            "vit_b1": 0.88,
            "vit_b2": 0.90,
            "vit_b6": 0.90,
            "vit_a": 0.92,
            "lycopene": 0.95,
            "quercetin": 0.90,
            "total_phenolics": 0.85,
        },
        "default_retention": 1.00,
    },
    "boiled_broth": {
        "label_en": "Boiled & Broth Consumed (Sambar / Soup)",
        "label_ta": "வேகவைத்து சாற்றுடன் உட்கொள்ளுதல் (சாம்பார் / சூப்)",
        "retention_multipliers": {
            "vit_c": 0.70,
            "vit_b9": 0.75,
            "vit_b1": 0.80,
            "vit_b2": 0.85,
            "vit_b6": 0.85,
            "vit_a": 0.88,
        },
        "default_retention": 1.00,
    },
    "boiled_drained": {
        "label_en": "Boiled & Cooking Water Drained",
        "label_ta": "வேகவைத்து நீரை வடித்தல்",
        "retention_multipliers": {
            "vit_c": 0.45,
            "vit_b9": 0.50,
            "vit_b1": 0.55,
            "vit_b2": 0.60,
            "vit_b6": 0.60,
            "potassium": 0.65,
            "sodium": 0.70,
            "calcium": 0.85,
            "magnesium": 0.80,
            "iron": 0.85,
        },
        "default_retention": 0.90,
    },
    "dried_powder": {
        "label_en": "Solar-Dried / Dehydrated Peel Powder",
        "label_ta": "உலர்த்தி அரைத்த தோல் பொடி",
        "retention_multipliers": {
            "vit_c": 0.60,
            "vit_b9": 0.70,
            "vit_a": 0.85,
            "flavonoids": 0.95,
            "quercetin": 0.95,
            "total_phenolics": 0.90,
        },
        "default_retention": 1.00,
    },
}


def get_retention_factor(nutrient_code: str, prep_method: str) -> float:
    config = PREPARATION_METHOD_CONFIG.get(prep_method, PREPARATION_METHOD_CONFIG["fresh_raw"])
    return config["retention_multipliers"].get(nutrient_code, config["default_retention"])


def calculate_nutrient_estimation(db: Session, input_data: EstimationInput) -> EstimationResponse:
    # 1. Resolve vegetable
    veg: Optional[Vegetable] = None
    if input_data.vegetable_id:
        veg = db.query(Vegetable).filter(Vegetable.id == input_data.vegetable_id).first()
    elif input_data.vegetable_slug:
        veg = db.query(Vegetable).filter(Vegetable.slug == input_data.vegetable_slug.strip().lower()).first()

    if not veg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vegetable '{input_data.vegetable_slug or input_data.vegetable_id}' not found.",
        )

    # 2. Get Peel Yield Ratio
    yield_ratio = db.query(PeelYieldRatio).filter(PeelYieldRatio.vegetable_id == veg.id).first()
    if not yield_ratio:
        # Fallback reasonable botanical default
        avg_peel_pct = 15.0
        min_peel_pct = 10.0
        max_peel_pct = 20.0
        moisture_pct = 88.0
        dry_pct = 12.0
        pulp_notes_en = "Vegetable skin periderm is rich in protective dietary fiber and polyphenolic antioxidants."
        pulp_notes_ta = "காய்கறி தோலில் பாதுகாப்பு நார்ச்சத்தும் ஆக்ஸிஜனேற்றிகளும் நிறைந்துள்ளன."
    else:
        avg_peel_pct = yield_ratio.average_peel_percentage
        min_peel_pct = yield_ratio.min_peel_percentage
        max_peel_pct = yield_ratio.max_peel_percentage
        moisture_pct = yield_ratio.moisture_percentage_fresh
        dry_pct = yield_ratio.dry_matter_percentage
        pulp_notes_en = yield_ratio.pulp_comparison_notes_en or ""
        pulp_notes_ta = yield_ratio.pulp_comparison_notes_ta or ""

    # 3. Resolve Peel Weight
    input_type = input_data.input_weight_type.strip().lower()
    if input_type == "whole_vegetable":
        calculated_peel_weight = input_data.input_weight_grams * (avg_peel_pct / 100.0)
        peel_weight_range = {
            "min": round(input_data.input_weight_grams * (min_peel_pct / 100.0), 2),
            "max": round(input_data.input_weight_grams * (max_peel_pct / 100.0), 2),
        }
    else:
        input_type = "peel"
        calculated_peel_weight = input_data.input_weight_grams
        peel_weight_range = {
            "min": round(input_data.input_weight_grams * 0.95, 2),
            "max": round(input_data.input_weight_grams * 1.05, 2),
        }

    moisture_weight = round(calculated_peel_weight * (moisture_pct / 100.0), 2)
    dry_matter_weight = round(calculated_peel_weight * (dry_pct / 100.0), 2)

    # 4. Preparation Method and Population Group Config
    prep_method = input_data.preparation_method.strip().lower()
    if prep_method not in PREPARATION_METHOD_CONFIG:
        prep_method = "fresh_raw"
    prep_config = PREPARATION_METHOD_CONFIG[prep_method]

    pop_group = input_data.population_group.strip().lower()
    if pop_group not in POPULATION_GROUP_LABELS:
        pop_group = "adult_male"
    pop_labels = POPULATION_GROUP_LABELS[pop_group]

    servings = max(1, input_data.servings)

    # 5. Fetch Daily Reference Intakes for this demographic
    dris = {
        d.nutrient_code: d
        for d in db.query(DailyReferenceIntake)
        .filter(DailyReferenceIntake.population_group == pop_group)
        .all()
    }

    # 6. Fetch Nutrient Profile & Measurements
    profile = (
        db.query(NutrientProfile)
        .options(
            joinedload(NutrientProfile.measurements).joinedload(NutrientMeasurement.nutrient)
        )
        .filter(NutrientProfile.vegetable_id == veg.id)
        .first()
    )

    nutrient_details: List[NutrientIntakeDetail] = []
    superior_nutrients_list: List[str] = []

    if profile and profile.measurements:
        weight_factor = calculated_peel_weight / 100.0
        min_factor = peel_weight_range["min"] / 100.0
        max_factor = peel_weight_range["max"] / 100.0

        for m in profile.measurements:
            nut = m.nutrient
            if not nut:
                continue

            retention = get_retention_factor(nut.code, prep_method)

            # Concentration conversion if profile was dry weight basis
            conc_raw = m.concentration_per_100g
            if profile.fresh_or_dry_basis == "dry_weight" and prep_method != "dried_powder":
                # Convert dry basis concentration to fresh basis: C_fresh = C_dry * (100 - moisture%) / 100
                conc_raw = conc_raw * (dry_pct / 100.0)

            est_amount = round(weight_factor * conc_raw * retention, 3)
            est_per_serving = round(est_amount / servings, 3)

            min_est = None
            max_est = None
            if m.min_value is not None:
                min_c = m.min_value if profile.fresh_or_dry_basis != "dry_weight" else m.min_value * (dry_pct / 100.0)
                min_est = round(min_factor * min_c * retention, 3)
            if m.max_value is not None:
                max_c = m.max_value if profile.fresh_or_dry_basis != "dry_weight" else m.max_value * (dry_pct / 100.0)
                max_est = round(max_factor * max_c * retention, 3)

            # RDA calculations
            dri_item = dris.get(nut.code)
            rda_val = dri_item.rda_value if dri_item else None
            pct_rda = None
            rda_status = None
            rda_label_en = None
            rda_label_ta = None

            if rda_val and rda_val > 0:
                pct_rda = round((est_amount / rda_val) * 100.0, 1)
                if pct_rda >= 30.0:
                    rda_status = "exceptional"
                    rda_label_en = "Exceptional / High Source (>30% RDA)"
                    rda_label_ta = "அற்புதமான ஆதாரம் (>30% RDA)"
                    superior_nutrients_list.append(nut.name_en)
                elif pct_rda >= 15.0:
                    rda_status = "good"
                    rda_label_en = "Good Source (15-30% RDA)"
                    rda_label_ta = "நல்ல ஆதாரம் (15-30% RDA)"
                    superior_nutrients_list.append(nut.name_en)
                elif pct_rda >= 5.0:
                    rda_status = "moderate"
                    rda_label_en = "Moderate Source (5-15% RDA)"
                    rda_label_ta = "மிதமான ஆதாரம் (5-15% RDA)"
                else:
                    rda_status = "trace"
                    rda_label_en = "Trace Source (<5% RDA)"
                    rda_label_ta = "குறைந்த ஆதாரம் (<5% RDA)"

            nutrient_details.append(
                NutrientIntakeDetail(
                    nutrient_code=nut.code,
                    nutrient_name_en=nut.name_en,
                    nutrient_name_ta=nut.name_ta,
                    category=nut.category,
                    concentration_per_100g_raw=round(conc_raw, 2),
                    unit=m.unit,
                    retention_factor=retention,
                    estimated_amount=est_amount,
                    estimated_amount_per_serving=est_per_serving,
                    min_estimated_amount=min_est,
                    max_estimated_amount=max_est,
                    confidence_interval=m.confidence_interval,
                    rda_value=rda_val,
                    percentage_rda=pct_rda,
                    rda_status=rda_status,
                    rda_status_label_en=rda_label_en,
                    rda_status_label_ta=rda_label_ta,
                    biological_role_en=nut.biological_role_en,
                    biological_role_ta=nut.biological_role_ta,
                )
            )

    # 7. Environmental Impact
    wet_waste_kg = round(calculated_peel_weight / 1000.0, 4)
    ghg_avoided = round(wet_waste_kg * 0.52, 4)  # 0.52 kg CO2e / kg diverted
    compost_pot = round(wet_waste_kg * 0.25, 4)  # 0.25 kg compost / kg peel

    env_impact = EnvironmentalImpact(
        wet_waste_diverted_kg=wet_waste_kg,
        ghg_emissions_avoided_kg_co2e=ghg_avoided,
        compost_potential_kg=compost_pot,
        valorization_readiness="Verified for culinary preparation and organic composting",
    )

    # 8. Superiority Highlight
    superiority = NutritionalSuperiorityHighlight(
        comparison_en=pulp_notes_en,
        comparison_ta=pulp_notes_ta,
        superior_nutrients=list(set(superior_nutrients_list)),
    )

    return EstimationResponse(
        vegetable_id=veg.id,
        vegetable_slug=veg.slug,
        vegetable_name_en=veg.name_en,
        vegetable_name_ta=veg.name_ta,
        input_weight_grams=input_data.input_weight_grams,
        input_weight_type=input_type,
        calculated_peel_weight_grams=round(calculated_peel_weight, 2),
        peel_weight_range_grams=peel_weight_range,
        peel_yield_percentage=avg_peel_pct,
        dry_matter_weight_grams=dry_matter_weight,
        moisture_weight_grams=moisture_weight,
        preparation_method=prep_method,
        preparation_method_label_en=prep_config["label_en"],
        preparation_method_label_ta=prep_config["label_ta"],
        population_group=pop_group,
        population_group_label_en=pop_labels["en"],
        population_group_label_ta=pop_labels["ta"],
        servings=servings,
        nutrients=nutrient_details,
        environmental_impact=env_impact,
        superiority=superiority,
        scientific_basis_notes="Formulations based on ICMR-NIN IFCT 2017 & USDA FoodData Central validated peel measurements.",
        timestamp=datetime.now(timezone.utc),
    )
