import logging
from sqlalchemy.orm import Session
import app.db.base
from app.models.vegetable import Vegetable
from app.models.nutrient import PeelYieldRatio, DailyReferenceIntake, ScientificSource

logger = logging.getLogger(__name__)

# Empirical Peel Yield and Moisture/Dry-Matter characteristics for all 50 botanical vegetables
# Based on ICMR-NIN Indian Food Composition Tables (IFCT), USDA FoodData Central, and peer-reviewed literature.
PEEL_YIELD_DATA = [
    # 1. Carrot
    {
        "slug": "carrot",
        "avg": 12.0, "min": 8.5, "max": 16.0, "moisture": 88.2, "dry": 11.8, "factor": 0.14,
        "notes_en": "Carrot peel and outer periderm layer contain up to 2.5x higher concentrations of carotenoids (beta-carotene) and polyacetylenes (falcarinol) than the inner core parenchyma.",
        "notes_ta": "கேரட் தோலில் உள் பகுதியை விட 2.5 மடங்கு அதிக பீட்டா கரோட்டின் மற்றும் அழற்சி எதிர்ப்பு பாலிஅசிட்டிலின்கள் உள்ளன."
    },
    # 2. Potato
    {
        "slug": "potato",
        "avg": 11.5, "min": 8.0, "max": 15.0, "moisture": 81.0, "dry": 19.0, "factor": 0.18,
        "notes_en": "Potato peel periderm possesses 70% of the tuber's total phenolic compounds (primarily chlorogenic acid) and 3x more insoluble fiber than peeled potato flesh.",
        "notes_ta": "உருளைக்கிழங்கு தோலில் கிழங்கின் மொத்த பினாலிக் சேர்மங்களில் 70% மற்றும் 3 மடங்கு கூடுதல் நார்ச்சத்து உள்ளது."
    },
    # 3. Sweet Potato
    {
        "slug": "sweet-potato",
        "avg": 12.5, "min": 9.0, "max": 16.5, "moisture": 77.0, "dry": 23.0, "factor": 0.20,
        "notes_en": "Sweet potato peel is exceptionally rich in anthocyanins (in purple varieties) and dietary fiber, yielding 4.2g fiber per 100g compared to 2.5g in boiled flesh.",
        "notes_ta": "சர்க்கரைவள்ளிக் கிழங்கு தோலில் உள் பகுதியை விட அதிக நார்ச்சத்து மற்றும் ஆந்தோசயனின் ஆக்ஸிஜனேற்றிகள் உள்ளன."
    },
    # 4. Beetroot
    {
        "slug": "beetroot",
        "avg": 14.0, "min": 10.0, "max": 18.0, "moisture": 86.5, "dry": 13.5, "factor": 0.15,
        "notes_en": "Beetroot peel exhibits the highest concentration of betalains (betacyanin pigment) and total phenolic acids, almost 3x higher than core root flesh.",
        "notes_ta": "பீட்ரூட் தோலில் உள் பகுதியை விட 3 மடங்கு அதிக பீட்டாலைன் நிறமிகள் மற்றும் ஆக்ஸிஜனேற்றிகள் உள்ளன."
    },
    # 5. Radish
    {
        "slug": "radish",
        "avg": 13.0, "min": 9.5, "max": 17.0, "moisture": 93.5, "dry": 6.5, "factor": 0.10,
        "notes_en": "Radish epidermal skin contains pungent glucosinolates and allyl isothiocyanates providing potent antimicrobial defense and higher ascorbic acid than root core.",
        "notes_ta": "முள்ளங்கி தோலில் காரத்தன்மை கொண்ட குளுக்கோசினோலேட்டுகள் மற்றும் அதிக வைட்டமின் சி உள்ளது."
    },
    # 6. Turnip
    {
        "slug": "turnip",
        "avg": 13.5, "min": 10.0, "max": 17.5, "moisture": 91.0, "dry": 9.0, "factor": 0.12,
        "notes_en": "Turnip skin contains glucosinolates, sulfur compounds, and dietary fiber that are 1.8x more concentrated than in the fleshy storage root.",
        "notes_ta": "டர்னிப் தோலில் சல்பர் சேர்மங்கள் மற்றும் நார்ச்சத்து அதிகம் உள்ளன."
    },
    # 7. Parsnip
    {
        "slug": "parsnip",
        "avg": 14.0, "min": 10.5, "max": 18.0, "moisture": 79.5, "dry": 20.5, "factor": 0.19,
        "notes_en": "Parsnip peel contains aromatic polyacetylenes and insoluble lignin fiber 2x higher than root parenchyma.",
        "notes_ta": "பார்ஸ்னிப் தோலில் பாலிஅசிட்டிலின்கள் மற்றும் லிக்னின் நார்ச்சத்து அதிகம் உள்ளன."
    },
    # 8. Cassava / Tapioca
    {
        "slug": "cassava-tapioca",
        "avg": 22.0, "min": 16.0, "max": 28.0, "moisture": 62.0, "dry": 38.0, "factor": 0.32,
        "notes_en": "Cassava peel (periderm + cortex) represents ~20-25% tuber weight; high in starch and fiber, but strictly non-edible raw due to cyanogenic glucosides. Ideal for biochar and composting.",
        "notes_ta": "மரவள்ளிக்கிழங்கு தோலில் சயனோஜெனிக் நச்சு இருப்பதால் பச்சையாக உண்ணக்கூடாது; உரம் மற்றும் உயிரி எரிபொருளுக்கு உகந்தது."
    },
    # 9. Elephant Foot Yam
    {
        "slug": "elephant-foot-yam",
        "avg": 24.0, "min": 18.0, "max": 30.0, "moisture": 74.0, "dry": 26.0, "factor": 0.22,
        "notes_en": "Yam outer rind/bark is high in structural lignocellulose and calcium oxalate raphides. Excellent compost feedstock or bio-adsorbent.",
        "notes_ta": "சேனைக்கிழங்கு தோலில் கால்சியம் ஆக்சலேட் மற்றும் நார்ச்சத்து அதிகம்; உரம் தயாரிக்க சிறந்தது."
    },
    # 10. Greater Yam
    {
        "slug": "greater-yam",
        "avg": 20.0, "min": 15.0, "max": 26.0, "moisture": 70.0, "dry": 30.0, "factor": 0.25,
        "notes_en": "Greater yam thick peel is rich in resistant starch and tannins.",
        "notes_ta": "காச்சில் கிழங்கு தோலில் டானின் மற்றும் ஸ்டார்ச் நிறைந்துள்ளன."
    },
    # 11. Taro / Colocasia
    {
        "slug": "taro-colocasia",
        "avg": 18.0, "min": 13.0, "max": 23.0, "moisture": 73.0, "dry": 27.0, "factor": 0.24,
        "notes_en": "Colocasia corm peel is high in mucilage and arabinogalactans; requires prolonged boiling/cooking to deactivate oxalate needles.",
        "notes_ta": "சேப்பங்கிழங்கு தோலில் வழவழப்பு மற்றும் ஆக்சலேட் உள்ளது; நன்கு சமைத்து பயன்படுத்த வேண்டும்."
    },
    # 12. Jerusalem Artichoke
    {
        "slug": "jerusalem-artichoke",
        "avg": 12.0, "min": 8.0, "max": 16.0, "moisture": 78.0, "dry": 22.0, "factor": 0.18,
        "notes_en": "Skin contains high inulin prebiotic fructooligosaccharides supporting gut microbiota.",
        "notes_ta": "ஜெருசலேம் கூனைப்பூ தோலில் குடல் நலனுக்கு உதவும் இன்யூலின் நார்ச்சத்து உள்ளது."
    },
    # 13. Pumpkin
    {
        "slug": "pumpkin",
        "avg": 22.0, "min": 16.0, "max": 28.0, "moisture": 89.0, "dry": 11.0, "factor": 0.15,
        "notes_en": "Pumpkin thick rind contains 2.8x more lutein and beta-carotene and double the pectin fiber of inner pumpkin pulp.",
        "notes_ta": "பூசணிக்காய் தோலில் சதைப்பகுதியை விட 2.8 மடங்கு அதிக லுடீன் மற்றும் பெக்டின் நார்ச்சத்து உள்ளது."
    },
    # 14. Bottle Gourd
    {
        "slug": "bottle-gourd",
        "avg": 14.0, "min": 10.0, "max": 19.0, "moisture": 94.0, "dry": 6.0, "factor": 0.10,
        "notes_en": "Bottle gourd peel is tender and completely edible when non-bitter, offering 3.1g insoluble fiber per 100g and high potassium.",
        "notes_ta": "சுரைக்காய் தோல் மென்மையானது, கசப்பில்லாத போது உண்ணக்கூடியது; அதிக நார்ச்சத்து மற்றும் பொட்டாசியம் நிறைந்தது."
    },
    # 15. Bitter Gourd
    {
        "slug": "bitter-gourd",
        "avg": 16.0, "min": 11.0, "max": 22.0, "moisture": 91.5, "dry": 8.5, "factor": 0.12,
        "notes_en": "Bitter gourd outer warty ridges contain highest concentrations of momordicines, charantin, and polypeptide-p active anti-diabetic compounds.",
        "notes_ta": "பாகற்காய் மேல்தோல் வரிம்புகளில் சரண்டின் மற்றும் நீரிழிவு எதிர்ப்பு மோர்மோர்டிசின் மிக அதிகம்."
    },
    # 16. Ridge Gourd
    {
        "slug": "ridge-gourd",
        "avg": 22.0, "min": 17.0, "max": 28.0, "moisture": 93.0, "dry": 7.0, "factor": 0.11,
        "notes_en": "Ridge gourd peel is a prized culinary ingredient in Tamil cuisine (Peerkangai Thuvaiyal), featuring 3.8g fiber and 38mg calcium per 100g.",
        "notes_ta": "பீர்க்கங்காய் தோல் துவையலுக்கு மிக உகந்தது; 100 கிராமுக்கு 3.8 கிராம் நார்ச்சத்து மற்றும் 38 மிகி கால்சியம் கொண்டது."
    },
    # 17. Snake Gourd
    {
        "slug": "snake-gourd",
        "avg": 12.0, "min": 8.0, "max": 16.0, "moisture": 94.5, "dry": 5.5, "factor": 0.09,
        "notes_en": "Snake gourd white-striped epidermal layer is rich in flavonoids and water-soluble minerals.",
        "notes_ta": "புடலங்காய் தோலில் நீர்ச்சத்து, தாதுக்கள் மற்றும் ஃபிளாவனாய்டுகள் உள்ளன."
    },
    # 18. Ash Gourd
    {
        "slug": "ash-gourd",
        "avg": 18.0, "min": 13.0, "max": 24.0, "moisture": 95.0, "dry": 5.0, "factor": 0.08,
        "notes_en": "Ash gourd waxy outer rind contains crystalline triterpenes and insoluble cellulose.",
        "notes_ta": "சாம்பல் பூசணி மெழுகு தோலில் செல்லுலோஸ் மற்றும் டிரைடர்பீன்கள் உள்ளன."
    },
    # 19. Sponge Gourd
    {
        "slug": "sponge-gourd",
        "avg": 16.0, "min": 12.0, "max": 21.0, "moisture": 93.0, "dry": 7.0, "factor": 0.11,
        "notes_en": "Tender sponge gourd skin provides high dietary fiber and natural saponins.",
        "notes_ta": "நுரை பீர்க்கங்காய் தோலில் நார்ச்சத்து மற்றும் இயற்கையான சபோனின்கள் உள்ளன."
    },
    # 20. Ivy Gourd
    {
        "slug": "ivy-gourd",
        "avg": 7.0, "min": 4.0, "max": 10.0, "moisture": 93.0, "dry": 7.0, "factor": 0.10,
        "notes_en": "Ivy gourd tips and outer skin are high in beta-carotene; typically consumed whole with skin.",
        "notes_ta": "கோவைக்காய் தோலுடன் சாப்பிடக்கூடியது; அதிக பீட்டா கரோட்டின் கொண்டது."
    },
    # 21. Pointed Gourd
    {
        "slug": "pointed-gourd",
        "avg": 8.0, "min": 5.0, "max": 11.0, "moisture": 92.0, "dry": 8.0, "factor": 0.11,
        "notes_en": "Pointed gourd (Parwal) peel is rich in magnesium and vitamin A.",
        "notes_ta": "பர்வால் தோலில் மெக்னீசியம் மற்றும் வைட்டமின் ஏ உள்ளன."
    },
    # 22. Chayote
    {
        "slug": "chayote",
        "avg": 11.0, "min": 7.0, "max": 15.0, "moisture": 94.0, "dry": 6.0, "factor": 0.10,
        "notes_en": "Tender chayote skin is completely edible, providing folate and potassium.",
        "notes_ta": "சீமை கத்திரிக்காய் தோல் மென்மையானது, ஃபோலேட் மற்றும் பொட்டாசியம் நிறைந்தது."
    },
    # 23. Cucumber
    {
        "slug": "cucumber",
        "avg": 15.0, "min": 10.0, "max": 20.0, "moisture": 95.2, "dry": 4.8, "factor": 0.08,
        "notes_en": "Cucumber peel holds almost all the cucurbitacin, chlorophyll, and insoluble fiber of cucumber, plus 5x more vitamin K than peeled cucumber flesh.",
        "notes_ta": "வெள்ளரிக்காய் தோலில் சதையை விட 5 மடங்கு அதிக வைட்டமின் கே மற்றும் குளோரோபில் உள்ளது."
    },
    # 24. Zucchini
    {
        "slug": "zucchini",
        "avg": 12.0, "min": 8.0, "max": 16.0, "moisture": 94.0, "dry": 6.0, "factor": 0.10,
        "notes_en": "Zucchini dark green skin contains 90% of its lutein and zeaxanthin carotenoids.",
        "notes_ta": "சுக்கினி தோலில் அதன் 90% லுடீன் கண் ஆரோக்கிய சத்துக்கள் உள்ளன."
    },
    # 25. Yellow Squash
    {
        "slug": "yellow-squash",
        "avg": 12.5, "min": 8.5, "max": 16.5, "moisture": 93.5, "dry": 6.5, "factor": 0.10,
        "notes_en": "Yellow squash skin is loaded with beta-cryptoxanthin and vitamin C.",
        "notes_ta": "மஞ்சள் சுரைக்காய் தோலில் வைட்டமின் சி மற்றும் கரோட்டினாய்டுகள் உள்ளன."
    },
    # 26. Butternut Squash
    {
        "slug": "butternut-squash",
        "avg": 18.0, "min": 13.0, "max": 24.0, "moisture": 86.0, "dry": 14.0, "factor": 0.16,
        "notes_en": "Thick outer skin protects high provitamin A reserves; excellent for roasting or puree.",
        "notes_ta": "பட்டர்நட் பூசணி தோலில் அதிக வைட்டமின் ஏ முன்னோடிகள் உள்ளன."
    },
    # 27. Chow-Chow
    {
        "slug": "chow-chow",
        "avg": 11.5, "min": 8.0, "max": 15.5, "moisture": 94.0, "dry": 6.0, "factor": 0.10,
        "notes_en": "Chow-chow peel is fibrous and high in amino acids like aspartic acid.",
        "notes_ta": "சௌ-சௌ தோலில் அமினோ அமிலங்கள் மற்றும் நார்ச்சத்து உள்ளன."
    },
    # 28. Brinjal / Eggplant
    {
        "slug": "brinjal-eggplant",
        "avg": 10.0, "min": 6.5, "max": 14.0, "moisture": 92.0, "dry": 8.0, "factor": 0.11,
        "notes_en": "Eggplant purple skin contains nasunin, a powerful anthocyanin antioxidant that protects brain cell membrane lipids from oxidation.",
        "notes_ta": "கத்தரிக்காய் ஊதா தோலில் மூளை செல்களை பாதுகாக்கும் நசுனின் என்ற சக்திவாய்ந்த ஆந்தோசயனின் உள்ளது."
    },
    # 29. Tomato
    {
        "slug": "tomato",
        "avg": 8.0, "min": 5.0, "max": 12.0, "moisture": 93.5, "dry": 6.5, "factor": 0.11,
        "notes_en": "Tomato epidermal skin contains 2.5x to 3x higher lycopene and phenolic flavonoids per gram than the locular tomato pulp.",
        "notes_ta": "தக்காளி தோலில் தக்காளி கூழை விட 3 மடங்கு அதிக லைகோபீன் மற்றும் ஃபிளாவனாய்டுகள் உள்ளன."
    },
    # 30. Green Plantain
    {
        "slug": "green-plantain",
        "avg": 36.0, "min": 28.0, "max": 44.0, "moisture": 84.0, "dry": 16.0, "factor": 0.18,
        "notes_en": "Raw banana / plantain peel accounts for ~36% fruit weight; rich in potassium (up to 780mg/100g), dopamine precursor L-dopa, and dietary fiber. Widely cooked in Vazhaikkai Thol Poriyal.",
        "notes_ta": "வாழைக்காய் தோல் எடையில் 36% கொண்டது; பொட்டாசியம் (780 மிகி) மற்றும் நார்ச்சத்து நிறைந்தது. பொரியலுக்கு உகந்தது."
    },
    # 31. Raw Papaya
    {
        "slug": "raw-papaya",
        "avg": 16.0, "min": 11.0, "max": 22.0, "moisture": 90.0, "dry": 10.0, "factor": 0.13,
        "notes_en": "Green papaya skin contains the proteolytic enzyme papain and benzyl isothiocyanate with digestive and tenderizing properties.",
        "notes_ta": "பப்பாளிக்காய் தோலில் செரிமானத்திற்கு உதவும் பப்பாயின் நொதி உள்ளது."
    },
    # 32. Drumstick Pods
    {
        "slug": "drumstick-pods",
        "avg": 15.0, "min": 10.0, "max": 20.0, "moisture": 86.0, "dry": 14.0, "factor": 0.15,
        "notes_en": "Outer fibrous rind of Moringa oleifera pods has high calcium (85mg/100g), iron, and quercetin.",
        "notes_ta": "முருங்கைக்காய் மேல்தோலில் கால்சியம் (85 மிகி), இரும்புச்சத்து மற்றும் குவர்செடின் உள்ளன."
    },
    # 33. Broad Beans
    {
        "slug": "broad-beans",
        "avg": 42.0, "min": 32.0, "max": 52.0, "moisture": 82.0, "dry": 18.0, "factor": 0.20,
        "notes_en": "Broad bean pod shells represent over 40% pod weight; rich in L-DOPA and hemicellulose.",
        "notes_ta": "அவரைக்காய் நெற்றுத் தோலில் நார்ச்சத்து மற்றும் தாவர சேர்மங்கள் அதிகம்."
    },
    # 34. Peas
    {
        "slug": "peas",
        "avg": 48.0, "min": 38.0, "max": 58.0, "moisture": 81.0, "dry": 19.0, "factor": 0.21,
        "notes_en": "Green pea pod shells comprise nearly 50% pod weight; sweet and tender shells yield 4.5g dietary fiber and 28mg vitamin C.",
        "notes_ta": "பட்டாணி நெற்று தோலில் 4.5 கிராம் நார்ச்சத்து மற்றும் 28 மிகி வைட்டமின் சி உள்ளது."
    },
    # 35. French Beans
    {
        "slug": "french-beans",
        "avg": 8.0, "min": 5.0, "max": 12.0, "moisture": 89.0, "dry": 11.0, "factor": 0.13,
        "notes_en": "French bean tips and strings contain silicon, fiber, and chlorogenic acid.",
        "notes_ta": "பீன்ஸ் நுனி மற்றும் நாரில் சிலிக்கான் மற்றும் நார்ச்சத்து உள்ளன."
    },
    # 36. Cluster Beans
    {
        "slug": "cluster-beans",
        "avg": 9.0, "min": 6.0, "max": 13.0, "moisture": 84.0, "dry": 16.0, "factor": 0.17,
        "notes_en": "Guar / cluster bean pod tips and outer fiber contain natural galactomannan gum.",
        "notes_ta": "கொத்தவரங்காய் தோலில் கேலக்டோமன்னன் மற்றும் நார்ச்சத்து உள்ளன."
    },
    # 37. Capsicum / Bell Pepper
    {
        "slug": "capsicum-bell-pepper",
        "avg": 14.0, "min": 9.0, "max": 18.0, "moisture": 92.5, "dry": 7.5, "factor": 0.11,
        "notes_en": "Capsicum calyx, seeds, and stem core yield high capsaicinoids and ascorbic acid.",
        "notes_ta": "குடைமிளகாய் தண்டு மற்றும் தோலில் வைட்டமின் சி மற்றும் ஆன்டிஆக்ஸிடன்ட்கள் உள்ளன."
    },
    # 38. Green Chilli
    {
        "slug": "green-chilli",
        "avg": 7.0, "min": 4.0, "max": 10.0, "moisture": 85.0, "dry": 15.0, "factor": 0.16,
        "notes_en": "Green chilli calyx and pedicel contain high capsaicin and pungent volatile oils.",
        "notes_ta": "பச்சை மிளகாய் காம்பில் கேப்சைசின் சேர்மங்கள் உள்ளன."
    },
    # 39. Okra / Lady's Finger
    {
        "slug": "okra-ladys-finger",
        "avg": 12.0, "min": 8.0, "max": 16.0, "moisture": 88.0, "dry": 12.0, "factor": 0.14,
        "notes_en": "Okra caps (peduncle) and tail tips are rich in soluble pectin mucilage and calcium.",
        "notes_ta": "வெண்டைக்காய் காம்பு மற்றும் நுனியில் கரையக்கூடிய பெக்டின் வழவழப்பு மற்றும் கால்சியம் உள்ளன."
    },
    # 40. Onion
    {
        "slug": "onion",
        "avg": 8.5, "min": 5.0, "max": 12.0, "moisture": 14.0, "dry": 86.0, "factor": 0.70,
        "notes_en": "Dry outer onion skins contain 20x to 40x more quercetin bioflavonoids than inner fleshy edible scales. Extraordinary natural antioxidant source.",
        "notes_ta": "வெங்காயத்தின் உலர்ந்த மேல்தோலில் உள் பகுதியை விட 20-40 மடங்கு அதிக குவர்செடின் ஆக்ஸிஜனேற்றி உள்ளது."
    },
    # 41. Garlic
    {
        "slug": "garlic",
        "avg": 9.0, "min": 6.0, "max": 13.0, "moisture": 18.0, "dry": 82.0, "factor": 0.65,
        "notes_en": "Garlic papery tunic skins contain caffeic acid, allicin derivatives, and 6x more phenylpropanoid antioxidants than the cloves.",
        "notes_ta": "பூண்டு மெல்லிய தோலில் பூண்டு பல்லை விட 6 மடங்கு அதிக பினில்புரபனாய்டு ஆக்ஸிஜனேற்றிகள் உள்ளன."
    },
    # 42. Shallots
    {
        "slug": "shallots",
        "avg": 10.0, "min": 7.0, "max": 14.0, "moisture": 16.0, "dry": 84.0, "factor": 0.68,
        "notes_en": "Small onion / shallot outer reddish skins contain concentrated quercetin-3-glucoside and organosulfur compounds.",
        "notes_ta": "சின்ன வெங்காயத் தோலில் குவர்செடின் மற்றும் ஆர்கனோசல்ஃபர் சேர்மங்கள் மிக அதிகம்."
    },
    # 43. Ginger
    {
        "slug": "ginger",
        "avg": 12.0, "min": 8.0, "max": 16.0, "moisture": 80.0, "dry": 20.0, "factor": 0.19,
        "notes_en": "Ginger rhizome epidermis holds 2x the concentration of gingerols and 6-shogaol essential oils compared to inner core.",
        "notes_ta": "இஞ்சி தோலில் உள் சதையை விட 2 மடங்கு அதிக ஜிஞ்சரால் மருத்துவ எண்ணெய் சேர்மங்கள் உள்ளன."
    },
    # 44. Turmeric
    {
        "slug": "turmeric",
        "avg": 13.0, "min": 9.0, "max": 17.0, "moisture": 79.0, "dry": 21.0, "factor": 0.20,
        "notes_en": "Fresh turmeric root peel holds rich golden curcuminoids, turmerones, and essential sesquiterpenes.",
        "notes_ta": "பச்சை மஞ்சள் தோலில் குர்குமினாய்டுகள் மற்றும் டர்மெரோன் எண்ணெய் நிறைந்துள்ளன."
    },
    # 45. Cabbage Outer Leaves
    {
        "slug": "cabbage-outer-leaves",
        "avg": 18.0, "min": 12.0, "max": 25.0, "moisture": 91.0, "dry": 9.0, "factor": 0.12,
        "notes_en": "Dark green cabbage outer wrapper leaves receive direct sunlight, producing 3x more vitamin C and 10x more beta-carotene than pale inner head leaves.",
        "notes_ta": "முட்டைக்கோசின் வெளிப்புற பச்சை இலைகளில் உள் வெளிறிய இலைகளை விட 3 மடங்கு அதிக வைட்டமின் சி மற்றும் 10 மடங்கு அதிக பீட்டா கரோட்டின் உள்ளது."
    },
    # 46. Cauliflower Outer Leaves
    {
        "slug": "cauliflower-outer-leaves",
        "avg": 35.0, "min": 25.0, "max": 45.0, "moisture": 89.0, "dry": 11.0, "factor": 0.14,
        "notes_en": "Cauliflower green leaves and stalk constitute up to 35-45% of total head weight; they contain 42mg iron, 430mg calcium, and 68mg vitamin C per 100g, far surpassing the white florets.",
        "notes_ta": "காலிஃபிளவர் இலைகள் மற்றும் தண்டு எடையில் 35% ஆகும்; வெள்ளை பூவை விட இதில் இரும்புச்சத்து, கால்சியம் (430 மிகி) மற்றும் வைட்டமின் சி அதிகம் உள்ளது."
    },
    # 47. Broccoli Stalk Outer Layer
    {
        "slug": "broccoli-stalk-outer-layer",
        "avg": 28.0, "min": 20.0, "max": 38.0, "moisture": 90.0, "dry": 10.0, "factor": 0.13,
        "notes_en": "Broccoli stalks and fibrous skin are extremely high in calcium and sulforaphane glucosinolate precursors.",
        "notes_ta": "ப்ரோக்கோலி தண்டு மற்றும் மேல்தோலில் சல்ஃபோராபேன் மற்றும் கால்சியம் அதிகம் உள்ளன."
    },
    # 48. Banana Stem Outer Layers
    {
        "slug": "banana-stem-outer-layers",
        "avg": 26.0, "min": 18.0, "max": 35.0, "moisture": 92.5, "dry": 7.5, "factor": 0.11,
        "notes_en": "Outer fibrous sheath of the banana pseudostem is extremely rich in lignocellulose fiber, potassium, and astringent tannins.",
        "notes_ta": "வாழைத்தண்டு வெளிப்புற மட்டையில் நார்ச்சத்து மற்றும் பொட்டாசியம் மிக அதிகம்; சிறுநீரக கல் தடுப்புக்கு பாரம்பரியமாக பயன்படுகிறது."
    },
    # 49. Lotus Stem Outer Layer
    {
        "slug": "lotus-stem-outer-layer",
        "avg": 14.0, "min": 9.5, "max": 18.0, "moisture": 83.0, "dry": 17.0, "factor": 0.18,
        "notes_en": "Lotus rhizome outer skin is high in dietary fiber, iron, and polyphenol oxidase inhibitors.",
        "notes_ta": "தாமரைத்தண்டு தோலில் நார்ச்சத்து மற்றும் இரும்புச்சத்து அதிகம் உள்ளன."
    },
    # 50. Corn Husk
    {
        "slug": "corn-husk",
        "avg": 28.0, "min": 20.0, "max": 36.0, "moisture": 55.0, "dry": 45.0, "factor": 0.40,
        "notes_en": "Corn husks (bracts) are tough and rich in arabinoxylans and ferulic acid; ideal for compost, biodegradable wrap, or fiber extraction.",
        "notes_ta": "மக்காச்சோள உமி நார்ச்சத்தும் பெரூலிக் அமிலமும் நிறைந்தது; உரம் மற்றும் இயற்கை தட்டுகள் செய்ய சிறந்தது."
    },
]

# Standard Daily Reference Intakes (RDA / DRI) based on ICMR-NIN 2020 Recommended Dietary Allowances for Indians
# Pop groups: adult_male, adult_female, pregnant_woman, lactating_mother, children_7_9y
RDA_DATA = [
    # Vitamin C (Ascorbic Acid) - mg
    {"nutrient": "vit_c", "group": "adult_male", "val": 80.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Adult sedentary/moderate male requirement"},
    {"nutrient": "vit_c", "group": "adult_female", "val": 65.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Adult sedentary/moderate female requirement"},
    {"nutrient": "vit_c", "group": "pregnant_woman", "val": 80.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Second and third trimester"},
    {"nutrient": "vit_c", "group": "lactating_mother", "val": 115.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "0 to 12 months lactation"},
    {"nutrient": "vit_c", "group": "children_7_9y", "val": 35.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Children age 7-9 years"},

    # Vitamin A (Retinol Equivalent) - mcg
    {"nutrient": "vit_a", "group": "adult_male", "val": 1000.0, "unit": "mcg", "auth": "ICMR-NIN 2020", "notes_en": "Adult male requirement (as Retinol Equivalent)"},
    {"nutrient": "vit_a", "group": "adult_female", "val": 840.0, "unit": "mcg", "auth": "ICMR-NIN 2020", "notes_en": "Adult female requirement"},
    {"nutrient": "vit_a", "group": "pregnant_woman", "val": 900.0, "unit": "mcg", "auth": "ICMR-NIN 2020", "notes_en": "Pregnancy requirement"},
    {"nutrient": "vit_a", "group": "lactating_mother", "val": 1360.0, "unit": "mcg", "auth": "ICMR-NIN 2020", "notes_en": "Lactation requirement"},
    {"nutrient": "vit_a", "group": "children_7_9y", "val": 630.0, "unit": "mcg", "auth": "ICMR-NIN 2020", "notes_en": "Children age 7-9 years"},

    # Dietary Fibre - g
    {"nutrient": "dietary_fibre", "group": "adult_male", "val": 30.0, "unit": "g", "auth": "ICMR-NIN 2020", "notes_en": "Minimum recommended daily intake for adults"},
    {"nutrient": "dietary_fibre", "group": "adult_female", "val": 25.0, "unit": "g", "auth": "ICMR-NIN 2020", "notes_en": "Adult female dietary fiber requirement"},
    {"nutrient": "dietary_fibre", "group": "pregnant_woman", "val": 30.0, "unit": "g", "auth": "ICMR-NIN 2020", "notes_en": "To prevent gestational constipation"},
    {"nutrient": "dietary_fibre", "group": "lactating_mother", "val": 30.0, "unit": "g", "auth": "ICMR-NIN 2020", "notes_en": "Lactating mother"},
    {"nutrient": "dietary_fibre", "group": "children_7_9y", "val": 22.0, "unit": "g", "auth": "ICMR-NIN 2020", "notes_en": "Children age 7-9 years"},

    # Calcium - mg
    {"nutrient": "calcium", "group": "adult_male", "val": 1000.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Adult male bone health"},
    {"nutrient": "calcium", "group": "adult_female", "val": 1000.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Adult female bone density maintenance"},
    {"nutrient": "calcium", "group": "pregnant_woman", "val": 1000.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Fetal skeletal development"},
    {"nutrient": "calcium", "group": "lactating_mother", "val": 1200.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Breast milk mineral replenishment"},
    {"nutrient": "calcium", "group": "children_7_9y", "val": 650.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Growing children skeletal growth"},

    # Iron - mg
    {"nutrient": "iron", "group": "adult_male", "val": 19.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Adult male hemoglobin maintenance"},
    {"nutrient": "iron", "group": "adult_female", "val": 29.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Menstruating female iron loss replacement"},
    {"nutrient": "iron", "group": "pregnant_woman", "val": 27.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Maternal blood volume expansion"},
    {"nutrient": "iron", "group": "lactating_mother", "val": 15.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Postpartum recovery"},
    {"nutrient": "iron", "group": "children_7_9y", "val": 15.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Children age 7-9 years"},

    # Potassium - mg
    {"nutrient": "potassium", "group": "adult_male", "val": 3500.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Cardiovascular and electrolyte homeostasis"},
    {"nutrient": "potassium", "group": "adult_female", "val": 3500.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Adult female electrolyte balance"},
    {"nutrient": "potassium", "group": "pregnant_woman", "val": 3500.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Pregnancy fluid regulation"},
    {"nutrient": "potassium", "group": "lactating_mother", "val": 3500.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Lactating mother"},
    {"nutrient": "potassium", "group": "children_7_9y", "val": 2500.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Children age 7-9 years"},

    # Magnesium - mg
    {"nutrient": "magnesium", "group": "adult_male", "val": 385.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Enzyme cofactor and neuromuscular function"},
    {"nutrient": "magnesium", "group": "adult_female", "val": 325.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Adult female requirement"},
    {"nutrient": "magnesium", "group": "pregnant_woman", "val": 385.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Pregnancy neuromuscular health"},
    {"nutrient": "magnesium", "group": "lactating_mother", "val": 385.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Lactation"},
    {"nutrient": "magnesium", "group": "children_7_9y", "val": 175.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Children age 7-9 years"},

    # Zinc - mg
    {"nutrient": "zinc", "group": "adult_male", "val": 17.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Immune integrity and cellular repair"},
    {"nutrient": "zinc", "group": "adult_female", "val": 13.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Adult female immune requirement"},
    {"nutrient": "zinc", "group": "pregnant_woman", "val": 14.5, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Embryonic cellular proliferation"},
    {"nutrient": "zinc", "group": "lactating_mother", "val": 14.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Infant immune transfer in milk"},
    {"nutrient": "zinc", "group": "children_7_9y", "val": 7.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Children age 7-9 years"},

    # Vitamin B1 (Thiamine) - mg
    {"nutrient": "vit_b1", "group": "adult_male", "val": 1.4, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Energy metabolism coenzyme"},
    {"nutrient": "vit_b1", "group": "adult_female", "val": 1.4, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Carbohydrate metabolism"},
    {"nutrient": "vit_b1", "group": "pregnant_woman", "val": 2.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Gestational energy support"},
    {"nutrient": "vit_b1", "group": "lactating_mother", "val": 2.1, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Lactation"},
    {"nutrient": "vit_b1", "group": "children_7_9y", "val": 0.9, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Children"},

    # Vitamin B2 (Riboflavin) - mg
    {"nutrient": "vit_b2", "group": "adult_male", "val": 2.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "FAD/FMN coenzyme"},
    {"nutrient": "vit_b2", "group": "adult_female", "val": 1.9, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Cellular respiration"},
    {"nutrient": "vit_b2", "group": "pregnant_woman", "val": 2.7, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Pregnancy"},
    {"nutrient": "vit_b2", "group": "lactating_mother", "val": 3.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Lactation"},
    {"nutrient": "vit_b2", "group": "children_7_9y", "val": 1.3, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Children"},

    # Vitamin B3 (Niacin) - mg
    {"nutrient": "vit_b3", "group": "adult_male", "val": 14.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "NAD/NADP cellular redox"},
    {"nutrient": "vit_b3", "group": "adult_female", "val": 11.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Adult female"},
    {"nutrient": "vit_b3", "group": "pregnant_woman", "val": 13.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Pregnancy"},
    {"nutrient": "vit_b3", "group": "lactating_mother", "val": 16.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Lactation"},
    {"nutrient": "vit_b3", "group": "children_7_9y", "val": 9.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Children"},

    # Vitamin B6 (Pyridoxine) - mg
    {"nutrient": "vit_b6", "group": "adult_male", "val": 1.9, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Amino acid transamination"},
    {"nutrient": "vit_b6", "group": "adult_female", "val": 1.9, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Adult female"},
    {"nutrient": "vit_b6", "group": "pregnant_woman", "val": 2.5, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Pregnancy"},
    {"nutrient": "vit_b6", "group": "lactating_mother", "val": 2.5, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Lactation"},
    {"nutrient": "vit_b6", "group": "children_7_9y", "val": 1.2, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Children"},

    # Vitamin B9 (Folate) - mcg
    {"nutrient": "vit_b9", "group": "adult_male", "val": 300.0, "unit": "mcg", "auth": "ICMR-NIN 2020", "notes_en": "One-carbon metabolism & DNA synthesis"},
    {"nutrient": "vit_b9", "group": "adult_female", "val": 220.0, "unit": "mcg", "auth": "ICMR-NIN 2020", "notes_en": "Adult female"},
    {"nutrient": "vit_b9", "group": "pregnant_woman", "val": 570.0, "unit": "mcg", "auth": "ICMR-NIN 2020", "notes_en": "Neural tube defect prevention"},
    {"nutrient": "vit_b9", "group": "lactating_mother", "val": 330.0, "unit": "mcg", "auth": "ICMR-NIN 2020", "notes_en": "Lactation"},
    {"nutrient": "vit_b9", "group": "children_7_9y", "val": 170.0, "unit": "mcg", "auth": "ICMR-NIN 2020", "notes_en": "Children"},

    # Phosphorus - mg
    {"nutrient": "phosphorus", "group": "adult_male", "val": 1000.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Bone mineral matrix"},
    {"nutrient": "phosphorus", "group": "adult_female", "val": 1000.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Bone mineral matrix"},
    {"nutrient": "phosphorus", "group": "pregnant_woman", "val": 1000.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Pregnancy"},
    {"nutrient": "phosphorus", "group": "lactating_mother", "val": 1200.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Lactation"},
    {"nutrient": "phosphorus", "group": "children_7_9y", "val": 650.0, "unit": "mg", "auth": "ICMR-NIN 2020", "notes_en": "Children"},
]


def seed_phase6_peel_yield_and_dri(db: Session) -> None:
    """Seed botanical peel yield ratios for all 50 vegetables and comprehensive ICMR-NIN 2020 RDA tables."""
    logger.info("Ingesting Phase 6 peel yield ratios and daily reference intake datasets...")

    # Load Scientific Sources
    source = db.query(ScientificSource).first()
    source_id = source.id if source else None

    # 1. Seed Peel Yield Ratios for all 50 vegetables
    vegs = {v.slug: v for v in db.query(Vegetable).all()}

    yield_count = 0
    for data in PEEL_YIELD_DATA:
        slug = data["slug"]
        veg = vegs.get(slug)
        if not veg:
            logger.warning(f"Vegetable with slug '{slug}' not found for yield ratio seed.")
            continue

        existing = db.query(PeelYieldRatio).filter(PeelYieldRatio.vegetable_id == veg.id).first()
        if not existing:
            ratio = PeelYieldRatio(
                vegetable_id=veg.id,
                average_peel_percentage=data["avg"],
                min_peel_percentage=data["min"],
                max_peel_percentage=data["max"],
                moisture_percentage_fresh=data["moisture"],
                dry_matter_percentage=data["dry"],
                water_loss_dehydration_factor=data["factor"],
                pulp_comparison_notes_en=data["notes_en"],
                pulp_comparison_notes_ta=data["notes_ta"],
                source_id=source_id,
            )
            db.add(ratio)
            yield_count += 1
        else:
            existing.average_peel_percentage = data["avg"]
            existing.min_peel_percentage = data["min"]
            existing.max_peel_percentage = data["max"]
            existing.moisture_percentage_fresh = data["moisture"]
            existing.dry_matter_percentage = data["dry"]
            existing.water_loss_dehydration_factor = data["factor"]
            existing.pulp_comparison_notes_en = data["notes_en"]
            existing.pulp_comparison_notes_ta = data["notes_ta"]

    db.commit()
    logger.info(f"Seeded {yield_count} new PeelYieldRatio records for 50 vegetables.")

    # 2. Seed Daily Reference Intakes (RDAs)
    dri_count = 0
    for rda in RDA_DATA:
        existing_dri = (
            db.query(DailyReferenceIntake)
            .filter(
                DailyReferenceIntake.nutrient_code == rda["nutrient"],
                DailyReferenceIntake.population_group == rda["group"],
            )
            .first()
        )
        if not existing_dri:
            dri = DailyReferenceIntake(
                nutrient_code=rda["nutrient"],
                population_group=rda["group"],
                rda_value=rda["val"],
                unit=rda["unit"],
                standard_authority=rda["auth"],
                notes_en=rda["notes_en"],
            )
            db.add(dri)
            dri_count += 1
        else:
            existing_dri.rda_value = rda["val"]
            existing_dri.unit = rda["unit"]
            existing_dri.standard_authority = rda["auth"]
            existing_dri.notes_en = rda["notes_en"]

    db.commit()
    logger.info(f"Seeded {dri_count} new DailyReferenceIntake records.")
