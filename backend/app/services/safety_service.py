import logging
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.safety import SafetyRule
from app.models.vegetable import Vegetable
from app.models.reuse import ReuseMethod, ReuseRecommendation
from app.schemas.safety import (
    SafetyConditionFlags,
    SafetyEvaluationResponse,
    SafetyRuleDetail,
    ConservativeAlternative,
)

logger = logging.getLogger("smart_peel_safety_engine")


def evaluate_peel_safety(
    db: Session,
    vegetable_slug: str,
    conditions: Optional[SafetyConditionFlags] = None,
    scan_confidence: Optional[float] = None,
) -> SafetyEvaluationResponse:
    """
    Core Food Safety Engine:
    Evaluates plant-specific biological and chemical hazards, dynamic user physical conditions
    (sprouting, greening, mould, bitterness), and AI uncertainty.
    Enforces strict scientific protocol: Never certify a peel as edible based on camera image alone.
    """
    conditions = conditions or SafetyConditionFlags()

    # 1. Retrieve confirmed vegetable
    veg = db.query(Vegetable).filter(Vegetable.slug == vegetable_slug.strip().lower()).first()
    if not veg:
        raise ValueError(f"Vegetable '{vegetable_slug}' not found.")

    # 2. Query existing safety rules for this vegetable
    rules = db.query(SafetyRule).filter(SafetyRule.vegetable_id == veg.id).all()

    active_hazards: List[SafetyRuleDetail] = []
    for r in rules:
        ref_text = (
            f"{r.reference_source.title} ({r.reference_source.publication_year or ''})"
            if r.reference_source
            else "ICMR-NIN / FAO Food Safety Guidelines"
        )
        active_hazards.append(
            SafetyRuleDetail(
                id=r.id,
                code=r.code,
                hazard_type=r.hazard_type,
                severity=r.severity,
                rule_description_en=r.rule_description_en,
                rule_description_ta=r.rule_description_ta,
                scientific_reference=ref_text,
                conservative_alternative_en=r.conservative_alternative_en,
                conservative_alternative_ta=r.conservative_alternative_ta,
            )
        )

    # 3. Dynamic Condition Evaluations
    is_hazardous = False
    overall_status = veg.food_safety_status
    edible_allowed = overall_status in ["safe_edible", "conditional_cooking_required"]
    requires_special_processing = overall_status == "conditional_cooking_required"
    proc_en: Optional[str] = None
    proc_ta: Optional[str] = None

    # Condition A: Spoilage / Visible Mould
    if conditions.has_visible_mould:
        is_hazardous = True
        overall_status = "critical_hazard_discard"
        edible_allowed = False
        requires_special_processing = False
        active_hazards.insert(
            0,
            SafetyRuleDetail(
                id=9001,
                code="SR_CRITICAL_MYCOTOXIN",
                hazard_type="fungal_mycotoxin",
                severity="critical",
                rule_description_en="Visible fungal mycelia or mould detected. High probability of aflatoxin or patulin mycotoxins. Must NOT be consumed or fed to livestock.",
                rule_description_ta="பூஞ்சை தொற்று கண்டறியப்பட்டது. மைக்கோடாக்சின் நச்சு ஆபத்து உள்ளது. உணவுக்கோ அல்லது கால்நடைகளுக்கோ பயன்படுத்தக்கூடாது.",
                scientific_reference="WHO Food Safety: Mycotoxins Technical Report 2023",
                conservative_alternative_en="Dispose via deep anaerobic composting or municipal waste diversion.",
                conservative_alternative_ta="ஆழமான உரம் குழி அல்லது நகராட்சி கழிவு முறையில் அகற்றவும்.",
            ),
        )

    # Condition B: Green skin or Sprouted potato
    if veg.slug == "potato" and conditions.is_green_or_sprouted:
        is_hazardous = True
        overall_status = "critical_hazard_discard"
        edible_allowed = False
        requires_special_processing = False
        active_hazards.insert(
            0,
            SafetyRuleDetail(
                id=9002,
                code="SR_CRITICAL_POTATO_SOLANINE",
                hazard_type="glycoalkaloid",
                severity="critical",
                rule_description_en="Green discoloration indicates heavy accumulation of toxic steroidal glycoalkaloids (alpha-solanine and alpha-chaconine). Heat-stable; not destroyed by cooking. Severely hazardous.",
                rule_description_ta="பச்சை நிற மாற்றம் சோலனைன் நச்சு திரட்சியைக் குறிக்கிறது. இது சமைத்தாலும் அழியாது. கண்டிப்பாக உண்ணக்கூடாது.",
                scientific_reference="EFSA Panel on Contaminants in the Food Chain (CONTAM) 2020",
                conservative_alternative_en="Divert exclusively to anaerobic biogas digester or hot compost pile.",
                conservative_alternative_ta="உயிர்வாயு ஆலை அல்லது சூடான உரமாக்கலுக்கு மட்டும் பயன்படுத்தவும்.",
            ),
        )

    # Condition C: Bitter taste in Cucurbits / Gourds
    gourd_slugs = ["cucumber", "pumpkin", "bottle-gourd", "ridge-gourd", "bitter-gourd", "ash-gourd", "snake-gourd"]
    if veg.slug in gourd_slugs and conditions.is_bitter_tasting:
        is_hazardous = True
        overall_status = "critical_hazard_discard"
        edible_allowed = False
        active_hazards.insert(
            0,
            SafetyRuleDetail(
                id=9003,
                code="SR_CRITICAL_CUCURBITACIN_TOXICITY",
                hazard_type="cucurbitacin",
                severity="critical",
                rule_description_en="Abnormal bitterness in cucurbits/gourds indicates toxic cucurbitacin levels. Ingestion can cause severe hemorrhagic gastritis. Discard immediately.",
                rule_description_ta="சுரைக்காய்/வெள்ளரி குடும்பத்தில் கசப்பு தன்மை நச்சு குக்குர்பிடாசின் இருப்பதைக் குறிக்கிறது. உட்கொள்வது இரைப்பை ரத்தக்கசிவை ஏற்படுத்தலாம்.",
                scientific_reference="Clinical Toxicology: Toxic Squash Syndrome Case Reviews",
                conservative_alternative_en="Compost only; avoid animal consumption.",
                conservative_alternative_ta="மண்புழு உரமாக்கல் அல்லது கழிவு உரமாக மாற்றவும்.",
            ),
        )

    # Condition D: Cassava peel inherent toxicity
    if veg.slug == "cassava" or veg.slug == "tapioca":
        is_hazardous = True
        overall_status = "inedible_valorize_only"
        edible_allowed = False
        requires_special_processing = True
        proc_en = "Cassava peels contain toxic cyanogenic glucosides (linamarin). Strictly inedible raw. Industrial valorization or multi-day fermentation required."
        proc_ta = "மரவள்ளிக்கிழங்கு தோலில் சயனைடு நச்சு உள்ளது. பச்சையாக உண்ணவே கூடாது. பல நாள் நொதித்தல் அல்லது தொழில்துறை பயன்பாட்டிற்கு மட்டுமே."

    # Condition E: Taro / Colocasia / Elephant Foot Yam calcium oxalate raphides
    if veg.slug in ["taro", "colocasia", "elephant-foot-yam", "yam"]:
        requires_special_processing = True
        proc_en = "Peels contain sharp calcium oxalate raphides that cause intense itching and swelling of mucosal tissues. Must be soaked in tamarind/lemon acid bath and boiled thoroughly."
        proc_ta = "தோலில் கால்சியம் ஆக்சலேட் ஊசி போன்ற படிகங்கள் உள்ளன. புளிக் கரைசலில் ஊறவைத்து, நன்கு வேகவைக்க வேண்டும்."

    # Condition F: AI Uncertainty / Low Confidence Rejection
    if scan_confidence is not None and scan_confidence < 0.65:
        edible_allowed = False
        active_hazards.append(
            SafetyRuleDetail(
                id=9004,
                code="SR_UNCERTAIN_AI_PREDICTION",
                hazard_type="uncertain_classification",
                severity="warning",
                rule_description_en="AI classification confidence is below 65%. Computer vision alone must never be used to certify an unknown peel as safe for culinary consumption.",
                rule_description_ta="செயற்கை நுண்ணறிவு நம்பிக்கை அளவு 65%க்கு குறைவாக உள்ளது. கேமரா தோற்றத்தை மட்டுமே கொண்டு உணவாகப் பயன்படுத்த ஒப்புதல் அளிக்க முடியாது.",
                scientific_reference="ISO/IEC 24029 Assessment of Machine Learning Robustness",
                conservative_alternative_en="Confirm botanical identity manually before any culinary use.",
                conservative_alternative_ta="உணவாகப் பயன்படுத்தும் முன் தாவர வகையை கைமுறையாக உறுதிப்படுத்தவும்.",
            ),
        )

    # Condition G: Surface Pesticide & Microbial Wash requirement
    if conditions.is_unwashed:
        active_hazards.append(
            SafetyRuleDetail(
                id=9005,
                code="SR_SURFACE_PESTICIDE_RESIDUE",
                hazard_type="pesticide_residue",
                severity="notice",
                rule_description_en="Market peels carry potential agrochemical residues and soil microbes. Soak for 15 minutes in 2% salt water or 1% baking soda solution and scrub under running water.",
                rule_description_ta="சந்தைக் காய்கறிகளில் பூச்சிக்கொல்லி எச்சங்கள் இருக்கலாம். 2% உப்பு நீர் அல்லது 1% சோடா உப்புக் கரைசலில் 15 நிமிடம் ஊறவைத்து கழுவவும்.",
                scientific_reference="FSSAI Safe Food Washing Protocols 2022",
                conservative_alternative_en="Abrasive wash or culinary peeling with discard.",
                conservative_alternative_ta="நன்கு உரசி கழுவுதல் அல்லது உரமாக மாற்றுதல்.",
            ),
        )

    # 4. Conservative Alternative Valorization Options
    conservative_alternatives = [
        ConservativeAlternative(
            method_code="aerobic_compost",
            name_en="Aerobic Composting",
            name_ta="காற்றோட்ட உரமாக்கல்",
            category="composting",
            description_en="Safe microbial decomposition into nutrient-rich humus soil amendment.",
            description_ta="நுண்ணுயிர்கள் மூலம் ஊட்டச்சத்து நிறைந்த இயற்கை உரமாக மாற்றுதல்.",
        ),
        ConservativeAlternative(
            method_code="biogas_anaerobic",
            name_en="Anaerobic Biogas Feedstock",
            name_ta="உயிர்வாயு உற்பத்தி",
            category="biogas",
            description_en="Converts organic biomass into renewable methane fuel in sealed digester tanks.",
            description_ta="கழிவுகளை மீத்தேன் உயிர் எரிபொருளாக மாற்றும் முறை.",
        ),
        ConservativeAlternative(
            method_code="vermicompost",
            name_en="Vermicomposting (Earthworms)",
            name_ta="மண்புழு உரமாக்கல்",
            category="vermicompost",
            description_en="Degradation by earthworms (Eisenia fetida) producing high-grade bio-fertilizer.",
            description_ta="மண்புழுக்கள் மூலம் உயர்தர இயற்கை உரமாக மாற்றுதல்.",
        ),
    ]

    disclaimer_en = (
        "CRITICAL SCIENTIFIC SAFETY DISCLAIMER: This system provides scientific educational references. "
        "Camera appearance cannot detect chemical toxins, pesticides, or microbial pathogens. "
        "Never consume peels with abnormal bitterness, greening, or visible spoilage."
    )
    disclaimer_ta = (
        "முக்கிய அறிவியல் பாதுகாப்பு மறுப்பு: இந்த அமைப்பு கல்வித் தரவுகளை மட்டுமே வழங்குகிறது. "
        "கேமரா படத்தால் ரசாயன நச்சுகள், பூச்சிக்கொல்லிகள் அல்லது பாக்டீரியாக்களைக் கண்டறிய முடியாது. "
        "கசப்பு, பச்சை நிறம் அல்லது பூஞ்சை உள்ள தோல்களை ஒருபோதும் உண்ணக்கூடாது."
    )

    return SafetyEvaluationResponse(
        vegetable_slug=veg.slug,
        vegetable_name_en=veg.name_en,
        vegetable_name_ta=veg.name_ta,
        scientific_name=veg.scientific_name,
        intrinsic_safety_status=veg.food_safety_status,
        overall_safety_status=overall_status,
        edible_recommendation_allowed=edible_allowed,
        is_hazardous=is_hazardous,
        requires_special_processing=requires_special_processing,
        processing_instructions_en=proc_en,
        processing_instructions_ta=proc_ta,
        active_hazards=active_hazards,
        conservative_alternatives=conservative_alternatives,
        general_safety_disclaimer_en=disclaimer_en,
        general_safety_disclaimer_ta=disclaimer_ta,
    )
