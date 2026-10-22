"""
Master Knowledge Base & Recommendation Data for Meaningful Products Made From Vegetable Waste.
Covers Eco-Home & Bio-Enzymes, Organic Gardening, Artisanal Crafts, Natural Skincare,
Artisanal Culinary Upcycling, and Bio-Materials.
"""
from typing import List, Dict, Any, Optional

WASTE_CREATIONS: List[Dict[str, Any]] = [
    {
        "id": "bio_enzyme_cleaner",
        "title_en": "Citrus & Mixed Peel Bio-Enzyme Multi-Purpose Cleaner",
        "title_ta": "சிட்ரஸ் & காய்கறி தோல் பயோ-என்சைம் பல்நோக்கு கிளீனர்",
        "category": "eco_home",
        "category_name_en": "Eco-Home & Natural Cleaning",
        "category_name_ta": "வீட்டுப் பராமரிப்பு & இயற்கை கிளீனர்",
        "suitable_peels": ["orange", "lemon", "lime", "cucumber", "carrot", "apple", "mixed", "all_vegetables"],
        "difficulty": "Ferment",
        "prep_time_minutes": 15,
        "total_time": "30-90 Days Fermentation",
        "estimated_output": "1 Litre Concentrated Eco-Cleaner",
        "icon_name": "cleaning_services_rounded",
        "impact_summary_en": "Replaces 3 commercial chemical cleaner bottles, saves plastic packaging, and eliminates synthetic VOCs in home greywater.",
        "impact_summary_ta": "3 பிளாஸ்டிக் பாட்டில்கள் மற்றும் ரசாயன கிளீனர்களை தவிர்க்கிறது; 100% மக்கும் இயற்கை கழிவுநீர்.",
        "required_materials_en": [
            "300g Fresh citrus and vegetable peel scraps (clean and pesticide-washed)",
            "100g Natural unrefined jaggery or brown sugar (carbon fuel)",
            "1000ml (1 Litre) Clean chlorine-free water",
            "1 Clean 2-Litre plastic screw-top bottle (leaves 25% gas headspace)",
            "1 Pinch active dry baker's yeast (optional, accelerates fermentation from 90 to 30 days)"
        ],
        "required_materials_ta": [
            "300 கிராம் எலுமிச்சை, ஆரஞ்சு அல்லது காய்கறி தோல்கள்",
            "100 கிராம் நாட்டுச்சர்க்கரை அல்லது வெல்லம்",
            "1 லிட்டர் சுத்தமான தண்ணீர்",
            "1 இரண்டு லிட்டர் பிளாஸ்டிக் பாட்டில் (வாயு சேர இடம் தேவை)",
            "1 சிட்டிகை ஈஸ்ட் (விரைவாக 30 நாளில் நொதிக்க வைக்க உதவும்)"
        ],
        "step_by_step_instructions_en": [
            "1. Chop clean peels into 1-2 cm pieces to maximize microbial surface area.",
            "2. Dissolve 100g jaggery or brown sugar completely in 1 litre of room temperature water.",
            "3. Place peel scraps into the plastic bottle and pour the sweetened water over them, ensuring at least 20-25% empty headspace at the top.",
            "4. Add a pinch of yeast if available to accelerate microbial establishment. Cap tightly and shake once.",
            "5. Store in a dark, warm, well-ventilated cabinet away from direct sunlight.",
            "6. CRITICAL SAFETY STEP: Unscrew cap slightly once daily for the first 30 days to vent accumulated carbon dioxide (CO2) gas, then reseal immediately.",
            "7. Strain the golden-brown fermented enzyme after 90 days (or 30 days with yeast). Dilute 1:10 with water for floors, countertops, and sinks."
        ],
        "step_by_step_instructions_ta": [
            "1. தோல்களை 1-2 செ.மீ அளவுக்கு நறுக்கிக் கொள்ளவும்.",
            "2. ஒரு லிட்டர் தண்ணீரில் 100 கிராம் வெல்லத்தை முழுமையாக கரைக்கவும்.",
            "3. நறுக்கிய தோல்களை பாட்டிலில் போட்டு, வெல்ல நீரைக் கலக்கவும். மேலே 25% காற்று இடைவெளி விடவும்.",
            "4. விருப்பப்பட்டால் ஒரு சிட்டிகை ஈஸ்ட் சேர்த்து மூடியை இறுக்கமாக மூடவும்.",
            "5. சூரிய ஒளி படாத நிழலான இடத்தில் வைக்கவும்.",
            "6. முக்கிய பாதுகாப்பு விதி: முதல் 30 நாட்களுக்கு தினமும் மூடியை லேசாக திறந்து மீத்தேன்/CO2 காற்றை வெளியேற்றி உடனே மூட வேண்டும்.",
            "7. 30 முதல் 90 நாட்களுக்குப் பின் திரவத்தை வடிகட்டி, 1:10 விகிதத்தில் தண்ணீருடன் கலந்து தரைகள் மற்றும் பாத்திரங்களை சுத்தம் செய்யலாம்."
        ],
        "safety_and_storage_en": "Never use glass containers; accumulating CO2 pressure during fermentation can burst glass. Use flexible PET bottles. Keep out of direct sunlight.",
        "safety_and_storage_ta": "கண்ணாடி பாட்டில்களைப் பயன்படுத்தக்கூடாது; வாயு அழுத்தத்தால் வெடிக்கலாம். பிளாஸ்டிக் பாட்டில்களை மட்டுமே பயன்படுத்தவும்.",
        "scientific_rationale_en": "Anaerobic fermentation by native yeasts and acetic acid bacteria metabolizes jaggery sucrose into organic acetic, citric, and lactic acids along with active protease and amylase enzymes that digest organic grease and biofilm.",
        "scientific_rationale_ta": "நுண்ணுயிர் நொதித்தல் மூலம் அசிட்டிக் மற்றும் சிட்ரிக் அமிலங்கள் உருவாகி, கறைகள் மற்றும் எண்ணெய்ப் பசையை ரசாயனமின்றி இயற்கையாக நீக்குகின்றன."
    },
    {
        "id": "biodegradable_seedling_pots",
        "title_en": "Biodegradable Vegetable Peel Seedling Pots",
        "title_ta": "மக்கும் காய்கறி தோல் விதை நாற்று கோப்பைகள்",
        "category": "garden_soil",
        "category_name_en": "Organic Gardening & Bio-Pots",
        "category_name_ta": "இயற்கை உரங்கள் & விதை நாற்றுக் கோப்பைகள்",
        "suitable_peels": ["pumpkin", "bottle-gourd", "banana", "sweet-potato", "carrot", "mixed"],
        "difficulty": "Easy",
        "prep_time_minutes": 25,
        "total_time": "24-48 Hours Drying",
        "estimated_output": "6-8 Biodegradable Nursery Pots",
        "icon_name": "potted_plant_rounded",
        "impact_summary_en": "Eliminates disposable plastic nursery seed plugs; pots disintegrate naturally in soil without transplant root disturbance.",
        "impact_summary_ta": "பிளாஸ்டிக் நர்சரி கப்புகளை தவிர்க்கிறது; வேர்களை தொந்தரவு செய்யாமல் நேரடியாக மண்ணில் புதைக்கலாம்.",
        "required_materials_en": [
            "350g Coarse fibrous peels (pumpkin rind, bottle gourd, banana skins, squash)",
            "50g Clean scrap cardboard or shredded paper egg carton",
            "200ml Warm water",
            "Muffin baking tin or silicone baking cups (as mold)",
            "Food processor or mortar pestle"
        ],
        "required_materials_ta": [
            "350 கிராம் நார்சத்து மிகுந்த காய்கறி தோல்கள் (பூசணி, சுரைக்காய், வாழைப்பழம்)",
            "50 கிராம் நறுக்கிய அட்டைப்பெட்டி அல்லது முட்டை அட்டை காகிதம்",
            "200 மி.லி வெதுவெதுப்பான தண்ணீர்",
            "மஃபின் பேக்கிங் தட்டு அல்லது கோப்பைகள் (வடிவமைப்பிற்கு)",
            "மிக்ஸி அல்லது அம்மிக் கல்"
        ],
        "step_by_step_instructions_en": [
            "1. Coarsely chop fibrous vegetable peels and soak in warm water with paper scraps for 20 minutes.",
            "2. Pulse briefly in a blender into a fibrous, dough-like pulp (avoid blending into liquid).",
            "3. Squeeze pulp balls with your hands to drain excess standing water.",
            "4. Press pulp firmly against the inside walls and base of muffin tins, forming uniform 5mm thick cups.",
            "5. Dry under hot sun for 24-48 hours until completely rigid, dry, and moisture-free.",
            "6. Pop dried biodegradable cups out of the tin. Fill with potting mix, plant your seeds, and water gently.",
            "7. When seedlings develop 4 true leaves, plant the entire bio-pot directly into garden soil—zero root shock!"
        ],
        "step_by_step_instructions_ta": [
            "1. காய்கறி தோல்களை நறுக்கி காகித துண்டுகளுடன் வெதுவெதுப்பான நீரில் 20 நிமிடங்கள் ஊற வைக்கவும்.",
            "2. மிக்ஸியில் லேசாக அரைத்து நார் பசை போல மாற்றவும் (அதிகமாக அரைக்கக்கூடாது).",
            "3. பிழிந்து அதிகப்படியான தண்ணீரை நீக்கவும்.",
            "4. மஃபின் தட்டின் ஓரங்களில் 5 மி.மீ தடிமனுக்கு கைகளால் அழுத்தி கோப்பை வடிவில் உருவாக்கவும்.",
            "5. வெயிலில் 24-48 மணிநேரம் முழுமையாக காய வைக்கவும்.",
            "6. காய்ந்த பின் கோப்பைகளை எடுத்து மண் நிரப்பி விதைகளை விதைக்கவும்.",
            "7. நாற்று வளர்ந்ததும் கோப்பையோடு சேர்த்து நேரடியாக மண்ணில் நடவு செய்யலாம்."
        ],
        "safety_and_storage_en": "Store in a bone-dry location before planting to prevent mould. Ensure complete solar dehydration.",
        "safety_and_storage_ta": "ஈரப்பதம் இல்லாத உலர்ந்த இடத்தில் சேமிக்கவும். பூஞ்சை பிடிக்காமல் வெயிலில் நன்கு காய வைக்க வேண்டும்.",
        "scientific_rationale_en": "Lignocellulosic fibers cross-link under mechanical compaction and hydrogen bond upon evaporation, producing a structurally stable porous matrix that decomposes in damp soil within 21 days.",
        "scientific_rationale_ta": "தாவர செல்லுலோஸ் நார்கள் ஒன்றுடன் ஒன்று பின்னிப் பிணைந்து உறுதியான அமைப்பைத் தருகின்றன. மண்ணில் நடப்பட்ட 3 வாரங்களில் மட்கி உரமாக மாறுகின்றன."
    },
    {
        "id": "cold_steeped_peel_tea",
        "title_en": "48-Hour High-Potassium Liquid Foliar Peel Tea",
        "title_ta": "48 மணிநேர பொட்டாசியம் நிறைந்த திரவ இலை உரம்",
        "category": "garden_soil",
        "category_name_en": "Organic Gardening & Bio-Pots",
        "category_name_ta": "இயற்கை உரங்கள் & விதை நாற்றுக் கோப்பைகள்",
        "suitable_peels": ["banana", "potato", "carrot", "cucumber", "beetroot", "pumpkin", "all_vegetables"],
        "difficulty": "Easy",
        "prep_time_minutes": 10,
        "total_time": "48 Hours Steeping",
        "estimated_output": "2 Litres Liquid Organic Foliar Tonic",
        "icon_name": "yard_rounded",
        "impact_summary_en": "Replaces synthetic NPK chemical fertilizers, improves root microbiome, and boosts blooming in flowering plants.",
        "impact_summary_ta": "செயற்கை ரசாயன உரங்களை தவிர்க்கிறது; செடிகளின் பூக்கும் திறனை அதிகரித்து வேர்களை பலப்படுத்துகிறது.",
        "required_materials_en": [
            "400g Fresh washed vegetable peels (potato, carrot, cucumber, banana, pumpkin)",
            "2 Litres Clean dechlorinated water (tap water left standing 4 hours)",
            "Clean bucket or pitcher with cloth cover",
            "Fine mesh kitchen sieve",
            "Garden trigger spray bottle"
        ],
        "required_materials_ta": [
            "400 கிராம் புதிய காய்கறி தோல்கள் (உருளை, கேரட், வெள்ளரி, வாழை, பூசணி)",
            "2 லிட்டர் சுத்தமான தண்ணீர்",
            "துணியால் மூடக்கூடிய வாளி அல்லது பாத்திரம்",
            "வடிகட்டி",
            "ஸ்பிரே பாட்டில்"
        ],
        "step_by_step_instructions_en": [
            "1. Roughly chop vegetable peels into 2 cm pieces to expose nutrient-rich cell vacuole surfaces.",
            "2. Submerge peels into 2 litres of water in a clean bucket.",
            "3. Cover with a breathable cotton cloth to prevent insect intrusion while allowing oxygen exchange.",
            "4. Steep for 36-48 hours in a cool shaded room, stirring vigorously once daily.",
            "5. Strain the golden-amber liquid through a fine mesh sieve. (Add spent peel solids to your compost heap).",
            "6. Dilute 1:1 with clean water and spray onto plant leaves (foliar feed) or pour directly into root soil once every 7-10 days."
        ],
        "step_by_step_instructions_ta": [
            "1. காய்கறி தோல்களை 2 செ.மீ அளவுக்கு நறுக்கி பாத்திரத்தில் போடவும்.",
            "2. 2 லிட்டர் தண்ணீரை ஊற்றி நன்கு கலக்கவும்.",
            "3. பூச்சிகள் புகாமல் இருக்க சுத்தமான பருத்தி துணியால் மூடி வைக்கவும்.",
            "4. 48 மணிநேரம் நிழலில் ஊற வைக்கவும்; தினமும் ஒருமுறை குச்சியால் கலக்கி விடவும்.",
            "5. வடிகட்டி திரவத்தை தனியாக எடுக்கவும். மீதமுள்ள தோல்களை உரமாக பயன்படுத்தலாம்.",
            "6. இந்த திரவத்தை சம அளவு தண்ணீருடன் கலந்து செடிகளின் இலைகள் மற்றும் வேர்களுக்கு வாரத்திற்கு ஒருமுறை தெளிக்கவும்."
        ],
        "safety_and_storage_en": "Use within 5 days of steeping. Avoid leaving beyond 72 hours without aeration to prevent foul anaerobic fermentation.",
        "safety_and_storage_ta": "தயாரித்த 5 நாட்களுக்குள் பயன்படுத்த வேண்டும். துர்நாற்றம் வராமல் இருக்க 72 மணி நேரத்திற்கு மேல் ஊற வைக்க வேண்டாம்.",
        "scientific_rationale_en": "Osmotic diffusion rapidly leaches intracellular ionic potassium (K+), nitrates, and micronutrients into water, allowing direct stomatal uptake when applied foliarly.",
        "scientific_rationale_ta": "தோலில் உள்ள பொட்டாசியம் மற்றும் தாதுக்கள் நீரில் கரைந்து, இலைத்துளைகள் வழியாக செடிகளால் உடனடியாக உறிஞ்சப்படுகின்றன."
    },
    {
        "id": "beetroot_botanical_watercolors",
        "title_en": "Beetroot & Plant Peel Non-Toxic Artisan Watercolors",
        "title_ta": "பீட்ரூட் & தாவர தோல் இயற்கை வாட்டர்கலர் வண்ணப்பூச்சுகள்",
        "category": "arts_crafts",
        "category_name_en": "Artisanal Crafts & Natural Dyes",
        "category_name_ta": "இயற்கை சாயங்கள் & கைவினைப் பொருட்கள்",
        "suitable_peels": ["beetroot", "red-cabbage", "spinach", "carrot", "onion"],
        "difficulty": "Easy",
        "prep_time_minutes": 20,
        "total_time": "1 Hour",
        "estimated_output": "3 Pots of Pure Natural Paint",
        "icon_name": "palette_rounded",
        "impact_summary_en": "100% edible-origin, zero synthetic petro-dyes, completely non-toxic and safe for children's art and eco-calligraphy.",
        "impact_summary_ta": "குழந்தைகளுக்கு முற்றிலும் பாதுகாப்பான, நச்சுத்தன்மையற்ற இயற்கை வண்ணங்கள்; ரசாயன நிறமிகள் அற்றது.",
        "required_materials_en": [
            "250g Fresh beetroot peels (for magenta/red) or onion skins (for golden-bronze)",
            "120ml Water",
            "1 Teaspoon White vinegar or lemon juice (pH chromophore stabilizer)",
            "1/2 Teaspoon Sea salt (natural microbial inhibitor)",
            "1 Teaspoon Cornstarch or gum arabic (viscosity binder)",
            "Small glass vials or ice cube paint wells"
        ],
        "required_materials_ta": [
            "250 கிராம் பீட்ரூட் தோல் (சிவப்பு நிறத்திற்கு) அல்லது வெங்காயத் தோல் (தங்க நிறத்திற்கு)",
            "120 மி.லி தண்ணீர்",
            "1 தேக்கரண்டி எலுமிச்சை சாறு அல்லது வினிகர்",
            "1/2 தேக்கரண்டி உப்பு",
            "1 தேக்கரண்டி சோள மாவு (பசையாக்க)",
            "சிறிய கண்ணாடி குப்பிகள் அல்லது ஐஸ் தட்டு"
        ],
        "step_by_step_instructions_en": [
            "1. Simmer chopped peels in 120ml water on low heat for 15-20 minutes until water is deeply concentrated.",
            "2. Strain hot liquid through a fine cloth, squeezing out all vibrant liquid pigment into a heatproof bowl.",
            "3. Whisk in 1 tsp white vinegar or lemon juice to stabilize and brighten the betalain/anthocyanin pigment.",
            "4. Add 1/2 tsp salt and 1 tsp cornstarch. Simmer over low flame for 90 seconds while stirring constantly until silky smooth.",
            "5. Pour into small glass pots or an ice-cube tray to set. Dip your paintbrushes and create botanical watercolor illustrations!"
        ],
        "step_by_step_instructions_ta": [
            "1. தோல்களை 120 மி.லி தண்ணீரில் 15-20 நிமிடங்கள் குறைந்த தீயில் கொதிக்க வைக்கவும்.",
            "2. வடிகட்டி அடர்ந்த வண்ணத் திரவத்தை மட்டும் எடுக்கவும்.",
            "3. ஒரு தேக்கரண்டி எலுமிச்சை சாறு அல்லது வினிகர் சேர்த்து கலக்கவும் (நிறம் மாறாமல் இருக்க உதவும்).",
            "4. உப்பு மற்றும் சோள மாவு சேர்த்து குறைந்த தீயில் 2 நிமிடங்கள் கிளறவும்.",
            "5. கண்ணாடி பாட்டில்கள் அல்லது ஐஸ் தட்டில் ஊற்றி வைத்து ஓவியங்கள் வரைய பயன்படுத்தலாம்!"
        ],
        "safety_and_storage_en": "Store refrigerated in sealed pots; stable for 3-4 weeks. Freeze into pigment ice cubes for 6 months.",
        "safety_and_storage_ta": "குளிர்பதனப் பெட்டியில் (ஃப்ரிட்ஜ்) மூடி வைத்தால் 3-4 வாரங்கள் கெடாமல் இருக்கும்.",
        "scientific_rationale_en": "Betalain betacyanins in beetroot provide rich chromatic absorption at 538 nm. Mild acid maintains the zwitterionic structure against thermal decolorization.",
        "scientific_rationale_ta": "பீட்ரூட்டில் உள்ள பீட்டாலைன் நிறமிகள் பிரகாசமான இயற்கை சிவப்பு நிறத்தை அளிக்கின்றன; எலுமிச்சையின் அமிலம் நிறத்தை நிலைநிறுத்துகிறது."
    },
    {
        "id": "golden_onion_skin_textile_dye",
        "title_en": "Golden Onion Skin Artisan Textile Dye",
        "title_ta": "இயற்கை பொன்னிற வெங்காயத் தோல் ஜவுளி சாயம்",
        "category": "arts_crafts",
        "category_name_en": "Artisanal Crafts & Natural Dyes",
        "category_name_ta": "இயற்கை சாயங்கள் & கைவினைப் பொருட்கள்",
        "suitable_peels": ["onion", "shallots", "pomegranate-peel"],
        "difficulty": "Moderate",
        "prep_time_minutes": 25,
        "total_time": "2 Hours",
        "estimated_output": "1.5 Litres Natural Fabric Dye Bath",
        "icon_name": "brush_rounded",
        "impact_summary_en": "Replaces petrochemical azo fabric dyes; gives natural cotton, linen, silk, and wool a light-fast amber gold tone.",
        "impact_summary_ta": "செயற்கை ஜவுளி சாயங்களை தவிர்க்கிறது; பருத்தி மற்றும் பட்டு துணிகளுக்கு அழகான தங்க நிறத்தை அளிக்கிறது.",
        "required_materials_en": [
            "100g Dry papery outer skins of yellow and red onions",
            "1.5 Litres Water",
            "1 Teaspoon Alum powder (potassium aluminum sulfate) or 2 tbsp table salt as mordant",
            "White 100% cotton cloth, handkerchief, canvas tote bag, or wool yarn"
        ],
        "required_materials_ta": [
            "100 கிராம் காய்ந்த வெங்காயத் தோல்",
            "1.5 லிட்டர் தண்ணீர்",
            "1 தேக்கரண்டி படிகாரம் (Alum) அல்லது 2 தேக்கரண்டி உப்பு",
            "வெள்ளை பருத்தி துணி அல்லது சணல் பை"
        ],
        "step_by_step_instructions_en": [
            "1. Pre-mordant your fabric: dissolve 1 tsp alum or 2 tbsp salt in 500ml warm water, submerge clean fabric for 30 minutes.",
            "2. In a stainless steel pot, simmer onion skins in 1.5 litres of water for 45 minutes until bath turns rich copper-amber.",
            "3. Strain out spent onion skins to leave a clean, particulate-free dye liquor.",
            "4. Submerge pre-soaked wet fabric into the warm dye pot, gently stirring to ensure uniform contact.",
            "5. Simmer gently on low heat for 45-60 minutes, turning fabric occasionally with wooden tongs.",
            "6. Remove fabric, rinse thoroughly under running cold water until runoff is crystal clear, and dry flat in the shade."
        ],
        "step_by_step_instructions_ta": [
            "1. துணியை படிகாரம் அல்லது உப்பு கலந்த நீரில் 30 நிமிடங்கள் ஊற வைக்கவும்.",
            "2. ஒரு பாத்திரத்தில் வெங்காயத் தோலை 1.5 லிட்டர் தண்ணீரில் 45 நிமிடங்கள் கொதிக்க வைக்கவும்.",
            "3. தோல்களை வடிகட்டி அடர் தங்க நிற சாய நீரை மட்டும் எடுக்கவும்.",
            "4. ஊற வைத்த துணியை இந்த சாய நீரில் நனைத்து குறைந்த தீயில் 45 நிமிடங்கள் கொதிக்க வைக்கவும்.",
            "5. துணியை வெளியே எடுத்து குளிர்ந்த நீரில் அலசவும்; பின்னர் நிழலில் உலர்த்தவும்."
        ],
        "safety_and_storage_en": "Use dedicated non-food pots when working with alum mordants. Work in a well-ventilated kitchen.",
        "safety_and_storage_ta": "படிகாரம் பயன்படுத்தும் போது நல்ல காற்றோட்டமான இடத்தில் செய்ய வேண்டும்.",
        "scientific_rationale_en": "Quercetin and polyphenol aglycones naturally concentrated in onion skins coordinate with Al3+ aluminum ions on cellulose fibers, imparting permanent wash-fast golden color.",
        "scientific_rationale_ta": "வெங்காயத் தோலில் உள்ள குவர்செட்டின் (Quercetin) என்ற இயற்கை பொருள் பருத்தி நூல்களுடன் இணைந்து நிரந்தர பொன்னிற சாயத்தை தருகிறது."
    },
    {
        "id": "zero_waste_veggie_bouillon",
        "title_en": "Zero-Waste Gourmet Umami Vegetable Seasoning Salt",
        "title_ta": "பூஜ்ஜிய கழிவு இயற்கை காய்கறி மசாலா & சூப் பவுடர்",
        "category": "culinary_gourmet",
        "category_name_en": "Artisanal Culinary & Kitchen Goods",
        "category_name_ta": "சமையல் மதிப்புக்கூட்டல் & உணவுப் பொருட்கள்",
        "suitable_peels": ["carrot", "potato", "pumpkin", "cucumber", "bottle-gourd", "onion"],
        "difficulty": "Easy",
        "prep_time_minutes": 20,
        "total_time": "3 Hours (Baking/Sun-drying)",
        "estimated_output": "150g All-Natural Seasoning Powder",
        "icon_name": "soup_kitchen_rounded",
        "impact_summary_en": "Rescues culinary vegetable trimmings into chef-grade seasoning salt; 100% free of synthetic MSG, palm oil, or preservatives.",
        "impact_summary_ta": "வீட்டு காய்கறி கழிவுகளை சுவையான சூப் பவுடராக மாற்றுகிறது; அஜினோமோட்டோ மற்றும் ரசாயனங்கள் அற்றது.",
        "required_materials_en": [
            "500g Thoroughly scrubbed, clean edible peels (carrot, pumpkin, non-green potato, celery, onion)",
            "2 Teaspoons Rock salt or Himalayan pink salt",
            "1 Teaspoon Whole black peppercorns",
            "1 Teaspoon Cumin seeds, dried rosemary, or coriander seeds",
            "1 Tablespoon Roasted gram powder or nutritional yeast (optional umami booster)"
        ],
        "required_materials_ta": [
            "500 கிராம் சுத்தமாக கழுவப்பட்ட காய்கறி தோல்கள் (கேரட், பூசணி, உருளை, வெங்காயம்)",
            "2 தேக்கரண்டி கல் உப்பு அல்லது இந்துப்பு",
            "1 தேக்கரண்டி மிளகு",
            "1 தேக்கரண்டி சீரகம் அல்லது கொத்தமல்லி",
            "1 தேக்கரண்டி பொட்டுக்கடலை மாவு"
        ],
        "step_by_step_instructions_en": [
            "1. Scrub peels thoroughly with a vegetable brush to eliminate surface soil. Pat completely dry with kitchen towel.",
            "2. Lay peels in a single non-overlapping layer on a parchment-lined baking tray.",
            "3. Dehydrate in an oven at 100°C for 2.5 to 3 hours (or sun-dry under fine mesh netting for 2 full sunny days) until brittle and chip-dry.",
            "4. Transfer crisp dried peels into a dry spice grinder along with rock salt, peppercorns, and roasted cumin.",
            "5. Pulse into a fine, fragrant savory powder.",
            "6. Store in an airtight spice shaker. Stir 1 teaspoon into boiling water for instant comforting vegetable broth, or dust over roasted vegetables, dal, and popcorn!"
        ],
        "step_by_step_instructions_ta": [
            "1. தோல்களை நன்கு கழுவி ஈரம் போக துணியால் துடைக்கவும்.",
            "2. ஒரு தட்டில் பரப்பி வெயிலில் 2 நாட்கள் அல்லது அவனில் 100°C-ல் மொறுமொறுப்பாகும் வரை உலர்த்தவும்.",
            "3. காய்ந்த தோல்களுடன் கல் உப்பு, மிளகு, சீரகம் சேர்த்து மிக்ஸியில் நைசாக அரைக்கவும்.",
            "4. காற்றுப்புகாத பாட்டிலில் அடைத்து வைக்கவும்.",
            "5. சுடுநீரில் ஒரு ஸ்பூன் கலந்தால் சத்தான காய்கறி சூப் தயார்! சாதம் மற்றும் பொரியலிலும் தூவி உண்ணலாம்."
        ],
        "safety_and_storage_en": "CRITICAL: Never use green or sprouted potato peels (toxic solanine risk). Use only fresh, firm peels. Store airtight away from steam.",
        "safety_and_storage_ta": "முக்கியம்: பச்சை நிற உருளைக்கிழங்கு தோல்களை பயன்படுத்தக்கூடாது. உலர்ந்த பாட்டிலில் மூடி வைக்கவும்.",
        "scientific_rationale_en": "Moisture evaporation concentrates natural glutamic acid and mineral salts in botanical skins, providing full-bodied natural umami without MSG.",
        "scientific_rationale_ta": "ஈரப்பதம் வெளியேறும்போது காய்கறிகளில் உள்ள இயற்கை குளுடாமிக் அமிலம் மற்றும் தாதுக்கள் அடர்த்தியாகி சுவையான இயற்கை சுவையை அளிக்கின்றன."
    },
    {
        "id": "allium_pest_repellent_spray",
        "title_en": "Allium & Chilli Natural Botanical Pest Repellent Spray",
        "title_ta": "வெங்காயம் & மிளகாய் இயற்கை பூச்சிவிரட்டி தெளிப்பு",
        "category": "garden_soil",
        "category_name_en": "Organic Gardening & Bio-Pots",
        "category_name_ta": "இயற்கை உரங்கள் & விதை நாற்றுக் கோப்பைகள்",
        "suitable_peels": ["onion", "garlic", "chilli", "ginger", "potato"],
        "difficulty": "Easy",
        "prep_time_minutes": 15,
        "total_time": "24 Hours Steeping",
        "estimated_output": "1 Litre Organic Bug Defense Spray",
        "icon_name": "pest_control_rounded",
        "impact_summary_en": "Protects vegetable garden crops against aphids, mites, and whiteflies without synthetic neurotoxic chemicals.",
        "impact_summary_ta": "செடிகளில் வரும் அசுவினி மற்றும் பூச்சிகளை ரசாயனமின்றி இயற்கையாக விரட்டுகிறது.",
        "required_materials_en": [
            "150g Onion skins, garlic papery husks, and hot chilli tops/scraps",
            "1000ml (1 Litre) Boiling hot water",
            "1/2 Teaspoon Mild organic liquid dish soap or neem oil (adherence surfactant)",
            "1 Spray bottle and fine cloth strainer"
        ],
        "required_materials_ta": [
            "150 கிராம் வெங்காயம், பூண்டு தோல்கள் மற்றும் மிளகாய் காம்புகள்",
            "1 லிட்டர் கொதிக்கும் தண்ணீர்",
            "1/2 தேக்கரண்டி சோப் திரவம் அல்லது வேப்ப எண்ணெய்",
            "ஸ்பிரே பாட்டில் மற்றும் வடிகட்டும் துணி"
        ],
        "step_by_step_instructions_en": [
            "1. Place allium peel scraps and crushed chilli tops into a heat-safe glass or ceramic bowl.",
            "2. Pour 1 litre of boiling water directly over the scraps and cover immediately with a lid to trap sulfurous volatile compounds.",
            "3. Let steep undisturbed at room temperature for 24 hours.",
            "4. Strain the infusion through a fine cloth into your spray bottle.",
            "5. Add 1/2 teaspoon of liquid soap (this breaks surface tension, enabling spray to stick to insect cuticles and waxy leaves).",
            "6. Spray liberally onto leaf undersides and stems in the early morning or evening to deter aphids, spider mites, and caterpillars."
        ],
        "step_by_step_instructions_ta": [
            "1. வெங்காயம், பூண்டு தோல்கள் மற்றும் மிளகாய் கழிவுகளை ஒரு பாத்திரத்தில் போடவும்.",
            "2. 1 லிட்டர் கொதிக்கும் நீரை ஊற்றி உடனடியாக தட்டு போட்டு மூடவும்.",
            "3. 24 மணிநேரம் ஊற வைக்கவும்.",
            "4. துணியால் வடிகட்டி ஸ்பிரே பாட்டிலில் ஊற்றவும்.",
            "5. அரை தேக்கரண்டி சோப் திரவம் சேர்க்கவும் (இது இலைகளில் மருந்து ஒட்ட உதவும்).",
            "6. அதிகாலை அல்லது மாலையில் பூச்சிகள் உள்ள இலைகளின் அடிப்பகுதியில் தெளிக்கவும்."
        ],
        "safety_and_storage_en": "Wear gloves when straining hot chilli infusion. Avoid eye contact. Do not spray during harsh midday sun to avoid leaf scorch.",
        "safety_and_storage_ta": "கண்களில் படாமல் பார்த்துக் கொள்ளவும். நண்பகல் வெயில் நேரத்தில் தெளிக்கக்கூடாது.",
        "scientific_rationale_en": "Allicin metabolites and pungent capsaicinoids act as neuro-sensory deterrents to insect herbivores, while soap dissolves the lipid wax coating of soft-bodied pests.",
        "scientific_rationale_ta": "பூண்டு மற்றும் வெங்காயத்தில் உள்ள கந்தக மூலக்கூறுகள் பூச்சிகளை விரட்டுகின்றன; சோப் திரவம் பூச்சிகளின் மெழுகு அடுக்கை நீக்குகிறது."
    },
    {
        "id": "cucumber_potato_glow_scrub",
        "title_en": "Botanical Peel Exfoliating Face Scrub & Glow Pack",
        "title_ta": "காய்கறி தோல் இயற்கை முகப்பொலிவு ஸ்க்ரப் பவுடர்",
        "category": "natural_wellness",
        "category_name_en": "Natural Skincare & Wellness",
        "category_name_ta": "இயற்கை அழகு & ஆரோக்கியம்",
        "suitable_peels": ["cucumber", "potato", "carrot", "orange", "beetroot"],
        "difficulty": "Easy",
        "prep_time_minutes": 15,
        "total_time": "24 Hours (Drying)",
        "estimated_output": "100g Botanical Exfoliating Powder",
        "icon_name": "spa_rounded",
        "impact_summary_en": "Replaces plastic microbeads in commercial scrubs with 100% natural, biodegradable plant skin exfoliants.",
        "impact_summary_ta": "பிளாஸ்டிக் மைக்ரோபீட்ஸை தவிர்க்கிறது; சருமத்திற்கு இயற்கையான பளபளப்பை அளிக்கிறது.",
        "required_materials_en": [
            "200g Fresh washed cucumber, carrot, or non-green potato peels",
            "2 Tablespoons Besan (chickpea flour) or ground oats",
            "1/2 Teaspoon Pure wild turmeric (kasturi manjal)",
            "Rose water, raw milk, or yogurt for paste reconstitution"
        ],
        "required_materials_ta": [
            "200 கிராம் புதிய வெள்ளரி, கேரட் அல்லது உருளைக்கிழங்கு தோல்கள்",
            "2 தேக்கரண்டி கடலை மாவு அல்லது ஓட்ஸ் பொடி",
            "1/2 தேக்கரண்டி கஸ்தூரி மஞ்சள்",
            "ரோஸ் வாட்டர் அல்லது தயிர் (குழைக்க)"
        ],
        "step_by_step_instructions_en": [
            "1. Scrub peels thoroughly and dry completely under shade or low oven (60°C) until crisp.",
            "2. Mill dried peels in a blender into a soft, mildly textured exfoliating grain.",
            "3. Mix the ground peel powder with chickpea flour and wild turmeric. Store dry in an airtight jar.",
            "4. To use: scoop 1 tablespoon into a small bowl, mix with 2 tablespoons rose water or curd into a smooth paste.",
            "5. Gently massage in upward circular motions on face and neck for 2 minutes, leave for 10 minutes, and rinse with lukewarm water."
        ],
        "step_by_step_instructions_ta": [
            "1. தோல்களை நன்கு கழுவி நிழலில் அல்லது குறைந்த வெப்பத்தில் உலர்த்தவும்.",
            "2. மிக்ஸியில் மெல்லிய துகள்களாக அரைக்கவும்.",
            "3. கடலை மாவு மற்றும் கஸ்தூரி மஞ்சள் சேர்த்து கலந்து பாட்டிலில் வைக்கவும்.",
            "4. பயன்படுத்தும் போது: ஒரு ஸ்பூன் பொடியுடன் ரோஸ் வாட்டர் அல்லது தயிர் சேர்த்து குழைக்கவும்.",
            "5. முகத்தில் தடவி 10 நிமிடங்கள் கழித்து குளிர்ந்த நீரால் கழுவவும்."
        ],
        "safety_and_storage_en": "Conduct a small forearm patch test 24 hours prior to facial application. Do not use green potato skins.",
        "safety_and_storage_ta": "முகத்தில் போடுவதற்கு முன் கையில் சிறிதளவு தடவி ஒவ்வாமை உள்ளதா என சோதித்துப் பார்க்கவும்.",
        "scientific_rationale_en": "Cucumber peel silica strengthens skin resilience; potato catecholase enzyme helps fade hyperpigmentation, while carrot beta-carotene provides topical antioxidant defense.",
        "scientific_rationale_ta": "வெள்ளரி தோலில் உள்ள சிலிக்கா சருமத்தை மிருதுவாக்குகிறது; உருளைத்தோல் முகத்தில் உள்ள கரும்புள்ளிகளை மங்கச் செய்கிறது."
    },
    {
        "id": "fibrous_peel_seed_paper",
        "title_en": "Botanical Waste Seed Paper & Greeting Cards",
        "title_ta": "காய்கறி கழிவு விதை காகிதம் & கைவினை வாழ்த்து அட்டைகள்",
        "category": "arts_crafts",
        "category_name_en": "Artisanal Crafts & Natural Dyes",
        "category_name_ta": "இயற்கை சாயங்கள் & கைவினைப் பொருட்கள்",
        "suitable_peels": ["pumpkin", "bottle-gourd", "sweet-potato", "carrot", "corn", "all_vegetables"],
        "difficulty": "Moderate",
        "prep_time_minutes": 35,
        "total_time": "24 Hours",
        "estimated_output": "4 Textured Plantable Greeting Cards",
        "icon_name": "note_alt_rounded",
        "impact_summary_en": "100% tree-free paper; embedded with basil or flower seeds so recipient can plant the card in soil to sprout!",
        "impact_summary_ta": "மரம் வெட்டாமல் தயாரிக்கப்படும் காகிதம்; கார்டில் உள்ள விதைகளை மண்ணில் நட்டால் செடி முளைக்கும்!",
        "required_materials_en": [
            "250g Fibrous vegetable peels (boiled 15 mins to soften cellulose)",
            "100g Shredded scrap cardboard or discarded paper",
            "1 Teaspoon Wildflower, marigold, or holy basil (tulsi) seeds",
            "Wire mesh screen / frame (deckle) or flat kitchen splash guard",
            "Cotton towels and rolling pin"
        ],
        "required_materials_ta": [
            "250 கிராம் நார்சத்து காய்கறி தோல்கள் (15 நிமிடம் வேகவைத்தது)",
            "100 கிராம் பழைய காகித துண்டுகள்",
            "1 தேக்கரண்டி துளசி அல்லது பூ விதைகள்",
            "கம்பி வலை அல்லது ஜல்லடை",
            "பருத்தி துணி"
        ],
        "step_by_step_instructions_en": [
            "1. Boil tough peels for 15 minutes to soften cellulose fibers.",
            "2. Blend softened peels and soaked scrap paper with 500ml water into a thick, uniform paper slurry.",
            "3. Pour slurry into a wide shallow basin. GENTLY stir in plant seeds with a spoon (do not blend seeds).",
            "4. Submerge your mesh screen underneath the pulp and lift slowly upward to catch an even fiber sheet.",
            "5. Flip the wet paper sheet onto a cotton towel, press firmly with a rolling pin to absorb water, and peel off carefully.",
            "6. Dry in a breezy shade for 24 hours. Trim edges into greeting card or bookmark sizes and write heartfelt notes with botanical ink!"
        ],
        "step_by_step_instructions_ta": [
            "1. காய்கறி தோல்களை 15 நிமிடங்கள் வேகவைத்து மென்மையாக்கவும்.",
            "2. வேகவைத்த தோல்களையும் பழைய காகிதத்தையும் மிக்ஸியில் கூழாக அரைக்கவும்.",
            "3. அகலமான பாத்திரத்தில் தண்ணீருடன் இந்த கூழை கலந்து, விதைகளை கைகளால் தூவி கலக்கவும்.",
            "4. கம்பி வலையை பாத்திரத்திற்குள் விட்டு மெதுவாக மேலே தூக்கி சமமாக காகிதத்தை எடுக்கவும்.",
            "5. துணியின் மேல் கவிழ்த்து தண்ணீரை ஒற்றி எடுத்து நிழலில் உலர்த்தவும்.",
            "6. 24 மணிநேரத்தில் அழகிய வாழ்த்து அட்டை தயார்! பயன்படுத்திய பின் மண்ணில் புதைத்தால் செடி வளரும்."
        ],
        "safety_and_storage_en": "Never dry seed paper in a heated oven, as heat will kill the internal plant embryo. Air dry only.",
        "safety_and_storage_ta": "அவனில் வைக்கக்கூடாது; வெப்பத்தால் விதைகள் இறந்துவிடும். காற்றில் மட்டுமே உலர்த்த வேண்டும்.",
        "scientific_rationale_en": "Boiling disrupts hemicellulose matrix, releasing flexible cellulose microfibrils that form interlaced hydrogen networks upon dehydration, bonding paper with zero chemical adhesives.",
        "scientific_rationale_ta": "செல்லுலோஸ் நார்கள் இயற்கையாகவே ஒன்றுடன் ஒன்று பின்னிப் பிணைந்து பசை இல்லாமலேயே உறுதியான காகிதமாக மாறுகின்றன."
    },
    {
        "id": "potato_starch_bioplastic_sheet",
        "title_en": "DIY Biodegradable Starch Bioplastic Film",
        "title_ta": "மக்கும் உருளை மாவுச்சத்து பயோ-பிளாஸ்டிக் தாள்",
        "category": "biomaterials",
        "category_name_en": "Bio-Materials & Green Science",
        "category_name_ta": "உயிரிப் பொருட்கள் & பசுமை அறிவியல்",
        "suitable_peels": ["potato", "sweet-potato", "cassava-tapioca"],
        "difficulty": "Moderate",
        "prep_time_minutes": 30,
        "total_time": "24 Hours (Curing)",
        "estimated_output": "2 Flexible Biodegradable Bioplastic Sheets",
        "icon_name": "science_rounded",
        "impact_summary_en": "Educational prototype demonstrating renewable plant-based alternative to single-use polyethylene packaging.",
        "impact_summary_ta": "பிளாஸ்டிக்கிற்கு மாற்றான மக்கும் இயற்கை பயோ-பிளாஸ்டிக் தயாரிக்கும் முறை.",
        "required_materials_en": [
            "300g Potato or cassava peels",
            "150ml Water for starch extraction",
            "1 Tablespoon Vegetable glycerin (natural plasticizer)",
            "1 Teaspoon White vinegar (acid catalyst)",
            "Non-stick silicone baking mat or glass baking dish"
        ],
        "required_materials_ta": [
            "300 கிராம் உருளைக்கிழங்கு அல்லது மரவள்ளிக்கிழங்கு தோல்",
            "150 மி.லி தண்ணீர்",
            "1 தேக்கரண்டி கிளிசரின் (Glycerin)",
            "1 தேக்கரண்டி வினிகர்",
            "சிலிகான் தட்டு அல்லது கண்ணாடி தட்டு"
        ],
        "step_by_step_instructions_en": [
            "1. Blend potato peels with 150ml water into a smooth slurry. Strain through a fine muslin cloth into a clear bowl.",
            "2. Let the liquid settle undisturbed for 25 minutes; white starch sediment will collect firmly at the bottom.",
            "3. Pour off the top cloudy water, leaving pure white wet starch paste in the bowl.",
            "4. Combine 2 tablespoons of extracted starch, 100ml water, 1 tbsp glycerin, and 1 tsp vinegar in a small saucepan.",
            "5. Stir continuously over low-medium heat for 4-5 minutes until the mixture turns from cloudy liquid into a glossy, thick translucent gel.",
            "6. Immediately pour and smooth thinly onto a silicone baking mat. Allow to dry at room temperature for 24-36 hours, then gently peel off a flexible bioplastic film!"
        ],
        "step_by_step_instructions_ta": [
            "1. உருளைக்கிழங்கு தோலை தண்ணீருடன் அரைத்து துணியில் வடிகட்டவும்.",
            "2. 25 நிமிடங்கள் அசையாமல் வைக்கவும்; அடியில் வெள்ளை மாவுச்சத்து படியும்.",
            "3. மேலே உள்ள தண்ணீரை வடித்துவிட்டு அடியில் உள்ள மாவை எடுக்கவும்.",
            "4. ஒரு பாத்திரத்தில் 2 ஸ்பூன் மாவு, 100 மி.லி தண்ணீர், 1 ஸ்பூன் கிளிசரின், 1 ஸ்பூன் வினிகர் சேர்க்கவும்.",
            "5. குறைந்த தீயில் 4-5 நிமிடங்கள் கிளறினால் கண்ணாடி போன்ற ஜெல் உருவாகும்.",
            "6. சிலிகான் தட்டில் மெல்லியதாக பரப்பி 24 மணிநேரம் உலர்த்தினால் மக்கும் பயோ-பிளாஸ்டிக் தாள் தயார்!"
        ],
        "safety_and_storage_en": "Adult supervision required when cooking gel on stovetop. Not intended for prolonged immersion in water.",
        "safety_and_storage_ta": "அடுப்பில் கிளறும் போது பெரியவர்கள் மேற்பார்வை அவசியம்.",
        "scientific_rationale_en": "Thermal gelatinization unravels linear amylose polymer chains, which vinegar acid untangles. Glycerin molecules insert between polymer chains, preventing recrystallization and bestowing elastic flexibility.",
        "scientific_rationale_ta": "உருளை மாவுச்சத்தின் அமிலிய பாலிமர் சங்கிலிகள் கிளிசரினுடன் இணைந்து நெகிழும் தன்மையுடைய பிளாஸ்டிக் அமைப்பை உருவாக்குகின்றன."
    },
    {
        "id": "aromatic_botanical_potpourri",
        "title_en": "Botanical Citrus & Peel Wardrobe Potpourri Sachets",
        "title_ta": "நறுமண காய்கறி & பழத்தோல் வாசனைப் பைகள்",
        "category": "eco_home",
        "category_name_en": "Eco-Home & Natural Cleaning",
        "category_name_ta": "வீட்டுப் பராமரிப்பு & இயற்கை கிளீனர்",
        "suitable_peels": ["cucumber", "orange", "apple", "carrot", "beetroot"],
        "difficulty": "Easy",
        "prep_time_minutes": 15,
        "total_time": "2 Days Sun-Drying",
        "estimated_output": "3 Linen Scented Drawstring Pouches",
        "icon_name": "local_florist_rounded",
        "impact_summary_en": "Replaces synthetic chemical aerosol air fresheners and phthalate scented closet fresheners.",
        "impact_summary_ta": "செயற்கை ரசாயன ஏர்-ஃப்ரெஷ்னர்களை தவிர்க்கிறது; துணி அலமாரிகளுக்கு இயற்கையான நறுமணம் அளிக்கிறது.",
        "required_materials_en": [
            "250g Peel ribbons (cucumber, orange, apple, beetroot, lemon sliced thinly)",
            "2 Whole cinnamon sticks, 6 whole cloves, 2 star anise pods",
            "4-5 Drops pure natural lavender, citrus, or eucalyptus essential oil",
            "3 Breathable small cotton, linen, or jute drawstring pouches"
        ],
        "required_materials_ta": [
            "250 கிராம் நீளமாக நறுக்கப்பட்ட பழம் மற்றும் காய்கறி தோல்கள்",
            "2 பட்டை, 6 கிராம்பு, 2 அன்னாசிப்பூ",
            "4 சொட்டு யூகலிப்டஸ் அல்லது லாவெண்டர் எண்ணெய்",
            "3 சிறிய பருத்தி அல்லது சணல் பைகள்"
        ],
        "step_by_step_instructions_en": [
            "1. Shave clean peels into long thin curly ribbons using a standard vegetable peeler.",
            "2. Spread curls onto a bamboo tray and sun-dry for 48 hours until completely crisp and curled.",
            "3. In a bowl, toss the crispy dried peels with cinnamon sticks, cloves, and star anise.",
            "4. Add essential oil drops, transfer to a sealed glass jar, and let cure for 24 hours to infuse spices deeply into peel pores.",
            "5. Scoop the potpourri blend into jute or cotton drawstring pouches.",
            "6. Place inside clothes wardrobes, linen cupboards, luggage bags, or car interiors for months of uplifting natural botanical aroma!"
        ],
        "step_by_step_instructions_ta": [
            "1. தோல்களை மெல்லிய சுருள் பட்டைகளாக நறுக்கவும்.",
            "2. தட்டில் பரப்பி வெயிலில் 2 நாட்கள் மொறுமொறுப்பாகும் வரை உலர்த்தவும்.",
            "3. காய்ந்த தோல்களுடன் பட்டை, கிராம்பு, அன்னாசிப்பூ மற்றும் நறுமண எண்ணெய் சேர்க்கவும்.",
            "4. ஒரு நாள் மூடி வைத்து பின்னர் சிறிய துணிப்பைகளில் நிரப்பவும்.",
            "5. துணி அலமாரி மற்றும் கார்களில் வைத்தால் பல வாரங்களுக்கு இனிமையான நறுமணம் வீசும்!"
        ],
        "safety_and_storage_en": "Ensure peels are 100% moisture-free before packing in pouches to avoid cupboard mildew.",
        "safety_and_storage_ta": "பூஞ்சை பிடிக்காமல் இருக்க தோல்கள் முழுமையாக காய்ந்திருக்க வேண்டும்.",
        "scientific_rationale_en": "Dehydrated cellulose matrix possesses high micro-capillary porosity, capturing and gradually desorbing hydrophobic terpene and ester aroma molecules through slow vapor diffusion.",
        "scientific_rationale_ta": "காய்ந்த தோலின் நுண்ணிய துவாரங்கள் நறுமண மூலக்கூறுகளை உறிஞ்சி மெதுவாக காற்றில் பரப்புகின்றன."
    },
    {
        "id": "crispy_baked_peel_chips",
        "title_en": "Gourmet Spiced Peel Chips (Air-Fried or Oven-Baked)",
        "title_ta": "சுவையான மொறுமொறு காய்கறி தோல் சிப்ஸ்",
        "category": "culinary_gourmet",
        "category_name_en": "Artisanal Culinary & Kitchen Goods",
        "category_name_ta": "சமையல் மதிப்புக்கூட்டல் & உணவுப் பொருட்கள்",
        "suitable_peels": ["potato", "sweet-potato", "carrot", "beetroot", "pumpkin"],
        "difficulty": "Easy",
        "prep_time_minutes": 10,
        "total_time": "25 Minutes",
        "estimated_output": "1 Bowl Crispy Dietary Fiber Snack",
        "icon_name": "lunch_dining_rounded",
        "impact_summary_en": "Diverts edible nutrient-dense peel ribbons from the bin into a crunchy, potassium and fiber-packed family snack.",
        "impact_summary_ta": "காய்கறி கழிவை சத்தான சிப்ஸாக மாற்றுகிறது; நார்ச்சத்து மற்றும் பொட்டாசியம் நிறைந்தது.",
        "required_materials_en": [
            "250g Clean, fresh, strictly NON-GREEN potato, sweet potato, pumpkin, or carrot peel ribbons",
            "1.5 Tablespoons Olive oil or cold-pressed coconut oil",
            "1/2 Teaspoon Sea salt",
            "1/2 Teaspoon Chaat masala or smoked paprika",
            "1/4 Teaspoon Freshly cracked black pepper"
        ],
        "required_materials_ta": [
            "250 கிராம் சுத்தமான உருளைக்கிழங்கு (பச்சை நிறமில்லாதது), கேரட், பூசணி தோல்கள்",
            "1.5 தேக்கரண்டி ஆலிவ் எண்ணெய் அல்லது நல்லெண்ணெய்",
            "1/2 தேக்கரண்டி உப்பு",
            "1/2 தேக்கரண்டி சாட் மசாலா அல்லது மிளகாய்த்தூள்",
            "1/4 தேக்கரண்டி மிளகுத்தூள்"
        ],
        "step_by_step_instructions_en": [
            "1. Thoroughly scrub and wash vegetable skins to eliminate all surface particles. Pat completely dry with kitchen towel.",
            "2. Toss dry peel ribbons in a mixing bowl with olive oil, salt, pepper, and chaat masala until evenly glistening.",
            "3. Arrange in a single flat layer on a parchment-lined baking sheet or air-fryer basket.",
            "4. Bake at 200°C for 12-15 minutes (or air-fry at 190°C for 9-11 minutes), shaking halfway through until golden and crackling crisp.",
            "5. Cool for 2 minutes on paper towels (they become noticeably crisper as moisture leaves) and enjoy right away!"
        ],
        "step_by_step_instructions_ta": [
            "1. தோல்களை நன்கு கழுவி ஈரம் இல்லாமல் துடைத்துக் கொள்ளவும்.",
            "2. ஒரு பாத்திரத்தில் எண்ணெய், உப்பு, மிளகுத்தூள் மற்றும் சாட் மசாலா சேர்த்து தோல்களுடன் கலக்கவும்.",
            "3. பேக்கிங் தட்டில் அல்லது ஏர்-பிரையரில் பரப்பவும்.",
            "4. 200°C வெப்பத்தில் 12-15 நிமிடங்கள் பொன்னிறமாக மொறுமொறுப்பாகும் வரை வறுக்கவும்.",
            "5. 2 நிமிடங்கள் ஆற வைத்து சுடச்சுட சுவைக்கவும்!"
        ],
        "safety_and_storage_en": "CRITICAL FOOD SAFETY NOTICE: Never consume green, damaged, or sprouted potato skins; toxic solanine is heat-stable and will not degrade during frying. Use only fresh, golden peels.",
        "safety_and_storage_ta": "முக்கிய உணவு பாதுகாப்பு எச்சரிக்கை: பச்சை நிறம் அல்லது முளைவிட்ட உருளைக்கிழங்கு தோல்களை ஒருபோதும் சாப்பிடக்கூடாது (சோலனைன் நச்சு). புதிய தோல்களை மட்டுமே பயன்படுத்தவும்.",
        "scientific_rationale_en": "High dry heat induces rapid Maillard browning and starch crisping on the outer cellular layer while preserving internal dietary potassium, polyphenols, and insoluble fiber.",
        "scientific_rationale_ta": "அதிக வெப்பத்தில் வறுக்கும்போது தோலில் உள்ள நார்ச்சத்து மொறுமொறுப்பாக மாறி சுவையையும் சத்தையும் தருகிறது."
    },
    {
        "id": "apple_peel_cinnamon_tea",
        "title_en": "Artisanal Apple Peel & Cinnamon Spiced Tea",
        "title_ta": "ஆப்பிள் தோல் & இலவங்கப்பட்டை நறுமண மூலிகை டீ",
        "category": "culinary_gourmet",
        "category_name_en": "Artisanal Culinary Upcycling",
        "category_name_ta": "சமையல் கலை & புதுமையான உணவு தயாரிப்பு",
        "suitable_peels": ["apple", "mixed"],
        "difficulty": "Easy",
        "prep_time_minutes": 10,
        "total_time": "25 Minutes",
        "estimated_output": "4 Servings Aromatic Herbal Tea",
        "icon_name": "soup_kitchen_rounded",
        "impact_summary_en": "Upcycles 100g of sweet apple peel ribbons into a comforting, caffeine-free antioxidant herbal infusion rich in quercetin.",
        "impact_summary_ta": "100 கிராம் ஆப்பிள் தோலை நோய் எதிர்ப்பு சக்தி நிறைந்த சுவையான மூலிகை டீயாக மாற்றுகிறது.",
        "required_materials_en": [
            "Peels from 4-5 organic apples (washed thoroughly)",
            "1 Cinnamon stick (Ceylon cinnamon preferred)",
            "3 Whole cloves & 1 green cardamom pod",
            "800ml (3-4 cups) Filtered drinking water",
            "1-2 tsp Pure honey or maple syrup (optional, to taste)"
        ],
        "required_materials_ta": [
            "4-5 நன்கு கழுவிய ஆப்பிள் பழங்களின் தோல்கள்",
            "1 சிறிய இலவங்கப்பட்டை சுருள்",
            "3 கிராம்பு & 1 ஏலக்காய்",
            "800 மி.லி சுத்தமான தண்ணீர்",
            "1-2 தேக்கரண்டி தேன் (விருப்பத்திற்கேற்ப)"
        ],
        "step_by_step_instructions_en": [
            "1. Soak apple peels in warm water with 1 teaspoon baking soda for 5 minutes, then rinse cleanly to remove surface waxes.",
            "2. Bring 800ml of water to a rolling boil in a stainless steel saucepan.",
            "3. Add the clean apple peel ribbons, cinnamon stick, cloves, and crushed cardamom pod.",
            "4. Reduce heat to low, cover with lid, and gently simmer for 15-20 minutes until the liquid turns a warm amber-rose hue.",
            "5. Strain the aromatic infusion into mugs through a fine stainless steel mesh strainer.",
            "6. Stir in honey to taste and serve steaming hot with an optional cinnamon stick garnish."
        ],
        "step_by_step_instructions_ta": [
            "1. ஆப்பிள் தோல்களை வெதுவெதுப்பான பேக்கிங் சோடா நீரில் 5 நிமிடங்கள் ஊறவைத்து, மெழுகை நீக்க நன்கு கழுவவும்.",
            "2. ஒரு பாத்திரத்தில் 800 மி.லி தண்ணீரை கொதிக்க வைக்கவும்.",
            "3. கழுவிய ஆப்பிள் தோல்கள், இலவங்கப்பட்டை, கிராம்பு மற்றும் நசுக்கிய ஏலக்காயை சேர்க்கவும்.",
            "4. தீயைக் குறைத்து, மூடி போட்டு 15-20 நிமிடங்கள் கொதிக்க வைக்கவும். தண்ணீர் பொன்னிற இளஞ்சிவப்பாக மாறும்.",
            "5. வடிகட்டி கோப்பைகளில் ஊற்றி, தேன் சேர்த்து சூடாக பருகவும்!"
        ],
        "safety_and_storage_en": "Ensure all orchard waxes and residual pesticide residues are rinsed with baking soda water before boiling. Store strained leftover tea in a glass jar in the refrigerator for up to 3 days.",
        "safety_and_storage_ta": "மெழுகு பூச்சை நீக்க நன்கு கழுவுவது அவசியம். மீதமுள்ள டீயை குளிர்சாதன பெட்டியில் 3 நாட்கள் வரை வைத்திருக்கலாம்.",
        "scientific_rationale_en": "Heat extraction releases water-soluble quercetin glycosides, chlorogenic acid, and catechins concentrated predominantly in the apple peel epidermis, providing anti-inflammatory and cellular antioxidant benefits.",
        "scientific_rationale_ta": "ஆப்பிள் தோலில் உள்ள குவெர்செடின் மற்றும் பாலிபினால்கள் கொதிநீரில் எளிதாக கரைந்து உடலுக்கு நோய் எதிர்ப்பு சக்தியை அளிக்கின்றன."
    },
    {
        "id": "raw_apple_cider_vinegar",
        "title_en": "Homemade Live-Culture Apple Cider Vinegar (with the 'Mother')",
        "title_ta": "இயற்கை முறையில் தயாரிக்கப்படும் ஆப்பிள் சிடர் வினிகர்",
        "category": "eco_home",
        "category_name_en": "Eco-Home & Natural Cleaning",
        "category_name_ta": "வீட்டுப் பராமரிப்பு & இயற்கை கிளீனர்",
        "suitable_peels": ["apple", "mixed"],
        "difficulty": "Ferment",
        "prep_time_minutes": 15,
        "total_time": "4-6 Weeks Fermentation",
        "estimated_output": "750ml Raw Probiotic Vinegar",
        "icon_name": "science_rounded",
        "impact_summary_en": "Converts 250g of kitchen apple waste into a premium artisanal probiotic vinegar, diverting waste and eliminating single-use plastic bottles.",
        "impact_summary_ta": "250 கிராம் கழிவு ஆப்பிள் தோலை மருத்துவ குணம் வாய்ந்த இயற்கை வினிகராக மாற்றுகிறது.",
        "required_materials_en": [
            "250g Clean apple peels and cores (free of mold)",
            "2 tbsp Unrefined cane sugar or raw honey",
            "750ml Non-chlorinated filtered water",
            "1 Wide-mouth 1-litre glass jar",
            "1 Breathable cloth square (cheesecloth or clean cotton) & rubber band"
        ],
        "required_materials_ta": [
            "250 கிராம் ஆப்பிள் தோல்கள் மற்றும் நடுப்பகுதி",
            "2 மேஜைக்கரண்டி நாட்டுச்சர்க்கரை அல்லது தேன்",
            "750 மி.லி குளோரின் இல்லாத தண்ணீர்",
            "1 அகலமான 1 லிட்டர் கண்ணாடி பாட்டில்",
            "1 பருத்தி துணி & ரப்பர் பேண்ட்"
        ],
        "step_by_step_instructions_en": [
            "1. Fill clean glass jar two-thirds full with fresh apple peel ribbons and cores.",
            "2. Dissolve 2 tablespoons of sugar in 750ml room-temperature filtered water.",
            "3. Pour sweetened water over the apple peels until completely submerged (use a small glass weight or fermentation disk to keep peels underwater).",
            "4. Cover jar mouth with breathable cotton cloth and secure tightly with a rubber band to allow gas exchange while keeping fruit flies out.",
            "5. Store in a dark cupboard at room temperature (20-25°C). Stir once every 2-3 days for the first two weeks.",
            "6. After 3 weeks, strain out solids. Return liquid to jar, re-cover with cloth, and ferment for another 2-3 weeks until tart and acidic.",
            "7. Decant into a swing-top bottle; a cloudy gel-like 'Mother of Vinegar' will naturally form on top, indicating raw probiotic vitality."
        ],
        "step_by_step_instructions_ta": [
            "1. கண்ணாடி பாட்டிலில் முக்கால் பகுதி வரை நறுக்கிய ஆப்பிள் தோல்களை நிரப்பவும்.",
            "2. தண்ணீரில் நாட்டுச்சர்க்கரையை நன்கு கரைத்து பாட்டிலில் ஊற்றவும். தோல்கள் தண்ணீரில் மூழ்கி இருக்க வேண்டும்.",
            "3. பாட்டிலின் வாயை மெல்லிய துணியால் மூடி ரப்பர் பேண்ட் போடவும்.",
            "4. இருட்டான இடத்தில் 3 வாரங்கள் வைக்கவும். 2 நாட்களுக்கு ஒருமுறை மரக்கரண்டியால் கிளறிவிடவும்.",
            "5. 3 வாரங்களுக்குப் பின் தோல்களை வடிகட்டி எடுத்துவிட்டு, நீரை மீண்டும் 3 வாரங்கள் புளிக்க வைக்கவும்.",
            "6. புளிப்புச் சுவை வந்ததும் பாட்டிலில் அடைத்து பயன்படுத்தலாம். இதன் மேல் வளரும் படலம் இயற்கை நுண்ணுயிர் சத்துக்கள் நிறைந்தது."
        ],
        "safety_and_storage_en": "Ensure peels stay submerged below water to prevent surface mold. If white kahm yeast forms, simply skim it off; if green/black mold appears, discard and restart with fresh peels.",
        "safety_and_storage_ta": "பூஞ்சை பிடிக்காமல் இருக்க தோல்கள் தண்ணீருக்குள் மூழ்கியிருப்பது அவசியம். துணியை இறுக்கமாக கட்டவும்.",
        "scientific_rationale_en": "Two-stage bio-fermentation: wild Saccharomyces yeasts first convert apple sugars into ethanol; Acetobacter aceti bacteria then oxidize ethanol into beneficial acetic, malic, and lactic acids.",
        "scientific_rationale_ta": "ஈஸ்ட் மற்றும் அசிட்டோபாக்டர் நுண்ணுயிர்கள் சர்க்கரையை ஆப்பிள் வினிகர் அமிலமாக மாற்றி செரிமான நலனை மேம்படுத்துகின்றன."
    },
    {
        "id": "crispy_cinnamon_apple_chips",
        "title_en": "Crisp Cinnamon-Glazed Baked Apple Peel Chips",
        "title_ta": "மொறுமொறுப்பான ஆப்பிள் தோல் சினமன் சிப்ஸ்",
        "category": "culinary_gourmet",
        "category_name_en": "Artisanal Culinary Upcycling",
        "category_name_ta": "சமையல் கலை & புதுமையான உணவு தயாரிப்பு",
        "suitable_peels": ["apple"],
        "difficulty": "Easy",
        "prep_time_minutes": 5,
        "total_time": "25 Minutes",
        "estimated_output": "1 Large Bowl Crunchy Sweet Snack",
        "icon_name": "lunch_dining_rounded",
        "impact_summary_en": "Transforms discarded apple peel spirals into an addictive, dietary-fiber-rich zero-waste alternative to processed snacks.",
        "impact_summary_ta": "தூக்கி எறியப்படும் ஆப்பிள் தோலை நார்ச்சத்து மிகுந்த மொறுமொறுப்பான ஆரோக்கிய சிப்ஸாக மாற்றுகிறது.",
        "required_materials_en": [
            "150g Fresh apple peel ribbons (spiral peelings work best)",
            "1 tsp Melted virgin coconut oil or melted ghee",
            "1/2 tsp Ground Ceylon cinnamon",
            "1 tsp Coconut sugar or brown sugar",
            "1 Tiny pinch sea salt"
        ],
        "required_materials_ta": [
            "150 கிராம் புதிய ஆப்பிள் தோல்கள்",
            "1 தேக்கரண்டி தேங்காய் எண்ணெய் அல்லது நெய்",
            "1/2 தேக்கரண்டி இலவங்கப்பட்டை தூள்",
            "1 தேக்கரண்டி நாட்டுச்சர்க்கரை",
            "1 சிட்டிகை உப்பு"
        ],
        "step_by_step_instructions_en": [
            "1. Preheat oven to 150°C (300°F) or preheat air fryer to 140°C.",
            "2. Pat apple peels completely dry with clean kitchen towels (vital for maximum crispness).",
            "3. In a bowl, toss peel ribbons with melted coconut oil, cinnamon, sugar, and pinch of salt until lightly coated.",
            "4. Spread in a single layer on a parchment-lined baking sheet, ensuring peels do not heavily overlap.",
            "5. Bake for 18-22 minutes (or air-fry for 10-12 minutes), flipping once at the halfway point until edges curl and turn golden-crisp.",
            "6. Remove from oven and let cool completely on a wire rack for 5 minutes; chips will crisp up dramatically as they cool."
        ],
        "step_by_step_instructions_ta": [
            "1. அவனில் 150°C அல்லது ஏர்-பிரையரில் 140°C வெப்பநிலையை முன்கூட்டியே அமைக்கவும்.",
            "2. தோல்களை ஈரம் இல்லாமல் துடைத்துக் கொள்ளவும்.",
            "3. ஒரு பாத்திரத்தில் தேங்காய் எண்ணெய், இலவங்கப்பட்டை தூள், சர்க்கரை மற்றும் உப்பு சேர்த்து தோல்களுடன் கலக்கவும்.",
            "4. பேக்கிங் தட்டில் பரப்பி 18-22 நிமிடங்கள் பொன்னிறமாகும் வரை சுட்டு எடுக்கவும்.",
            "5. 5 நிமிடங்கள் ஆற வைக்கவும்; ஆறியவுடன் மிகவும் மொறுமொறுப்பாக மாறிவிடும்."
        ],
        "safety_and_storage_en": "Keep baking temperature below 160°C to prevent cinnamon and natural fruit fructose from burning. Store in an airtight container with a desiccant pack for up to 5 days.",
        "safety_and_storage_ta": "சர்க்கரை கருகாமல் இருக்க மிதமான சூட்டில் சுட வேண்டும். காற்றுப்புகாத டப்பாவில் 5 நாட்கள் வரை மொறுமொறுப்புடன் இருக்கும்.",
        "scientific_rationale_en": "Controlled dehydration caramelizes apple fructose while setting the pectin and cellulose matrix into a crispy lattice, delivering 3.7g of insoluble dietary fiber per serving.",
        "scientific_rationale_ta": "மிதமான வெப்பத்தில் உலர்த்தும்போது இயற்கை சர்க்கரை கேரமலைஸ் ஆகி பெக்டின் நார்ச்சத்துடன் மொறுமொறுப்பான அமைப்பை தருகிறது."
    },
    {
        "id": "natural_apple_pectin_extract",
        "title_en": "Homemade Natural Liquid Apple Pectin Extract",
        "title_ta": "வீட்டிலேயே தயாரிக்கும் இயற்கை ஆப்பிள் பெக்டின் ஜெல்லி திரவம்",
        "category": "biomaterials",
        "category_name_en": "Bio-Materials & Sustainable Crafts",
        "category_name_ta": "மக்கும் பொருட்கள் & கைவினைப் பொருட்கள்",
        "suitable_peels": ["apple"],
        "difficulty": "Moderate",
        "prep_time_minutes": 15,
        "total_time": "50 Minutes",
        "estimated_output": "300ml Concentrated Liquid Pectin",
        "icon_name": "science_rounded",
        "impact_summary_en": "Replaces synthetic commercial gelatin/pectin powders for jams, fruit jellies, and desserts using 100% kitchen peel waste.",
        "impact_summary_ta": "கடைகளில் விற்கும் ரசாயன ஜெல்லி பவுடருக்கு பதிலாக 100% இயற்கை பெக்டின் ஜாம் தயாரிப்பு திரவம்.",
        "required_materials_en": [
            "300g Fresh apple peels and cores (unpeeled tart apples work best)",
            "500ml Filtered water",
            "2 tbsp Fresh lemon juice (citric acid lowers pH to assist pectin solubility)",
            "Fine mesh sieve and cotton cheesecloth"
        ],
        "required_materials_ta": [
            "300 கிராம் ஆப்பிள் தோல்கள் மற்றும் நடுப்பகுதி",
            "500 மி.லி சுத்தமான தண்ணீர்",
            "2 மேஜைக்கரண்டி எலுமிச்சை சாறு",
            "வடிகட்டும் பருத்தி துணி"
        ],
        "step_by_step_instructions_en": [
            "1. Place apple peels and cores in a heavy-bottomed pot and pour in 500ml water and 2 tbsp lemon juice.",
            "2. Bring to a boil, then reduce heat to medium-low and simmer gently for 35-40 minutes until peels are mushy and liquid has halved.",
            "3. Pour mixture through a cheesecloth-lined sieve suspended over a glass bowl. Do not squeeze the cloth (squeezing causes cloudiness); let it gravity-drip for 30 minutes.",
            "4. Test your pectin strength: Add 1 tsp of cooled extract to 1 tbsp of rubbing alcohol in a small glass; if it forms a firm jelly blob, your pectin is potent!",
            "5. Store in sterilized glass jars in the fridge for 1 week or freeze in ice cube trays for up to 6 months for your jam-making days."
        ],
        "step_by_step_instructions_ta": [
            "1. ஒரு பாத்திரத்தில் ஆப்பிள் தோல்கள், 500 மி.லி தண்ணீர் மற்றும் எலுமிச்சை சாறு சேர்க்கவும்.",
            "2. மிதமான தீயில் 35-40 நிமிடங்கள் கொதிக்க வைக்கவும். தண்ணீர் பாதியாக குறையும் வரை கொதிக்க வேண்டும்.",
            "3. மெல்லிய துணியில் ஊற்றி வடிகட்டவும் (துணியை பிழியக்கூடாது, மெதுவாக சொட்ட விட வேண்டும்).",
            "4. வடிகட்டிய திரவம் ஜெல் போன்ற இயற்கை பெக்டின் ஆகும். இதனை ஜாம் அல்லது ஜெல்லி செய்யும்போது சேர்க்கலாம்.",
            "5. கண்ணாடி பாட்டிலில் அடைத்து 1 வாரம் குளிர்சாதன பெட்டியில் அல்லது 6 மாதங்கள் உறைநிலையில் வைக்கலாம்."
        ],
        "safety_and_storage_en": "Never consume the rubbing alcohol test portion (discard immediately). Store food-grade pectin extract strictly in clean sterilized airtight jars.",
        "safety_and_storage_ta": "பரிசோதனைக்கு பயன்படுத்திய ஆல்கஹால் பகுதியை உட்கொள்ளக்கூடாது. சுத்தமான பாட்டிலில் சேமிக்கவும்.",
        "scientific_rationale_en": "Acidic thermal hydrolysis cleaves protopectin present in apple middle lamella into water-soluble methylated polygalacturonic acid, which forms a 3D hydrogen-bonded gel network in the presence of sugar.",
        "scientific_rationale_ta": "ஆப்பிள் தோலில் உள்ள இயற்கை பெக்டின் அமில சூட்டில் கரைந்து சர்க்கரையுடன் சேரும்போது இயற்கையான ஜெல்லி அமைப்பை உருவாக்குகிறது."
    },
    {
        "id": "banana_peel_traditional_poriyal",
        "title_en": "Traditional South Indian Vazhaikkai Thol Poriyal & Chutney",
        "title_ta": "பாரம்பரிய வாழைக்காய் தோல் பொரியல் & துவையல்",
        "category": "culinary_gourmet",
        "category_name_en": "Artisanal Culinary Upcycling",
        "category_name_ta": "சமையல் கலை & புதுமையான உணவு தயாரிப்பு",
        "suitable_peels": ["green-plantain", "banana"],
        "difficulty": "Easy",
        "prep_time_minutes": 15,
        "total_time": "20 Minutes",
        "estimated_output": "3 Servings High-Fiber Poriyal",
        "icon_name": "soup_kitchen_rounded",
        "impact_summary_en": "Converts 200g of raw plantain skins into an authentic, prebiotic-dense stir-fry packed with resistant starch and potassium.",
        "impact_summary_ta": "200 கிராம் வாழைக்காய் தோலை சுவையான மற்றும் சத்தான பொரியலாக மாற்றுகிறது; நார்ச்சத்து நிறைந்தது.",
        "required_materials_en": [
            "200g Fresh washed raw plantain (green banana) peels, diced into 5mm cubes",
            "1 tbsp Cold-pressed coconut oil or sesame oil",
            "1/2 tsp Mustard seeds, 1 tsp urad dal, 1 sprig curry leaves",
            "2 Dry red chillies, 1/4 tsp turmeric powder, 1/2 tsp salt",
            "2 tbsp Freshly grated coconut"
        ],
        "required_materials_ta": [
            "200 கிராம் நறுக்கிய வாழைக்காய் தோல்",
            "1 மேஜைக்கரண்டி தேங்காய் எண்ணெய்",
            "1/2 தேக்கரண்டி கடுகு, 1 தேக்கரண்டி உளுத்தம் பருப்பு, கறிவேப்பிலை",
            "2 காய்ந்த மிளகாய், மஞ்சள் தூள், உப்பு",
            "2 மேஜைக்கரண்டி துருவிய தேங்காய்"
        ],
        "step_by_step_instructions_en": [
            "1. Boil diced banana peels in salted water with 1/4 tsp turmeric for 6-8 minutes until tender; drain well.",
            "2. Heat coconut oil in a skillet. Splutter mustard seeds, urad dal, dried chillies, and curry leaves.",
            "3. Add the boiled banana peel cubes and sauté for 4-5 minutes on medium heat.",
            "4. Toss with freshly grated coconut, adjust salt, and serve hot with steamed rice and sambar!"
        ],
        "step_by_step_instructions_ta": [
            "1. நறுக்கிய தோலை மஞ்சள் தூள் மற்றும் உப்பு சேர்த்த நீரில் 6-8 நிமிடங்கள் வேகவைத்து தண்ணீரை வடிக்கவும்.",
            "2. கடாயில் எண்ணெய் ஊற்றி கடுகு, உளுந்து, காய்ந்த மிளகாய், கறிவேப்பிலை தாளிக்கவும்.",
            "3. வெந்த வாழைக்காய் தோலை சேர்த்து 4-5 நிமிடங்கள் வதக்கவும்.",
            "4. துருவிய தேங்காய் சேர்த்து கிளறி இறக்கினால் சுவையான பொரியல் தயார்!"
        ],
        "safety_and_storage_en": "Always cook raw plantain peels thoroughly to neutralize astringent soluble tannins. Store cooked dish in the fridge for up to 2 days.",
        "safety_and_storage_ta": "வாழைக்காய் தோலை பச்சையாக சாப்பிடக்கூடாது; வேகவைத்து மட்டுமே சமைக்க வேண்டும்.",
        "scientific_rationale_en": "Boiling gelatinizes resistant starch (RS3) and hydrolyzes astringent polyphenols, unlocking gut-friendly prebiotic butyrate production during colonic fermentation.",
        "scientific_rationale_ta": "வேகவைக்கும் போது தோலில் உள்ள டானின் குறைந்து உடலுக்கு நன்மை செய்யும் ப்ரீபயாடிக் நார்ச்சத்தாக மாறுகிறது."
    },
    {
        "id": "banana_peel_potassium_fertilizer",
        "title_en": "High-Potassium Banana Peel Organic Floral Booster",
        "title_ta": "பொட்டாசியம் நிறைந்த வாழைப்பழத் தோல் இயற்கை பூ உரக்கரைசல்",
        "category": "garden_soil",
        "category_name_en": "Organic Gardening & Bio-Pots",
        "category_name_ta": "இயற்கை உரங்கள் & விதை நாற்றுக் கோப்பைகள்",
        "suitable_peels": ["green-plantain", "banana"],
        "difficulty": "Easy",
        "prep_time_minutes": 10,
        "total_time": "72 Hours Steeping",
        "estimated_output": "2 Litres Liquid Organic Potassium Fertilizer",
        "icon_name": "yard_rounded",
        "impact_summary_en": "Supplies pure ionic potassium and phosphorus to flowering plants, stimulating heavy flower budding in roses, jasmine, and tomatoes.",
        "impact_summary_ta": "ரோஜா, மல்லிகை மற்றும் தக்காளி செடிகள் அதிக பூக்கள் பூக்க உதவும் 100% இயற்கை பொட்டாசியம் உரம்.",
        "required_materials_en": [
            "Peels from 4-5 ripe or raw bananas (chopped into 2cm pieces)",
            "2 Litres Clean non-chlorinated water",
            "1 Clean glass jar or bucket with breathable cloth cover"
        ],
        "required_materials_ta": [
            "4-5 நறுக்கிய வாழைப்பழத் தோல்கள்",
            "2 லிட்டர் சுத்தமான தண்ணீர்",
            "துணியால் மூடக்கூடிய பாத்திரம்"
        ],
        "step_by_step_instructions_en": [
            "1. Place chopped banana peels into a glass jar or bucket.",
            "2. Pour 2 litres of water over peels and cover with a breathable cloth to keep insects out.",
            "3. Steep in shade for 48-72 hours, stirring once daily until water turns rich tea-brown.",
            "4. Strain liquid and dilute 1:1 with fresh water. Pour onto garden root soil once a week."
        ],
        "step_by_step_instructions_ta": [
            "1. நறுக்கிய தோல்களை பாத்திரத்தில் போட்டு 2 லிட்டர் தண்ணீர் ஊற்றவும்.",
            "2. துணியால் மூடி 3 நாட்கள் நிழலில் வைக்கவும்.",
            "3. வடிகட்டி சம அளவு தண்ணீருடன் கலந்து செடிகளின் வேர்களுக்கு வாரம் ஒருமுறை ஊற்றவும்."
        ],
        "safety_and_storage_en": "Use within 5 days of brewing. Bury spent peel scraps into garden soil or compost heap.",
        "safety_and_storage_ta": "தயாரித்த 5 நாட்களுக்குள் பயன்படுத்தவும். தோல்களை உரக்குழியில் போடலாம்.",
        "scientific_rationale_en": "Banana peel dry matter contains up to 42% potassium (K2O), which leaches readily into aqueous solution for rapid ionic root absorption.",
        "scientific_rationale_ta": "வாழைப்பழத் தோலில் உள்ள 42% பொட்டாசியம் நீரில் எளிதில் கரைந்து வேர்களுக்கு உடனடி சத்தாக கிடைக்கிறது."
    },
    {
        "id": "ridge_gourd_peel_thogayal",
        "title_en": "Artisanal Tamil Peerkangai Thol Thogayal (Ridge Gourd Peel Chutney)",
        "title_ta": "பாரம்பரிய பீர்க்கங்காய் தோல் துவையல்",
        "category": "culinary_gourmet",
        "category_name_en": "Artisanal Culinary Upcycling",
        "category_name_ta": "சமையல் கலை & புதுமையான உணவு தயாரிப்பு",
        "suitable_peels": ["ridge-gourd"],
        "difficulty": "Easy",
        "prep_time_minutes": 15,
        "total_time": "20 Minutes",
        "estimated_output": "4 Servings Nutrient-Dense Peel Chutney",
        "icon_name": "soup_kitchen_rounded",
        "impact_summary_en": "Rescues fibrous outer ridges of luffa gourds into a beloved South Indian zinc and dietary fiber-rich culinary accompaniment.",
        "impact_summary_ta": "பீர்க்கங்காய் தோலை சுவையான பாரம்பரிய துவையலாக மாற்றுகிறது; துத்தநாகம் மற்றும் நார்ச்சத்து மிகுந்தது.",
        "required_materials_en": [
            "250g Washed green ridge gourd peel trimmings (coarsely chopped)",
            "1.5 tbsp Sesame oil (gingelly oil)",
            "2 tbsp Chana dal (Bengal gram) & 1 tbsp Urad dal",
            "4-5 Whole dry red chillies & 1 pinch asafoetida (hing)",
            "1 Small marble-sized tamarind piece & 1/2 tsp salt"
        ],
        "required_materials_ta": [
            "250 கிராம் பீர்க்கங்காய் தோல்",
            "1.5 மேஜைக்கரண்டி நல்லெண்ணெய்",
            "2 மேஜைக்கரண்டி கடலைப்பருப்பு, 1 மேஜைக்கரண்டி உளுத்தம் பருப்பு",
            "4 காய்ந்த மிளகாய், பெருங்காயம்",
            "சிறிய எலுமிச்சை அளவு புளி, உப்பு"
        ],
        "step_by_step_instructions_en": [
            "1. Heat 1 tbsp oil in a pan. Roast chana dal, urad dal, red chillies, and asafoetida until golden brown; transfer to plate.",
            "2. In the same pan, add remaining oil and sauté chopped ridge gourd peels on medium heat for 6-8 minutes until tender and moisture evaporates.",
            "3. Allow both roasted dals and cooked peels to cool to room temperature.",
            "4. Grind in a mixer with tamarind and salt with very minimal water into a thick, coarse savory thogayal.",
            "5. Serve mixed with hot steamed rice and sesame oil or as a side for idli and dosa!"
        ],
        "step_by_step_instructions_ta": [
            "1. கடாயில் எண்ணெய் ஊற்றி கடலைப்பருப்பு, உளுந்து, காய்ந்த மிளகாய், பெருங்காயம் வறுத்து தனியாக வைக்கவும்.",
            "2. அதே கடாயில் பீர்க்கங்காய் தோலை சேர்த்து 6-8 நிமிடங்கள் பச்சை வாசனை போகும் வரை வதக்கவும்.",
            "3. ஆறிய பின் புளி, உப்பு சேர்த்து மிக்ஸியில் கெட்டியாக அரைக்கவும்.",
            "4. சூடான சாதத்தில் நல்லெண்ணெய் ஊற்றி இந்த துவையலை கலந்து சாப்பிட சுவை அற்புதம்!"
        ],
        "safety_and_storage_en": "Taste peel piece before cooking; if gourd is intensely bitter due to cucurbitacins, discard entirely. Store chutney in fridge for up to 4 days.",
        "safety_and_storage_ta": "கசப்பு சுவை கொண்ட காய்களை பயன்படுத்தக்கூடாது. ஃப்ரிட்ஜில் 4 நாட்கள் வரை கெடாமல் இருக்கும்.",
        "scientific_rationale_en": "Outer epidermal ridges are concentrated in insoluble cellulose, hemicellulose, and bioactive chlorophyllides that stimulate peristalsis and regulate bowel motility.",
        "scientific_rationale_ta": "பீர்க்கங்காய் தோலில் உள்ள நார்ச்சத்து செரிமானத்தை சீராக்கி மலச்சிக்கலை போக்குகிறது."
    },
    {
        "id": "bottle_gourd_peel_crispy_fry",
        "title_en": "Crispy Tempered Bottle Gourd Peel Stir-Fry (Sorakkai Thol Varuval)",
        "title_ta": "மொறுமொறு சுரைக்காய் தோல் வறுவல்",
        "category": "culinary_gourmet",
        "category_name_en": "Artisanal Culinary Upcycling",
        "category_name_ta": "சமையல் கலை & புதுமையான உணவு தயாரிப்பு",
        "suitable_peels": ["bottle-gourd"],
        "difficulty": "Easy",
        "prep_time_minutes": 10,
        "total_time": "15 Minutes",
        "estimated_output": "2 Servings Crispy Side Dish",
        "icon_name": "lunch_dining_rounded",
        "impact_summary_en": "Prevents disposal of tender bottle gourd skins by turning them into a crunchy, cooling cumin-tempered side dish.",
        "impact_summary_ta": "சுரைக்காய் தோலை மொறுமொறுப்பான வறுவலாக மாற்றி உடலை குளிர்ச்சியாக வைக்க உதவுகிறது.",
        "required_materials_en": [
            "200g Tender green bottle gourd peels (shredded finely into matchsticks)",
            "1 tbsp Mustard oil or peanut oil",
            "1/2 tsp Cumin seeds & 1/2 tsp turmeric powder",
            "1/2 tsp Kashmiri chilli powder & 1/2 tsp salt"
        ],
        "required_materials_ta": [
            "200 கிராம் மெல்லியதாக நறுக்கிய சுரைக்காய் தோல்",
            "1 மேஜைக்கரண்டி எண்ணெய்",
            "1/2 தேக்கரண்டி சீரகம், மஞ்சள் தூள்",
            "மிளகாய்த்தூள், உப்பு"
        ],
        "step_by_step_instructions_en": [
            "1. Shred washed bottle gourd peels into thin matchsticks.",
            "2. Heat oil in a pan, add cumin seeds until fragrant.",
            "3. Add shredded peels, turmeric, chilli powder, and salt.",
            "4. Sauté on medium-high heat for 7-9 minutes without covering until edges are blistered and crisp."
        ],
        "step_by_step_instructions_ta": [
            "1. சுரைக்காய் தோலை மெல்லிய நீளத் துண்டுகளாக நறுக்கவும்.",
            "2. கடாயில் எண்ணெய் ஊற்றி சீரகம் தாளிக்கவும்.",
            "3. நறுக்கிய தோல், மஞ்சள் தூள், மிளகாய்த்தூள், உப்பு சேர்க்கவும்.",
            "4. மூடி போடாமல் 7-9 நிமிடங்கள் மொறுமொறுப்பாகும் வரை வதக்கி பரிமாறவும்."
        ],
        "safety_and_storage_en": "CRITICAL: If the bottle gourd peel has an intensely bitter taste, discard immediately (toxic cucurbitacin poisoning hazard).",
        "safety_and_storage_ta": "கசப்பு சுவை கொண்ட சுரைக்காயை ஒருபோதும் பயன்படுத்தக்கூடாது.",
        "scientific_rationale_en": "Bottle gourd peel holds high moisture and water-soluble minerals that promote hydration and cellular fluid equilibrium.",
        "scientific_rationale_ta": "இதில் உள்ள தாதுக்கள் உடலின் நீர்ச்சத்தை சமநிலையில் வைக்க உதவுகின்றன."
    },
    {
        "id": "bitter_gourd_peel_crisps",
        "title_en": "Sun-Dried Spiced Bitter Gourd Peel Diabetic Crisps",
        "title_ta": "உலர்ந்த பாகற்காய் தோல் நீரிழிவு தடுப்பு மொறுமொறு சிப்ஸ்",
        "category": "culinary_gourmet",
        "category_name_en": "Artisanal Culinary Upcycling",
        "category_name_ta": "சமையல் கலை & புதுமையான உணவு தயாரிப்பு",
        "suitable_peels": ["bitter-gourd"],
        "difficulty": "Easy",
        "prep_time_minutes": 15,
        "total_time": "2 Days Sun-Drying",
        "estimated_output": "1 Jar Healthy Crunchy Diabetic Wafers",
        "icon_name": "lunch_dining_rounded",
        "impact_summary_en": "Diverts rough warty bitter gourd skins into a medicinal, crunchy diabetic snack that supports glucose metabolic health.",
        "impact_summary_ta": "பாகற்காய் தோலை ரத்த சர்க்கரையை கட்டுப்படுத்தும் சுவையான வற்றலாக மாற்றுகிறது.",
        "required_materials_en": [
            "250g Outer scraped ridged skin of bitter gourds (karela)",
            "1 tsp Rock salt & 1/2 tsp turmeric powder",
            "1 tsp Fresh lemon juice",
            "1/2 tsp Roasted cumin powder & 1/2 tsp amchur (dry mango powder)"
        ],
        "required_materials_ta": [
            "250 கிராம் பாகற்காய் வெளிப்புற தோல்",
            "1 தேக்கரண்டி கல் உப்பு, மஞ்சள் தூள்",
            "1 தேக்கரண்டி எலுமிச்சை சாறு",
            "சீரகத்தூள், மாங்காய்த்தூள்"
        ],
        "step_by_step_instructions_en": [
            "1. Toss scraped bitter gourd peels with salt, turmeric, and lemon juice; let sit for 20 minutes (this draws out excess sharp bitterness).",
            "2. Gently squeeze out the bitter liquid and spread peels in a single layer on a drying tray.",
            "3. Sun-dry for 2 days until bone-dry and brittle.",
            "4. Toss with cumin powder and amchur. Store in an airtight jar. Air-fry or roast with a drop of oil for 3 minutes for a guilt-free crunch!"
        ],
        "step_by_step_instructions_ta": [
            "1. தோலில் உப்பு, மஞ்சள் தூள், எலுமிச்சை சாறு கலந்து 20 நிமிடங்கள் வைக்கவும்.",
            "2. கசப்பு நீரை பிழிந்து எடுத்துவிட்டு தட்டில் பரப்பி 2 நாட்கள் வெயிலில் காய வைக்கவும்.",
            "3. காய்ந்த வற்றலை பாட்டிலில் சேமிக்கவும். சாப்பிடும் போது லேசாக வறுத்து சாப்பிடலாம்."
        ],
        "safety_and_storage_en": "Individuals with glucose-6-phosphate dehydrogenase (G6PD) deficiency or pregnant individuals should consume bitter gourd sparingly.",
        "safety_and_storage_ta": "கர்ப்பிணிகள் பாகற்காயை அதிகமாக உட்கொள்வதை தவிர்க்க வேண்டும்.",
        "scientific_rationale_en": "Momordicin and charantin saponins in the outer exocarp enhance peripheral glucose uptake and activate AMPK metabolic pathways.",
        "scientific_rationale_ta": "பாகற்காய் தோலில் உள்ள சாரின்டின் ரத்தத்தில் சர்க்கரை அளவை சீராக வைக்க உதவுகிறது."
    },
    {
        "id": "tomato_skin_lycopene_powder",
        "title_en": "Sun-Dried Lycopene-Rich Tomato Skin Flakes & Umami Powder",
        "title_ta": "சூரிய ஒளியில் உலர்த்திய தக்காளி தோல் லைகோபீன் பவுடர்",
        "category": "culinary_gourmet",
        "category_name_en": "Artisanal Culinary Upcycling",
        "category_name_ta": "சமையல் கலை & புதுமையான உணவு தயாரிப்பு",
        "suitable_peels": ["tomato"],
        "difficulty": "Easy",
        "prep_time_minutes": 10,
        "total_time": "1-2 Days Sun-Drying",
        "estimated_output": "100g Pure Red Lycopene Seasoning",
        "icon_name": "soup_kitchen_rounded",
        "impact_summary_en": "Recovers 100% of blanching tomato skins into a chef-grade, brilliant ruby seasoning powder bursting with bioavailable lycopene.",
        "impact_summary_ta": "தக்காளி தோலை வீணாக்காமல் சக்திவாய்ந்த ஆன்டிஆக்ஸிடன்ட் சூப் பவுடராக மாற்றுகிறது.",
        "required_materials_en": [
            "Skins from 1-2 kg blanched ripe red tomatoes",
            "1/2 tsp Sea salt & 1/4 tsp dried oregano or garlic powder",
            "Spice grinder"
        ],
        "required_materials_ta": [
            "தக்காளி தோல்கள்",
            "உப்பு, பூண்டுத்தூள்",
            "மிக்ஸி"
        ],
        "step_by_step_instructions_en": [
            "1. Lay discarded tomato peel skins in a single flat layer on parchment paper.",
            "2. Sun-dry for 1-2 days (or bake at 80°C for 3 hours) until paper-crisp and shatterable.",
            "3. Mill in a spice grinder with sea salt and garlic powder into ruby-red umami dust.",
            "4. Sprinkle over pizzas, pasta, soups, salads, and curries for a blast of savory brightness and color!"
        ],
        "step_by_step_instructions_ta": [
            "1. தக்காளி தோல்களை தட்டில் பரப்பி வெயிலில் 2 நாட்கள் மொறுமொறுப்பாகும் வரை உலர்த்தவும்.",
            "2. காய்ந்த தோல்களுடன் உப்பு சேர்த்து மிக்ஸியில் பொடியாக அரைக்கவும்.",
            "3. சூப், சாம்பார் மற்றும் கிரேவிகளில் தூவி பயன்படுத்தினால் நிறமும் சுவையும் அதிகரிக்கும்!"
        ],
        "safety_and_storage_en": "Store in a dry glass jar away from moisture; retains vibrant red hue for up to 6 months.",
        "safety_and_storage_ta": "ஈரப்பதம் இல்லாத பாட்டிலில் 6 மாதங்கள் வரை வைத்து பயன்படுத்தலாம்.",
        "scientific_rationale_en": "Tomato epidermal peel holds up to 80% of total fruit lycopene; dehydration concentrates all-trans-lycopene isomers by a factor of 10x.",
        "scientific_rationale_ta": "தக்காளி தோலில் 80% லைகோபீன் சத்து உள்ளது; இது இதய ஆரோக்கியத்திற்கு மிகவும் நல்லது."
    },
    {
        "id": "ginger_garlic_peel_immune_kashayam",
        "title_en": "Ginger & Garlic Husk Botanical Immune-Defense Kashayam",
        "title_ta": "இஞ்சி & பூண்டு தோல் மூலிகை நோய் எதிர்ப்பு கஷாயம்",
        "category": "natural_wellness",
        "category_name_en": "Natural Wellness & Home Apothecary",
        "category_name_ta": "இயற்கை மருத்துவம் & வீட்டு நலம்",
        "suitable_peels": ["ginger", "garlic"],
        "difficulty": "Easy",
        "prep_time_minutes": 10,
        "total_time": "20 Minutes",
        "estimated_output": "3 Servings Herbal Decoction",
        "icon_name": "spa_rounded",
        "impact_summary_en": "Extracts anti-inflammatory gingerols and antimicrobial allicin derivatives from root trimmings into a soothing Ayurvedic decoction.",
        "impact_summary_ta": "இஞ்சி மற்றும் பூண்டு தோலை சளி மற்றும் தொண்டை வலியை குணப்படுத்தும் மூலிகை கஷாயமாக மாற்றுகிறது.",
        "required_materials_en": [
            "50g Clean scrubbed ginger peels & papery garlic skins",
            "600ml Water",
            "1/2 tsp Crushed black peppercorns & 1/2 tsp cumin seeds",
            "5-6 Fresh holy basil (tulsi) leaves & 1 tbsp palm jaggery"
        ],
        "required_materials_ta": [
            "50 கிராம் நன்கு கழுவிய இஞ்சி மற்றும் பூண்டு தோல்கள்",
            "600 மி.லி தண்ணீர்",
            "மிளகு, சீரகம்",
            "துளசி இலைகள், பனங்கற்கண்டு"
        ],
        "step_by_step_instructions_en": [
            "1. Wash ginger and garlic peels carefully to remove microscopic soil traces.",
            "2. In a saucepan, bring water to boil with peels, crushed pepper, cumin, and tulsi leaves.",
            "3. Simmer gently for 12-15 minutes until liquid is reduced by half.",
            "4. Strain into cups, sweeten with palm jaggery, and sip warm to soothe colds, throat irritation, and sluggish digestion."
        ],
        "step_by_step_instructions_ta": [
            "1. இஞ்சி மற்றும் பூண்டு தோல்களை நன்கு கழுவவும்.",
            "2. பாத்திரத்தில் தண்ணீருடன் தோல்கள், மிளகு, சீரகம், துளசி சேர்த்து கொதிக்க வைக்கவும்.",
            "3. நீர் பாதியாக குறையும் வரை கொதிக்க வைத்து வடிகட்டவும்.",
            "4. பனங்கற்கண்டு சேர்த்து சூடாக குடித்தால் சளி, இருமல் உடனே தீரும்!"
        ],
        "safety_and_storage_en": "Scrub root ginger peel thoroughly before use. Freshly prepare daily for maximum volatile therapeutic potency.",
        "safety_and_storage_ta": "மண்ணை நீக்க இஞ்சி தோலை நன்கு கழுவுவது அவசியம்.",
        "scientific_rationale_en": "Sub-epidermal root layers hold high concentrations of phenolic gingerols and shogaols, delivering vasodilation and immunomodulatory activity.",
        "scientific_rationale_ta": "இஞ்சி தோலில் உள்ள ஜிஞ்சரால் தொண்டை அழற்சியை போக்கி நோய் எதிர்ப்பு சக்தியை அதிகரிக்கிறது."
    },
    {
        "id": "candied_citrus_peel_delight",
        "title_en": "Artisanal Candied Orange & Citrus Peel Ribbons",
        "title_ta": "இனிப்பு பாகில் தோய்த்த ஆரஞ்சு & சிட்ரஸ் தோல் மிட்டாய்",
        "category": "culinary_gourmet",
        "category_name_en": "Artisanal Culinary Upcycling",
        "category_name_ta": "சமையல் கலை & புதுமையான உணவு தயாரிப்பு",
        "suitable_peels": ["orange"],
        "difficulty": "Moderate",
        "prep_time_minutes": 20,
        "total_time": "45 Minutes",
        "estimated_output": "150g Zesty Sweet Peel Confections",
        "icon_name": "lunch_dining_rounded",
        "impact_summary_en": "Upcycles aromatic citrus flavedo into zesty, vitamin C and bioflavonoid-packed gourmet sweets, cakes, and pastry garnishes.",
        "impact_summary_ta": "ஆரஞ்சு தோலை சுவையான இயற்கை மிட்டாயாக மாற்றுகிறது; வைட்டமின் சி மிகுந்தது.",
        "required_materials_en": [
            "Peels from 3-4 clean oranges or lemons (cut into uniform 5mm strips)",
            "1 cup Water & 1 cup Raw cane sugar",
            "Extra sugar for crystal coating"
        ],
        "required_materials_ta": [
            "3-4 ஆரஞ்சு பழங்களின் தோல்கள் (நீளமாக நறுக்கியது)",
            "1 கப் தண்ணீர், 1 கப் நாட்டுச்சர்க்கரை"
        ],
        "step_by_step_instructions_en": [
            "1. Blanch sliced orange peels in boiling water for 5 minutes; drain and repeat twice (this removes excess bitterness).",
            "2. In a saucepan, dissolve 1 cup sugar in 1 cup water and bring to a simmer.",
            "3. Add blanched peels and simmer gently on low heat for 35-40 minutes until translucent and syrup is thick.",
            "4. Lift peel strips with tongs, roll in sugar, and dry on a wire rack for 4 hours until crystallized and chewy!"
        ],
        "step_by_step_instructions_ta": [
            "1. ஆரஞ்சு தோல்களை கொதிநீரில் 5 நிமிடம் போட்டு தண்ணீரை வடிக்கவும் (கசப்பு நீங்க உதவும்).",
            "2. பாத்திரத்தில் சர்க்கரையும் தண்ணீரும் சேர்த்து பாகு காய்ச்சவும்.",
            "3. தோல்களை சேர்த்து 35 நிமிடங்கள் குறைந்த தீயில் கொதிக்க வைக்கவும்.",
            "4. தோல்களை எடுத்து சர்க்கரையில் புரட்டி உலர்த்தினால் சுவையான ஆரஞ்சு தோல் மிட்டாய் தயார்!"
        ],
        "safety_and_storage_en": "Use pesticide-free unwaxed citrus where possible. Store candied peels in an airtight container for up to 3 months.",
        "safety_and_storage_ta": "சுத்தமான பாட்டிலில் அடைத்து 3 மாதங்கள் வரை வைத்து சாப்பிடலாம்.",
        "scientific_rationale_en": "Osmotic sugar infusion displaces moisture in peel flavedo cavities, preserving natural d-limonene terpenes and hesperidin bioflavonoids against microbial decay.",
        "scientific_rationale_ta": "சர்க்கரைப் பாகு தோலின் ஈரப்பதத்தை நீக்கி நீண்ட நாட்கள் கெடாமல் பாதுகாக்கிறது."
    },
    {
        "id": "quercetin_onion_skin_broth",
        "title_en": "Pure Quercetin-Concentrated Golden Onion Skin Healing Broth",
        "title_ta": "குவர்செடின் நிறைந்த தங்க வெங்காயத் தோல் மருத்துவ சூப்",
        "category": "natural_wellness",
        "category_name_en": "Natural Wellness & Home Apothecary",
        "category_name_ta": "இயற்கை மருத்துவம் & வீட்டு நலம்",
        "suitable_peels": ["onion", "shallots"],
        "difficulty": "Easy",
        "prep_time_minutes": 10,
        "total_time": "30 Minutes",
        "estimated_output": "4 Servings Anti-Inflammatory Broth",
        "icon_name": "soup_kitchen_rounded",
        "impact_summary_en": "Harnesses dry papery onion skins into an exceptionally potent antioxidant broth containing up to 48x more quercetin than the inner flesh.",
        "impact_summary_ta": "வெங்காயத்தின் உள்பகுதியை விட 48 மடங்கு அதிக ஆன்டிஆக்ஸிடன்ட் கொண்ட இயற்கை மருத்துவ சூப்.",
        "required_materials_en": [
            "Dry papery outer skins of 5-6 clean yellow/red onions (free of mold)",
            "1 Litre Filtered water",
            "2 Cloves garlic (crushed), 1 slice fresh ginger, 1 sprig fresh coriander",
            "1/2 tsp Himalayan salt & a squeeze of fresh lemon juice"
        ],
        "required_materials_ta": [
            "5-6 வெங்காயங்களின் சுத்தமான காய்ந்த தோல்கள்",
            "1 லிட்டர் தண்ணீர்",
            "பூண்டு, இஞ்சி, கொத்தமல்லி",
            "உப்பு, எலுமிச்சை சாறு"
        ],
        "step_by_step_instructions_en": [
            "1. Rinse dry onion skins quickly under cold water to remove dust.",
            "2. Add onion skins, crushed garlic, and ginger to 1 litre of water in a pot.",
            "3. Simmer on low-medium flame for 25-30 minutes until the broth turns rich golden-amber.",
            "4. Strain the onion skins out through a fine sieve (inedible fiber removed).",
            "5. Season with salt, lemon juice, and fresh coriander; sip warm as a soothing anti-inflammatory tonic!"
        ],
        "step_by_step_instructions_ta": [
            "1. வெங்காயத் தோல்களை தண்ணீரில் லேசாக கழுவவும்.",
            "2. பாத்திரத்தில் தண்ணீருடன் தோல்கள், பூண்டு, இஞ்சி சேர்த்து 25 நிமிடங்கள் கொதிக்க வைக்கவும்.",
            "3. தண்ணீர் தங்க நிறமாக மாறியதும் தோல்களை வடிகட்டி தனியாக எடுக்கவும்.",
            "4. உப்பு, எலுமிச்சை சாறு சேர்த்து சூடாக பருகினால் உடலுக்கு அளப்பரிய நோய் எதிர்ப்பு சக்தி கிடைக்கும்!"
        ],
        "safety_and_storage_en": "Always strain and discard papery skins before drinking; papery skins are fibrous and indigestible. Store strained broth refrigerated for up to 4 days.",
        "safety_and_storage_ta": "தோலை சாப்பிடக்கூடாது; வடிகட்டிய நீரை மட்டுமே பருக வேண்டும்.",
        "scientific_rationale_en": "Quercetin aglycone (3,3',4',5,7-pentahydroxyflavone) is concentrated in the dry outer protective scale leaves to defend against UV and pathogens, acting as a potent free-radical scavenger.",
        "scientific_rationale_ta": "வெங்காயத் தோலில் உள்ள குவர்செடின் உடலின் நோய் எதிர்ப்பு மண்டலத்தை பலப்படுத்துகிறது."
    }
]


def get_all_creations(
    category: Optional[str] = None,
    vegetable_slug: Optional[str] = None,
    difficulty: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Filters creations based on optional category, vegetable slug, or difficulty."""
    results = WASTE_CREATIONS
    if category and category.lower() != "all":
        results = [c for c in results if c["category"] == category.lower()]
    if difficulty and difficulty.lower() != "all":
        results = [c for c in results if c["difficulty"].lower() == difficulty.lower()]
    if vegetable_slug and vegetable_slug.lower() not in ("all", "mixed"):
        slug = vegetable_slug.strip().lower()
        slug_aliases = {slug}
        if slug in ("green-plantain", "raw-banana", "banana"):
            slug_aliases.update(["green-plantain", "banana", "raw-banana"])
        if slug in ("orange", "citrus", "lemon"):
            slug_aliases.update(["orange", "citrus", "lemon"])
        if slug in ("onion", "shallots"):
            slug_aliases.update(["onion", "shallots"])

        results = [
            c for c in results
            if any(alias in c["suitable_peels"] for alias in slug_aliases)
            or "all_vegetables" in c["suitable_peels"]
            or "mixed" in c["suitable_peels"]
        ]
    return results


def get_creation_by_id(creation_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves a single creation item by ID."""
    for c in WASTE_CREATIONS:
        if c["id"] == creation_id.strip():
            return c
    return None
