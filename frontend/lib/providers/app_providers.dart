import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_riverpod/legacy.dart';
import '../models/app_models.dart';

// Complete 50-vegetable catalogue for instant offline responsiveness & local caching
final List<VegetableItem> initialCatalogue = [
  // Group A — Root Vegetables (1-12)
  const VegetableItem(
    id: 1,
    slug: 'carrot',
    nameEn: 'Carrot',
    nameTa: 'கேரட்',
    scientificName: 'Daucus carota',
    category: 'Root Vegetable',
    plantPart: 'Vegetable Peel',
    isAiSupported: true,
    aiClassName: 'carrot_peel',
    nutrientDataStatus: 'available',
    foodSafetyStatus: 'safe_edible',
    knownHazardsEn: 'Low hazard; wash thoroughly to remove soil microbes and surface pesticide residues.',
    knownHazardsTa: 'மண் துகள்கள் மற்றும் பூச்சிக்கொல்லி எச்சங்களை அகற்ற நன்கு கழுவ வேண்டும்.',
  ),
  const VegetableItem(
    id: 2,
    slug: 'potato',
    nameEn: 'Potato',
    nameTa: 'உருளைக்கிழங்கு',
    scientificName: 'Solanum tuberosum',
    category: 'Root Vegetable',
    plantPart: 'Vegetable Peel',
    isAiSupported: true,
    aiClassName: 'potato_peel',
    nutrientDataStatus: 'available',
    foodSafetyStatus: 'conditional_cooking_required',
    knownHazardsEn: 'CRITICAL: Solanine glycoalkaloids accumulate in green, sprouted, or damaged potato peels. Toxic if consumed; discard green peels.',
    knownHazardsTa: 'முக்கிய எச்சரிக்கை: பச்சை நிறம் அல்லது முளைகட்டிய உருளைக்கிழங்கு தோலில் சோலானின் நச்சு காணப்படும். உண்ணக்கூடாது.',
  ),
  const VegetableItem(
    id: 3,
    slug: 'sweet-potato',
    nameEn: 'Sweet potato',
    nameTa: 'சர்க்கரைவள்ளி கிழங்கு',
    scientificName: 'Ipomoea batatas',
    category: 'Root Vegetable',
    plantPart: 'Vegetable Peel',
    isAiSupported: false,
    nutrientDataStatus: 'available',
    foodSafetyStatus: 'conditional_cooking_required',
    knownHazardsEn: 'Safe when cooked; wash thoroughly; moldy sweet potato peels contain toxic ipomeamarone.',
    knownHazardsTa: 'சமைத்து உண்ணலாம்; பூஞ்சை பிடித்த தோல்களை கண்டிப்பாக பயன்படுத்தக்கூடாது.',
  ),
  const VegetableItem(
    id: 4,
    slug: 'beetroot',
    nameEn: 'Beetroot',
    nameTa: 'பீட்ரூட்',
    scientificName: 'Beta vulgaris',
    category: 'Root Vegetable',
    plantPart: 'Vegetable Peel',
    isAiSupported: true,
    aiClassName: 'beetroot_peel',
    nutrientDataStatus: 'available',
    foodSafetyStatus: 'safe_edible',
    knownHazardsEn: 'Rich in betalains and nitrates; peel can harbor soil organisms; scrub thoroughly before culinary use.',
    knownHazardsTa: 'மண் பாக்டீரியாக்களை அகற்ற நன்கு தேய்த்து கழுவ வேண்டும்.',
  ),
  const VegetableItem(
    id: 5,
    slug: 'radish',
    nameEn: 'Radish',
    nameTa: 'முள்ளங்கி',
    scientificName: 'Raphanus sativus',
    category: 'Root Vegetable',
    plantPart: 'Vegetable Peel',
    isAiSupported: false,
    nutrientDataStatus: 'available',
    foodSafetyStatus: 'safe_edible',
    knownHazardsEn: 'Contains pungent glucosinolates; safe when washed; peppery flavor.',
    knownHazardsTa: 'நன்கு கழுவி சமையலில் பயன்படுத்தலாம்; காரத்தன்மை கொண்டது.',
  ),
  const VegetableItem(
    id: 6,
    slug: 'turnip',
    nameEn: 'Turnip',
    nameTa: 'நூல் கோல் / டர்னிப்',
    scientificName: 'Brassica rapa subsp. rapa',
    category: 'Root Vegetable',
    plantPart: 'Vegetable Peel',
    isAiSupported: false,
    nutrientDataStatus: 'available',
    foodSafetyStatus: 'conditional_cooking_required',
    knownHazardsEn: 'Fibrous outer rind; wash and boil or compost.',
    knownHazardsTa: 'நார்ச்சத்து அதிகம்; வேகவைத்து பயன்படுத்தலாம் அல்லது உரமாக்கலாம்.',
  ),
  const VegetableItem(
    id: 7,
    slug: 'parsnip',
    nameEn: 'Parsnip',
    nameTa: 'பார்ஸ்னிப்',
    scientificName: 'Pastinaca sativa',
    category: 'Root Vegetable',
    plantPart: 'Vegetable Peel',
    isAiSupported: false,
    nutrientDataStatus: 'incomplete',
    foodSafetyStatus: 'conditional_cooking_required',
    knownHazardsEn: 'Contains furanocoumarins which can cause mild photosensitivity; culinary cooking recommended.',
    knownHazardsTa: 'சமைத்த பின் பயன்படுத்தவும்.',
  ),
  const VegetableItem(
    id: 8,
    slug: 'cassava-tapioca',
    nameEn: 'Cassava / Tapioca',
    nameTa: 'மரவள்ளிக்கிழங்கு',
    scientificName: 'Manihot esculenta',
    category: 'Root Vegetable',
    plantPart: 'Vegetable Peel',
    isAiSupported: false,
    nutrientDataStatus: 'available',
    foodSafetyStatus: 'hazardous_raw',
    knownHazardsEn: 'HIGH DANGER: Cassava peel contains lethal cyanogenic glucosides (linamarin). Strictly prohibited for human food or raw feed.',
    knownHazardsTa: 'அபாய எச்சரிக்கை: மரவள்ளிக்கிழங்கு தோலில் சயனைடு நச்சுத்தன்மை உள்ளது. சாப்பிடக்கூடாது. உரமாக்க மட்டுமே சிறந்தது.',
  ),
  const VegetableItem(
    id: 9,
    slug: 'elephant-foot-yam',
    nameEn: 'Elephant foot yam',
    nameTa: 'சேனைக்கிழங்கு',
    scientificName: 'Amorphophallus paeoniifolius',
    category: 'Root Vegetable',
    plantPart: 'Vegetable Peel',
    isAiSupported: false,
    nutrientDataStatus: 'incomplete',
    foodSafetyStatus: 'hazardous_raw',
    knownHazardsEn: 'Contains sharp needle-like calcium oxalate raphide crystals causing severe throat irritation and itching.',
    knownHazardsTa: 'அரிப்பு உண்டாக்கும் கால்சியம் ஆக்சலேட் படிகங்கள் நிறைந்தது. பச்சையாக சாப்பிடக்கூடாது.',
  ),
  const VegetableItem(
    id: 10,
    slug: 'greater-yam',
    nameEn: 'Greater yam',
    nameTa: 'காச்சில் / பெரும் சேம்பு',
    scientificName: 'Dioscorea alata',
    category: 'Root Vegetable',
    plantPart: 'Vegetable Peel',
    isAiSupported: false,
    nutrientDataStatus: 'incomplete',
    foodSafetyStatus: 'conditional_cooking_required',
    knownHazardsEn: 'Contains mucilage and trace oxalates; remove peel before consumption or compost.',
    knownHazardsTa: 'அரிப்பு தன்மை; உரமாக்க ஏற்றது.',
  ),
  const VegetableItem(
    id: 11,
    slug: 'taro-colocasia',
    nameEn: 'Taro / Colocasia',
    nameTa: 'சேப்பங்கிழங்கு',
    scientificName: 'Colocasia esculenta',
    category: 'Root Vegetable',
    plantPart: 'Vegetable Peel',
    isAiSupported: false,
    nutrientDataStatus: 'incomplete',
    foodSafetyStatus: 'hazardous_raw',
    knownHazardsEn: 'Contains sharp calcium oxalate raphide needles causing throat swelling and intense itchiness.',
    knownHazardsTa: 'அரிப்பு உண்டாக்கும் கால்சியம் ஆக்சலேட் படிகங்கள் நிறைந்தது.',
  ),
  const VegetableItem(
    id: 12,
    slug: 'jerusalem-artichoke',
    nameEn: 'Jerusalem artichoke',
    nameTa: 'ஜெருசலேம் கூனைப்பூ',
    scientificName: 'Helianthus tuberosus',
    category: 'Root Vegetable',
    plantPart: 'Vegetable Peel',
    isAiSupported: false,
    nutrientDataStatus: 'incomplete',
    foodSafetyStatus: 'safe_edible',
    knownHazardsEn: 'High in inulin dietary fibre; excessive intake can cause intestinal flatulence.',
    knownHazardsTa: 'இன்யூலின் நார்ச்சத்து அதிகம்; மிதமாக உட்கொள்ளவும்.',
  ),

  // Group B — Gourds & Cucurbits (13-27)
  const VegetableItem(
    id: 13,
    slug: 'pumpkin',
    nameEn: 'Pumpkin',
    nameTa: 'பூசணிக்காய்',
    scientificName: 'Cucurbita moschata',
    category: 'Gourds & Cucurbits',
    plantPart: 'Thick Rind',
    isAiSupported: true,
    aiClassName: 'pumpkin_peel',
    nutrientDataStatus: 'available',
    foodSafetyStatus: 'safe_edible',
    knownHazardsEn: 'Extremely safe when cooked; discard if flesh or peel tastes unusually bitter.',
    knownHazardsTa: 'சமைக்க மிகவும் பாதுகாப்பானது; கசப்பு சுவை இருந்தால் தவிர்க்கவும்.',
  ),
  const VegetableItem(
    id: 14,
    slug: 'bottle-gourd',
    nameEn: 'Bottle gourd',
    nameTa: 'சுரைக்காய்',
    scientificName: 'Lagenaria siceraria',
    category: 'Gourds & Cucurbits',
    plantPart: 'Vegetable Peel',
    isAiSupported: false,
    nutrientDataStatus: 'available',
    foodSafetyStatus: 'safe_edible',
    knownHazardsEn: 'IMPORTANT: Discard if peel or juice tastes intensely bitter due to toxic cucurbitacins.',
    knownHazardsTa: 'கசப்பு சுவை கொண்ட சுரைக்காயை ஒருபோதும் உட்கொள்ளக்கூடாது.',
  ),
  const VegetableItem(
    id: 15,
    slug: 'bitter-gourd',
    nameEn: 'Bitter gourd',
    nameTa: 'பாகற்காய்',
    scientificName: 'Momordica charantia',
    category: 'Gourds & Cucurbits',
    plantPart: 'Thick Rind',
    isAiSupported: false,
    nutrientDataStatus: 'available',
    foodSafetyStatus: 'safe_edible',
    knownHazardsEn: 'Naturally bitter due to momordicins and charantin; hypoglycemic properties.',
    knownHazardsTa: 'இயற்கையான கசப்பு கொண்டது; இரத்த சர்க்கரையை குறைக்கும் தன்மை கொண்டது.',
  ),
  const VegetableItem(
    id: 16,
    slug: 'ridge-gourd',
    nameEn: 'Ridge gourd',
    nameTa: 'பீர்க்கங்காய்',
    scientificName: 'Luffa acutangula',
    category: 'Gourds & Cucurbits',
    plantPart: 'Vegetable Peel',
    isAiSupported: false,
    nutrientDataStatus: 'available',
    foodSafetyStatus: 'safe_edible',
    knownHazardsEn: 'Outer fibrous ridges can be cooked into traditional South Indian peel chutney (Thogayal).',
    knownHazardsTa: 'இதன் தோலில் சத்தான துவையல் செய்யலாம்; கசப்பு இருந்தால் தவிர்க்கவும்.',
  ),
  const VegetableItem(
    id: 17,
    slug: 'snake-gourd',
    nameEn: 'Snake gourd',
    nameTa: 'புடலங்காய்',
    scientificName: 'Trichosanthes cucumerina',
    category: 'Gourds & Cucurbits',
    plantPart: 'Thin Skin',
    isAiSupported: false,
    nutrientDataStatus: 'available',
    foodSafetyStatus: 'safe_edible',
    knownHazardsEn: 'Gentle scraping recommended; discard if noticeably bitter.',
    knownHazardsTa: 'லேசாக சுரண்டி கழுவி பயன்படுத்தலாம்.',
  ),
  const VegetableItem(
    id: 18,
    slug: 'ash-gourd',
    nameEn: 'Ash gourd',
    nameTa: 'சாம்பல் பூசணி / வெண்பூசணி',
    scientificName: 'Benincasa hispida',
    category: 'Gourds & Cucurbits',
    plantPart: 'Thick Rind',
    isAiSupported: false,
    nutrientDataStatus: 'available',
    foodSafetyStatus: 'safe_edible',
    knownHazardsEn: 'White chalky wax on rind should be washed off before processing; great for composting.',
    knownHazardsTa: 'வெளிப்புற வெள்ளை மெழுகு அடுக்கை கழுவி நீக்க வேண்டும்.',
  ),
  const VegetableItem(
    id: 19,
    slug: 'sponge-gourd',
    nameEn: 'Sponge gourd',
    nameTa: 'நுரை பீர்க்கங்காய்',
    scientificName: 'Luffa aegyptiaca',
    category: 'Gourds & Cucurbits',
    plantPart: 'Vegetable Peel',
    isAiSupported: false,
    nutrientDataStatus: 'incomplete',
    foodSafetyStatus: 'safe_edible',
    knownHazardsEn: 'Mature skins become fibrous sponge (loofah); young peels edible if cooked.',
    knownHazardsTa: 'முதிர்ந்த தோல் நார் பயன்பாட்டிற்கு ஏற்றது.',
  ),
  const VegetableItem(
    id: 20,
    slug: 'ivy-gourd',
    nameEn: 'Ivy gourd',
    nameTa: 'கோவைக்காய்',
    scientificName: 'Coccinia grandis',
    category: 'Gourds & Cucurbits',
    plantPart: 'Thin Skin',
    isAiSupported: false,
    nutrientDataStatus: 'incomplete',
    foodSafetyStatus: 'safe_edible',
    knownHazardsEn: 'Entire skin typically consumed intact; wash thoroughly.',
    knownHazardsTa: 'முழுமையாக சாப்பிடக்கூடியது; கழுவி பயன்படுத்தவும்.',
  ),
  const VegetableItem(
    id: 21,
    slug: 'pointed-gourd',
    nameEn: 'Pointed gourd',
    nameTa: 'பர்வால்',
    scientificName: 'Trichosanthes dioica',
    category: 'Gourds & Cucurbits',
    plantPart: 'Thin Skin',
    isAiSupported: false,
    nutrientDataStatus: 'incomplete',
    foodSafetyStatus: 'safe_edible',
    knownHazardsEn: 'Lightly scraped; discard stem ends; pesticide wash advisable.',
    knownHazardsTa: 'லேசாக சுரண்டி சமைக்கலாம்.',
  ),
  const VegetableItem(
    id: 22,
    slug: 'chayote',
    nameEn: 'Chayote',
    nameTa: 'மேராக்காய்',
    scientificName: 'Sechium edule',
    category: 'Gourds & Cucurbits',
    plantPart: 'Vegetable Peel',
    isAiSupported: false,
    nutrientDataStatus: 'incomplete',
    foodSafetyStatus: 'safe_edible',
    knownHazardsEn: 'Peeling exudes a sticky latex that can temporarily numb fingers.',
    knownHazardsTa: 'தோல் நீக்கும்போது ஒட்டும் பிசின் வரலாம்; கையுறை பயன்படுத்தலாம்.',
  ),
  const VegetableItem(
    id: 23,
    slug: 'cucumber',
    nameEn: 'Cucumber',
    nameTa: 'வெள்ளரிக்காய்',
    scientificName: 'Cucumis sativus',
    category: 'Gourds & Cucurbits',
    plantPart: 'Vegetable Peel',
    isAiSupported: true,
    aiClassName: 'cucumber_peel',
    nutrientDataStatus: 'available',
    foodSafetyStatus: 'safe_edible',
    knownHazardsEn: 'High moisture and silica; wash thoroughly to remove waxes applied for shipping.',
    knownHazardsTa: 'மெழுகு பூச்சுகளை அகற்ற வெதுவெதுப்பான நீரில் கழுவ வேண்டும்.',
  ),
  const VegetableItem(
    id: 24,
    slug: 'zucchini',
    nameEn: 'Zucchini',
    nameTa: 'சுக்கினி',
    scientificName: 'Cucurbita pepo',
    category: 'Gourds & Cucurbits',
    plantPart: 'Thin Skin',
    isAiSupported: false,
    nutrientDataStatus: 'available',
    foodSafetyStatus: 'safe_edible',
    knownHazardsEn: 'Tender skin with lutein; discard if taste is distinctly bitter.',
    knownHazardsTa: 'மெல்லிய தோல்; சமைக்க சிறந்தது.',
  ),
  const VegetableItem(
    id: 25,
    slug: 'yellow-squash',
    nameEn: 'Yellow squash',
    nameTa: 'மஞ்சள் ஸ்குவாஷ்',
    scientificName: 'Cucurbita pepo var. recticollis',
    category: 'Gourds & Cucurbits',
    plantPart: 'Thin Skin',
    isAiSupported: false,
    nutrientDataStatus: 'incomplete',
    foodSafetyStatus: 'safe_edible',
    knownHazardsEn: 'Edible skin; wash surface thoroughly.',
    knownHazardsTa: 'சமையல் மற்றும் உரமாக்கலுக்கு ஏற்றது.',
  ),
  const VegetableItem(
    id: 26,
    slug: 'butternut-squash',
    nameEn: 'Butternut squash',
    nameTa: 'பட்டர்நட் பூசணி',
    scientificName: 'Cucurbita moschata',
    category: 'Gourds & Cucurbits',
    plantPart: 'Thick Rind',
    isAiSupported: false,
    nutrientDataStatus: 'incomplete',
    foodSafetyStatus: 'conditional_cooking_required',
    knownHazardsEn: 'Tough rind; can be roasted or boiled into broth; compostable.',
    knownHazardsTa: 'கடினமான தோல்; வேகவைத்து பயன்படுத்தலாம் அல்லது உரமாக்கலாம்.',
  ),
  const VegetableItem(
    id: 27,
    slug: 'chow-chow',
    nameEn: 'Chow chow',
    nameTa: 'செள செள',
    scientificName: 'Sechium edule',
    category: 'Gourds & Cucurbits',
    plantPart: 'Vegetable Peel',
    isAiSupported: false,
    nutrientDataStatus: 'incomplete',
    foodSafetyStatus: 'safe_edible',
    knownHazardsEn: 'Peels can be seasoned into chutney or added to compost bins.',
    knownHazardsTa: 'துவையல் செய்ய உகந்தது.',
  ),

  // Group C — Solanaceous & Common Vegetables (28-39)
  const VegetableItem(
    id: 28,
    slug: 'brinjal-eggplant',
    nameEn: 'Brinjal / Eggplant',
    nameTa: 'கத்தரிக்காய்',
    scientificName: 'Solanum melongena',
    category: 'Solanaceous & Common Roots',
    plantPart: 'Thin Skin',
    isAiSupported: false,
    nutrientDataStatus: 'available',
    foodSafetyStatus: 'safe_edible',
    knownHazardsEn: 'Contains nasunin anthocyanin; solanine levels increase if overgrown or bitter.',
    knownHazardsTa: 'நசுனின் நிறமி நிறைந்தது; முதிர்ந்த காய்களை தவிர்க்கவும்.',
  ),
  const VegetableItem(
    id: 29,
    slug: 'tomato',
    nameEn: 'Tomato',
    nameTa: 'தக்காளி',
    scientificName: 'Solanum lycopersicum',
    category: 'Solanaceous & Common Roots',
    plantPart: 'Thin Skin',
    isAiSupported: false,
    nutrientDataStatus: 'available',
    foodSafetyStatus: 'safe_edible',
    knownHazardsEn: 'Highest concentration of lycopene; skins are safe but tough for infants to digest.',
    knownHazardsTa: 'லைகோபீன் சத்து மிகுந்தது; சமையலில் முழுமையாக பயன்படுத்தலாம்.',
  ),
  const VegetableItem(
    id: 30,
    slug: 'green-plantain',
    nameEn: 'Green plantain / Raw banana',
    nameTa: 'வாழைக்காய்',
    scientificName: 'Musa paradisiaca',
    category: 'Solanaceous & Common Roots',
    plantPart: 'Vegetable Peel',
    isAiSupported: false,
    nutrientDataStatus: 'available',
    foodSafetyStatus: 'conditional_cooking_required',
    knownHazardsEn: 'High tannins and resistant starch; excellent for South Indian Vazhaikkai Thol poriyal after boiling.',
    knownHazardsTa: 'டான்னின் நிறைந்தது; வேகவைத்து பொரியல் செய்ய ஏற்றது.',
  ),
  const VegetableItem(
    id: 31,
    slug: 'raw-papaya',
    nameEn: 'Raw papaya',
    nameTa: 'பப்பாளிக்காய்',
    scientificName: 'Carica papaya',
    category: 'Solanaceous & Common Roots',
    plantPart: 'Vegetable Peel',
    isAiSupported: false,
    nutrientDataStatus: 'incomplete',
    foodSafetyStatus: 'conditional_cooking_required',
    knownHazardsEn: 'Latex contains proteolytic enzyme papain; pregnant women should avoid raw papaya peel.',
    knownHazardsTa: 'பப்பாளி பிசினில் பப்பாயின் என்சைம் உள்ளதால் கர்ப்பிணிகள் தவிர்க்க வேண்டும்.',
  ),
  const VegetableItem(
    id: 32,
    slug: 'drumstick-pods',
    nameEn: 'Drumstick pods / Moringa pods',
    nameTa: 'முருங்கைக்காய்',
    scientificName: 'Moringa oleifera',
    category: 'Legumes & Pods',
    plantPart: 'Pod Shell',
    isAiSupported: false,
    nutrientDataStatus: 'incomplete',
    foodSafetyStatus: 'inedible_valorize_only',
    knownHazardsEn: 'Tough fibrous outer shell. Inedible; prime candidate for composting.',
    knownHazardsTa: 'மிகவும் கடினமான நார்; சாப்பிட இயலாது; உரமாக்க மட்டுமே ஏற்றது.',
  ),
  const VegetableItem(
    id: 33,
    slug: 'broad-beans',
    nameEn: 'Broad beans',
    nameTa: 'அவரைக்காய்',
    scientificName: 'Vicia faba',
    category: 'Legumes & Pods',
    plantPart: 'Pod Shell',
    isAiSupported: false,
    nutrientDataStatus: 'incomplete',
    foodSafetyStatus: 'safe_edible',
    knownHazardsEn: 'Individuals with G6PD deficiency must avoid faba beans due to favism risk.',
    knownHazardsTa: 'G6PD குறைபாடு உள்ளவர்கள் அவரைக்காயை தவிர்க்க வேண்டும்.',
  ),
  const VegetableItem(
    id: 34,
    slug: 'peas',
    nameEn: 'Peas',
    nameTa: 'பட்டாணி',
    scientificName: 'Pisum sativum',
    category: 'Legumes & Pods',
    plantPart: 'Pod Shell',
    isAiSupported: false,
    nutrientDataStatus: 'available',
    foodSafetyStatus: 'conditional_cooking_required',
    knownHazardsEn: 'Sweet pea empty pods can be boiled into purees or composted.',
    knownHazardsTa: 'உள் நார் நீக்கி வேகவைத்து சூப் செய்யலாம் அல்லது உரமாக்கலாம்.',
  ),
  const VegetableItem(
    id: 35,
    slug: 'french-beans',
    nameEn: 'French beans',
    nameTa: 'பீன்ஸ்',
    scientificName: 'Phaseolus vulgaris',
    category: 'Legumes & Pods',
    plantPart: 'Pod Shell',
    isAiSupported: false,
    nutrientDataStatus: 'incomplete',
    foodSafetyStatus: 'safe_edible',
    knownHazardsEn: 'Consume cooked; contains lectins that degrade upon heating.',
    knownHazardsTa: 'லெக்டின்களை செயலிழக்கச் செய்ய சமைத்து உண்ண வேண்டும்.',
  ),
  const VegetableItem(
    id: 36,
    slug: 'cluster-beans',
    nameEn: 'Cluster beans',
    nameTa: 'கொத்தவரங்காய்',
    scientificName: 'Cyamopsis tetragonoloba',
    category: 'Legumes & Pods',
    plantPart: 'Pod Shell',
    isAiSupported: false,
    nutrientDataStatus: 'incomplete',
    foodSafetyStatus: 'safe_edible',
    knownHazardsEn: 'Source of guar gum fibre; wash and cook thoroughly.',
    knownHazardsTa: 'குவார் கம் நார்ச்சத்து நிறைந்தது; சமைத்து உண்ணவும்.',
  ),
  const VegetableItem(
    id: 37,
    slug: 'capsicum-bell-pepper',
    nameEn: 'Capsicum / Bell pepper',
    nameTa: 'குடைமிளகாய்',
    scientificName: 'Capsicum annuum',
    category: 'Solanaceous & Common Roots',
    plantPart: 'Thin Skin',
    isAiSupported: false,
    nutrientDataStatus: 'available',
    foodSafetyStatus: 'safe_edible',
    knownHazardsEn: 'Safe and rich in vitamin C; discard moldy stems.',
    knownHazardsTa: 'வைட்டமின் சி நிறைந்தது; பாதுகாப்பானது.',
  ),
  const VegetableItem(
    id: 38,
    slug: 'green-chilli',
    nameEn: 'Green chilli',
    nameTa: 'பச்சை மிளகாய்',
    scientificName: 'Capsicum frutescens',
    category: 'Solanaceous & Common Roots',
    plantPart: 'Thin Skin',
    isAiSupported: false,
    nutrientDataStatus: 'incomplete',
    foodSafetyStatus: 'safe_edible',
    knownHazardsEn: 'Contains capsaicin; wear gloves when handling; avoid eye contact.',
    knownHazardsTa: 'கேப்சைசின் எரிச்சலை உண்டாக்கும்; கவனமாக கையாளவும்.',
  ),
  const VegetableItem(
    id: 39,
    slug: 'okra-ladys-finger',
    nameEn: "Okra / Lady's finger",
    nameTa: 'வெண்டைக்காய்',
    scientificName: 'Abelmoschus esculentus',
    category: 'Solanaceous & Common Roots',
    plantPart: 'Pod Shell',
    isAiSupported: false,
    nutrientDataStatus: 'available',
    foodSafetyStatus: 'safe_edible',
    knownHazardsEn: 'Mucilaginous soluble fibre; discarded ends decompose rapidly in compost.',
    knownHazardsTa: 'மக்கும் தன்மை மிக்கது; உரத்திற்கு சிறந்தது.',
  ),

  // Group D — Bulbs and Aromatics (40-44)
  const VegetableItem(
    id: 40,
    slug: 'onion',
    nameEn: 'Onion',
    nameTa: 'வெங்காயம்',
    scientificName: 'Allium cepa',
    category: 'Bulbs & Aromatics',
    plantPart: 'Thin Skin',
    isAiSupported: false,
    nutrientDataStatus: 'available',
    foodSafetyStatus: 'inedible_valorize_only',
    knownHazardsEn: 'Indigestible papery outer skin; exceptionally high quercetin bioflavonoids for natural dyes and broth extraction.',
    knownHazardsTa: 'உண்ண இயலாது; குவர்செடின் நிறமி மற்றும் இயற்கை சாயம் எடுக்க சிறந்தது.',
  ),
  const VegetableItem(
    id: 41,
    slug: 'garlic',
    nameEn: 'Garlic',
    nameTa: 'பூண்டு',
    scientificName: 'Allium sativum',
    category: 'Bulbs & Aromatics',
    plantPart: 'Thin Skin',
    isAiSupported: false,
    nutrientDataStatus: 'available',
    foodSafetyStatus: 'inedible_valorize_only',
    knownHazardsEn: 'Papery skins are fibrous; ideal for insect-repellent mulches or composting.',
    knownHazardsTa: 'பூச்சி விரட்டி மற்றும் இயற்கை உரத்திற்கு சிறந்தது.',
  ),
  const VegetableItem(
    id: 42,
    slug: 'shallots',
    nameEn: 'Shallots',
    nameTa: 'சின்ன வெங்காயம்',
    scientificName: 'Allium cepa var. aggregatum',
    category: 'Bulbs & Aromatics',
    plantPart: 'Thin Skin',
    isAiSupported: false,
    nutrientDataStatus: 'incomplete',
    foodSafetyStatus: 'inedible_valorize_only',
    knownHazardsEn: 'High polyphenol skin; extract for eco-friendly textile dyeing or compost.',
    knownHazardsTa: 'இயற்கை சாயத்திற்கு சிறந்தது.',
  ),
  const VegetableItem(
    id: 43,
    slug: 'ginger',
    nameEn: 'Ginger',
    nameTa: 'இஞ்சி',
    scientificName: 'Zingiber officinale',
    category: 'Bulbs & Aromatics',
    plantPart: 'Thin Skin',
    isAiSupported: false,
    nutrientDataStatus: 'available',
    foodSafetyStatus: 'safe_edible',
    knownHazardsEn: 'Wash soil carefully; ginger peel can be infused into herbal tea or dried for spice blends.',
    knownHazardsTa: 'மண்ணை நீக்க நன்கு கழுவ வேண்டும்; இஞ்சி டீ தயாரிக்கலாம்.',
  ),
  const VegetableItem(
    id: 44,
    slug: 'turmeric',
    nameEn: 'Turmeric',
    nameTa: 'மஞ்சள்',
    scientificName: 'Curcuma longa',
    category: 'Bulbs & Aromatics',
    plantPart: 'Thin Skin',
    isAiSupported: false,
    nutrientDataStatus: 'available',
    foodSafetyStatus: 'safe_edible',
    knownHazardsEn: 'Contains curcumin; stains skin and clothing; excellent antimicrobial composting agent.',
    knownHazardsTa: 'குர்குமின் நிறைந்தது; கிருமி நாசினி தன்மை கொண்டது.',
  ),

  // Group E — Plant Outer Layers & Stems (45-50)
  const VegetableItem(
    id: 45,
    slug: 'cabbage-outer-leaves',
    nameEn: 'Cabbage outer leaves',
    nameTa: 'முட்டைக்கோஸ் வெளிப்புற இலைகள்',
    scientificName: 'Brassica oleracea var. capitata',
    category: 'Plant Outer Layer',
    plantPart: 'Outer Leaves',
    isAiSupported: false,
    nutrientDataStatus: 'available',
    foodSafetyStatus: 'conditional_cooking_required',
    knownHazardsEn: 'Highest pesticide exposure layer; wash rigorously in baking soda solution or salt water.',
    knownHazardsTa: 'பூச்சிக்கொல்லி எச்சங்கள் அதிகம் இருக்கும் என்பதால் உப்பு/பேக்கிங் சோடா நீரில் நன்கு கழுவ வேண்டும்.',
  ),
  const VegetableItem(
    id: 46,
    slug: 'cauliflower-outer-leaves',
    nameEn: 'Cauliflower outer leaves',
    nameTa: 'காலிஃபிளவர் வெளிப்புற இலைகள்',
    scientificName: 'Brassica oleracea var. botrytis',
    category: 'Plant Outer Layer',
    plantPart: 'Outer Leaves',
    isAiSupported: false,
    nutrientDataStatus: 'available',
    foodSafetyStatus: 'safe_edible',
    knownHazardsEn: 'Higher in iron and beta-carotene than florets. Highly nutritious in stir-fries.',
    knownHazardsTa: 'வெள்ளை பூவை விட இரும்புச்சத்து அதிகம்; சமைத்து உண்ண மிகவும் சிறந்தது.',
  ),
  const VegetableItem(
    id: 47,
    slug: 'broccoli-stalk-outer-layer',
    nameEn: 'Broccoli stalk outer layer',
    nameTa: 'ப்ரோக்கோலி தண்டு வெளிப்புற அடுக்கு',
    scientificName: 'Brassica oleracea var. italica',
    category: 'Plant Outer Layer',
    plantPart: 'Stem Outer Layer',
    isAiSupported: false,
    nutrientDataStatus: 'available',
    foodSafetyStatus: 'safe_edible',
    knownHazardsEn: 'Fibrous outer peel; peel lightly, chop finely and cook into soups.',
    knownHazardsTa: 'நார்ச்சத்து நிறைந்தது; சூப் செய்ய சிறந்தது.',
  ),
  const VegetableItem(
    id: 48,
    slug: 'banana-stem-outer-layers',
    nameEn: 'Banana stem outer layers',
    nameTa: 'வாழைத்தண்டு வெளிப்புற அடுக்கு',
    scientificName: 'Musa acuminata',
    category: 'Plant Outer Layer',
    plantPart: 'Stem Outer Layer',
    isAiSupported: false,
    nutrientDataStatus: 'incomplete',
    foodSafetyStatus: 'inedible_valorize_only',
    knownHazardsEn: 'Tough high-tensile fibres. Inedible; prime feedstock for paper, textile yarn, and compost.',
    knownHazardsTa: 'கடினமான இயற்கை நார்; காகிதம் மற்றும் கைவினை பொருட்கள் செய்ய ஏற்றது.',
  ),
  const VegetableItem(
    id: 49,
    slug: 'lotus-stem-outer-layer',
    nameEn: 'Lotus stem outer layer',
    nameTa: 'தாமரை தண்டு வெளிப்புற அடுக்கு',
    scientificName: 'Nelumbo nucifera',
    category: 'Plant Outer Layer',
    plantPart: 'Stem Outer Layer',
    isAiSupported: false,
    nutrientDataStatus: 'incomplete',
    foodSafetyStatus: 'conditional_cooking_required',
    knownHazardsEn: 'Aquatic stem surface can harbor parasites; MUST NEVER be consumed raw. Cook thoroughly.',
    knownHazardsTa: 'நீர் ஒட்டுண்ணிகள் இருக்க வாய்ப்புள்ளதால் பச்சையாக சாப்பிடக்கூடாது; வேகவைக்க வேண்டும்.',
  ),
  const VegetableItem(
    id: 50,
    slug: 'corn-husk',
    nameEn: 'Corn husk',
    nameTa: 'மக்காச்சோள உமி / சோளத்தோல்',
    scientificName: 'Zea mays',
    category: 'Plant Outer Layer',
    plantPart: 'Husk / Sheath',
    isAiSupported: false,
    nutrientDataStatus: 'incomplete',
    foodSafetyStatus: 'inedible_valorize_only',
    knownHazardsEn: 'Inedible tough silica sheath. Used as steaming wrappers, bio-packaging, and compost mulch.',
    knownHazardsTa: 'சாப்பிட இயலாது; உணவு வேகவைக்கும் உறை மற்றும் மக்கும் உரமாக பயன்படும்.',
  ),
];

// Catalogue Provider
final catalogueProvider = Provider<List<VegetableItem>>((ref) {
  return initialCatalogue;
});

// Currently Selected Vegetable
class SelectedVegetableNotifier extends StateNotifier<VegetableItem> {
  SelectedVegetableNotifier() : super(initialCatalogue.first);

  void select(VegetableItem veg) {
    state = veg;
  }

  void selectBySlug(String slug) {
    final found = initialCatalogue.firstWhere(
      (v) => v.slug == slug,
      orElse: () => initialCatalogue.first,
    );
    state = found;
  }
}

final selectedVegetableProvider = StateNotifierProvider<SelectedVegetableNotifier, VegetableItem>((ref) {
  return SelectedVegetableNotifier();
});

// Active Scan Result Provider
class CurrentScanNotifier extends StateNotifier<ScanResult?> {
  CurrentScanNotifier() : super(null);

  void setScan(ScanResult result) {
    state = result;
  }

  void confirmVegetable(VegetableItem veg) {
    if (state != null) {
      state = state!.copyWith(isConfirmed: true, confirmedVegetable: veg);
    }
  }

  void setWeight(double grams) {
    if (state != null) {
      state = state!.copyWith(weightGrams: grams);
    }
  }

  void clear() {
    state = null;
  }
}

final currentScanProvider = StateNotifierProvider<CurrentScanNotifier, ScanResult?>((ref) {
  return CurrentScanNotifier();
});

// Scan History Provider
class ScanHistoryNotifier extends StateNotifier<List<ScanResult>> {
  ScanHistoryNotifier() : super([
    ScanResult(
      scanId: 'SCN-101',
      imagePath: 'assets/sample_carrot.jpg',
      predictedVegetable: initialCatalogue[0],
      confidence: 0.94,
      isConfirmed: true,
      weightGrams: 85.0,
      scannedAt: DateTime.now().subtract(const Duration(hours: 2)),
    ),
    ScanResult(
      scanId: 'SCN-102',
      imagePath: 'assets/sample_potato.jpg',
      predictedVegetable: initialCatalogue[1],
      confidence: 0.89,
      isConfirmed: true,
      weightGrams: 120.0,
      scannedAt: DateTime.now().subtract(const Duration(days: 1)),
    ),
  ]);

  void addScan(ScanResult result) {
    state = [result, ...state];
  }
}

final scanHistoryProvider = StateNotifierProvider<ScanHistoryNotifier, List<ScanResult>>((ref) {
  return ScanHistoryNotifier();
});

// User Session State Provider
class UserSession {
  final bool isAuthenticated;
  final bool isAdmin;
  final String email;
  final String fullName;

  const UserSession({
    required this.isAuthenticated,
    required this.isAdmin,
    required this.email,
    required this.fullName,
  });
}

class AuthNotifier extends StateNotifier<UserSession> {
  AuthNotifier() : super(const UserSession(
    isAuthenticated: false,
    isAdmin: false,
    email: '',
    fullName: 'Guest User',
  ));

  void login(String email, String name, bool isAdmin) {
    state = UserSession(
      isAuthenticated: true,
      isAdmin: isAdmin,
      email: email,
      fullName: name,
    );
  }

  void logout() {
    state = const UserSession(
      isAuthenticated: false,
      isAdmin: false,
      email: '',
      fullName: 'Guest User',
    );
  }
}

final authProvider = StateNotifierProvider<AuthNotifier, UserSession>((ref) {
  return AuthNotifier();
});

// Dynamic Nutrients Repository for Selected Vegetable
final nutrientsForSelectedVegetableProvider = Provider<List<NutrientItem>>((ref) {
  final veg = ref.watch(selectedVegetableProvider);

  if (veg.slug == 'carrot') {
    return [
      const NutrientItem(code: 'vit_a', nameEn: 'Vitamin A / Carotenoids', nameTa: 'வைட்டமின் ஏ / கரோட்டினாய்டுகள்', category: 'vitamin', unit: 'mcg', concentrationPer100g: 835.0, biologicalRoleEn: 'Supports vision, immune integrity and mucosal epithelial regeneration.', biologicalRoleTa: 'பார்வைத்திறன் மற்றும் நோய் எதிர்ப்பு சக்தியை ஆதரிக்கிறது.'),
      const NutrientItem(code: 'vit_c', nameEn: 'Vitamin C (Ascorbic Acid)', nameTa: 'வைட்டமின் சி', category: 'vitamin', unit: 'mg', concentrationPer100g: 5.9, biologicalRoleEn: 'Potent antioxidant, cofactor in collagen synthesis.', biologicalRoleTa: 'கொலாஜன் உருவாக்கம் மற்றும் செல் பாதுகாப்பிற்கு உதவுகிறது.'),
      const NutrientItem(code: 'calcium', nameEn: 'Calcium (Ca)', nameTa: 'கால்சியம்', category: 'mineral', unit: 'mg', concentrationPer100g: 33.0, biologicalRoleEn: 'Bone and tooth structural integrity.', biologicalRoleTa: 'எலும்பு மற்றும் பற்களுக்கு உறுதி அளிக்கிறது.'),
      const NutrientItem(code: 'potassium', nameEn: 'Potassium (K)', nameTa: 'பொட்டாசியம்', category: 'mineral', unit: 'mg', concentrationPer100g: 320.0, biologicalRoleEn: 'Electrolyte balance, fluid homeostasis and cardiac rhythm.', biologicalRoleTa: 'இரத்த அழுத்தம் மற்றும் இதய துடிப்பை சீராக்குகிறது.'),
      const NutrientItem(code: 'dietary_fibre', nameEn: 'Total Dietary Fibre', nameTa: 'மொத்த உணவு நார்ச்சத்து', category: 'other', unit: 'g', concentrationPer100g: 2.8, biologicalRoleEn: 'Bowel motility, glycemic regulation, and gut microbiome nourishment.', biologicalRoleTa: 'செரிமானம் மற்றும் குடல் நலனை மேம்படுத்துகிறது.'),
      const NutrientItem(code: 'total_phenolics', nameEn: 'Total Phenolics (GAE)', nameTa: 'மொத்த பினாலிக் சேர்மங்கள்', category: 'other', unit: 'mg GAE', concentrationPer100g: 142.5, biologicalRoleEn: 'Free-radical scavenging protective bioactives.', biologicalRoleTa: 'செல்களை சேதத்திலிருந்து காக்கும் ஆக்ஸிஜனேற்றிகள்.'),
    ];
  } else if (veg.slug == 'potato') {
    return [
      const NutrientItem(code: 'vit_c', nameEn: 'Vitamin C', nameTa: 'வைட்டமின் சி', category: 'vitamin', unit: 'mg', concentrationPer100g: 11.4, biologicalRoleEn: 'Immune support and oxidative stress protection.', biologicalRoleTa: 'நோய் எதிர்ப்பு சக்தி அளிக்கிறது.'),
      const NutrientItem(code: 'potassium', nameEn: 'Potassium (K)', nameTa: 'பொட்டாசியம்', category: 'mineral', unit: 'mg', concentrationPer100g: 413.0, biologicalRoleEn: 'Muscle contraction and blood pressure regulation.', biologicalRoleTa: 'இரத்த அழுத்தத்தை சீராக்க உதவுகிறது.'),
      const NutrientItem(code: 'iron', nameEn: 'Iron (Fe)', nameTa: 'இரும்புச்சத்து', category: 'mineral', unit: 'mg', concentrationPer100g: 1.8, biologicalRoleEn: 'Haemoglobin oxygen transport.', biologicalRoleTa: 'இரத்த சிவப்பணு உற்பத்திக்கு உதவுகிறது.'),
      const NutrientItem(code: 'dietary_fibre', nameEn: 'Total Dietary Fibre', nameTa: 'மொத்த உணவு நார்ச்சத்து', category: 'other', unit: 'g', concentrationPer100g: 3.2, biologicalRoleEn: 'Promotes gut satiety and healthy intestinal peristalsis.', biologicalRoleTa: 'குடல் இயக்கத்தை சீராக்குகிறது.'),
    ];
  } else if (veg.slug == 'beetroot') {
    return [
      const NutrientItem(code: 'vit_c', nameEn: 'Vitamin C', nameTa: 'வைட்டமின் சி', category: 'vitamin', unit: 'mg', concentrationPer100g: 4.9, biologicalRoleEn: 'Antioxidant and endothelial integrity.', biologicalRoleTa: 'ஆக்ஸிஜனேற்ற தடுப்புக்கு உதவுகிறது.'),
      const NutrientItem(code: 'potassium', nameEn: 'Potassium (K)', nameTa: 'பொட்டாசியம்', category: 'mineral', unit: 'mg', concentrationPer100g: 336.0, biologicalRoleEn: 'Fluid balance and cardiovascular health.', biologicalRoleTa: 'இதய நலனை காக்கிறது.'),
      const NutrientItem(code: 'betalains', nameEn: 'Betalains (Bio-Pigments)', nameTa: 'பீட்டலைன்கள்', category: 'other', unit: 'mg', concentrationPer100g: 168.0, biologicalRoleEn: 'Potent natural antioxidants with liver-protective properties.', biologicalRoleTa: 'கல்லீரல் பாதுகாப்பு மற்றும் செல்களை காக்கும் இயற்கை நிறமிகள்.'),
      const NutrientItem(code: 'dietary_fibre', nameEn: 'Total Dietary Fibre', nameTa: 'மொத்த உணவு நார்ச்சத்து', category: 'other', unit: 'g', concentrationPer100g: 2.9, biologicalRoleEn: 'Improves digestion and gut flora.', biologicalRoleTa: 'செரிமானத்தை சீராக்குகிறது.'),
    ];
  }

  // Generic indicative profile for other vegetables
  return [
    const NutrientItem(code: 'dietary_fibre', nameEn: 'Dietary Fibre', nameTa: 'உணவு நார்ச்சத்து', category: 'other', unit: 'g', concentrationPer100g: 2.1, biologicalRoleEn: 'Promotes digestion and gut health.', biologicalRoleTa: 'செரிமானத்தை ஊக்குவிக்கிறது.'),
    const NutrientItem(code: 'potassium', nameEn: 'Potassium', nameTa: 'பொட்டாசியம்', category: 'mineral', unit: 'mg', concentrationPer100g: 195.0, biologicalRoleEn: 'Electrolyte balance.', biologicalRoleTa: 'உடலில் நீர் சமநிலையை பராமரிக்கிறது.'),
    const NutrientItem(code: 'total_phenolics', nameEn: 'Total Phenolics', nameTa: 'பினாலிக் சேர்மங்கள்', category: 'other', unit: 'mg GAE', concentrationPer100g: 65.0, biologicalRoleEn: 'Cellular antioxidant protection.', biologicalRoleTa: 'செல் பாதுகாப்பு அளிக்கிறது.'),
  ];
});

// Safety Rules for Selected Vegetable
final safetyRulesForSelectedVegetableProvider = Provider<List<SafetyRuleItem>>((ref) {
  final veg = ref.watch(selectedVegetableProvider);

  if (veg.slug == 'potato') {
    return [
      const SafetyRuleItem(
        code: 'SR_POTATO_SOLANINE',
        hazardType: 'glycoalkaloid',
        severity: 'critical',
        descriptionEn: 'CRITICAL WARNING: Exposure to light or sprouting triggers chlorophyll and toxic solanine/chaconine glycoalkaloid synthesis. Never eat green potato peels.',
        descriptionTa: 'முக்கிய எச்சரிக்கை: பச்சை நிறம் அல்லது முளைகட்டிய உருளைக்கிழங்கு தோல்களில் சோலானின் நச்சு உருவாகும். ஒருபோதும் உண்ணக்கூடாது.',
        alternativeEn: 'Divert strictly to aerobic composting away from edible crop beds.',
        alternativeTa: 'உரமாக்கலுக்கு மட்டும் பயன்படுத்தவும்.',
      ),
    ];
  } else if (veg.slug == 'cassava-tapioca') {
    return [
      const SafetyRuleItem(
        code: 'SR_CASSAVA_CYANIDE',
        hazardType: 'cyanogenic_glucoside',
        severity: 'critical',
        descriptionEn: 'LETHAL HAZARD: Cassava peels contain linamarin which releases hydrogen cyanide upon enzymatic hydrolysis. PROHIBITED for culinary broth, food, or raw animal feed.',
        descriptionTa: 'அபாய எச்சரிக்கை: மரவள்ளிக்கிழங்கு தோலில் சயனைடு நச்சு உள்ளது. சமையல் அல்லது விலங்கு தீவனத்திற்கு கண்டிப்பாக பயன்படுத்தக்கூடாது.',
        alternativeEn: 'Divert to municipal composting, biogas anaerobic digestion, or industrial bio-char production.',
        alternativeTa: 'உயிர்வாயு உற்பத்தி அல்லது உரமாக்கலுக்கு பயன்படுத்தவும்.',
      ),
    ];
  } else if (veg.slug == 'taro-colocasia') {
    return [
      const SafetyRuleItem(
        code: 'SR_TARO_OXALATE',
        hazardType: 'oxalate_raphide',
        severity: 'warning',
        descriptionEn: 'Contains microscopic needle-like calcium oxalate raphide crystals that cause severe throat irritation and dermal itching.',
        descriptionTa: 'கால்சியம் ஆக்சலேட் ஊசி போன்ற படிகங்கள் அரிப்பை உண்டாக்கும்.',
        alternativeEn: 'Divert to composting with organic matter to break down oxalates.',
        alternativeTa: 'இயற்கை உரமாக்கல் முறைக்கு மாற்றவும்.',
      ),
    ];
  }

  return [
    const SafetyRuleItem(
      code: 'SR_GENERAL_HYGIENE',
      hazardType: 'pesticide_and_soil_bacteria',
      severity: 'notice',
      descriptionEn: 'Peels are the outermost barrier and accumulate soil microbes and pesticide residues. Soak and rinse thoroughly with clean water.',
      descriptionTa: 'தோலில் மண் துகள்கள் மற்றும் பூச்சிக்கொல்லி எச்சங்கள் இருக்கும் என்பதால் நன்கு கழுவ வேண்டும்.',
      alternativeEn: 'Composting if uncertain about chemical sprays or agricultural treatments.',
      alternativeTa: 'உரமாக்கல் முறைக்கு மாற்றலாம்.',
    ),
  ];
});

// Reuse Recommendations for Selected Vegetable
final reuseMethodsForSelectedVegetableProvider = Provider<List<ReuseMethodItem>>((ref) {
  final veg = ref.watch(selectedVegetableProvider);

  if (veg.foodSafetyStatus == 'hazardous_raw' || veg.foodSafetyStatus == 'inedible_valorize_only') {
    return [
      const ReuseMethodItem(
        code: 'aerobic_composting',
        nameEn: 'Aerobic Composting',
        nameTa: 'காற்றுள்ள உரமாக்கல்',
        category: 'Composting',
        evidenceRank: 1,
        instructionsEn: 'Chop peels into 2cm pieces, blend with dry brown matter (leaves/sawdust) in 1:2 ratio. Maintains high microbial heat breakdown.',
        instructionsTa: 'தோல்களை சிறு துண்டுகளாக நறுக்கி, காய்ந்த இலைகளுடன் 1:2 விகிதத்தில் கலந்து உரமாக்கவும்.',
      ),
      const ReuseMethodItem(
        code: 'biogas_anaerobic',
        nameEn: 'Biogas Anaerobic Digestion',
        nameTa: 'உயிர்வாயு உற்பத்தி',
        category: 'Biogas',
        evidenceRank: 2,
        instructionsEn: 'High-methane organic feedstock for anaerobic digesters. Produces green fuel and nutrient-rich bio-slurry.',
        instructionsTa: 'உயிர்வாயு ஆலைகளுக்கு உகந்த கரிம மூலப்பொருள்; மீத்தேன் வாயு மற்றும் இயற்கை உரம் உற்பத்தி செய்யும்.',
      ),
      const ReuseMethodItem(
        code: 'natural_pigment',
        nameEn: 'Natural Bio-Pigment Extraction',
        nameTa: 'இயற்கை வண்ண நிறமி பிரித்தெடுத்தல்',
        category: 'Bio-materials',
        evidenceRank: 3,
        instructionsEn: 'Simmer dry peels in water (or ethanol extraction) to isolate polyphenols and bio-colorants for textile and artisan crafts.',
        instructionsTa: 'தோல்களை கொதிக்க வைத்து இயற்கை சாயம் தயாரித்து ஜவுளிகளுக்கு பயன்படுத்தலாம்.',
      ),
    ];
  }

  return [
    const ReuseMethodItem(
      code: 'culinary_stock',
      nameEn: 'Nutrient-Rich Vegetable Broth',
      nameTa: 'சமையல் காய்கறி சூப் / சாறு',
      category: 'Culinary Food',
      evidenceRank: 1,
      instructionsEn: 'Scrub peels cleanly, freeze until 250g collected, then simmer with water, peppercorns, and herbs for 45 minutes. Strain thoroughly.',
      instructionsTa: 'நன்கு கழுவிய தோல்களை தண்ணீரில் மிளகு, மூலிகைகளுடன் 45 நிமிடங்கள் வேகவைத்து சத்தான சூப் தயாரிக்கவும்.',
    ),
    const ReuseMethodItem(
      code: 'culinary_crisps',
      nameEn: 'Baked Crispy Peel Chips',
      nameTa: 'வறுக்கப்பட்ட காய்கறி சிப்ஸ்',
      category: 'Culinary Food',
      evidenceRank: 2,
      instructionsEn: 'Toss dry clean peels with a drizzle of olive oil, turmeric, and pinch of salt. Bake at 180°C for 15-20 minutes until crisp.',
      instructionsTa: 'எண்ணெய், மஞ்சள், உப்பு சேர்த்து 180°C வெப்பத்தில் 15-20 நிமிடங்கள் வறுத்து ஆரோக்கியமான சிப்ஸ் செய்யலாம்.',
    ),
    const ReuseMethodItem(
      code: 'vermicomposting',
      nameEn: 'Vermicomposting',
      nameTa: 'மண்புழு உரமாக்கல்',
      category: 'Composting',
      evidenceRank: 3,
      instructionsEn: 'Ideal worm food for Eisenia fetida bins. Accelerates premium organic vermicast production within 45 days.',
      instructionsTa: 'மண்புழுக்களுக்கு சிறந்த உணவு; 45 நாட்களில் தரமான மண்புழு உரம் கிடைக்கும்.',
    ),
  ];
});
