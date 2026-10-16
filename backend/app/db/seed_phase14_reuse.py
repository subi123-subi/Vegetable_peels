"""
Phase 14 — Vegetable Waste Utilization Engine Database Seeder
Seeds evidence-based valorization recommendations for vegetable peels and residues.
"""
import sys
from pathlib import Path

# Add backend directory to path
BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BACKEND_DIR))

import app.models
from app.db.session import SessionLocal
from app.models.reuse import ReuseMethod, ReuseRecommendation
from app.models.vegetable import Vegetable, PlantPart
from app.models.nutrient import ScientificSource


def seed_reuse_recommendations():
    db = SessionLocal()
    try:
        # Check if recommendations already seeded
        existing_count = db.query(ReuseRecommendation).count()
        if existing_count > 0:
            print(f"Reuse recommendations already seeded ({existing_count} records). Skipping.")
            return

        print("Seeding Phase 14 Vegetable Waste Utilization Recommendations...")

        # 1. Fetch lookup maps
        methods = {m.code: m for m in db.query(ReuseMethod).all()}
        sources = {s.source_type: s for s in db.query(ScientificSource).all()}
        default_source = db.query(ScientificSource).first()

        peel_part = db.query(PlantPart).filter(PlantPart.code == "peel").first()
        if not peel_part:
            peel_part = db.query(PlantPart).first()

        vegs = db.query(Vegetable).all()

        # Detailed custom profiles for key vegetables
        custom_profiles = {
            "carrot": [
                {
                    "method": "culinary_stock",
                    "rank": 1,
                    "en": "Simmer washed carrot peels with celery and aromatics for 45 mins to produce a carotenoid-enriched golden culinary stock.",
                    "ta": "கழுவிய கேரட் தோல்களை 45 நிமிடங்கள் கொதிக்க வைத்து வைட்டமின் நிறைந்த காய்கறி சூப்/ஸ்டாக் தயாரிக்கலாம்.",
                    "warn_en": "Ensure abrasive washing to remove clinging soil particles.",
                    "warn_ta": "மண் துகள்களை நீக்க நன்கு கழுவ வேண்டும்.",
                },
                {
                    "method": "natural_pigment",
                    "rank": 1,
                    "en": "Solar dry and grind into fine orange beta-carotene powder for clean-label food coloring and baking.",
                    "ta": "வெயிலில் உலர்த்தி அரைத்து இயற்கை ஆரஞ்சு நிறமூட்டியாக பேக்கிங் மற்றும் உணவுகளில் பயன்படுத்தலாம்.",
                    "warn_en": "Avoid high direct ultraviolet overexposure which degrades carotenoid stability.",
                    "warn_ta": "அதிக வெப்பத்தில் நிறம் மங்கக்கூடும்.",
                },
                {
                    "method": "aerobic_composting",
                    "rank": 2,
                    "en": "Layer high-moisture carrot peels (C:N ~18:1) with dry brown leaves (carbon source) to maintain ideal 30:1 composting balance.",
                    "ta": "கேரட் தோல்களை காய்ந்த இலைகளுடன் கலந்து சிறந்த இயற்கை உரமாக மாற்றலாம்.",
                    "warn_en": "Chop finely to accelerate thermophilic microbial breakdown.",
                    "warn_ta": "சிறியதாக நறுக்கினால் விரைவாக மட்கும்.",
                },
                {
                    "method": "biogas_anaerobic",
                    "rank": 2,
                    "en": "High carbohydrate content produces biomethane yield of 380-420 mL CH4/g volatile solids in anaerobic digesters.",
                    "ta": "உயிர்வாயு கலனில் செலுத்தி ஒரு கிலோவுக்கு 400 மி.லி மீத்தேன் எரிபொருள் பெறலாம்.",
                    "warn_en": "Mix with buffering manure to prevent digester acidification.",
                    "warn_ta": "அமிலத்தன்மையை சமன் செய்ய சாணத்துடன் கலக்கவும்.",
                },
            ],
            "potato": [
                {
                    "method": "culinary_crisps",
                    "rank": 1,
                    "en": "Toss clean, NON-GREEN potato peel ribbons with olive oil and spices, bake at 200°C for 15 mins for dietary fiber crisps.",
                    "ta": "பச்சை நிறமில்லாத உருளைக்கிழங்கு தோலை எண்ணெய் மற்றும் மசாலா சேர்த்து வறுத்து சுவையான சிப்ஸ் செய்யலாம்.",
                    "warn_en": "CRITICAL: Never consume green or sprouted peels due to toxic solanine glycoalkaloids.",
                    "warn_ta": "முக்கியம்: சோலனைன் நச்சு உள்ளதால் பச்சை நிற தோல்களை சமைக்கக்கூடாது.",
                },
                {
                    "method": "bio_materials",
                    "rank": 2,
                    "en": "Extract residual starch and cellulose fibers for biodegradable packaging and bioplastic prototyping.",
                    "ta": "தோலில் உள்ள மாவுச்சத்து மற்றும் நார்ச்சத்தை மக்கும் பிளாஸ்டிக் மாற்றாகப் பயன்படுத்தலாம்.",
                    "warn_en": "Requires drying and mechanical milling.",
                    "warn_ta": "உலர்த்தி அரைப்பது அவசியம்.",
                },
                {
                    "method": "vermicomposting",
                    "rank": 2,
                    "en": "Pre-compost for 7 days before introducing to earthworm beds to prevent excessive heat and anaerobic fermentation.",
                    "ta": "மண்புழு படுக்கையில் இடுவதற்கு முன் 7 நாட்கள் முன்கூட்டியே மட்க வைக்க வேண்டும்.",
                    "warn_en": "Earthworms avoid raw solanine concentrations; partial breakdown mandatory.",
                    "warn_ta": "பச்சை உருளைத்தோல் மண்புழுக்களுக்கு உகந்ததல்ல.",
                },
            ],
            "beetroot": [
                {
                    "method": "natural_pigment",
                    "rank": 1,
                    "en": "Aqueous extraction of betanin pigment at 40°C with 0.1% citric acid yields vibrant red-purple eco-friendly dye and food tint.",
                    "ta": "40°C வெதுவெதுப்பான நீரில் எலுமிச்சை சாறு சேர்த்து இயற்கை அடர் சிவப்பு நிறமியை பிரித்தெடுக்கலாம்.",
                    "warn_en": "Heat sensitive; temperatures above 60°C degrade betalain chromophores.",
                    "warn_ta": "60°Cக்கு மேல் சூடாக்கினால் நிறம் மங்கும்.",
                },
                {
                    "method": "culinary_stock",
                    "rank": 2,
                    "en": "Grate peels into traditional South Indian Poriyal or sauté with lentils (Thuvaiyal) for concentrated antioxidant intake.",
                    "ta": "தோலை துருவி துவையல் அல்லது பொரியல் செய்து உண்ணலாம்; அதிக ஆக்ஸிஜனேற்ற தடுப்பான் நிறைந்தது.",
                    "warn_en": "Wash thoroughly to eliminate geosmin earthy aroma.",
                    "warn_ta": "மண் வாசனை போக நன்கு கழுவவும்.",
                },
                {
                    "method": "aerobic_composting",
                    "rank": 2,
                    "en": "Rich in potassium (K) and boron trace minerals; enhances compost nutrient profile for flowering crops.",
                    "ta": "பொட்டாசியம் மற்றும் போரான் சத்துக்கள் நிறைந்த உரமாக மாறும்.",
                    "warn_en": "Balances acidic sandy soils.",
                    "warn_ta": "அமில மண்ணிற்கு ஏற்றது.",
                },
            ],
            "cucumber": [
                {
                    "method": "culinary_stock",
                    "rank": 1,
                    "en": "Blend fresh peels with mint, lime, and cold water for a hydrating, silica-rich digestive cooler.",
                    "ta": "புதினா, எலுமிச்சையுடன் சேர்த்து அரைத்து குளிர்ச்சியான மூலிகை பானம் தயாரிக்கலாம்.",
                    "warn_en": "Discard immediately if noticeable cucurbitacin bitterness is detected.",
                    "warn_ta": "கசப்பு தன்மை இருந்தால் பயன்படுத்தக்கூடாது.",
                },
                {
                    "method": "vermicomposting",
                    "rank": 1,
                    "en": "High moisture content (94%) provides optimal hydration for earthworm composting bins.",
                    "ta": "அதிக ஈரப்பதம் (94%) கொண்டதால் மண்புழு படுக்கைக்கு சிறந்த ஈரப்பதம் அளிக்கிறது.",
                    "warn_en": "Balance with dry cardboard shreds to prevent waterlogging.",
                    "warn_ta": "அதிக ஈரம் தேங்காமல் காய்ந்த காகிதம் சேர்க்கவும்.",
                },
            ],
            "pumpkin": [
                {
                    "method": "culinary_stock",
                    "rank": 1,
                    "en": "Boil firm pumpkin rinds with coconut, cumin, and shallots for nutrient-dense South Indian Kootu or spicy stir-fry.",
                    "ta": "பூசணி தோலை தேங்காய், சீரகத்துடன் சேர்த்து சுவையான கூட்டு அல்லது பொரியல் செய்யலாம்.",
                    "warn_en": "Thorough cooking required to soften tough outer lignified epidermis.",
                    "warn_ta": "நன்கு வேகவைக்க வேண்டும்.",
                },
                {
                    "method": "biogas_anaerobic",
                    "rank": 2,
                    "en": "Excellent biomethane substrate with rapid anaerobic digestibility and minimal volatile acid inhibition.",
                    "ta": "உயிர்வாயு உற்பத்திக்கு மிகச் சிறந்த மூலப்பொருள்.",
                    "warn_en": "Mince into 5mm chips for optimal enzymatic access.",
                    "warn_ta": "பொடியாக நறுக்கி இடவும்.",
                },
                {
                    "method": "aerobic_composting",
                    "rank": 2,
                    "en": "Decomposes rapidly, releasing potassium, calcium, and phosphorus into organic gardening compost.",
                    "ta": "மண்ணிற்குத் தேவையான பொட்டாசியம், கால்சியம் சத்துக்களை வேகமாக அளிக்கிறது.",
                    "warn_en": "High water content; turn pile regularly to aerate.",
                    "warn_ta": "காற்று புக வாரம் ஒருமுறை கிளற வேண்டும்.",
                },
            ],
            "cassava": [
                {
                    "method": "biogas_anaerobic",
                    "rank": 1,
                    "en": "Cassava peels have high starch content suited for anaerobic industrial bio-methanation and energy recovery.",
                    "ta": "மரவள்ளிக்கிழங்கு தோலை தொழிற்துறை உயிர்வாயு மின்சார உற்பத்திக்கு பயன்படுத்தலாம்.",
                    "warn_en": "Strictly INEDIBLE for culinary use due to cyanogenic glucosides.",
                    "warn_ta": "சயனைடு நச்சு உள்ளதால் உணவாக உட்கொள்ளக்கூடாது.",
                },
                {
                    "method": "aerobic_composting",
                    "rank": 2,
                    "en": "Extended thermophilic composting (60°C for 21 days) completely degrades cyanogenic glucosides into harmless nitrogen.",
                    "ta": "21 நாட்கள் சூடான உரத்தில் இடும்போது சயனைடு நச்சு முற்றிலும் அழிந்து சிறந்த உரமாகிறது.",
                    "warn_en": "Keep away from domestic pets and livestock during early decomposition.",
                    "warn_ta": "ஆரம்ப கட்டத்தில் ஆடு, மாடுகள் உண்பதை தடுக்கவும்.",
                },
            ],
        }

        created_count = 0

        for veg in vegs:
            part_id = veg.plant_part_id or peel_part.id

            # If specific custom recommendations defined
            if veg.slug in custom_profiles:
                for item in custom_profiles[veg.slug]:
                    m = methods.get(item["method"])
                    if not m:
                        continue
                    rec = ReuseRecommendation(
                        vegetable_id=veg.id,
                        plant_part_id=part_id,
                        reuse_method_id=m.id,
                        evidence_rank=item["rank"],
                        preparation_instructions_en=item["en"],
                        preparation_instructions_ta=item["ta"],
                        limitations_and_warnings_en=item.get("warn_en"),
                        limitations_and_warnings_ta=item.get("warn_ta"),
                        reference_id=default_source.id if default_source else None,
                    )
                    db.add(rec)
                    created_count += 1
            else:
                # Default scientifically responsible recommendations based on safety status
                is_food_safe = veg.food_safety_status in ["safe_edible", "conditional_cooking_required"]

                # 1. Culinary recommendation if food safe
                if is_food_safe:
                    stock_m = methods.get("culinary_stock")
                    if stock_m:
                        db.add(
                            ReuseRecommendation(
                                vegetable_id=veg.id,
                                plant_part_id=part_id,
                                reuse_method_id=stock_m.id,
                                evidence_rank=2,
                                preparation_instructions_en=f"Wash {veg.name_en} peels thoroughly. Simmer with pepper and aromatics for an immune-supportive herbal broth.",
                                preparation_instructions_ta=f"{veg.name_ta} தோல்களை நன்கு கழுவி, மிளகு சேர்த்து ஊட்டச்சத்து மிக்க ரசம் அல்லது சூப் செய்யலாம்.",
                                limitations_and_warnings_en="Ensure clean produce without pesticide residues.",
                                limitations_and_warnings_ta="பூச்சிக்கொல்லி இல்லாத சுத்தமான காய்கறி தோலை மட்டுமே பயன்படுத்தவும்.",
                                reference_id=default_source.id if default_source else None,
                            )
                        )
                        created_count += 1

                # 2. Aerobic Composting for all
                comp_m = methods.get("aerobic_composting")
                if comp_m:
                    db.add(
                        ReuseRecommendation(
                            vegetable_id=veg.id,
                            plant_part_id=part_id,
                            reuse_method_id=comp_m.id,
                            evidence_rank=1,
                            preparation_instructions_en=f"Mix {veg.name_en} scraps with dry garden leaves in a 2:1 ratio for balanced domestic aerobic compost.",
                            preparation_instructions_ta=f"{veg.name_ta} கழிவுகளை காய்ந்த இலைகளுடன் 2:1 விகிதத்தில் கலந்து வீட்டு உரமாக்கலில் பயன்படுத்தவும்.",
                            limitations_and_warnings_en="Aerate the compost heap weekly.",
                            limitations_and_warnings_ta="வாரம் ஒருமுறை உரம் கலவையை கிளறி விடவும்.",
                            reference_id=default_source.id if default_source else None,
                        )
                    )
                    created_count += 1

                # 3. Vermicomposting
                vermi_m = methods.get("vermicomposting")
                if vermi_m:
                    db.add(
                        ReuseRecommendation(
                            vegetable_id=veg.id,
                            plant_part_id=part_id,
                            reuse_method_id=vermi_m.id,
                            evidence_rank=2,
                            preparation_instructions_en=f"Chop {veg.name_en} residue into small pieces and add to earthworm bin as green nitrogenous bedding feed.",
                            preparation_instructions_ta=f"{veg.name_ta} கழிவுகளை சிறிதாக நறுக்கி மண்புழு படுக்கையில் இயற்கை உணவாக சேர்க்கவும்.",
                            limitations_and_warnings_en="Avoid overfeeding to prevent bin souring.",
                            limitations_and_warnings_ta="அளவுக்கு அதிகமாக இடுவதைத் தவிர்க்கவும்.",
                            reference_id=default_source.id if default_source else None,
                        )
                    )
                    created_count += 1

        db.commit()
        print(f"Successfully seeded {created_count} Phase 14 Reuse Recommendations across {len(vegs)} vegetables!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding reuse recommendations: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_reuse_recommendations()
