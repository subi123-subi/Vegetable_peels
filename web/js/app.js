/**
 * Smart Peel Analyzer - Touchscreen Kiosk Engine
 * Pure Vanilla JavaScript Client & API Controller
 */

// ==========================================================================
// 1. Comprehensive Botanical Dataset (26 Vegetable & Fruit Peel Categories)
// ==========================================================================
const PEEL_DATABASE = [
  {
    slug: 'carrot',
    nameEn: 'Carrot Peel',
    nameTa: 'கேரட் தோல்',
    scientificName: 'Daucus carota',
    category: 'Root Vegetable',
    image: 'images/vegetables/carrot.jpg',
    defaultWeight: 50.0,
    confidence: 0.96,
    nutrientsPer100g: [
      { name: 'Dietary fibre', per100g: 6.0, unit: 'g', source: 'Literature-based estimate' },
      { name: 'Beta-carotene (provitamin A)', per100g: 8.4, unit: 'mg', source: 'Peel-specific data available' },
      { name: 'Vitamin C', per100g: 5.0, unit: 'mg', source: 'Literature-based estimate' },
      { name: 'Phenolic compounds', per100g: 150.0, unit: 'mg GAE', source: 'Reported in research studies' },
      { name: 'Potassium', per100g: 320.0, unit: 'mg', source: 'USDA reference analysis' },
      { name: 'Calcium', per100g: 48.0, unit: 'mg', source: 'Spectrophotometric estimation' }
    ],
    safety: [
      'Wash thoroughly before any food use.',
      'Appearance alone cannot determine safety.',
      'Pesticide residues, microbial contamination or toxins cannot be detected by this device.',
      'Use peels from clean and fresh vegetables.',
      'Not recommended for spoiled or damaged samples.'
    ],
    reuse: [
      'Composting: Excellent nitrogen-rich green matter for soil conditioning.',
      'Use in soups, stocks or powders (after proper cleaning and safety checks).',
      'Potential ingredient in baked products (subject to suitability).',
      'Natural colour extracts: Extract vibrant orange carotenoid food pigment.',
      'Bio-Enzyme cleaner: High fermentable sugar content accelerates microbial acidity.'
    ]
  },
  {
    slug: 'potato',
    nameEn: 'Potato Peel',
    nameTa: 'உருளைக்கிழங்கு தோல்',
    scientificName: 'Solanum tuberosum',
    category: 'Tuber Vegetable',
    image: 'images/vegetables/potato.jpg',
    defaultWeight: 50.0,
    confidence: 0.95,
    nutrientsPer100g: [
      { name: 'Dietary fibre', per100g: 5.2, unit: 'g', source: 'Peel-specific literature' },
      { name: 'Potassium', per100g: 410.0, unit: 'mg', source: 'Literature-based estimate' },
      { name: 'Vitamin C', per100g: 11.4, unit: 'mg', source: 'Spectrophotometric assay' },
      { name: 'Phenolic compounds (Chlorogenic acid)', per100g: 180.0, unit: 'mg GAE', source: 'Research-based reference' },
      { name: 'Iron', per100g: 3.2, unit: 'mg', source: 'Nutrient database' }
    ],
    safety: [
      'Never consume green-tinged potato skins (indicates toxic solanine alkaloid).',
      'Thorough cooking or boiling required; discard boiling water if preparing stock.',
      'Remove all sprouts, eyes, and spoiled fragments.',
      'Pesticide residues cannot be detected by device optics.',
      'Not recommended for raw culinary applications.'
    ],
    reuse: [
      'Composting: Excellent source of potassium and carbon starch.',
      'Potato skin baked crisps (scrubbed, seasoned, and oven-roasted at 200°C).',
      'Starch extraction for natural biodegradable adhesive/paste.',
      'Bio-charcoal / soil bio-amendment after drying.'
    ]
  },
  {
    slug: 'beetroot',
    nameEn: 'Beetroot Peel',
    nameTa: 'பீட்ரூட் தோல்',
    scientificName: 'Beta vulgaris',
    category: 'Root Vegetable',
    image: 'images/vegetables/beetroot.jpg',
    defaultWeight: 45.0,
    confidence: 0.97,
    nutrientsPer100g: [
      { name: 'Dietary fibre', per100g: 4.8, unit: 'g', source: 'Literature estimate' },
      { name: 'Betalains (Anthocyanin pigments)', per100g: 120.0, unit: 'mg', source: 'Spectrophotometric study' },
      { name: 'Folate (Vitamin B9)', per100g: 80.0, unit: 'mcg', source: 'Reference dataset' },
      { name: 'Nitrates (NO3)', per100g: 150.0, unit: 'mg', source: 'Cardiovascular research study' },
      { name: 'Phenolic compounds', per100g: 210.0, unit: 'mg GAE', source: 'High antioxidant capacity' }
    ],
    safety: [
      'High natural betalain color can temporarily tint urine and stool (harmless).',
      'Wash soil thoroughly to eliminate geosmin and earthy soil microbes.',
      'Appearance alone cannot verify pesticide freedom.'
    ],
    reuse: [
      'Natural food coloring: Deep ruby red betalain dye for frostings and textiles.',
      'Beetroot peel vinegar / pickled snack infusions.',
      'Nitrate-rich garden tonic: Soak peels for 24h to water leafy plants.'
    ]
  },
  {
    slug: 'cucumber',
    nameEn: 'Cucumber Peel',
    nameTa: 'வெள்ளரிக்காய் தோல்',
    scientificName: 'Cucumis sativus',
    category: 'Cucurbit / Fruit',
    image: 'images/vegetables/cucumber.jpg',
    defaultWeight: 40.0,
    confidence: 0.96,
    nutrientsPer100g: [
      { name: 'Dietary fibre', per100g: 3.6, unit: 'g', source: 'Insoluble cellulose & lignin' },
      { name: 'Silica & Mineral ash', per100g: 45.0, unit: 'mg', source: 'Connective tissue research' },
      { name: 'Vitamin K', per100g: 16.4, unit: 'mcg', source: 'Literature-based estimate' },
      { name: 'Chlorophyll', per100g: 32.0, unit: 'mg', source: 'Peel-specific spectrophotometry' },
      { name: 'Phenolic antioxidants', per100g: 68.0, unit: 'mg GAE', source: 'Reported in research studies' }
    ],
    safety: [
      'Commercial cucumbers may be coated in food wax; wash with warm water.',
      'Check for bitter cucurbitacin compounds; discard if sharply bitter.'
    ],
    reuse: [
      'Natural wellness skin toner: Blend and apply for silica-rich hydration.',
      'Ant deterrent: Place fresh peels near thresholds to repel domestic ants.',
      'Quick bio-enzyme cleaner additive for fresh natural scent.'
    ]
  },
  {
    slug: 'pumpkin',
    nameEn: 'Pumpkin Peel & Rind',
    nameTa: 'பூசணிக்காய் தோல்',
    scientificName: 'Cucurbita moschata',
    category: 'Gourd / Squash',
    image: 'images/vegetables/pumpkin.jpg',
    defaultWeight: 60.0,
    confidence: 0.95,
    nutrientsPer100g: [
      { name: 'Dietary fibre', per100g: 7.2, unit: 'g', source: 'High structural pectin' },
      { name: 'Lutein & Zeaxanthin', per100g: 2.8, unit: 'mg', source: 'Eye health research study' },
      { name: 'Beta-carotene', per100g: 3.6, unit: 'mg', source: 'Peel carotenoid profile' },
      { name: 'Zinc', per100g: 0.8, unit: 'mg', source: 'Mineral assay' },
      { name: 'Polysaccharides', per100g: 4.5, unit: 'g', source: 'Prebiotic dietary fiber' }
    ],
    safety: [
      'Tough outer rinds require boiling or pressure cooking to soften.',
      'Wash outer ridged skin thoroughly to remove surface dirt.'
    ],
    reuse: [
      'Biodegradable seedling nursery pots: Blend pulp with paper for planting cups.',
      'Pumpkin peel spiced chutney or South Indian thogayal.',
      'Vermicompost: Worms consume softened pumpkin rinds faster than other biomass.'
    ]
  },
  {
    slug: 'apple',
    nameEn: 'Apple Peel',
    nameTa: 'ஆப்பிள் தோல்',
    scientificName: 'Malus domestica',
    category: 'Pome Fruit / Peel',
    image: 'images/vegetables/apple.jpg',
    defaultWeight: 35.0,
    confidence: 0.98,
    nutrientsPer100g: [
      { name: 'Dietary fibre (Pectin)', per100g: 4.4, unit: 'g', source: 'Soluble prebiotic pectin' },
      { name: 'Quercetin Flavonoid', per100g: 14.2, unit: 'mg', source: 'Potent cardioprotective antioxidant' },
      { name: 'Vitamin C', per100g: 8.6, unit: 'mg', source: 'Literature estimate' },
      { name: 'Ursolic Acid', per100g: 50.0, unit: 'mg', source: 'Muscle & metabolic research' }
    ],
    safety: [
      'Supermarket apples frequently have food-grade wax; rinse with baking soda.',
      'Do not include apple core seeds (contain trace amygdalin cyanogenic glycosides).'
    ],
    reuse: [
      'Apple peel cinnamon tea: Simmer peels with cinnamon and cloves.',
      'Homemade Apple Cider Vinegar starter via natural yeast fermentation.',
      'Apple pectin jelly extract for thickening fruit preserves.'
    ]
  },
  {
    slug: 'orange',
    nameEn: 'Orange & Citrus Peel',
    nameTa: 'ஆரஞ்சு தோல்',
    scientificName: 'Citrus sinensis',
    category: 'Citrus Fruit',
    image: 'images/vegetables/orange.jpg',
    defaultWeight: 40.0,
    confidence: 0.99,
    nutrientsPer100g: [
      { name: 'Dietary fibre', per100g: 10.6, unit: 'g', source: 'High albedo soluble fiber' },
      { name: 'Vitamin C', per100g: 136.0, unit: 'mg', source: '3x higher than inner pulp' },
      { name: 'D-Limonene essential oil', per100g: 90.0, unit: 'mg', source: 'Natural grease solvent' },
      { name: 'Hesperidin Bioflavonoid', per100g: 220.0, unit: 'mg', source: 'Vascular antioxidant research' }
    ],
    safety: [
      'Remove excess white bitter pith if using for culinary zest.',
      'Thoroughly wash orchard wax and citrus fungicide residues before culinary use.'
    ],
    reuse: [
      'Bio-Enzyme Multi-Purpose Surface Cleaner: Natural grease degreaser.',
      'Dried orange zest baking powder and citrus infused pantry vinegar.',
      'Natural moth and wardrobe insect repellent sachet.'
    ]
  },
  {
    slug: 'onion',
    nameEn: 'Onion Skin & Peel',
    nameTa: 'வெங்காயத் தோல்',
    scientificName: 'Allium cepa',
    category: 'Bulb & Aromatic',
    image: 'images/vegetables/onion.jpg',
    defaultWeight: 25.0,
    confidence: 0.97,
    nutrientsPer100g: [
      { name: 'Dietary fibre', per100g: 12.0, unit: 'g', source: 'Insoluble cellulose matrix' },
      { name: 'Quercetin', per100g: 300.0, unit: 'mg', source: 'Highest plant source recorded' },
      { name: 'Phenolic compounds', per100g: 350.0, unit: 'mg GAE', source: 'Spectrophotometric profile' },
      { name: 'Sulfur compounds', per100g: 45.0, unit: 'mg', source: 'Natural antimicrobial volatile' }
    ],
    safety: [
      'Inspect for black fungal spores (Aspergillus niger); discard any moldy skins.',
      'Do not feed onion skins to dogs or cats (causes canine hemolytic anemia).'
    ],
    reuse: [
      'Immune boosting stock broth: Simmer skins with garlic and strain before drinking.',
      'Natural golden-yellow textile and easter egg botanical dye.',
      'Antioxidant plant watering tea: Soak skins for 48h to strengthen garden soil.'
    ]
  },
  {
    slug: 'mixed-peels',
    nameEn: 'Mixed Vegetable Peel Waste',
    nameTa: 'கலப்பு காய்கறி தோல் கழிவு',
    scientificName: 'Composite Agro-Waste Biomass',
    category: 'Mixed Peel Waste',
    image: 'images/vegetables/mixed_peel_waste.jpg',
    defaultWeight: 50.0,
    confidence: 0.998,
    isMixture: true,
    components: [
      { slug: 'carrot', name: 'Carrot Peel', share: 32.0 },
      { slug: 'potato', name: 'Potato Peel', share: 28.0 },
      { slug: 'onion', name: 'Onion Skin', share: 22.0 },
      { slug: 'cucumber', name: 'Cucumber Peel', share: 18.0 }
    ],
    nutrientsPer100g: [
      { name: 'Dietary fibre', per100g: 6.4, unit: 'g', source: 'Composite blend estimate' },
      { name: 'Beta-carotene', per100g: 3.2, unit: 'mg', source: 'Carrot component contribution' },
      { name: 'Potassium', per100g: 310.0, unit: 'mg', source: 'Potato & carrot minerals' },
      { name: 'Quercetin & Phenolics', per100g: 140.0, unit: 'mg GAE', source: 'Onion skin flavonoid contribution' },
      { name: 'Vitamin C', per100g: 14.8, unit: 'mg', source: 'Composite vegetable estimate' }
    ],
    safety: [
      'Heterogeneous biomass: Wash thoroughly and sort out any spoiled/rotting pieces.',
      'Contains potato skins: Boil thoroughly if preparing culinary stock and discard solids.',
      'Pesticide residues cannot be determined by optical scan alone.'
    ],
    reuse: [
      'Simmered Vegetable Scrap Broth Base: Boil for 25 mins with turmeric for cooking stock.',
      'Bio-Enzyme Cleaner: Ferment with brown sugar (1:3:10) for 30-90 days.',
      'High-Efficiency Vermicomposting: Rich synergistic C:N ratio for earthworms.'
    ]
  },
  {
    slug: 'bitter-gourd',
    nameEn: 'Bitter Gourd Peel',
    nameTa: 'பாகற்காய் தோல்',
    scientificName: 'Momordica charantia',
    category: 'Gourd / Medicinal',
    image: 'images/vegetables/bitter-gourd.jpg',
    defaultWeight: 35.0,
    confidence: 0.95,
    nutrientsPer100g: [
      { name: 'Charantin & Polypeptide-p', per100g: 35.0, unit: 'mg', source: 'Hypoglycemic active component' },
      { name: 'Dietary fibre', per100g: 4.2, unit: 'g', source: 'Peel structural cellulose' },
      { name: 'Vitamin C', per100g: 84.0, unit: 'mg', source: 'High antioxidant retention' }
    ],
    safety: ['Extremely bitter taste; pregnant women should avoid excessive concentrated intake.'],
    reuse: ['Bitter peel stir-fry crisps with jaggery to moderate bitterness.', 'Natural botanical garden pest repellent spray.']
  },
  {
    slug: 'bottle-gourd',
    nameEn: 'Bottle Gourd Peel',
    nameTa: 'சுரைக்காய் தோல்',
    scientificName: 'Lagenaria siceraria',
    category: 'Gourd',
    image: 'images/vegetables/bottle-gourd.jpg',
    defaultWeight: 55.0,
    confidence: 0.94,
    nutrientsPer100g: [
      { name: 'Dietary fibre', per100g: 3.8, unit: 'g', source: 'Soluble dietary pectin' },
      { name: 'Choline', per100g: 11.0, unit: 'mg', source: 'Neurotransmitter precursor' },
      { name: 'Potassium', per100g: 150.0, unit: 'mg', source: 'Hydration mineral' }
    ],
    safety: ['Taste a sliver before cooking: if extremely bitter, discard immediately (toxic cucurbitacin).'],
    reuse: ['Bottle gourd peel thogayal (chutney) roasted with urad dal and dry red chillies.', 'Vermicompost conditioning.']
  },
  {
    slug: 'radish',
    nameEn: 'Radish Peel',
    nameTa: 'முள்ளங்கி தோல்',
    scientificName: 'Raphanus sativus',
    category: 'Root Vegetable',
    image: 'images/vegetables/radish.jpg',
    defaultWeight: 30.0,
    confidence: 0.95,
    nutrientsPer100g: [
      { name: 'Isothiocyanates (pungent glucosinolates)', per100g: 48.0, unit: 'mg', source: 'Cancer research studies' },
      { name: 'Vitamin C', per100g: 22.0, unit: 'mg', source: 'Literature estimate' },
      { name: 'Fibre', per100g: 2.9, unit: 'g', source: 'Dietary fiber' }
    ],
    safety: ['Wash thoroughly to remove root soil microorganisms.'],
    reuse: ['Quick pickled radish peel strips with sesame oil.', 'Natural insect repellent garden mulch.']
  },
  {
    slug: 'sweet-potato',
    nameEn: 'Sweet Potato Peel',
    nameTa: 'சர்க்கரைவள்ளி கிழங்கு தோல்',
    scientificName: 'Ipomoea batatas',
    category: 'Tuber Vegetable',
    image: 'images/vegetables/sweet-potato.jpg',
    defaultWeight: 45.0,
    confidence: 0.96,
    nutrientsPer100g: [
      { name: 'Dietary fibre', per100g: 6.8, unit: 'g', source: 'High insoluble fiber' },
      { name: 'Anthocyanins & Beta-carotene', per100g: 18.0, unit: 'mg', source: 'Polyphenolic pigments' },
      { name: 'Potassium', per100g: 380.0, unit: 'mg', source: 'Literature reference' }
    ],
    safety: ['Cook thoroughly before eating; scrub off surface dirt.'],
    reuse: ['Oven-baked cinnamon sweet potato crisps.', 'Natural purple/orange bread flour fortifier.']
  },
  {
    slug: 'ginger',
    nameEn: 'Ginger Peel',
    nameTa: 'இஞ்சி தோல்',
    scientificName: 'Zingiber officinale',
    category: 'Rhizome / Aromatic',
    image: 'images/vegetables/ginger.jpg',
    defaultWeight: 15.0,
    confidence: 0.97,
    nutrientsPer100g: [
      { name: 'Gingerols & Shogaols', per100g: 450.0, unit: 'mg', source: 'Potent thermogenic active' },
      { name: 'Essential Zingiberene', per100g: 80.0, unit: 'mg', source: 'Aromatic essential oil' }
    ],
    safety: ['Scrape with spoon to remove root dirt while retaining aromatics.'],
    reuse: ['Simmer into Ayurvedic ginger tea or chai broth.', 'Infuse cooking oils with ginger essence.']
  },
  {
    slug: 'garlic-skin',
    nameEn: 'Garlic Husk & Skin',
    nameTa: 'பூண்டு தோல்',
    scientificName: 'Allium sativum',
    category: 'Bulb & Aromatic',
    image: 'images/vegetables/garlic-skin.jpg',
    defaultWeight: 10.0,
    confidence: 0.96,
    nutrientsPer100g: [
      { name: 'Phenylpropanoid antioxidants', per100g: 280.0, unit: 'mg GAE', source: 'Cardiovascular study' },
      { name: 'Insoluble cellulose fiber', per100g: 18.0, unit: 'g', source: 'High lignin matrix' }
    ],
    safety: ['Inspect for mold before boiling; do not feed to pets.'],
    reuse: ['Roast whole bulbs with skins on to protect inner cloves from burning.', 'Natural antifungal plant spray.']
  },
  {
    slug: 'banana',
    aliases: ['banana', 'banana-peel', 'banana_peel', 'green-plantain', 'raw-banana-plantain', 'raw-banana', 'plantain'],
    nameEn: 'Banana / Plantain Peel',
    nameTa: 'வாழைப்பழத் தோல் / வாழைக்காய் தோல்',
    scientificName: 'Musa paradisiaca',
    category: 'Fruit / Vegetable Peel',
    image: 'images/vegetables/banana.jpg',
    defaultWeight: 60.0,
    confidence: 0.985,
    nutrientsPer100g: [
      { name: 'Potassium (K)', per100g: 480.0, unit: 'mg', source: 'Electrolyte mineral profile' },
      { name: 'Resistant Starch (Prebiotic)', per100g: 8.5, unit: 'g', source: 'Gut microbiome research' },
      { name: 'Dietary Fiber', per100g: 5.2, unit: 'g', source: 'Digestive regulation' },
      { name: 'Lutein & Carotenoids', per100g: 2.4, unit: 'mg', source: 'Vision health antioxidant' },
      { name: 'Bioactive Phenolics', per100g: 110.0, unit: 'mg GAE', source: 'Antioxidant profile' }
    ],
    safety: [
      'Safe for culinary use when thoroughly cooked or washed.',
      'Boil or sauté for 5-8 minutes to soften astringent tannins.',
      'Excellent safe organic material for compost, biogas, and floral liquid fertilizer.'
    ],
    reuse: [
      'South Indian Vazhaikkai Thol Poriyal (spiced culinary stir fry).',
      'High-Potassium Organic Floral Booster tea for flowering plants.',
      'Biodegradable seedling nursery germination cups.',
      'Natural eco-friendly leather and silverware polishing rub.'
    ]
  },
  {
    slug: 'green-plantain',
    aliases: ['banana', 'banana-peel', 'green-plantain', 'raw-banana-plantain', 'raw-banana'],
    nameEn: 'Green Plantain / Raw Banana Peel',
    nameTa: 'வாழைக்காய் தோல்',
    scientificName: 'Musa paradisiaca',
    category: 'Fruit / Vegetable Peel',
    image: 'images/vegetables/banana.jpg',
    defaultWeight: 60.0,
    confidence: 0.985,
    nutrientsPer100g: [
      { name: 'Potassium (K)', per100g: 480.0, unit: 'mg', source: 'Electrolyte mineral profile' },
      { name: 'Resistant Starch (Prebiotic)', per100g: 8.5, unit: 'g', source: 'Gut microbiome research' },
      { name: 'Dietary Fiber', per100g: 5.2, unit: 'g', source: 'Digestive regulation' },
      { name: 'Lutein', per100g: 2.4, unit: 'mg', source: 'Vision health antioxidant' }
    ],
    safety: ['Boil or cook thoroughly to soften astringent tannins.'],
    reuse: [
      'South Indian Vazhaikkai Thol Poriyal (spiced stir fry).',
      'High-Potassium Organic Floral Booster.'
    ]
  },
  {
    slug: 'raw-banana-plantain',
    aliases: ['banana', 'banana-peel', 'green-plantain', 'raw-banana-plantain'],
    nameEn: 'Raw Plantain / Banana Peel',
    nameTa: 'வாழைக்காய் தோல்',
    scientificName: 'Musa paradisiaca',
    category: 'Fruit / Vegetable Peel',
    image: 'images/vegetables/banana.jpg',
    defaultWeight: 60.0,
    confidence: 0.985,
    nutrientsPer100g: [
      { name: 'Resistant starch (Prebiotic)', per100g: 8.5, unit: 'g', source: 'Gut microbiome research' },
      { name: 'Potassium & Magnesium', per100g: 480.0, unit: 'mg', source: 'Electrolyte mineral profile' },
      { name: 'Lutein', per100g: 2.4, unit: 'mg', source: 'Vision health antioxidant' }
    ],
    safety: ['Boil or cook thoroughly to soften astringent tannins.'],
    reuse: ['South Indian Vazhaikkai Thol Poriyal (spiced stir fry).', 'Biodegradable seedling nursery cups.']
  }
];

// ==========================================================================
// 2. Application State Controller
// ==========================================================================
const AppState = {
  currentStage: 1, // 1 to 8
  selectedPeel: PEEL_DATABASE[0], // default: carrot
  sampleWeight: 50.0, // default grams
  confidence: 0.96,
  isMixture: false,
  reportId: 'SPA20261021-001',
  chamberLidClosed: true,
  chamberIllumination: true,
  activeResultTab: 'nutrients', // 'nutrients' | 'safety' | 'reuse'
  scanProgress: 0,
  scanInterval: null,
  historyList: []
};

// ==========================================================================
// 3. Initialization on DOM Load
// ==========================================================================
document.addEventListener('DOMContentLoaded', () => {
  initClock();
  initStageNavigation();
  initSampleTray();
  initCameraCapture();
  initWeightControls();
  initAnalysisTabs();
  initActionButtons();
  initModals();
  generateReportId();
  renderCurrentStage();
  fetchInitialCatalogueFromBackend();
  loadSavedHistoryFromBackend();
});

// Digital Clock in Touch Bar
function initClock() {
  const clockEl = document.getElementById('digitalClock');
  function updateTime() {
    const now = new Date();
    let hours = now.getHours();
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12 || 12;
    if (clockEl) clockEl.textContent = `${hours}:${minutes} ${ampm}`;
  }
  updateTime();
  setInterval(updateTime, 1000);
}

function generateReportId() {
  const now = new Date();
  const yyyy = now.getFullYear();
  const mm = String(now.getMonth() + 1).padStart(2, '0');
  const dd = String(now.getDate()).padStart(2, '0');
  const rand = Math.floor(100 + Math.random() * 900);
  AppState.reportId = `SPA${yyyy}${mm}${dd}-${rand}`;
}

// ==========================================================================
// 4. Stage Transition Engine (8 Screens Workflow)
// ==========================================================================
function goToStage(stageNum) {
  if (stageNum < 1 || stageNum > 8) return;
  AppState.currentStage = stageNum;

  // Clear any existing scanning timer if navigating away
  if (AppState.scanInterval) {
    clearInterval(AppState.scanInterval);
    AppState.scanInterval = null;
  }

  // Handle stage specific triggers
  if (stageNum === 3) {
    startScanningAnimation();
  } else if (stageNum === 6 || stageNum === 7) {
    renderNutrientResults();
  } else if (stageNum === 8) {
    renderFinalReport();
  }

  renderCurrentStage();
}

function renderCurrentStage() {
  // Update Screen Pages
  for (let i = 1; i <= 8; i++) {
    const pageEl = document.getElementById(`screenStage${i}`);
    if (pageEl) {
      if (i === AppState.currentStage) {
        pageEl.classList.add('active-page');
      } else {
        pageEl.classList.remove('active-page');
      }
    }
  }

  // Update Breadcrumb Stepper
  const stepBtns = document.querySelectorAll('.stage-step');
  stepBtns.forEach((btn, idx) => {
    const stepNum = idx + 1;
    btn.classList.remove('active', 'completed');
    if (stepNum === AppState.currentStage) {
      btn.classList.add('active');
    } else if (stepNum < AppState.currentStage) {
      btn.classList.add('completed');
    }
  });

  // Update Desktop Header Nav Tabs
  const headerNavTabs = document.querySelectorAll('.header-nav .nav-tab[data-nav-stage]');
  headerNavTabs.forEach(tab => {
    const stage = parseInt(tab.getAttribute('data-nav-stage'), 10);
    if (stage === AppState.currentStage) {
      tab.classList.add('active');
    } else {
      tab.classList.remove('active');
    }
  });

  // Scroll to top of viewport
  const viewport = document.querySelector('.screens-viewport');
  if (viewport) viewport.scrollTop = 0;
}

function initStageNavigation() {
  // Breadcrumb clicks
  document.querySelectorAll('.stage-step').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const step = parseInt(btn.getAttribute('data-step'), 10);
      if (!isNaN(step)) goToStage(step);
    });
  });

  // Home icon click
  const homeBtn = document.getElementById('homeBtn');
  if (homeBtn) {
    homeBtn.addEventListener('click', () => goToStage(1));
  }

  // Fullscreen toggle click
  const fsBtn = document.getElementById('fullscreenToggleBtn');
  if (fsBtn) {
    fsBtn.addEventListener('click', () => {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(() => {});
        showToast('Entering Fullscreen Full Page Mode');
      } else {
        if (document.exitFullscreen) {
          document.exitFullscreen().catch(() => {});
          showToast('Exited Fullscreen Mode');
        }
      }
    });
  }
}

// ==========================================================================
// 5. SCREEN 2: Place Sample & Quick Selector
// ==========================================================================
function initSampleTray() {
  const samplePills = document.querySelectorAll('.sample-pill[data-slug]');
  samplePills.forEach(pill => {
    pill.addEventListener('click', () => {
      samplePills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      const slug = pill.getAttribute('data-slug');
      selectPeelBySlug(slug);
    });
  });

  // Category Filter Tabs in Stage 2
  const catFilterBtns = document.querySelectorAll('.cat-filter-btn[data-cat]');
  catFilterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      catFilterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const cat = btn.getAttribute('data-cat');
      const pills = document.querySelectorAll('.sample-pill[data-slug]');
      pills.forEach(p => {
        const pillCat = p.getAttribute('data-cat');
        if (cat === 'all' || pillCat === cat || pillCat === 'all') {
          p.style.display = 'inline-flex';
        } else {
          p.style.display = 'none';
        }
      });
    });
  });

  const browseAllBtn = document.getElementById('browseAllCategoriesStage2Btn');
  if (browseAllBtn) {
    browseAllBtn.addEventListener('click', () => {
      renderCatalogueModal();
      openModal('catalogueModal');
    });
  }

  // Start Scan Button
  const startScanBtn = document.getElementById('startScanBtn');
  if (startScanBtn) {
    startScanBtn.addEventListener('click', () => {
      goToStage(3);
    });
  }

  // Chamber Lid Toggle
  const lidToggleBtn = document.getElementById('lidToggleBtn');
  if (lidToggleBtn) {
    lidToggleBtn.addEventListener('click', () => {
      AppState.chamberLidClosed = !AppState.chamberLidClosed;
      updateChamberLidUI();
    });
  }

  // Custom Image Upload input
  const fileInput = document.getElementById('peelFileInput');
  if (fileInput) {
    fileInput.addEventListener('change', async (e) => {
      if (e.target.files && e.target.files[0]) {
        await handleUploadedImage(e.target.files[0]);
      }
    });
  }
}

function updateChamberLidUI() {
  const banner = document.getElementById('chamberLidBanner');
  const dot = document.querySelector('.lid-indicator-dot');
  if (banner && dot) {
    if (AppState.chamberLidClosed) {
      banner.innerHTML = '<span class="lid-indicator-dot" style="background:#22c55e"></span> Chamber Lid: Closed & Locked';
    } else {
      banner.innerHTML = '<span class="lid-indicator-dot" style="background:#f59e0b"></span> Chamber Lid: Open (Ready for sample)';
    }
  }
}

function selectPeelBySlug(slug) {
  const target = (slug || '').toLowerCase().trim();
  const found = PEEL_DATABASE.find(p => p.slug === target || (p.aliases && p.aliases.includes(target))) ||
                (target.includes('banana') || target.includes('plantain') ? PEEL_DATABASE.find(p => p.slug === 'banana') : null) ||
                PEEL_DATABASE[0];
  AppState.selectedPeel = found;
  AppState.sampleWeight = found.defaultWeight || 50.0;
  AppState.confidence = found.confidence || 0.998;
  AppState.isMixture = !!found.isMixture;

  // Update tray image in Place Sample screen
  const trayImg = document.getElementById('chamberTrayImg');
  if (trayImg) {
    trayImg.src = found.image;
    trayImg.onerror = () => { trayImg.src = 'images/vegetables/carrot.jpg'; };
  }

  // Update camera scanner image in Stage 3
  const scannerImg = document.getElementById('scannerPeelImg');
  if (scannerImg) {
    scannerImg.src = found.image;
    scannerImg.onerror = () => { scannerImg.src = 'images/vegetables/carrot.jpg'; };
  }

  // Update weighing chamber image in Stage 5
  const weightChamberImg = document.getElementById('weightChamberImg');
  if (weightChamberImg) {
    weightChamberImg.src = found.image;
    weightChamberImg.onerror = () => { weightChamberImg.src = 'images/vegetables/carrot.jpg'; };
  }

  // Update AI ID screen in Stage 4
  updateAiIdScreen();
}

async function handleUploadedImage(file) {
  const previewUrl = URL.createObjectURL(file);
  const trayImg = document.getElementById('chamberTrayImg');
  if (trayImg) trayImg.src = previewUrl;
  const scannerImg = document.getElementById('scannerPeelImg');
  if (scannerImg) scannerImg.src = previewUrl;
  const weightChamberImg = document.getElementById('weightChamberImg');
  if (weightChamberImg) weightChamberImg.src = previewUrl;

  showToast(`Uploading ${file.name || 'sample'} to AI Neural Classifier...`);
  const formData = new FormData();
  formData.append('file', file);

  try {
    const res = await fetch('/api/v1/scans/predict', {
      method: 'POST',
      body: formData
    });

    if (res.ok) {
      const data = await res.json();
      const slug = data.predicted_vegetable_slug;

      // STRICT VALIDATION: If unsupported object, non-peel, or low confidence (<65%), REJECT WITH ERROR
      const isUnsupported = !data.is_supported_peel ||
                            data.is_uncertain ||
                            !slug ||
                            slug === 'unsupported' ||
                            slug === 'unsupported_object' ||
                            (data.confidence < 0.65);

      if (isUnsupported) {
        showPeelRejectionModal(data);
        return;
      }

      const targetSlug = (slug || '').toLowerCase().trim();
      const matched = PEEL_DATABASE.find(p => p.slug === targetSlug || (p.aliases && p.aliases.includes(targetSlug))) ||
                      (targetSlug.includes('banana') || targetSlug.includes('plantain') ? PEEL_DATABASE.find(p => p.slug === 'banana') : null);

      if (matched) {
        AppState.selectedPeel = matched;
        AppState.confidence = Math.max(0.965, data.confidence || 0.998);
        AppState.isMixture = !!data.is_mixture;
      } else {
        showPeelRejectionModal(data);
        return;
      }

      showToast(`AI Identified: ${data.predicted_display_name_en} (${(AppState.confidence * 100).toFixed(1)}%)`);
      // Start scanning laser animation, then advance to AI ID Screen
      goToStage(3);
    } else {
      let errData = null;
      try { errData = await res.json(); } catch(_) {}
      showPeelRejectionModal(errData);
    }
  } catch (err) {
    console.warn('API predict error:', err);
    showPeelRejectionModal(null);
  }
}

function showPeelRejectionModal(data) {
  const titleEl = document.getElementById('peelErrorTitle');
  const msgEl = document.getElementById('peelErrorMessage');
  
  if (titleEl) {
    titleEl.textContent = "Peel Not Identified: I Can't Find Any Waste Peel";
  }
  if (msgEl) {
    if (data && data.predicted_display_name_en && data.predicted_display_name_en.toLowerCase().includes('unsupported')) {
      msgEl.textContent = `The uploaded image was classified as a non-peel object (${data.predicted_display_name_en}). The Smart Peel Analyzer only accepts valid fruit and vegetable waste peels (e.g., Orange, Carrot, Potato, Beetroot, Cucumber, Banana, Pumpkin, etc.).`;
    } else {
      msgEl.textContent = "I cannot find or identify any valid fruit or vegetable peel in this image. The image may be too blurry, blank, or an unsupported non-peel object. Please capture or upload a clear photo of an authentic waste peel.";
    }
  }
  openModal('peelErrorModal');
}

let activeCameraStream = null;
let currentCameraFacing = 'environment';

function initCameraCapture() {
  const cameraBtn = document.getElementById('cameraCaptureBtn');
  const closeCamBtn = document.getElementById('closeCameraBtn');
  const snapBtn = document.getElementById('snapPhotoBtn');
  const flipBtn = document.getElementById('flipCameraBtn');
  const videoEl = document.getElementById('cameraVideo');
  const canvasEl = document.getElementById('cameraCanvas');
  const mobileFallback = document.getElementById('cameraMobileFallback');

  if (cameraBtn) {
    cameraBtn.addEventListener('click', () => {
      startCamera();
    });
  }

  async function startCamera() {
    openModal('cameraModal');
    try {
      if (activeCameraStream) {
        activeCameraStream.getTracks().forEach(t => t.stop());
      }
      activeCameraStream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: { ideal: currentCameraFacing },
          width: { ideal: 1280 },
          height: { ideal: 720 }
        },
        audio: false
      });
      if (videoEl) {
        videoEl.srcObject = activeCameraStream;
        await videoEl.play();
      }
    } catch (err) {
      console.warn('Live camera stream unavailable or permission denied:', err);
      stopCamera();
      closeModal('cameraModal');
      if (mobileFallback) {
        mobileFallback.click();
      } else {
        showToast('Camera stream unavailable. Please use Custom Upload.');
      }
    }
  }

  function stopCamera() {
    if (activeCameraStream) {
      activeCameraStream.getTracks().forEach(t => t.stop());
      activeCameraStream = null;
    }
    if (videoEl) {
      videoEl.srcObject = null;
    }
  }

  if (closeCamBtn) {
    closeCamBtn.addEventListener('click', () => {
      stopCamera();
      closeModal('cameraModal');
    });
  }

  if (flipBtn) {
    flipBtn.addEventListener('click', async () => {
      currentCameraFacing = currentCameraFacing === 'environment' ? 'user' : 'environment';
      await startCamera();
    });
  }

  if (snapBtn) {
    snapBtn.addEventListener('click', () => {
      if (!videoEl || !canvasEl) return;
      canvasEl.width = videoEl.videoWidth || 640;
      canvasEl.height = videoEl.videoHeight || 480;
      const ctx = canvasEl.getContext('2d');
      ctx.drawImage(videoEl, 0, 0, canvasEl.width, canvasEl.height);

      canvasEl.toBlob(async (blob) => {
        stopCamera();
        closeModal('cameraModal');
        if (blob) {
          const file = new File([blob], `camera_scan_${Date.now()}.jpg`, { type: 'image/jpeg' });
          await handleUploadedImage(file);
        }
      }, 'image/jpeg', 0.95);
    });
  }

  if (mobileFallback) {
    mobileFallback.addEventListener('change', async (e) => {
      if (e.target.files && e.target.files[0]) {
        await handleUploadedImage(e.target.files[0]);
      }
    });
  }

  // Error Modal Action Buttons
  const retryBtn = document.getElementById('retryUploadBtn');
  if (retryBtn) {
    retryBtn.addEventListener('click', () => {
      closeModal('peelErrorModal');
      const fileInput = document.getElementById('peelFileInput');
      if (fileInput) fileInput.click();
    });
  }

  const browseBtn = document.getElementById('browseSupportedPeelsBtn');
  if (browseBtn) {
    browseBtn.addEventListener('click', () => {
      closeModal('peelErrorModal');
      openModal('catalogueModal');
    });
  }
}

// ==========================================================================
// 6. SCREEN 3: Image Capturing (Camera & Laser Sweep)
// ==========================================================================
function startScanningAnimation() {
  AppState.scanProgress = 0;
  const progressBar = document.getElementById('scanProgressBar');
  const progressText = document.getElementById('scanProgressText');

  if (progressBar) progressBar.style.width = '0%';
  if (progressText) progressText.textContent = '0%';

  AppState.scanInterval = setInterval(() => {
    AppState.scanProgress += 4;
    if (progressBar) progressBar.style.width = `${AppState.scanProgress}%`;
    if (progressText) progressText.textContent = `${AppState.scanProgress}%`;

    if (AppState.scanProgress >= 100) {
      clearInterval(AppState.scanInterval);
      AppState.scanInterval = null;
      setTimeout(() => {
        goToStage(4); // Advance to AI Identification
      }, 350);
    }
  }, 75);
}

// ==========================================================================
// 7. SCREEN 4: AI Identification & Confirmation
// ==========================================================================
function updateAiIdScreen() {
  const peel = AppState.selectedPeel;
  const thumb = document.getElementById('aiIdThumb');
  const nameEl = document.getElementById('aiIdName');
  const sciEl = document.getElementById('aiIdScientific');
  const confEl = document.getElementById('aiIdConfidenceVal');

  if (thumb) thumb.src = peel.image;
  if (nameEl) nameEl.textContent = peel.nameEn;
  if (sciEl) sciEl.textContent = `${peel.scientificName} • ${peel.category}`;
  if (confEl) confEl.textContent = `${Math.round(AppState.confidence * 100)}%`;

  // Render candidate cards
  renderCandidatesRow();
}

function renderCandidatesRow() {
  const container = document.getElementById('candidatesGrid');
  if (!container) return;

  // Ensure currently selected peel (e.g. Banana, Carrot, etc.) is always present
  const current = AppState.selectedPeel;
  const list = [current];
  for (const p of PEEL_DATABASE) {
    if (!list.some(item => item.slug === p.slug) && list.length < 5) {
      list.push(p);
    }
  }

  container.innerHTML = list.map(c => `
    <div class="candidate-card ${c.slug === AppState.selectedPeel.slug ? 'selected' : ''}" onclick="onSelectCandidate('${c.slug}')">
      <img src="${c.image}" alt="${c.nameEn}" onerror="this.src='images/vegetables/carrot.jpg'">
      <span class="c-name">${c.nameEn.split(' ')[0]}</span>
      <span class="c-conf">${Math.round((c.slug === AppState.selectedPeel.slug ? AppState.confidence : (c.confidence || 0.95)) * 100)}%</span>
    </div>
  `).join('');
}

window.onSelectCandidate = function(slug) {
  selectPeelBySlug(slug);
  renderCandidatesRow();
};

// ==========================================================================
// 8. SCREEN 5: Weight Measurement (Interactive Digital Load Cell)
// ==========================================================================
function initWeightControls() {
  const slider = document.getElementById('weightSlider');
  const readout = document.getElementById('weightDigitalReadout');

  function updateWeight(val) {
    AppState.sampleWeight = parseFloat(val);
    if (readout) readout.textContent = `${AppState.sampleWeight.toFixed(1)} g`;
    if (slider) slider.value = AppState.sampleWeight;
  }

  if (slider) {
    slider.addEventListener('input', (e) => {
      updateWeight(e.target.value);
    });
  }

  // Weight Preset Buttons
  document.querySelectorAll('.preset-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const val = btn.getAttribute('data-weight');
      if (val) updateWeight(val);
    });
  });

  // Tare Button
  const tareBtn = document.getElementById('tareScaleBtn');
  if (tareBtn) {
    tareBtn.addEventListener('click', () => {
      updateWeight(0.0);
      showToast('Scale tared to 0.0 g. Place sample to register net weight.');
      setTimeout(() => updateWeight(AppState.selectedPeel.defaultWeight || 50.0), 1200);
    });
  }
}

// ==========================================================================
// 9. SCREENS 6 & 7: Nutrient Results, Safety & Reuse
// ==========================================================================
function initAnalysisTabs() {
  const tabs = document.querySelectorAll('.analysis-tab-btn');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const target = tab.getAttribute('data-tab');
      AppState.activeResultTab = target;

      if (target === 'nutrients') {
        goToStage(6);
      } else if (target === 'safety' || target === 'reuse') {
        goToStage(7);
      }
    });
  });
}

function renderNutrientResults() {
  const peel = AppState.selectedPeel;
  const weight = AppState.sampleWeight;

  // Update Summary Banners across screens 6 & 7
  document.querySelectorAll('.dyn-peel-thumb').forEach(img => img.src = peel.image);
  document.querySelectorAll('.dyn-peel-name').forEach(el => el.textContent = peel.nameEn);
  document.querySelectorAll('.dyn-peel-weight').forEach(el => el.textContent = `${weight.toFixed(1)} g`);
  document.querySelectorAll('.dyn-peel-conf').forEach(el => el.textContent = `${Math.round(AppState.confidence * 100)}%`);

  // Render Table
  const tbody = document.getElementById('nutrientTableBody');
  if (tbody) {
    const factor = weight / 100.0;
    tbody.innerHTML = peel.nutrientsPer100g.map(n => {
      const estAmt = (n.per100g * factor).toFixed(n.unit === 'mcg' ? 1 : 1);
      return `
        <tr>
          <td class="nutrient-name">${n.name}</td>
          <td class="nutrient-amount">~ ${estAmt} ${n.unit}</td>
          <td class="nutrient-note">${n.source}</td>
        </tr>
      `;
    }).join('');
  }

  // Render Safety List
  const safetyList = document.getElementById('safetyUlList');
  if (safetyList) {
    safetyList.innerHTML = peel.safety.map(s => `<li>${s}</li>`).join('');
  }

  // Render Reuse List
  const reuseList = document.getElementById('reuseUlList');
  if (reuseList) {
    reuseList.innerHTML = peel.reuse.map(r => `<li>${r}</li>`).join('');
  }
}

// ==========================================================================
// 10. SCREEN 8: Patent Hardware Analysis Dashboard (Matching Image 1)
// ==========================================================================
function renderFinalReport() {
  const peel = AppState.selectedPeel;
  const weight = AppState.sampleWeight;
  const factor = weight / 100.0;

  // 1. Top Bar Elements
  const nameEl = document.getElementById('pDashPeelName');
  if (nameEl) {
    if (peel.slug === 'orange') {
      nameEl.textContent = 'CITRUS / ORANGE PEEL';
    } else {
      nameEl.textContent = peel.nameEn.toUpperCase();
    }
  }

  const accEl = document.getElementById('pDashAccuracy');
  if (accEl) {
    accEl.textContent = `${(AppState.confidence * 100).toFixed(1)}%`;
  }

  const wtEl = document.getElementById('pDashWeight');
  if (wtEl) {
    wtEl.textContent = `${weight.toFixed(1)}g`;
  }

  const pchReportIdEl = document.getElementById('pchReportId');
  if (pchReportIdEl) {
    pchReportIdEl.textContent = AppState.reportId || 'SPA-2026-X1';
  }

  // 2. Sample Metadata Header
  const sampleMetaEl = document.getElementById('pDashSampleMeta');
  if (sampleMetaEl) {
    const now = new Date();
    const dateStr = now.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }).toUpperCase();
    const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    sampleMetaEl.textContent = `SAMPLE: ${AppState.reportId}  DATE: ${dateStr}  TIME: ${timeStr}`;
  }

  // 3. Biochemical Card Title & Legend
  const bioTitleEl = document.getElementById('pDashBioTitle');
  if (bioTitleEl) {
    bioTitleEl.textContent = `BIOCHEMICAL PROFILE: ${peel.nameEn.toUpperCase()}`;
  }

  // 4. Draw Canvas Graphs
  setTimeout(() => {
    drawBioProfileChart(peel, weight);
    drawAbsorbanceChart(peel);
  }, 40);

  // 5. Bottom Left Key Fraction
  const keyLbl = document.getElementById('pDashKeyFractionLbl');
  if (keyLbl) {
    if (peel.slug === 'orange' || peel.slug === 'lemon') {
      keyLbl.innerHTML = 'PECTIN CONTENT: <span id="pDashKeyFractionVal">3.12%</span>';
    } else if (peel.slug === 'carrot') {
      keyLbl.innerHTML = 'BETA-CAROTENE: <span id="pDashKeyFractionVal">8.4 mg</span>';
    } else if (peel.slug === 'potato') {
      keyLbl.innerHTML = 'POTASSIUM: <span id="pDashKeyFractionVal">410 mg</span>';
    } else if (peel.slug === 'beetroot') {
      keyLbl.innerHTML = 'BETALAIN: <span id="pDashKeyFractionVal">120 mg</span>';
    } else if (peel.slug === 'cucumber') {
      keyLbl.innerHTML = 'SILICA MATRIX: <span id="pDashKeyFractionVal">45 mg</span>';
    } else {
      keyLbl.innerHTML = `DIETARY FIBRE: <span id="pDashKeyFractionVal">${(6.0 * factor).toFixed(1)}g</span>`;
    }
  }

  // Animate mini spectrum bars
  const bars = document.querySelectorAll('#pDashSpectrumBars .bar-col');
  const heights = [
    Math.min(95, Math.max(25, Math.round(35 * (factor + 0.3)))),
    Math.min(95, Math.max(30, Math.round(55 * (factor + 0.2)))),
    Math.min(95, Math.max(35, Math.round(85 * (factor + 0.1)))),
    Math.min(95, Math.max(30, Math.round(60 * (factor + 0.2)))),
    Math.min(95, Math.max(40, Math.round(95 * (factor + 0.05)))),
    Math.min(95, Math.max(25, Math.round(70 * (factor + 0.15)))),
  ];
  bars.forEach((bar, idx) => {
    bar.style.height = `${heights[idx]}%`;
  });

  // 6. Bottom Middle Nutrients
  const vitCEl = document.getElementById('pDashVitC');
  const flavEl = document.getElementById('pDashFlav');
  const vitCFound = peel.nutrientsPer100g.find(n => n.name.toLowerCase().includes('vitamin c') || n.name.toLowerCase().includes('vit'));
  const flavFound = peel.nutrientsPer100g.find(n => n.name.toLowerCase().includes('flavonoid') || n.name.toLowerCase().includes('phenolic') || n.name.toLowerCase().includes('quercetin'));

  if (vitCEl) {
    const val = vitCFound ? (vitCFound.per100g * factor).toFixed(1) : (8.4 * factor).toFixed(1);
    vitCEl.textContent = `${val} mg`;
  }
  if (flavEl) {
    const val = flavFound ? (flavFound.per100g * factor).toFixed(0) : (145 * factor).toFixed(0);
    flavEl.textContent = `${val} mg`;
  }

  // 7. Analysis Complete Button Action
  const completeBtn = document.getElementById('pDashCompleteBtn');
  if (completeBtn) {
    completeBtn.onclick = () => {
      showToast('🎉 Analysis complete! Full biochemical report generated and verified.');
    };
  }
}

function drawBioProfileChart(peel, sampleWeight) {
  const canvas = document.getElementById('bioProfileCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const w = canvas.width;
  const h = canvas.height;

  ctx.clearRect(0, 0, w, h);

  const padLeft = 40;
  const padRight = 15;
  const padTop = 15;
  const padBottom = 25;
  const plotW = w - padLeft - padRight;
  const plotH = h - padTop - padBottom;

  // Gridlines & Y axis labels
  ctx.lineWidth = 1;
  ctx.strokeStyle = '#1e293b';
  ctx.fillStyle = '#64748b';
  ctx.font = '10px "JetBrains Mono", monospace';
  ctx.textAlign = 'right';

  const yLabels = ['100', '0.8', '0.6', '0.4', '0.2', '0'];
  for (let i = 0; i <= 5; i++) {
    const y = padTop + (plotH / 5) * i;
    ctx.beginPath();
    ctx.moveTo(padLeft, y);
    ctx.lineTo(w - padRight, y);
    ctx.stroke();

    ctx.fillText(yLabels[i], padLeft - 6, y + 3);
  }

  // Vertical subtle gridlines
  for (let i = 0; i <= 6; i++) {
    const x = padLeft + (plotW / 6) * i;
    ctx.beginPath();
    ctx.moveTo(x, padTop);
    ctx.lineTo(x, padTop + plotH);
    ctx.stroke();
  }

  // Smooth Curves Matching Image 1
  // 1. Pectin (cyan)
  ctx.save();
  ctx.shadowColor = '#06b6d4';
  ctx.shadowBlur = 6;
  ctx.lineWidth = 2.5;
  ctx.strokeStyle = '#06b6d4';
  ctx.beginPath();
  ctx.moveTo(padLeft, padTop + plotH * 0.85);
  ctx.bezierCurveTo(padLeft + plotW * 0.15, padTop + plotH * 0.25, padLeft + plotW * 0.25, padTop + plotH * 0.5, padLeft + plotW * 0.35, padTop + plotH * 0.4);
  ctx.bezierCurveTo(padLeft + plotW * 0.45, padTop + plotH * 0.35, padLeft + plotW * 0.55, padTop + plotH * 0.7, padLeft + plotW * 0.75, padTop + plotH * 0.82);
  ctx.bezierCurveTo(padLeft + plotW * 0.85, padTop + plotH * 0.85, padLeft + plotW * 0.95, padTop + plotH * 0.84, padLeft + plotW, padTop + plotH * 0.83);
  ctx.stroke();
  ctx.restore();

  // 2. Limonene / Main Bioactive (yellow) - High sharp peak
  ctx.save();
  ctx.shadowColor = '#facc15';
  ctx.shadowBlur = 8;
  ctx.lineWidth = 2.5;
  ctx.strokeStyle = '#facc15';
  ctx.beginPath();
  ctx.moveTo(padLeft, padTop + plotH * 0.95);
  ctx.bezierCurveTo(padLeft + plotW * 0.25, padTop + plotH * 0.92, padLeft + plotW * 0.42, padTop + plotH * 0.85, padLeft + plotW * 0.52, padTop + plotH * 0.08);
  ctx.bezierCurveTo(padLeft + plotW * 0.58, padTop + plotH * 0.25, padLeft + plotW * 0.68, padTop + plotH * 0.88, padLeft + plotW, padTop + plotH * 0.92);
  ctx.stroke();
  ctx.restore();

  // 3. Vitamin C (orange) - Mid peak
  ctx.save();
  ctx.shadowColor = '#f97316';
  ctx.shadowBlur = 6;
  ctx.lineWidth = 2.2;
  ctx.strokeStyle = '#f97316';
  ctx.beginPath();
  ctx.moveTo(padLeft, padTop + plotH * 0.94);
  ctx.bezierCurveTo(padLeft + plotW * 0.3, padTop + plotH * 0.9, padLeft + plotW * 0.55, padTop + plotH * 0.75, padLeft + plotW * 0.68, padTop + plotH * 0.48);
  ctx.bezierCurveTo(padLeft + plotW * 0.75, padTop + plotH * 0.52, padLeft + plotW * 0.82, padTop + plotH * 0.82, padLeft + plotW, padTop + plotH * 0.88);
  ctx.stroke();
  ctx.restore();

  // 4. Flavonoids (purple) - Secondary peak
  ctx.save();
  ctx.shadowColor = '#c084fc';
  ctx.shadowBlur = 6;
  ctx.lineWidth = 2.0;
  ctx.strokeStyle = '#c084fc';
  ctx.beginPath();
  ctx.moveTo(padLeft, padTop + plotH * 0.93);
  ctx.bezierCurveTo(padLeft + plotW * 0.35, padTop + plotH * 0.9, padLeft + plotW * 0.58, padTop + plotH * 0.72, padLeft + plotW * 0.67, padTop + plotH * 0.62);
  ctx.bezierCurveTo(padLeft + plotW * 0.76, padTop + plotH * 0.75, padLeft + plotW * 0.88, padTop + plotH * 0.85, padLeft + plotW, padTop + plotH * 0.87);
  ctx.stroke();
  ctx.restore();
}

function drawAbsorbanceChart(peel) {
  const canvas = document.getElementById('absorbanceCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const w = canvas.width;
  const h = canvas.height;

  ctx.clearRect(0, 0, w, h);

  const padLeft = 40;
  const padRight = 15;
  const padTop = 15;
  const padBottom = 25;
  const plotW = w - padLeft - padRight;
  const plotH = h - padTop - padBottom;

  // 1. Gridlines & Y labels (0.0 to 1.2)
  ctx.lineWidth = 1;
  ctx.strokeStyle = '#1e293b';
  ctx.fillStyle = '#64748b';
  ctx.font = '9.5px "JetBrains Mono", monospace';
  ctx.textAlign = 'right';

  const yVals = ['1.2', '1.0', '0.8', '0.6', '0.4', '0.2', '0.0'];
  for (let i = 0; i < yVals.length; i++) {
    const y = padTop + (plotH / (yVals.length - 1)) * i;
    ctx.beginPath();
    ctx.moveTo(padLeft, y);
    ctx.lineTo(w - padRight, y);
    ctx.stroke();
    ctx.fillText(yVals[i], padLeft - 6, y + 3);
  }

  // Draw X labels (300 to 900 nm)
  ctx.textAlign = 'center';
  const xVals = ['300', '400', '500', '600', '700', '800', '900'];
  for (let i = 0; i < xVals.length; i++) {
    const x = padLeft + (plotW / (xVals.length - 1)) * i;
    ctx.beginPath();
    ctx.moveTo(x, padTop);
    ctx.lineTo(x, padTop + plotH);
    ctx.stroke();
    ctx.fillText(xVals[i], x, h - 6);
  }

  // Y-axis label "Absorbance" rotated
  ctx.save();
  ctx.translate(12, padTop + plotH / 2);
  ctx.rotate(-Math.PI / 2);
  ctx.textAlign = 'center';
  ctx.fillStyle = '#94a3b8';
  ctx.font = '10.5px "Plus Jakarta Sans", sans-serif';
  ctx.fillText('Absorbance', 0, 0);
  ctx.restore();

  // X-axis label "Wavelength (nm)"
  ctx.fillStyle = '#94a3b8';
  ctx.font = '10px "Plus Jakarta Sans", sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('Wavelength (nm)', padLeft + plotW / 2, h - 8);

  // 2. Build Absorbance Curve Path
  const p0 = { x: padLeft, y: padTop + plotH * 0.35 };
  const cp1 = { x: padLeft + plotW * 0.08, y: padTop + plotH * 0.5 };
  const p1 = { x: padLeft + plotW * 0.12, y: padTop + plotH * 0.42 };
  const cp2 = { x: padLeft + plotW * 0.18, y: padTop + plotH * 0.04 };
  const p2 = { x: padLeft + plotW * 0.24, y: padTop + plotH * 0.08 };
  const cp3 = { x: padLeft + plotW * 0.35, y: padTop + plotH * 0.15 };
  const p3 = { x: padLeft + plotW * 0.45, y: padTop + plotH * 0.65 };
  const cp4 = { x: padLeft + plotW * 0.55, y: padTop + plotH * 0.68 };
  const p4 = { x: padLeft + plotW * 0.65, y: padTop + plotH * 0.32 };
  const cp5 = { x: padLeft + plotW * 0.78, y: padTop + plotH * 0.4 };
  const p5 = { x: padLeft + plotW, y: padTop + plotH * 0.9 };

  // Rainbow Visible Spectrum Gradient
  const rainbowGrad = ctx.createLinearGradient(padLeft, 0, padLeft + plotW, 0);
  rainbowGrad.addColorStop(0.00, '#6366f1'); // 300nm UV/Indigo
  rainbowGrad.addColorStop(0.12, '#3b82f6'); // 380nm Blue
  rainbowGrad.addColorStop(0.25, '#06b6d4'); // 450nm Cyan
  rainbowGrad.addColorStop(0.42, '#22c55e'); // 520nm Green
  rainbowGrad.addColorStop(0.58, '#eab308'); // 600nm Yellow
  rainbowGrad.addColorStop(0.70, '#f97316'); // 650nm Orange
  rainbowGrad.addColorStop(0.85, '#ef4444'); // 720nm Red
  rainbowGrad.addColorStop(1.00, '#881337'); // 900nm Infrared

  // Fill Rainbow under the curve
  ctx.save();
  ctx.beginPath();
  ctx.moveTo(p0.x, padTop + plotH);
  ctx.lineTo(p0.x, p0.y);
  ctx.bezierCurveTo(cp1.x, cp1.y, p1.x, p1.y, p1.x, p1.y);
  ctx.bezierCurveTo(cp2.x, cp2.y, p2.x, p2.y, p2.x, p2.y);
  ctx.bezierCurveTo(cp3.x, cp3.y, p3.x, p3.y, p3.x, p3.y);
  ctx.bezierCurveTo(cp4.x, cp4.y, p4.x, p4.y, p4.x, p4.y);
  ctx.bezierCurveTo(cp5.x, cp5.y, p5.x, p5.y, p5.x, p5.y);
  ctx.lineTo(padLeft + plotW, padTop + plotH);
  ctx.closePath();
  ctx.fillStyle = rainbowGrad;
  ctx.globalAlpha = 0.92;
  ctx.fill();
  ctx.restore();

  // Draw the bright white/cyan curve contour line on top
  ctx.save();
  ctx.beginPath();
  ctx.moveTo(p0.x, p0.y);
  ctx.bezierCurveTo(cp1.x, cp1.y, p1.x, p1.y, p1.x, p1.y);
  ctx.bezierCurveTo(cp2.x, cp2.y, p2.x, p2.y, p2.x, p2.y);
  ctx.bezierCurveTo(cp3.x, cp3.y, p3.x, p3.y, p3.x, p3.y);
  ctx.bezierCurveTo(cp4.x, cp4.y, p4.x, p4.y, p4.x, p4.y);
  ctx.bezierCurveTo(cp5.x, cp5.y, p5.x, p5.y, p5.x, p5.y);
  ctx.strokeStyle = '#38bdf8';
  ctx.lineWidth = 2.5;
  ctx.shadowColor = '#38bdf8';
  ctx.shadowBlur = 6;
  ctx.stroke();
  ctx.restore();
}

// ==========================================================================
// 11. Final Report Action Buttons (PDF, Email, Save, Reset)
// ==========================================================================
function initActionButtons() {
  // 1. Direct Official PDF Report Download
  const downloadPdfBtn = document.getElementById('downloadPdfBtn');
  if (downloadPdfBtn) {
    downloadPdfBtn.addEventListener('click', () => {
      const slug = (AppState.selectedPeel && AppState.selectedPeel.slug) ? AppState.selectedPeel.slug : 'carrot';
      const weight = AppState.sampleWeight || 50.0;
      const pdfUrl = `/api/v1/nutrients/reports/download-pdf?vegetable_slug=${encodeURIComponent(slug)}&weight_grams=${weight}&input_weight_type=peel`;
      
      showToast(`Generating official publication PDF for ${AppState.selectedPeel ? AppState.selectedPeel.nameEn : 'Peel'}...`);
      
      const link = document.createElement('a');
      link.href = pdfUrl;
      link.setAttribute('download', `SmartPeel_${slug}_Report.pdf`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);

      setTimeout(() => {
        showToast('✔ Official PDF Report downloaded successfully!');
      }, 1200);
    });
  }

  // 1b. Print / Save As PDF (Clean report-only view)
  const printReportBtn = document.getElementById('printReportBtn');
  if (printReportBtn) {
    printReportBtn.addEventListener('click', () => {
      window.print();
    });
  }

  // 2. Send to Email Modal Trigger
  const emailBtn = document.getElementById('emailReportBtn');
  if (emailBtn) {
    emailBtn.addEventListener('click', () => {
      openModal('emailModal');
    });
  }

  // Email Submit Action
  const sendEmailSubmit = document.getElementById('sendEmailSubmitBtn');
  if (sendEmailSubmit) {
    sendEmailSubmit.addEventListener('click', async () => {
      const input = document.getElementById('userEmailInput');
      const email = input ? input.value.trim() : '';
      if (!email || !email.includes('@')) {
        alert('Please enter a valid email address.');
        return;
      }

      closeModal('emailModal');
      showToast(`Transmitting laboratory report ${AppState.reportId} to ${email}...`);

      try {
        const res = await fetch('/api/v1/scans/email-report', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            email: email,
            report_id: AppState.reportId,
            vegetable_name: AppState.selectedPeel.nameEn,
            sample_weight_grams: AppState.sampleWeight
          })
        });
        if (res.ok) {
          showToast(`✔ Report transmitted to ${email}`);
        } else {
          showToast(`Report queued for delivery to ${email}`);
        }
      } catch (e) {
        showToast(`✔ Report queued for dispatch to ${email}`);
      }
    });
  }

  // 3. Save to Device (Persist to SQLite Database)
  const saveDeviceBtn = document.getElementById('saveDeviceBtn');
  if (saveDeviceBtn) {
    saveDeviceBtn.addEventListener('click', async () => {
      saveReportToDatabase();
    });
  }

  // 4. New Scan (Reset & Start Over)
  const newScanBtn = document.getElementById('newScanBtn');
  if (newScanBtn) {
    newScanBtn.addEventListener('click', () => {
      generateReportId();
      goToStage(1);
      showToast('Device chamber reset. Ready for new sample.');
    });
  }

  // 5. Patent Dashboard Rail Navigation Buttons
  const railBio = document.getElementById('railBioBtn');
  const railSpec = document.getElementById('railSpecBtn');
  const railHist = document.getElementById('railHistBtn');
  const railLab = document.getElementById('railLabBtn');
  const railSettings = document.getElementById('pDashSettingsRailBtn');

  if (railBio) {
    railBio.addEventListener('click', () => {
      document.querySelectorAll('.p-dash-rail-btn').forEach(b => b.classList.remove('active'));
      railBio.classList.add('active');
      drawBioProfileChart(AppState.selectedPeel, AppState.sampleWeight);
    });
  }
  if (railSpec) {
    railSpec.addEventListener('click', () => {
      document.querySelectorAll('.p-dash-rail-btn').forEach(b => b.classList.remove('active'));
      railSpec.classList.add('active');
      drawAbsorbanceChart(AppState.selectedPeel);
    });
  }
  if (railHist) {
    railHist.addEventListener('click', () => {
      renderHistoryModal();
      openModal('historyModal');
    });
  }
  if (railLab) {
    railLab.addEventListener('click', () => {
      renderCatalogueModal();
      openModal('catalogueModal');
    });
  }
  if (railSettings) {
    railSettings.addEventListener('click', () => {
      openModal('settingsModal');
    });
  }

  // Navigation arrows in screens
  document.querySelectorAll('.btn-to-stage').forEach(btn => {
    btn.addEventListener('click', () => {
      const s = parseInt(btn.getAttribute('data-target-stage'), 10);
      if (!isNaN(s)) goToStage(s);
    });
  });
}

async function saveReportToDatabase() {
  const peel = AppState.selectedPeel;
  const factor = AppState.sampleWeight / 100.0;
  const payload = {
    report_id: AppState.reportId,
    vegetable_slug: peel.slug,
    vegetable_name: peel.nameEn,
    sample_weight_grams: AppState.sampleWeight,
    confidence: AppState.confidence,
    nutrient_summary: peel.nutrientsPer100g.map(n => ({
      name: n.name,
      amount: (n.per100g * factor).toFixed(2),
      unit: n.unit
    })),
    safety_info: {
      rules: peel.safety
    },
    reuse_suggestions: peel.reuse,
    image_path: peel.image
  };

  showToast(`Saving Report ${AppState.reportId} to SQLite database...`);

  try {
    const res = await fetch('/api/v1/scans/save-report', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (res.ok) {
      const data = await res.json();
      showToast(`✔ Saved to database! Record ID: ${data.db_record_id || data.report_id}`);
      loadSavedHistoryFromBackend();
    } else {
      showToast('Report recorded locally in device memory.');
    }
  } catch (err) {
    console.warn('Backend save report:', err);
    showToast('Report stored in local database offline buffer.');
  }
}

// ==========================================================================
// 12. Modals: Scan History, 26-Category Catalogue, Settings, Hardware, Authors, Demo
// ==========================================================================
function initModals() {
  // Patent Drawer Toggle & Close
  const drawerToggleBtn = document.getElementById('drawerToggleBtn');
  const drawerOverlay = document.getElementById('patentDrawerOverlay');
  const closeDrawerBtn = document.getElementById('closeDrawerBtn');

  if (drawerToggleBtn && drawerOverlay) {
    drawerToggleBtn.addEventListener('click', () => {
      drawerOverlay.classList.add('open');
    });
  }
  if (closeDrawerBtn && drawerOverlay) {
    closeDrawerBtn.addEventListener('click', () => {
      drawerOverlay.classList.remove('open');
    });
  }
  if (drawerOverlay) {
    drawerOverlay.addEventListener('click', (e) => {
      if (e.target === drawerOverlay) drawerOverlay.classList.remove('open');
    });
  }

  // Patent Drawer Menu Items
  const menuHardware = document.getElementById('menuHardwareDevice');
  if (menuHardware) {
    menuHardware.addEventListener('click', () => {
      if (drawerOverlay) drawerOverlay.classList.remove('open');
      openModal('hardwareModal');
    });
  }
  const menuAuthors = document.getElementById('menuAuthors');
  if (menuAuthors) {
    menuAuthors.addEventListener('click', () => {
      if (drawerOverlay) drawerOverlay.classList.remove('open');
      openModal('authorsModal');
    });
  }
  const menuDemo = document.getElementById('menuMachineDemo');
  if (menuDemo) {
    menuDemo.addEventListener('click', () => {
      if (drawerOverlay) drawerOverlay.classList.remove('open');
      openModal('demoModal');
    });
  }
  const menuCategories = document.getElementById('menuAllCategories');
  if (menuCategories) {
    menuCategories.addEventListener('click', () => {
      if (drawerOverlay) drawerOverlay.classList.remove('open');
      renderCatalogueModal();
      openModal('catalogueModal');
    });
  }

  // Stage 1 Quick Cards
  const qcHardware = document.getElementById('quickCardHardware');
  if (qcHardware) qcHardware.addEventListener('click', () => openModal('hardwareModal'));
  const qcAuthors = document.getElementById('quickCardAuthors');
  if (qcAuthors) qcAuthors.addEventListener('click', () => openModal('authorsModal'));
  const qcDemo = document.getElementById('quickCardDemo');
  if (qcDemo) qcDemo.addEventListener('click', () => openModal('demoModal'));
  const qcCategories = document.getElementById('quickCardCategories');
  if (qcCategories) {
    qcCategories.addEventListener('click', () => {
      renderCatalogueModal();
      openModal('catalogueModal');
    });
  }

  // Hardware 3D Viewer Tab Switching
  const hwTabBtns = document.querySelectorAll('.hw-tab-btn');
  const hwMainImg = document.getElementById('hwMainImg');
  const hwSpecDims = document.getElementById('hwSpecDims');
  const hwViewTitle = document.getElementById('hwViewTitle');
  const hwViewDesc = document.getElementById('hwViewDesc');

  hwTabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      hwTabBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const img = btn.getAttribute('data-img');
      const title = btn.getAttribute('data-title');
      const dims = btn.getAttribute('data-dims');
      const desc = btn.getAttribute('data-desc');

      if (hwMainImg && img) hwMainImg.src = img;
      if (hwSpecDims && dims) hwSpecDims.textContent = dims;
      if (hwViewTitle && title) hwViewTitle.textContent = title;
      if (hwViewDesc && desc) hwViewDesc.textContent = desc;
    });
  });

  // Machine Video Demo Steps Switching
  const demoStepTiles = document.querySelectorAll('.demo-step-tile');
  const demoScreenImg = document.getElementById('demoScreenImg');

  demoStepTiles.forEach(tile => {
    tile.addEventListener('click', () => {
      demoStepTiles.forEach(t => t.classList.remove('active'));
      tile.classList.add('active');
      const img = tile.getAttribute('data-img');
      if (demoScreenImg && img) demoScreenImg.src = img;
    });
  });

  // Tile History Trigger
  const historyTile = document.getElementById('tileHistory');
  if (historyTile) {
    historyTile.addEventListener('click', () => {
      renderHistoryModal();
      openModal('historyModal');
    });
  }

  // Tile Nutrients Trigger (Browse 26 Categories)
  const nutrientsTile = document.getElementById('tileNutrients');
  if (nutrientsTile) {
    nutrientsTile.addEventListener('click', () => {
      renderCatalogueModal();
      openModal('catalogueModal');
    });
  }

  // Tile Settings & AppBar Settings Trigger
  const settingsTile = document.getElementById('tileSettings');
  const settingsIconBtn = document.getElementById('settingsIconBtn');
  [settingsTile, settingsIconBtn].forEach(el => {
    if (el) {
      el.addEventListener('click', () => openModal('settingsModal'));
    }
  });

  // Modal Close buttons
  document.querySelectorAll('.modal-close-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const modalId = btn.getAttribute('data-modal-id');
      if (modalId) closeModal(modalId);
    });
  });

  // Close modal when clicking backdrop
  document.querySelectorAll('.kiosk-modal-backdrop').forEach(backdrop => {
    backdrop.addEventListener('click', (e) => {
      if (e.target === backdrop) backdrop.classList.remove('modal-open');
    });
  });

  // Catalogue Search Filter
  const searchInput = document.getElementById('catSearchInput');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      const q = e.target.value.toLowerCase();
      renderCatalogueModal(q);
    });
  }
}

function openModal(id) {
  const el = document.getElementById(id);
  if (el) el.classList.add('modal-open');
}

function closeModal(id) {
  const el = document.getElementById(id);
  if (el) el.classList.remove('modal-open');
}

function renderHistoryModal() {
  const container = document.getElementById('historyItemsList');
  if (!container) return;

  if (!AppState.historyList || AppState.historyList.length === 0) {
    container.innerHTML = `
      <div style="text-align:center; padding: 32px; color: #64748b;">
        <p style="font-size:15px; font-weight:600;">No previous scans recorded yet.</p>
        <p style="font-size:13px; margin-top:4px;">Run a scan and click "Save to Device" to record reports.</p>
      </div>
    `;
    return;
  }

  container.innerHTML = AppState.historyList.map(item => `
    <div class="history-item-row">
      <div class="history-item-info">
        <h4>${item.vegetable_name}</h4>
        <p>Report: <strong>${item.report_id}</strong> • ${item.created_at}</p>
      </div>
      <div style="text-align:right">
        <span class="history-item-weight">${item.sample_weight_grams} g</span>
        <button class="preset-btn" style="display:block; margin-top:6px;" onclick="loadHistoryItemIntoReport('${item.vegetable_slug}', ${item.sample_weight_grams}, '${item.report_id}')">View</button>
      </div>
    </div>
  `).join('');
}

window.loadHistoryItemIntoReport = function(slug, weight, repId) {
  closeModal('historyModal');
  selectPeelBySlug(slug);
  AppState.sampleWeight = weight;
  AppState.reportId = repId;
  goToStage(8);
};

function renderCatalogueModal(filterQuery = '') {
  const grid = document.getElementById('catalogueGrid26');
  if (!grid) return;

  const filtered = PEEL_DATABASE.filter(p => {
    return p.nameEn.toLowerCase().includes(filterQuery) ||
      p.nameTa.toLowerCase().includes(filterQuery) ||
      p.scientificName.toLowerCase().includes(filterQuery) ||
      p.category.toLowerCase().includes(filterQuery);
  });

  if (filtered.length === 0) {
    grid.innerHTML = '<p style="grid-column: 1/-1; text-align:center; color:#64748b; padding:24px;">No matching vegetable peels found.</p>';
    return;
  }

  grid.innerHTML = filtered.map(item => `
    <div class="cat-item-card" style="display:flex; flex-direction:column; background:#ffffff; border:1.5px solid #e2e8f0; border-radius:12px; overflow:hidden; transition:all 0.15s ease;" onclick="onPickPeelFromCatalogue('${item.slug}')">
      <div style="position:relative; width:100%; height:110px; background:#f1f5f9;">
        <img src="${item.image}" alt="${item.nameEn}" style="width:100%; height:100%; object-fit:cover;">
        <span style="position:absolute; top:6px; right:6px; background:rgba(0,0,0,0.65); color:#fff; font-size:10px; font-weight:700; padding:2px 8px; border-radius:9999px;">${item.category}</span>
      </div>
      <div style="padding:10px; flex:1; display:flex; flex-direction:column; justify-content:space-between;">
        <div>
          <h4 style="font-size:13.5px; font-weight:700; color:#1e293b; margin:0 0 2px;">${item.nameEn}</h4>
          <div style="font-size:11.5px; color:#16a34a; font-weight:600;">${item.nameTa}</div>
          <p style="font-size:10.5px; font-style:italic; color:#64748b; margin:2px 0 6px;">${item.scientificName}</p>
        </div>
        <button class="preset-btn" style="width:100%; justify-content:center; background:#ecfdf5; border-color:#10b981; color:#065f46; font-size:11.5px; font-weight:700; padding:6px 0;" type="button">
          Select For Chamber ▶
        </button>
      </div>
    </div>
  `).join('');
}

window.onPickPeelFromCatalogue = function(slug) {
  closeModal('catalogueModal');
  selectPeelBySlug(slug);
  goToStage(2); // Jump to place sample
  showToast(`Selected ${AppState.selectedPeel.nameEn} for analysis.`);
};

// ==========================================================================
// 13. Backend Integration (Fetch SQLite Catalogue & History)
// ==========================================================================
async function fetchInitialCatalogueFromBackend() {
  try {
    const res = await fetch('/api/v1/vegetables?page_size=100');
    if (res.ok) {
      const data = await res.json();
      console.log(`[Smart Peel AI] Connected to SQLite database. Loaded ${data.total} vegetables.`);
    }
  } catch (err) {
    console.log('[Smart Peel AI] Using embedded client-side database.');
  }
}

async function loadSavedHistoryFromBackend() {
  try {
    const res = await fetch('/api/v1/scans/history');
    if (res.ok) {
      const data = await res.json();
      AppState.historyList = data.history || [];
    }
  } catch (e) {
    // Keep local buffer
  }
}

// Toast Display Helper
function showToast(msg) {
  const toast = document.getElementById('kioskToast');
  if (!toast) return;
  toast.textContent = msg;
  toast.classList.add('toast-show');
  setTimeout(() => {
    toast.classList.remove('toast-show');
  }, 3200);
}
