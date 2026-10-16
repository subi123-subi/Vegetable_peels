import logging
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.core.security import get_password_hash
from app.models.user import UserRole, User
from app.models.vegetable import PlantPart, Vegetable, VegetableAlias
from app.models.nutrient import ScientificSource, Nutrient, NutrientProfile, NutrientMeasurement
from app.models.safety import SafetyRule
from app.models.reuse import ReuseMethod, ReuseRecommendation
from app.models.scan import AIModelVersion
from app.models.translation import Translation

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    # 1. User Roles
    roles = {
        "admin": "System Administrator with full access",
        "researcher": "Scientific researcher with dataset edit permissions",
        "user": "Standard registered user",
    }
    role_objs = {}
    for r_name, r_desc in roles.items():
        role = db.query(UserRole).filter(UserRole.name == r_name).first()
        if not role:
            role = UserRole(name=r_name, description=r_desc)
            db.add(role)
            db.flush()
        role_objs[r_name] = role

    # 2. Admin User
    admin = db.query(User).filter(User.email == "admin@smartpeel.ai").first()
    if not admin:
        admin = User(
            email="admin@smartpeel.ai",
            hashed_password=get_password_hash("Admin@SmartPeel2026!"),
            full_name="Smart Peel System Administrator",
            role_id=role_objs["admin"].id,
            is_active=True,
            is_superuser=True,
            preferred_language="en",
        )
        db.add(admin)
        logger.info("Created default administrator: admin@smartpeel.ai")

    # 3. Plant Parts
    plant_parts_data = [
        {"code": "peel", "name_en": "Vegetable Peel", "name_ta": "தோல்", "desc": "Outer skin layer removed from root or fruit vegetables"},
        {"code": "skin", "name_en": "Thin Skin", "name_ta": "மெல்லிய தோல்", "desc": "Very thin outer epidermal layer (e.g., tomato, eggplant)"},
        {"code": "rind", "name_en": "Thick Rind", "name_ta": "தடித்த தோல் / ஓடு", "desc": "Thick, hard outer protective layer (e.g., pumpkin, watermelon, squash)"},
        {"code": "outer_leaves", "name_en": "Outer Leaves", "name_ta": "வெளிப்புற இலைகள்", "desc": "Tough outermost photosynthetic leaves (e.g., cabbage, cauliflower)"},
        {"code": "pod_shell", "name_en": "Pod Shell", "name_ta": "நெற்று / காய் தோல்", "desc": "Legume or seed pod casing (e.g., peas, broad beans)"},
        {"code": "stem_layer", "name_en": "Stem Outer Layer", "name_ta": "தண்டு வெளிப்புற அடுக்கு", "desc": "Fibrous outer covering of botanical stems (e.g., banana stem, lotus stem)"},
        {"code": "husk", "name_en": "Husk / Sheath", "name_ta": "உமி / மட்டை", "desc": "Dry fibrous outer bract or sheath (e.g., corn husk)"},
    ]
    part_objs = {}
    for p in plant_parts_data:
        part = db.query(PlantPart).filter(PlantPart.code == p["code"]).first()
        if not part:
            part = PlantPart(code=p["code"], name_en=p["name_en"], name_ta=p["name_ta"], description_en=p["desc"])
            db.add(part)
            db.flush()
        part_objs[p["code"]] = part

    # 4. Scientific Sources
    sources_data = [
        {
            "title": "Indian Food Composition Tables (IFCT 2017)",
            "authors": "Longvah T, Ananthan R, Bhaskarachary K, Venkaiah K",
            "publication_year": 2017,
            "journal_or_publisher": "National Institute of Nutrition, ICMR, Hyderabad",
            "doi_or_url": "https://www.ifct2017.com",
            "source_type": "icmr_nin",
            "reliability_rating": "high",
        },
        {
            "title": "USDA FoodData Central Nutrient Database",
            "authors": "U.S. Department of Agriculture, Agricultural Research Service",
            "publication_year": 2023,
            "journal_or_publisher": "USDA ARS",
            "doi_or_url": "https://fdc.nal.usda.gov",
            "source_type": "usda",
            "reliability_rating": "high",
        },
        {
            "title": "Valorization of Vegetable Peels: Nutritional Profile and Bioactive Compounds",
            "authors": "Kumar M, Chandran D, Tomar M, et al.",
            "publication_year": 2022,
            "journal_or_publisher": "Frontiers in Nutrition, 9:904261",
            "doi_or_url": "https://doi.org/10.3389/fnut.2022.904261",
            "source_type": "peer_reviewed",
            "reliability_rating": "high",
        },
    ]
    source_objs = []
    for s in sources_data:
        src = db.query(ScientificSource).filter(ScientificSource.title == s["title"]).first()
        if not src:
            src = ScientificSource(**s)
            db.add(src)
            db.flush()
        source_objs.append(src)

    # 5. Core Nutrients (Vitamins, Minerals, Fibres, Bioactives)
    nutrients_data = [
        # Vitamins
        {"code": "vit_a", "name_en": "Vitamin A / Carotenoids", "name_ta": "வைட்டமின் ஏ / கரோட்டினாய்டுகள்", "category": "vitamin", "unit": "mcg", "role_en": "Supports vision, immune response, and cellular differentiation.", "role_ta": "பார்வைத்திறன் மற்றும் நோய் எதிர்ப்பு சக்தியை ஆதரிக்கிறது."},
        {"code": "vit_b1", "name_en": "Vitamin B1 (Thiamine)", "name_ta": "வைட்டமின் பி1 (தயமின்)", "category": "vitamin", "unit": "mg", "role_en": "Crucial coenzyme in carbohydrate metabolism and nerve function.", "role_ta": "நரம்பு மண்டலம் மற்றும் ஆற்றல் உற்பத்திக்கு உதவுகிறது."},
        {"code": "vit_b2", "name_en": "Vitamin B2 (Riboflavin)", "name_ta": "வைட்டமின் பி2 (ரிபோஃப்ளேவின்)", "category": "vitamin", "unit": "mg", "role_en": "Involved in cellular energy release and redox coenzymes.", "role_ta": "செல்லுலார் ஆற்றல் உற்பத்திக்கு அவசியமானது."},
        {"code": "vit_b3", "name_en": "Vitamin B3 (Niacin)", "name_ta": "வைட்டமின் பி3 (நியாசின்)", "category": "vitamin", "unit": "mg", "role_en": "Participates in NAD/NADP hydrogen transfer reactions.", "role_ta": "செரிமானம் மற்றும் சரும ஆரோக்கியத்திற்கு உதவுகிறது."},
        {"code": "vit_b5", "name_en": "Vitamin B5 (Pantothenic Acid)", "name_ta": "வைட்டமின் பி5 (பாந்தோத்தேனிக் அமிலம்)", "category": "vitamin", "unit": "mg", "role_en": "Constituent of Coenzyme A, vital for fatty acid synthesis.", "role_ta": "கொழுப்பு அமில தொகுப்புக்கு முக்கியமானது."},
        {"code": "vit_b6", "name_en": "Vitamin B6 (Pyridoxine)", "name_ta": "வைட்டமின் பி6 (பைரிடாக்சின்)", "category": "vitamin", "unit": "mg", "role_en": "Amino acid transamination and neurotransmitter synthesis.", "role_ta": "அமினோ அமில வளர்ச்சி மற்றும் மூளை செயல்பாட்டிற்கு உதவுகிறது."},
        {"code": "vit_b7", "name_en": "Vitamin B7 (Biotin)", "name_ta": "வைட்டமின் பி7 (பயோட்டின்)", "category": "vitamin", "unit": "mcg", "role_en": "Cofactor in carboxylase enzymes in gluconeogenesis.", "role_ta": "செல்லுலார் வளர்சிதை மாற்றத்திற்கு உதவுகிறது."},
        {"code": "vit_b9", "name_en": "Vitamin B9 (Folate)", "name_ta": "வைட்டமின் பி9 (ஃபோலேட்)", "category": "vitamin", "unit": "mcg", "role_en": "Essential for DNA synthesis and red blood cell formation.", "role_ta": "டி.என்.ஏ தொகுப்பு மற்றும் இரத்த அணுக்கள் உருவாக்கத்திற்கு தேவையானது."},
        {"code": "vit_b12", "name_en": "Vitamin B12 (Cobalamin)", "name_ta": "வைட்டமின் பி12 (கோபாலமின்)", "category": "vitamin", "unit": "mcg", "role_en": "Neurological integrity; largely absent in plant peels except bacterial symbionts.", "role_ta": "நரம்பு மண்டல ஆரோக்கியத்திற்கு உதவுகிறது."},
        {"code": "vit_c", "name_en": "Vitamin C (Ascorbic Acid)", "name_ta": "வைட்டமின் சி (அஸ்கார்பிக் அமிலம்)", "category": "vitamin", "unit": "mg", "role_en": "Potent antioxidant, cofactor in collagen synthesis and iron uptake.", "role_ta": "சக்திவாய்ந்த ஆக்ஸிஜனேற்றி, கொலாஜன் மற்றும் இரும்பு உறிஞ்சுதலுக்கு முக்கியமானது."},
        {"code": "vit_d", "name_en": "Vitamin D", "name_ta": "வைட்டமின் டி", "category": "vitamin", "unit": "mcg", "role_en": "Regulates calcium homeostasis; minimal in plants except sun-exposed fungi.", "role_ta": "கால்சியம் சமநிலையை ஒழுங்குபடுத்துகிறது."},
        {"code": "vit_e", "name_en": "Vitamin E (Tocopherols)", "name_ta": "வைட்டமின் ஈ (டோகோபெரோல்)", "category": "vitamin", "unit": "mg", "role_en": "Lipophilic antioxidant protecting lipid bilayers against peroxidation.", "role_ta": "செல் சவ்வுகளை பாதுகாக்கும் ஆக்ஸிஜனேற்றி."},
        {"code": "vit_k", "name_en": "Vitamin K (Phylloquinone)", "name_ta": "வைட்டமின் கே (ஃபில்லோகுவினோன்)", "category": "vitamin", "unit": "mcg", "role_en": "Required for post-translational carboxylation of clotting factors.", "role_ta": "இரத்தம் உறைதல் மற்றும் எலும்பு வளர்ச்சிக்கு அவசியம்."},
        # Minerals
        {"code": "calcium", "name_en": "Calcium (Ca)", "name_ta": "கால்சியம் (சுண்ணாம்புச்சத்து)", "category": "mineral", "unit": "mg", "role_en": "Structural bone matrix constituent and intracellular second messenger.", "role_ta": "எலும்பு மற்றும் பற்களின் உறுதிக்கு முக்கியமானது."},
        {"code": "iron", "name_en": "Iron (Fe)", "name_ta": "இரும்புச்சத்து (Fe)", "category": "mineral", "unit": "mg", "role_en": "Haemoglobin core and electron transport in cytochromes.", "role_ta": "ஹீமோகுளோபின் மற்றும் இரத்த உருவாக்கத்திற்கு மிக முக்கியம்."},
        {"code": "magnesium", "name_en": "Magnesium (Mg)", "name_ta": "மெக்னீசியம் (Mg)", "category": "mineral", "unit": "mg", "role_en": "Cofactor in over 300 ATP-dependent enzymatic processes.", "role_ta": "தசை மற்றும் நரம்பு இயக்கங்களுக்கு 300+ என்சைம்களுக்கு உதவுகிறது."},
        {"code": "potassium", "name_en": "Potassium (K)", "name_ta": "பொட்டாசியம் (K)", "category": "mineral", "unit": "mg", "role_en": "Primary intracellular cation regulating fluid balance and cardiac rhythm.", "role_ta": "இரத்த அழுத்தம் மற்றும் இதய துடிப்பை சீராக்க உதவுகிறது."},
        {"code": "phosphorus", "name_en": "Phosphorus (P)", "name_ta": "பாஸ்பரஸ் (P)", "category": "mineral", "unit": "mg", "role_en": "Structural phosphodiester backbone of nucleic acids and ATP storage.", "role_ta": "எலும்பு வளர்ச்சி மற்றும் ஆற்றல் சேமிப்பிற்கு அவசியம்."},
        {"code": "sodium", "name_en": "Sodium (Na)", "name_ta": "சோடியம் (Na)", "category": "mineral", "unit": "mg", "role_en": "Extracellular electrolyte maintaining osmotic balance.", "role_ta": "உடலில் நீர் சமநிலையை பராமரிக்கிறது."},
        {"code": "zinc", "name_en": "Zinc (Zn)", "name_ta": "துத்தநாகம் (Zn)", "category": "mineral", "unit": "mg", "role_en": "Catalytic and structural zinc finger domains; cellular immunity.", "role_ta": "நோய் எதிர்ப்பு சக்தி மற்றும் செல் வளர்ச்சிக்கு தேவையானது."},
        {"code": "copper", "name_en": "Copper (Cu)", "name_ta": "செம்புச்சத்து (Cu)", "category": "mineral", "unit": "mg", "role_en": "Cofactor in superoxide dismutase, tyrosinase, and ceruloplasmin.", "role_ta": "செல்லுலார் என்சைம்கள் இயக்கத்திற்கு உதவுகிறது."},
        {"code": "manganese", "name_en": "Manganese (Mn)", "name_ta": "மாங்கனீசு (Mn)", "category": "mineral", "unit": "mg", "role_en": "Mitochondrial antioxidant SOD enzyme component.", "role_ta": "மைட்டோகாண்ட்ரியா பாதுகாப்புக்கு உதவுகிறது."},
        {"code": "selenium", "name_en": "Selenium (Se)", "name_ta": "செலீனியம் (Se)", "category": "mineral", "unit": "mcg", "role_en": "Essential trace element in selenocysteine (glutathione peroxidase).", "role_ta": "செல்லுலார் ஆக்ஸிஜனேற்ற தடுப்புக்கு முக்கியமானது."},
        # Other Bioactive Compounds
        {"code": "dietary_fibre", "name_en": "Total Dietary Fibre", "name_ta": "மொத்த உணவு நார்ச்சத்து", "category": "other", "unit": "g", "role_en": "Promotes colonic motility, short-chain fatty acid synthesis, and satiety.", "role_ta": "செரிமான மண்டல இயக்கம் மற்றும் குடல் நலத்திற்கு உதவுகிறது."},
        {"code": "soluble_fibre", "name_en": "Soluble Fibre", "name_ta": "கரையும் நார்ச்சத்து", "category": "other", "unit": "g", "role_en": "Pectin, gums and mucilage that attenuate glucose and lipid absorption.", "role_ta": "இரத்த சர்க்கரை மற்றும் கொழுப்பை சமப்படுத்த உதவுகிறது."},
        {"code": "insoluble_fibre", "name_en": "Insoluble Fibre", "name_ta": "கரையாத நார்ச்சத்து", "category": "other", "unit": "g", "role_en": "Cellulose, hemicellulose and lignin increasing stool bulk.", "role_ta": "மலக்குடல் கழிவு வெளியேற்றத்திற்கு உதவுகிறது."},
        {"code": "total_phenolics", "name_en": "Total Phenolics (GAE)", "name_ta": "மொத்த பினாலிக் சேர்மங்கள்", "category": "other", "unit": "mg GAE", "role_en": "Radical-scavenging bioactive plant secondary metabolites.", "role_ta": "உடல் செல்களை சேதத்திலிருந்து காக்கும் தாவர வேதிப்பொருட்கள்."},
        {"code": "flavonoids", "name_en": "Flavonoids", "name_ta": "ஃபிளவனாய்டுகள்", "category": "other", "unit": "mg", "role_en": "Polyphenolic antioxidant compounds modulating cellular signaling pathways.", "role_ta": "செல்லுலார் சிக்னலிங் சீராக்கும் தாவர ஆக்ஸிஜனேற்றிகள்."},
        {"code": "betalains", "name_en": "Betalains", "name_ta": "பீட்டலைன்கள்", "category": "other", "unit": "mg", "role_en": "Tyrosine-derived nitrogenous pigments with strong radical scavenging ability.", "role_ta": "பீட்ரூட்டில் காணப்படும் சக்திவாய்ந்த இயற்கை நிறமிகள்."},
    ]
    nutrient_objs = {}
    for n in nutrients_data:
        nut = db.query(Nutrient).filter(Nutrient.code == n["code"]).first()
        if not nut:
            nut = Nutrient(
                code=n["code"],
                name_en=n["name_en"],
                name_ta=n["name_ta"],
                category=n["category"],
                standard_unit=n["unit"],
                biological_role_en=n["role_en"],
                biological_role_ta=n["role_ta"],
            )
            db.add(nut)
            db.flush()
        nutrient_objs[n["code"]] = nut

    # 6. Reuse Methods
    reuse_methods_data = [
        {"code": "aerobic_composting", "name_en": "Aerobic Composting", "name_ta": "காற்றுள்ள உரமாக்கல்", "category": "composting", "desc_en": "Decomposition by oxygen-loving microbes into nutrient-rich soil amendment.", "desc_ta": "கரிம கழிவுகளை சத்து நிறைந்த உரமாக மாற்றும் முறை."},
        {"code": "vermicomposting", "name_en": "Vermicomposting", "name_ta": "மண்புழு உரமாக்கல்", "category": "vermicomposting", "desc_en": "Bio-oxidation and stabilization using specialized earthworms (Eisenia fetida).", "desc_ta": "மண்புழுக்கள் மூலம் தரமான இயற்கை உரம் தயாரிக்கும் முறை."},
        {"code": "biogas_anaerobic", "name_en": "Biogas Feedstock", "name_ta": "உயிர்வாயு உற்பத்தி", "category": "biogas", "desc_en": "Anaerobic digester substrate producing methane fuel and bio-slurry.", "desc_ta": "மீத்தேன் வாயு மற்றும் இயற்கை திரவ உரம் உற்பத்தி செய்யும் முறை."},
        {"code": "culinary_stock", "name_en": "Culinary Vegetable Stock", "name_ta": "சமையல் காய்கறி சூப் / சாறு", "category": "food", "desc_en": "Simmering thoroughly cleaned, food-safe peels for aromatic broth.", "desc_ta": "சுத்தமான காய்கறி தோல்களை வேகவைத்து சுவையான சூப் தயாரித்தல்."},
        {"code": "culinary_crisps", "name_en": "Baked Peel Crisps", "name_ta": "சுடப்பட்ட காய்கறி சிப்ஸ்", "category": "food", "desc_en": "Seasoning and baking/air-frying clean edible skins into crisp snacks.", "desc_ta": "மசாலா சேர்த்து வறுக்கப்பட்ட சத்தான சிப்ஸ் தயாரிப்பு."},
        {"code": "natural_pigment", "name_en": "Natural Pigment Extraction", "name_ta": "இயற்கை வண்ண நிறமி பிரித்தெடுத்தல்", "category": "pigment_extraction", "desc_en": "Extraction of safe bio-colorants (anthocyanins, betalains, carotenoids).", "desc_ta": "உணவு மற்றும் ஜவுளிகளுக்கான இயற்கை நிறமிகளைப் பிரித்தெடுத்தல்."},
        {"code": "bio_materials", "name_en": "Bio-Adsorbent & Fibre Recovery", "name_ta": "உயிரி உறிஞ்சி மற்றும் நார் பிரிப்பு", "category": "bio_materials", "desc_en": "Utilizing dried porous peel residue for wastewater heavy-metal adsorption.", "desc_ta": "கழிவுநீர் சுத்திகரிப்பு மற்றும் மறுசுழற்சிக்கான இயற்கை நார் பயன்பாடு."},
        {"code": "ruminant_feed", "name_en": "Controlled Livestock Feed", "name_ta": "கால்நடை தீவனம் (கட்டுப்படுத்தப்பட்ட)", "category": "animal_feed", "desc_en": "Safe, non-toxic peel forage supplemented for ruminant diet.", "desc_ta": "ஆராய்ச்சியால் உறுதிசெய்யப்பட்ட பாதுகாப்பான மாடுகளுக்கான தீவனம்."},
    ]
    reuse_objs = {}
    for rm in reuse_methods_data:
        method = db.query(ReuseMethod).filter(ReuseMethod.code == rm["code"]).first()
        if not method:
            method = ReuseMethod(
                code=rm["code"],
                name_en=rm["name_en"],
                name_ta=rm["name_ta"],
                category=rm["category"],
                description_en=rm["desc_en"],
                description_ta=rm["desc_ta"],
            )
            db.add(method)
            db.flush()
        reuse_objs[rm["code"]] = method

    # 7. Complete 50 Vegetables Catalogue (Group A through E)
    veg_catalogue = [
        # Group A — Root Vegetables (1-12)
        {"slug": "carrot", "name_en": "Carrot", "name_ta": "கேரட்", "sci": "Daucus carota", "cat": "Root Vegetable", "part": "peel", "ai": True, "ai_cls": "carrot_peel", "nut_st": "available", "safe_st": "safe_edible", "haz_en": "Low hazard; wash thoroughly to remove soil microbes and surface pesticide residues.", "haz_ta": "மண் துகள்கள் மற்றும் பூச்சிக்கொல்லி எச்சங்களை அகற்ற நன்கு கழுவ வேண்டும்."},
        {"slug": "potato", "name_en": "Potato", "name_ta": "உருளைக்கிழங்கு", "sci": "Solanum tuberosum", "cat": "Root Vegetable", "part": "peel", "ai": True, "ai_cls": "potato_peel", "nut_st": "available", "safe_st": "conditional_cooking_required", "haz_en": "CRITICAL: Solanine glycoalkaloids accumulate in green, sprouted, or damaged potato peels. Toxic if consumed; discard green peels.", "haz_ta": "முக்கிய எச்சரிக்கை: பச்சை நிறம் அல்லது முளைகட்டிய உருளைக்கிழங்கு தோலில் சோலானின் நச்சு காணப்படும். உண்ணக்கூடாது."},
        {"slug": "sweet-potato", "name_en": "Sweet potato", "name_ta": "சர்க்கரைவள்ளி கிழங்கு", "sci": "Ipomoea batatas", "cat": "Root Vegetable", "part": "peel", "ai": False, "ai_cls": None, "nut_st": "available", "safe_st": "conditional_cooking_required", "haz_en": "Safe when cooked; wash thoroughly; moldy sweet potato peels contain toxic ipomeamarone.", "haz_ta": "சமைத்து உண்ணலாம்; பூஞ்சை பிடித்த தோல்களை கண்டிப்பாக பயன்படுத்தக்கூடாது."},
        {"slug": "beetroot", "name_en": "Beetroot", "name_ta": "பீட்ரூட்", "sci": "Beta vulgaris", "cat": "Root Vegetable", "part": "peel", "ai": True, "ai_cls": "beetroot_peel", "nut_st": "available", "safe_st": "safe_edible", "haz_en": "Rich in betalains and nitrates; peel can harbor soil organisms; scrub thoroughly before culinary use.", "haz_ta": "மண் பாக்டீரியாக்களை அகற்ற நன்கு தேய்த்து கழுவ வேண்டும்."},
        {"slug": "radish", "name_en": "Radish", "name_ta": "முள்ளங்கி", "sci": "Raphanus sativus", "cat": "Root Vegetable", "part": "peel", "ai": False, "ai_cls": None, "nut_st": "available", "safe_st": "safe_edible", "haz_en": "Contains pungent glucosinolates; safe when washed; peppery flavor.", "haz_ta": "நன்கு கழுவி சமையலில் பயன்படுத்தலாம்; காரத்தன்மை கொண்டது."},
        {"slug": "turnip", "name_en": "Turnip", "name_ta": "நூல் கோல் / டர்னிப்", "sci": "Brassica rapa subsp. rapa", "cat": "Root Vegetable", "part": "peel", "ai": False, "ai_cls": None, "nut_st": "available", "safe_st": "conditional_cooking_required", "haz_en": "Fibrous outer rind; wash and boil or compost.", "haz_ta": "நார்ச்சத்து அதிகம்; வேகவைத்து பயன்படுத்தலாம் அல்லது உரமாக்கலாம்."},
        {"slug": "parsnip", "name_en": "Parsnip", "name_ta": "பார்ஸ்னிப்", "sci": "Pastinaca sativa", "cat": "Root Vegetable", "part": "peel", "ai": False, "ai_cls": None, "nut_st": "incomplete", "safe_st": "conditional_cooking_required", "haz_en": "Contains furanocoumarins which can cause mild photosensitivity; culinary cooking recommended.", "haz_ta": "சமைத்த பின் பயன்படுத்தவும்."},
        {"slug": "cassava-tapioca", "name_en": "Cassava / Tapioca", "name_ta": "மரவள்ளிக்கிழங்கு", "sci": "Manihot esculenta", "cat": "Root Vegetable", "part": "peel", "ai": False, "ai_cls": None, "nut_st": "available", "safe_st": "hazardous_raw", "haz_en": "HIGH DANGER: Cassava peel contains high concentrations of cyanogenic glucosides (linamarin). INEDIBLE raw or lightly cooked. Ideal for composting, biogas, or industrial bio-adsorption.", "haz_ta": "அபாய எச்சரிக்கை: மரவள்ளிக்கிழங்கு தோலில் சயனைடு நச்சுத்தன்மை (லினமரின்) உள்ளது. சாப்பிடக்கூடாது. உரமாக்க மட்டுமே சிறந்தது."},
        {"slug": "elephant-foot-yam", "name_en": "Elephant foot yam", "name_ta": "சேனைக்கிழங்கு", "sci": "Amorphophallus paeoniifolius", "cat": "Root Vegetable", "part": "peel", "ai": False, "ai_cls": None, "nut_st": "incomplete", "safe_st": "hazardous_raw", "haz_en": "Contains sharp needle-like calcium oxalate raphide crystals causing severe throat irritation and itching. Do not ingest raw; peel requires specialized boiling/acid treatment or composting.", "haz_ta": "அரிப்பு உண்டாக்கும் கால்சியம் ஆக்சலேட் படிகங்கள் நிறைந்தது. பச்சையாக சாப்பிடக்கூடாது."},
        {"slug": "greater-yam", "name_en": "Greater yam", "name_ta": "காச்சில் / பெரும் சேம்பு", "sci": "Dioscorea alata", "cat": "Root Vegetable", "part": "peel", "ai": False, "ai_cls": None, "nut_st": "incomplete", "safe_st": "conditional_cooking_required", "haz_en": "Contains mucilage and trace oxalates; remove peel before consumption or compost.", "haz_ta": "அரிப்பு தன்மை; உரமாக்க ஏற்றது."},
        {"slug": "taro-colocasia", "name_en": "Taro / Colocasia", "name_ta": "சேப்பங்கிழங்கு", "sci": "Colocasia esculenta", "cat": "Root Vegetable", "part": "peel", "ai": False, "ai_cls": None, "nut_st": "incomplete", "safe_st": "hazardous_raw", "haz_en": "Rich in calcium oxalate crystals. Causes severe skin itching and mucosal burning if not boiled with tamarind/acid. Peels best directed to composting.", "haz_ta": "கால்சியம் ஆக்சலேட் அரிப்பை ஏற்படுத்தும்; உரமாக்க சிறந்தது."},
        {"slug": "jerusalem-artichoke", "name_en": "Jerusalem artichoke", "name_ta": "ஜெருசலேம் கூனைப்பூ", "sci": "Helianthus tuberosus", "cat": "Root Vegetable", "part": "peel", "ai": False, "ai_cls": None, "nut_st": "incomplete", "safe_st": "safe_edible", "haz_en": "High in inulin dietary fibre; excessive intake can cause intestinal flatulence.", "haz_ta": "இன்யூலின் நார்ச்சத்து அதிகம்; மிதமாக உட்கொள்ளவும்."},

        # Group B — Gourds and Cucurbits (13-27)
        {"slug": "pumpkin", "name_en": "Pumpkin", "name_ta": "பூசணிக்காய்", "sci": "Cucurbita moschata", "cat": "Gourds & Cucurbits", "part": "rind", "ai": True, "ai_cls": "pumpkin_peel", "nut_st": "available", "safe_st": "safe_edible", "haz_en": "Extremely safe when cooked; discard if flesh/peel tastes unusually bitter (cucurbitacin toxicity).", "haz_ta": "சமைக்க மிகவும் பாதுகாப்பானது; கசப்பு சுவை இருந்தால் தவிர்க்கவும்."},
        {"slug": "bottle-gourd", "name_en": "Bottle gourd", "name_ta": "சுரைக்காய்", "sci": "Lagenaria siceraria", "cat": "Gourds & Cucurbits", "part": "peel", "ai": False, "ai_cls": None, "nut_st": "available", "safe_st": "safe_edible", "haz_en": "IMPORTANT: Discard if peel or juice tastes intensely bitter due to toxic cucurbitacins.", "haz_ta": "கசப்பு சுவை கொண்ட சுரைக்காயை ஒருபோதும் உட்கொள்ளக்கூடாது (குக்குர்பிடாசின் நச்சு)."},
        {"slug": "bitter-gourd", "name_en": "Bitter gourd", "name_ta": "பாகற்காய்", "sci": "Momordica charantia", "cat": "Gourds & Cucurbits", "part": "rind", "ai": False, "ai_cls": None, "nut_st": "available", "safe_st": "safe_edible", "haz_en": "Naturally bitter due to momordicins and charantin; hypoglycemic properties; wash thoroughly.", "haz_ta": "இயற்கையான கசப்பு கொண்டது; இரத்த சர்க்கரையை குறைக்கும் தன்மை கொண்டது."},
        {"slug": "ridge-gourd", "name_en": "Ridge gourd", "name_ta": "பீர்க்கங்காய்", "sci": "Luffa acutangula", "cat": "Gourds & Cucurbits", "part": "peel", "ai": False, "ai_cls": None, "nut_st": "available", "safe_st": "safe_edible", "haz_en": "Outer fibrous ridges can be cooked into traditional South Indian peel chutney (Thogayal); discard if bitter.", "haz_ta": "இதன் தோலில் சத்தான துவையல் செய்யலாம்; கசப்பு இருந்தால் தவிர்க்கவும்."},
        {"slug": "snake-gourd", "name_en": "Snake gourd", "name_ta": "புடலங்காய்", "sci": "Trichosanthes cucumerina", "cat": "Gourds & Cucurbits", "part": "skin", "ai": False, "ai_cls": None, "nut_st": "available", "safe_st": "safe_edible", "haz_en": "Gentle scraping recommended; discard if noticeably bitter.", "haz_ta": "லேசாக சுரண்டி கழுவி பயன்படுத்தலாம்."},
        {"slug": "ash-gourd", "name_en": "Ash gourd", "name_ta": "சாம்பல் பூசணி / வெண்பூசணி", "sci": "Benincasa hispida", "cat": "Gourds & Cucurbits", "part": "rind", "ai": False, "ai_cls": None, "nut_st": "available", "safe_st": "safe_edible", "haz_en": "White chalky wax on rind should be washed off before processing; great for composting and biogas.", "haz_ta": "வெளிப்புற வெள்ளை மெழுகு அடுக்கை கழுவி நீக்க வேண்டும்."},
        {"slug": "sponge-gourd", "name_en": "Sponge gourd", "name_ta": "நுரை பீர்க்கங்காய்", "sci": "Luffa aegyptiaca", "cat": "Gourds & Cucurbits", "part": "peel", "ai": False, "ai_cls": None, "nut_st": "incomplete", "safe_st": "safe_edible", "haz_en": "Mature skins become fibrous sponge (loofah); young peels edible if cooked.", "haz_ta": "முதிர்ந்த தோல் நார் பயன்பாட்டிற்கு ஏற்றது."},
        {"slug": "ivy-gourd", "name_en": "Ivy gourd", "name_ta": "கோவைக்காய்", "sci": "Coccinia grandis", "cat": "Gourds & Cucurbits", "part": "skin", "ai": False, "ai_cls": None, "nut_st": "incomplete", "safe_st": "safe_edible", "haz_en": "Entire skin typically consumed intact; wash thoroughly.", "haz_ta": "முழுமையாக சாப்பிடக்கூடியது; கழுவி பயன்படுத்தவும்."},
        {"slug": "pointed-gourd", "name_en": "Pointed gourd", "name_ta": "பர்வால்", "sci": "Trichosanthes dioica", "cat": "Gourds & Cucurbits", "part": "skin", "ai": False, "ai_cls": None, "nut_st": "incomplete", "safe_st": "safe_edible", "haz_en": "Lightly scraped; discard stem ends; pesticide wash advisable.", "haz_ta": "லேசாக சுரண்டி சமைக்கலாம்."},
        {"slug": "chayote", "name_en": "Chayote", "name_ta": "மேராக்காய்", "sci": "Sechium edule", "cat": "Gourds & Cucurbits", "part": "peel", "ai": False, "ai_cls": None, "nut_st": "incomplete", "safe_st": "safe_edible", "haz_en": "Peeling exudes a sticky latex that can temporarily numb fingers; harmless but wear gloves.", "haz_ta": "தோல் நீக்கும்போது ஒட்டும் பிசின் வரலாம்; கையுறை பயன்படுத்தலாம்."},
        {"slug": "cucumber", "name_en": "Cucumber", "name_ta": "வெள்ளரிக்காய்", "sci": "Cucumis sativus", "cat": "Gourds & Cucurbits", "part": "peel", "ai": True, "ai_cls": "cucumber_peel", "nut_st": "available", "safe_st": "safe_edible", "haz_en": "High moisture and silica; wash thoroughly to remove waxes applied for shipping.", "haz_ta": "மெழுகு பூச்சுகளை அகற்ற வெதுவெதுப்பான நீரில் கழுவ வேண்டும்."},
        {"slug": "zucchini", "name_en": "Zucchini", "name_ta": "சுக்கினி", "sci": "Cucurbita pepo", "cat": "Gourds & Cucurbits", "part": "skin", "ai": False, "ai_cls": None, "nut_st": "available", "safe_st": "safe_edible", "haz_en": "Tender skin with lutein; discard if taste is distinctly bitter.", "haz_ta": "மெல்லிய தோல்; சமைக்க சிறந்தது."},
        {"slug": "yellow-squash", "name_en": "Yellow squash", "name_ta": "மஞ்சள் ஸ்குவாஷ்", "sci": "Cucurbita pepo var. recticollis", "cat": "Gourds & Cucurbits", "part": "skin", "ai": False, "ai_cls": None, "nut_st": "incomplete", "safe_st": "safe_edible", "haz_en": "Edible skin; wash surface thoroughly.", "haz_ta": "சமையல் மற்றும் உரமாக்கலுக்கு ஏற்றது."},
        {"slug": "butternut-squash", "name_en": "Butternut squash", "name_ta": "பட்டர்நட் பூசணி", "sci": "Cucurbita moschata", "cat": "Gourds & Cucurbits", "part": "rind", "ai": False, "ai_cls": None, "nut_st": "incomplete", "safe_st": "conditional_cooking_required", "haz_en": "Tough rind; can be roasted or boiled into broth; compostable.", "haz_ta": "கடினமான தோல்; வேகவைத்து பயன்படுத்தலாம் அல்லது உரமாக்கலாம்."},
        {"slug": "chow-chow", "name_en": "Chow chow", "name_ta": "செள செள", "sci": "Sechium edule", "cat": "Gourds & Cucurbits", "part": "peel", "ai": False, "ai_cls": None, "nut_st": "incomplete", "safe_st": "safe_edible", "haz_en": "Peels can be seasoned into chutney or added to compost bins.", "haz_ta": "துவையல் செய்ய உகந்தது."},

        # Group C — Other Common Vegetables (28-39)
        {"slug": "brinjal-eggplant", "name_en": "Brinjal / Eggplant", "name_ta": "கத்தரிக்காய்", "sci": "Solanum melongena", "cat": "Common Vegetable", "part": "skin", "ai": False, "ai_cls": None, "nut_st": "available", "safe_st": "safe_edible", "haz_en": "Contains nasunin anthocyanin; solanine levels increase if overgrown or bitter.", "haz_ta": "நசுனின் நிறமி நிறைந்தது; முதிர்ந்த காய்களை தவிர்க்கவும்."},
        {"slug": "tomato", "name_en": "Tomato", "name_ta": "தக்காளி", "sci": "Solanum lycopersicum", "cat": "Common Vegetable", "part": "skin", "ai": False, "ai_cls": None, "nut_st": "available", "safe_st": "safe_edible", "haz_en": "Highest concentration of lycopene; skins are safe but tough for infants to digest.", "haz_ta": "லைகோபீன் சத்து மிகுந்தது; சமையலில் முழுமையாக பயன்படுத்தலாம்."},
        {"slug": "green-plantain", "name_en": "Green plantain / Raw banana", "name_ta": "வாழைக்காய்", "sci": "Musa paradisiaca", "cat": "Common Vegetable", "part": "peel", "ai": False, "ai_cls": None, "nut_st": "available", "safe_st": "conditional_cooking_required", "haz_en": "High tannins and resistant starch; excellent for South Indian Vazhaikkai Thol poriyal after boiling.", "haz_ta": "டான்னின் நிறைந்தது; வேகவைத்து பொரியல் செய்ய ஏற்றது."},
        {"slug": "raw-papaya", "name_en": "Raw papaya", "name_ta": "பப்பாளிக்காய்", "sci": "Carica papaya", "cat": "Common Vegetable", "part": "peel", "ai": False, "ai_cls": None, "nut_st": "incomplete", "safe_st": "conditional_cooking_required", "haz_en": "Latex contains proteolytic enzyme papain; pregnant women should avoid raw papaya peel.", "haz_ta": "பப்பாளி பிசினில் பப்பாயின் என்சைம் உள்ளதால் கர்ப்பிணிகள் தவிர்க்க வேண்டும்."},
        {"slug": "drumstick-pods", "name_en": "Drumstick pods / Moringa pods", "name_ta": "முருங்கைக்காய்", "sci": "Moringa oleifera", "cat": "Common Vegetable", "part": "pod_shell", "ai": False, "ai_cls": None, "nut_st": "incomplete", "safe_st": "inedible_valorize_only", "haz_en": "Tough, highly lignified fibrous outer shell. Inedible; prime candidate for composting and vermicomposting.", "haz_ta": "மிகவும் கடினமான நார்; சாப்பிட இயலாது; உரமாக்க மட்டுமே ஏற்றது."},
        {"slug": "broad-beans", "name_en": "Broad beans", "name_ta": "அவரைக்காய்", "sci": "Vicia faba", "cat": "Common Vegetable", "part": "pod_shell", "ai": False, "ai_cls": None, "nut_st": "incomplete", "safe_st": "safe_edible", "haz_en": "Individuals with G6PD deficiency must avoid faba beans due to favism risk.", "haz_ta": "G6PD குறைபாடு உள்ளவர்கள் அவரைக்காயை தவிர்க்க வேண்டும்."},
        {"slug": "peas", "name_en": "Peas", "name_ta": "பட்டாணி", "sci": "Pisum sativum", "cat": "Common Vegetable", "part": "pod_shell", "ai": False, "ai_cls": None, "nut_st": "available", "safe_st": "conditional_cooking_required", "haz_en": "Sweet pea empty pods can be boiled into purees or composted; remove fibrous inner membrane.", "haz_ta": "உள் நார் நீக்கி வேகவைத்து சூப் செய்யலாம் அல்லது உரமாக்கலாம்."},
        {"slug": "french-beans", "name_en": "French beans", "name_ta": "பீன்ஸ்", "sci": "Phaseolus vulgaris", "cat": "Common Vegetable", "part": "pod_shell", "ai": False, "ai_cls": None, "nut_st": "incomplete", "safe_st": "safe_edible", "haz_en": "Consume cooked; contains lectins (phytohaemagglutinin) that degrade upon heating.", "haz_ta": "லெக்டின்களை செயலிழக்கச் செய்ய சமைத்து உண்ண வேண்டும்."},
        {"slug": "cluster-beans", "name_en": "Cluster beans", "name_ta": "கொத்தவரங்காய்", "sci": "Cyamopsis tetragonoloba", "cat": "Common Vegetable", "part": "pod_shell", "ai": False, "ai_cls": None, "nut_st": "incomplete", "safe_st": "safe_edible", "haz_en": "Source of guar gum fibre; wash and cook thoroughly.", "haz_ta": "குவார் கம் நார்ச்சத்து நிறைந்தது; சமைத்து உண்ணவும்."},
        {"slug": "capsicum-bell-pepper", "name_en": "Capsicum / Bell pepper", "name_ta": "குடைமிளகாய்", "sci": "Capsicum annuum", "cat": "Common Vegetable", "part": "skin", "ai": False, "ai_cls": None, "nut_st": "available", "safe_st": "safe_edible", "haz_en": "Safe and rich in vitamin C; discard moldy stems.", "haz_ta": "வைட்டமின் சி நிறைந்தது; பாதுகாப்பானது."},
        {"slug": "green-chilli", "name_en": "Green chilli", "name_ta": "பச்சை மிளகாய்", "sci": "Capsicum frutescens", "cat": "Common Vegetable", "part": "skin", "ai": False, "ai_cls": None, "nut_st": "incomplete", "safe_st": "safe_edible", "haz_en": "Contains capsaicin; wear gloves when handling; avoid eye contact.", "haz_ta": "கேப்சைசின் எரிச்சலை உண்டாக்கும்; கவனமாக கையாளவும்."},
        {"slug": "okra-ladys-finger", "name_en": "Okra / Lady's finger", "name_ta": "வெண்டைக்காய்", "sci": "Abelmoschus esculentus", "cat": "Common Vegetable", "part": "pod_shell", "ai": False, "ai_cls": None, "nut_st": "available", "safe_st": "safe_edible", "haz_en": "Mucilaginous soluble fibre; discarded ends decompose rapidly in compost.", "haz_ta": "மக்கும் தன்மை மிக்கது; உரத்திற்கு சிறந்தது."},

        # Group D — Bulbs and Aromatics (40-44)
        {"slug": "onion", "name_en": "Onion", "name_ta": "வெங்காயம்", "sci": "Allium cepa", "cat": "Bulbs & Aromatics", "part": "peel", "ai": False, "ai_cls": None, "nut_st": "available", "safe_st": "inedible_valorize_only", "haz_en": "Dry papery skins are inedible but concentrated in quercetin bioflavonoids. Superb for natural dye extraction, broth infusion (strained), and composting.", "haz_ta": "உண்ண இயலாது; குவர்செடின் நிறமி மற்றும் இயற்கை சாயம் எடுக்க சிறந்தது."},
        {"slug": "garlic", "name_en": "Garlic", "name_ta": "பூண்டு", "sci": "Allium sativum", "cat": "Bulbs & Aromatics", "part": "peel", "ai": False, "ai_cls": None, "nut_st": "available", "safe_st": "inedible_valorize_only", "haz_en": "Papery skins are fibrous and indigestible; ideal for simmering stock, insect-repellent mulches, or composting.", "haz_ta": "பூச்சி விரட்டி மற்றும் இயற்கை உரத்திற்கு சிறந்தது."},
        {"slug": "shallots", "name_en": "Shallots", "name_ta": "சின்ன வெங்காயம்", "sci": "Allium cepa var. aggregatum", "cat": "Bulbs & Aromatics", "part": "peel", "ai": False, "ai_cls": None, "nut_st": "incomplete", "safe_st": "inedible_valorize_only", "haz_en": "High polyphenol skin; extract for eco-friendly textile dyeing or compost.", "haz_ta": "இயற்கை சாயத்திற்கு சிறந்தது."},
        {"slug": "ginger", "name_en": "Ginger", "name_ta": "இஞ்சி", "sci": "Zingiber officinale", "cat": "Bulbs & Aromatics", "part": "skin", "ai": False, "ai_cls": None, "nut_st": "available", "safe_st": "safe_edible", "haz_en": "Wash soil carefully; ginger peel can be infused into herbal tea or dried for spice blends.", "haz_ta": "மண்ணை நீக்க நன்கு கழுவ வேண்டும்; இஞ்சி டீ தயாரிக்கலாம்."},
        {"slug": "turmeric", "name_en": "Turmeric", "name_ta": "மஞ்சள்", "sci": "Curcuma longa", "cat": "Bulbs & Aromatics", "part": "skin", "ai": False, "ai_cls": None, "nut_st": "available", "safe_st": "safe_edible", "haz_en": "Contains curcumin; stains skin and clothing; excellent antimicrobial composting agent.", "haz_ta": "குர்குமின் நிறைந்தது; கிருமி நாசினி தன்மை கொண்டது."},

        # Group E — Other Edible Plant Outer Layers (45-50)
        {"slug": "cabbage-outer-leaves", "name_en": "Cabbage outer leaves", "name_ta": "முட்டைக்கோஸ் வெளிப்புற இலைகள்", "sci": "Brassica oleracea var. capitata", "cat": "Plant Outer Layer", "part": "outer_leaves", "ai": False, "ai_cls": None, "nut_st": "available", "safe_st": "conditional_cooking_required", "haz_en": "Highest pesticide exposure layer; wash rigorously in baking soda solution or salt water before cooking or composting.", "haz_ta": "பூச்சிக்கொல்லி எச்சங்கள் அதிகம் இருக்கும் என்பதால் உப்பு/பேக்கிங் சோடா நீரில் நன்கு கழுவ வேண்டும்."},
        {"slug": "cauliflower-outer-leaves", "name_en": "Cauliflower outer leaves", "name_ta": "காலிஃபிளவர் வெளிப்புற இலைகள்", "sci": "Brassica oleracea var. botrytis", "cat": "Plant Outer Layer", "part": "outer_leaves", "ai": False, "ai_cls": None, "nut_st": "available", "safe_st": "safe_edible", "haz_en": "Higher in iron and beta-carotene than the white florets. Highly nutritious in stir-fries after washing.", "haz_ta": "வெள்ளை பூவை விட இரும்புச்சத்து அதிகம்; சமைத்து உண்ண மிகவும் சிறந்தது."},
        {"slug": "broccoli-stalk-outer-layer", "name_en": "Broccoli stalk outer layer", "name_ta": "ப்ரோக்கோலி தண்டு வெளிப்புற அடுக்கு", "sci": "Brassica oleracea var. italica", "cat": "Plant Outer Layer", "part": "stem_layer", "ai": False, "ai_cls": None, "nut_st": "available", "safe_st": "safe_edible", "haz_en": "Fibrous outer peel; peel lightly, chop finely and cook into soups.", "haz_ta": "நார்ச்சத்து நிறைந்தது; சூப் செய்ய சிறந்தது."},
        {"slug": "banana-stem-outer-layers", "name_en": "Banana stem outer layers", "name_ta": "வாழைத்தண்டு வெளிப்புற அடுக்கு", "sci": "Musa acuminata", "cat": "Plant Outer Layer", "part": "stem_layer", "ai": False, "ai_cls": None, "nut_st": "incomplete", "safe_st": "inedible_valorize_only", "haz_en": "Tough, high-tensile lignocellulose fibres. Inedible; prime feedstock for handmade paper, textile yarn, and composting.", "haz_ta": "கடினமான இயற்கை நார்; காகிதம் மற்றும் கைவினை பொருட்கள் செய்ய ஏற்றது."},
        {"slug": "lotus-stem-outer-layer", "name_en": "Lotus stem outer layer", "name_ta": "தாமரை தண்டு வெளிப்புற அடுக்கு", "sci": "Nelumbo nucifera", "cat": "Plant Outer Layer", "part": "stem_layer", "ai": False, "ai_cls": None, "nut_st": "incomplete", "safe_st": "conditional_cooking_required", "haz_en": "Aquatic stem surface can harbor encysted parasites (Fasciolopsis buski); MUST NEVER be consumed raw. Cook thoroughly.", "haz_ta": "நீர் ஒட்டுண்ணிகள் இருக்க வாய்ப்புள்ளதால் பச்சையாக சாப்பிடக்கூடாது; வேகவைக்க வேண்டும்."},
        {"slug": "corn-husk", "name_en": "Corn husk", "name_ta": "மக்காச்சோள உமி / சோளத்தோல்", "sci": "Zea mays", "cat": "Plant Outer Layer", "part": "husk", "ai": False, "ai_cls": None, "nut_st": "incomplete", "safe_st": "inedible_valorize_only", "haz_en": "Inedible tough silica-rich sheath. Used traditionally as tamale steaming wrappers, biodegradable packaging, and compost mulch.", "haz_ta": "சாப்பிட இயலாது; உணவு வேகவைக்கும் உறை மற்றும் மக்கும் உரமாக பயன்படும்."},
    ]

    veg_objs = {}
    for v in veg_catalogue:
        veg = db.query(Vegetable).filter(Vegetable.slug == v["slug"]).first()
        if not veg:
            veg = Vegetable(
                slug=v["slug"],
                name_en=v["name_en"],
                name_ta=v["name_ta"],
                scientific_name=v["sci"],
                category=v["cat"],
                plant_part_id=part_objs[v["part"]].id,
                description_en=f"Discarded {v['part']} of {v['name_en']} ({v['sci']}).",
                description_ta=f"{v['name_ta']} காய்கறியின் {part_objs[v['part']].name_ta}.",
                is_ai_supported=v["ai"],
                ai_class_name=v["ai_cls"],
                is_manually_selectable=True,
                nutrient_data_status=v["nut_st"],
                food_safety_status=v["safe_st"],
                known_hazards_en=v["haz_en"],
                known_hazards_ta=v["haz_ta"],
                is_active=True,
            )
            db.add(veg)
            db.flush()
        veg_objs[v["slug"]] = veg

    # 8. Seed Validated Scientific Nutrient Profiles & Measurements for Peels
    # Carrot Peel (100g fresh basis)
    carrot = veg_objs["carrot"]
    carrot_prof = db.query(NutrientProfile).filter(NutrientProfile.vegetable_id == carrot.id).first()
    if not carrot_prof:
        carrot_prof = NutrientProfile(
            vegetable_id=carrot.id,
            plant_part_id=part_objs["peel"].id,
            source_id=source_objs[2].id,
            fresh_or_dry_basis="fresh_weight",
            sample_prep_method="Mechanically peeled, washed with distilled water",
            data_quality_status="validated_peel_measurement",
            uncertainty_notes="Values represent mean concentrations in fresh edible peel tissues.",
        )
        db.add(carrot_prof)
        db.flush()

        carrot_measurements = [
            (nutrient_objs["vit_a"].id, 835.0, "mcg"),
            (nutrient_objs["vit_c"].id, 5.9, "mg"),
            (nutrient_objs["calcium"].id, 33.0, "mg"),
            (nutrient_objs["potassium"].id, 320.0, "mg"),
            (nutrient_objs["dietary_fibre"].id, 2.8, "g"),
            (nutrient_objs["total_phenolics"].id, 142.5, "mg GAE"),
        ]
        for nid, val, unit in carrot_measurements:
            db.add(NutrientMeasurement(profile_id=carrot_prof.id, nutrient_id=nid, concentration_per_100g=val, unit=unit))

    # Potato Peel (100g fresh basis)
    potato = veg_objs["potato"]
    potato_prof = db.query(NutrientProfile).filter(NutrientProfile.vegetable_id == potato.id).first()
    if not potato_prof:
        potato_prof = NutrientProfile(
            vegetable_id=potato.id,
            plant_part_id=part_objs["peel"].id,
            source_id=source_objs[2].id,
            fresh_or_dry_basis="fresh_weight",
            sample_prep_method="Non-green tubers, peeled with standard peeler",
            data_quality_status="validated_peel_measurement",
            uncertainty_notes="Valid ONLY for non-green, non-sprouted tubers.",
        )
        db.add(potato_prof)
        db.flush()

        potato_measurements = [
            (nutrient_objs["vit_c"].id, 11.4, "mg"),
            (nutrient_objs["potassium"].id, 413.0, "mg"),
            (nutrient_objs["iron"].id, 1.8, "mg"),
            (nutrient_objs["dietary_fibre"].id, 3.2, "g"),
            (nutrient_objs["total_phenolics"].id, 115.0, "mg GAE"),
        ]
        for nid, val, unit in potato_measurements:
            db.add(NutrientMeasurement(profile_id=potato_prof.id, nutrient_id=nid, concentration_per_100g=val, unit=unit))

    # Beetroot Peel (100g fresh basis)
    beetroot = veg_objs["beetroot"]
    beetroot_prof = db.query(NutrientProfile).filter(NutrientProfile.vegetable_id == beetroot.id).first()
    if not beetroot_prof:
        beetroot_prof = NutrientProfile(
            vegetable_id=beetroot.id,
            plant_part_id=part_objs["peel"].id,
            source_id=source_objs[2].id,
            fresh_or_dry_basis="fresh_weight",
            sample_prep_method="Scrubbed and peeled fresh beetroot",
            data_quality_status="validated_peel_measurement",
            uncertainty_notes="Betalain content degrades rapidly above 60°C.",
        )
        db.add(beetroot_prof)
        db.flush()

        beetroot_measurements = [
            (nutrient_objs["vit_c"].id, 4.9, "mg"),
            (nutrient_objs["potassium"].id, 336.0, "mg"),
            (nutrient_objs["iron"].id, 0.8, "mg"),
            (nutrient_objs["dietary_fibre"].id, 2.9, "g"),
            (nutrient_objs["betalains"].id, 168.0, "mg"),
            (nutrient_objs["total_phenolics"].id, 195.0, "mg GAE"),
        ]
        for nid, val, unit in beetroot_measurements:
            db.add(NutrientMeasurement(profile_id=beetroot_prof.id, nutrient_id=nid, concentration_per_100g=val, unit=unit))

    # Cucumber Peel (100g fresh basis)
    cucumber = veg_objs["cucumber"]
    cuke_prof = db.query(NutrientProfile).filter(NutrientProfile.vegetable_id == cucumber.id).first()
    if not cuke_prof:
        cuke_prof = NutrientProfile(
            vegetable_id=cucumber.id,
            plant_part_id=part_objs["peel"].id,
            source_id=source_objs[1].id,
            fresh_or_dry_basis="fresh_weight",
            sample_prep_method="Peeled outer 1mm skin",
            data_quality_status="validated_peel_measurement",
            uncertainty_notes="Contains significant silica and vitamin K in outer green epidermis.",
        )
        db.add(cuke_prof)
        db.flush()

        cuke_measurements = [
            (nutrient_objs["vit_k"].id, 16.4, "mcg"),
            (nutrient_objs["vit_a"].id, 105.0, "mcg"),
            (nutrient_objs["potassium"].id, 147.0, "mg"),
            (nutrient_objs["dietary_fibre"].id, 1.5, "g"),
        ]
        for nid, val, unit in cuke_measurements:
            db.add(NutrientMeasurement(profile_id=cuke_prof.id, nutrient_id=nid, concentration_per_100g=val, unit=unit))

    # Pumpkin Peel / Rind (100g fresh basis)
    pumpkin = veg_objs["pumpkin"]
    pumpkin_prof = db.query(NutrientProfile).filter(NutrientProfile.vegetable_id == pumpkin.id).first()
    if not pumpkin_prof:
        pumpkin_prof = NutrientProfile(
            vegetable_id=pumpkin.id,
            plant_part_id=part_objs["rind"].id,
            source_id=source_objs[2].id,
            fresh_or_dry_basis="fresh_weight",
            sample_prep_method="Separated outer rind",
            data_quality_status="validated_peel_measurement",
            uncertainty_notes="Rind carotenoid concentrations are twice as concentrated as inner flesh.",
        )
        db.add(pumpkin_prof)
        db.flush()

        pumpkin_measurements = [
            (nutrient_objs["vit_a"].id, 650.0, "mcg"),
            (nutrient_objs["vit_c"].id, 9.0, "mg"),
            (nutrient_objs["potassium"].id, 340.0, "mg"),
            (nutrient_objs["dietary_fibre"].id, 3.8, "g"),
            (nutrient_objs["total_phenolics"].id, 120.0, "mg GAE"),
        ]
        for nid, val, unit in pumpkin_measurements:
            db.add(NutrientMeasurement(profile_id=pumpkin_prof.id, nutrient_id=nid, concentration_per_100g=val, unit=unit))

    # 9. Safety Rules Engine Baseline
    safety_data = [
        {
            "code": "SR_POTATO_SOLANINE",
            "veg": "potato",
            "hazard_type": "glycoalkaloid",
            "severity": "critical",
            "desc_en": "Exposure to light or sprouting triggers chlorophyll and toxic solanine/chaconine synthesis in potato peels. Green peels MUST NEVER be eaten. Discard immediately.",
            "desc_ta": "பச்சை நிறம் அல்லது முளைகட்டிய உருளைக்கிழங்கு தோல்களில் சோலானின் நச்சு உருவாகும். ஒருபோதும் உண்ணக்கூடாது.",
            "alt_en": "Divert entirely to aerobic composting away from edible crop beds.",
            "alt_ta": "உரமாக்கலுக்கு மட்டும் பயன்படுத்தவும்.",
        },
        {
            "code": "SR_CASSAVA_CYANIDE",
            "veg": "cassava-tapioca",
            "hazard_type": "cyanogenic_glucoside",
            "severity": "critical",
            "desc_en": "Cassava peels contain dangerous levels of linamarin, producing hydrogen cyanide upon enzymatic hydrolysis. STRICTLY PROHIBITED for culinary broth, human consumption, or raw animal feed.",
            "desc_ta": "மரவள்ளிக்கிழங்கு தோலில் உயிருக்கு ஆபத்தான சயனைடு நச்சு உள்ளது. சமையல் அல்லது விலங்கு தீவனத்திற்கு கண்டிப்பாக பயன்படுத்தக்கூடாது.",
            "alt_en": "Divert to municipal composting, biogas anaerobic digestion, or industrial bio-char production.",
            "alt_ta": "உயிர்வாயு உற்பத்தி அல்லது உரமாக்கலுக்கு பயன்படுத்தவும்.",
        },
        {
            "code": "SR_TARO_OXALATE",
            "veg": "taro-colocasia",
            "hazard_type": "oxalate_raphide",
            "severity": "warning",
            "desc_en": "Microscopic calcium oxalate raphide needles cause painful oral swelling and severe dermal itch. Requires prolonged boiling with tamarind or acidic medium if handled.",
            "desc_ta": "கால்சியம் ஆக்சலேட் ஊசி போன்ற படிகங்கள் அரிப்பை உண்டாக்கும்.",
            "alt_en": "Composting with organic matter to break down oxalates naturally.",
            "alt_ta": "இயற்கை உரமாக்கல் முறைக்கு மாற்றவும்.",
        },
        {
            "code": "SR_GOURD_CUCURBITACIN",
            "veg": "bottle-gourd",
            "hazard_type": "cucurbitacin",
            "severity": "critical",
            "desc_en": "Abnormally bitter cucurbits synthesize toxic cucurbitacins B and D, which induce severe gastrointestinal ulceration and toxicity. Taste check before preparing.",
            "desc_ta": "கசப்பு சுவை கொண்ட சுரைக்காய் குக்குர்பிடாசின் நச்சுத்தன்மை கொண்டது. உட்கொள்ளக்கூடாது.",
            "alt_en": "Immediately discard into composting bin.",
            "alt_ta": "உடனடியாக உரத்தில் இடவும்.",
        },
    ]

    for sd in safety_data:
        rule = db.query(SafetyRule).filter(SafetyRule.code == sd["code"]).first()
        if not rule and sd["veg"] in veg_objs:
            rule = SafetyRule(
                code=sd["code"],
                vegetable_id=veg_objs[sd["veg"]].id,
                hazard_type=sd["hazard_type"],
                severity=sd["severity"],
                rule_description_en=sd["desc_en"],
                rule_description_ta=sd["desc_ta"],
                conservative_alternative_en=sd["alt_en"],
                conservative_alternative_ta=sd["alt_ta"],
                scientific_reference_id=source_objs[2].id,
            )
            db.add(rule)

    # 10. AI Model Version Baseline
    ai_v1 = db.query(AIModelVersion).filter(AIModelVersion.version_tag == "v1.0.0-mobilenetv3").first()
    if not ai_v1:
        ai_v1 = AIModelVersion(
            version_tag="v1.0.0-mobilenetv3",
            model_architecture="MobileNetV3Large",
            weights_file_path="ai/models/smart_peel_mobilenetv3.keras",
            input_shape="224,224,3",
            class_labels={
                "0": "carrot_peel",
                "1": "potato_peel",
                "2": "beetroot_peel",
                "3": "cucumber_peel",
                "4": "pumpkin_peel",
            },
            accuracy=0.92,
            macro_f1=0.91,
            status="active",
        )
        db.add(ai_v1)

    # 11. Initial Translations for UI and Error Keys
    core_translations = [
        {"key": "app_title", "en": "Smart Peel AI", "ta": "ஸ்மார்ட் பீல் ஏஐ", "ctx": "ui"},
        {"key": "scan_peel", "en": "Scan Vegetable Peel", "ta": "காய்கறி தோலை ஸ்கேன் செய்க", "ctx": "ui"},
        {"key": "upload_image", "en": "Upload Image", "ta": "புகைப்படத்தை பதிவேற்றுக", "ctx": "ui"},
        {"key": "capture_camera", "en": "Take Photo", "ta": "புகைப்படம் எடுக்கவும்", "ctx": "ui"},
        {"key": "nutrient_profile", "en": "Nutrient Profile", "ta": "ஊட்டச்சத்து விவரம்", "ctx": "nutrient"},
        {"key": "safety_notice", "en": "Food Safety Evaluation", "ta": "உணவு பாதுகாப்பு மதிப்பீடு", "ctx": "safety"},
        {"key": "reuse_methods", "en": "Valorization & Reuse", "ta": "மறுபயன்பாடு மற்றும் பயன்பாட்டு முறைகள்", "ctx": "reuse"},
        {"key": "unsupported_image", "en": "Unsupported or uncertain image. Please confirm manually.", "ta": "ஆதரிக்கப்படாத படம் அல்லது நிச்சயமற்ற முடிவு. தயவுசெய்து கையேடாக தேர்வு செய்யவும்.", "ctx": "error"},
    ]
    for t in core_translations:
        tr_en = db.query(Translation).filter(Translation.translation_key == t["key"], Translation.language_code == "en").first()
        if not tr_en:
            db.add(Translation(translation_key=t["key"], language_code="en", translated_text=t["en"], context=t["ctx"]))
        tr_ta = db.query(Translation).filter(Translation.translation_key == t["key"], Translation.language_code == "ta").first()
        if not tr_ta:
            db.add(Translation(translation_key=t["key"], language_code="ta", translated_text=t["ta"], context=t["ctx"]))

    db.commit()
    logger.info("Database successfully seeded with 50 vegetables, 29 nutrients, plant parts, safety rules, and AI model baseline!")

    # Ingest Phase 5 and Phase 6 data
    try:
        from app.db.seed_phase5_nutrients import seed_phase5_nutrient_datasets
        seed_phase5_nutrient_datasets(db)
    except Exception as e:
        logger.warning(f"Phase 5 seeding note: {e}")

    try:
        from app.db.seed_phase6_estimation import seed_phase6_peel_yield_and_dri
        seed_phase6_peel_yield_and_dri(db)
    except Exception as e:
        logger.warning(f"Phase 6 seeding note: {e}")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()
