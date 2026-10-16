# SCIENTIFIC METHODOLOGY & NUTRITIONAL FORMULATIONS

## 1. Scientific Standards & Data Sources
Nutrient measurements and botanical valorization guidelines in SMART PEEL AI adhere to international and national nutritional databases:
1. **ICMR - National Institute of Nutrition (NIN)**: *Indian Food Composition Tables (IFCT 2017)*, Hyderabad, India.
2. **USDA Agricultural Research Service**: *FoodData Central (FDC)*, Foundation Foods & Survey Data.
3. **FAO / INFOODS**: *Food Composition Database for Biodiversity (BioFoodComp4.0)*.
4. **Peer-Reviewed Scientific Literature**: Indexed journal articles detailing peel-to-whole biochemical superiority and toxicological thresholds.

---

## 2. Weight-Based Estimation Mathematics

### 2.1 Peel Yield Formulation
When the user supplies whole vegetable weight ($W_{\text{whole}}$), calculated peel mass ($W_{\text{peel}}$) is derived from empirical yield distributions:
$$W_{\text{peel}} = W_{\text{whole}} \times \left( \frac{Y_{\text{mean}}}{100} \right)$$
Where $Y_{\text{mean}}$ is the species-specific empirical peel yield percentage (e.g., Carrot: 11.0%, Potato: 10.5%, Beetroot: 13.0%, Pumpkin: 16.5%).

### 2.2 Nutrient Yield Formulation
For nutrient $i$ with concentration $C_i$ (per 100g raw peel) and culinary retention factor $R_{i,\text{method}}$:
$$\text{Yield}_i = \left( \frac{W_{\text{peel}}}{100} \right) \times C_i \times R_{i,\text{method}}$$

### 2.3 Percentage Daily Reference Intake (% DRI / RDA)
For demographic group $g$ with recommended dietary allowance $\text{RDA}_{i,g}$:
$$\% \text{RDA}_i = \left( \frac{\text{Yield}_i}{\text{RDA}_{i,g}} \right) \times 100$$

---

## 3. Cooking Retention Multipliers

| Preparation Method | Water-Soluble (Vit C, B9) | Heat-Sensitive (Vit B1, B2) | Minerals & Dietary Fiber |
|---|---|---|---|
| **Fresh / Raw** | 1.00 (100%) | 1.00 (100%) | 1.00 (100%) |
| **Sautéed / Stir-Fried** | 0.80 (80%) | 0.88 - 0.90 (88-90%) | 0.98 - 1.00 (98-100%) |
| **Boiled / Simmered (Broth Retained)**| 0.70 (70%) | 0.82 (82%) | 1.00 (Leached into broth) |
| **Dehydrated / Powdered** | 0.65 (65%) | 0.85 (85%) | 1.00 (100%) |

---

## 4. Antinutritional & Toxicological Rules

1. **Potato Peel Solanine & Chaconne**:
   - Critical glycoalkaloid threshold: > 200 mg/kg fresh weight.
   - Triggered by light exposure (chlorophyll greening) and sprouting.
   - Action: Complete disqualification from culinary and animal feed pathways.
2. **Cassava Cyanogenic Glucosides (Linamarin)**:
   - Contains cyanogenic glycosides that liberate hydrogen cyanide upon enzymatic hydrolysis.
   - Action: Strict culinary prohibition. Requires industrial detoxicating drying or biogas anaerobic digestion.
3. **Taro Calcium Oxalate Raphides**:
   - Acicular needle crystals causing acute oropharyngeal irritation.
   - Action: Culinary utilization requires prolonged boiling (> 20 mins) or baking.
4. **Cucurbitacins**:
   - Extreme bitterness indicates cucurbitacin B/D triterpenoids causing toxic squash syndrome.
   - Action: Bitter-tasting cucumber or gourd peels must be discarded to composting.

---

## 5. Environmental & Climate Metrics (EPA WARM)
- **Landfill Diversion**: $1.0\text{ kg}$ wet peel diverted from landfill saves approximately $0.52\text{ kg CO}_2\text{e}$ of avoided anaerobic methane emissions.
- **Compost Yield**: $1.0\text{ kg}$ fresh peel produces approximately $0.25\text{ kg}$ of finished organic soil conditioner.
