import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/localization/app_locale.dart';
import '../../core/theme/app_theme.dart';
import '../../models/estimation_models.dart';
import '../../providers/app_providers.dart';
import '../../providers/estimation_provider.dart';

class NutrientEstimationScreen extends ConsumerStatefulWidget {
  const NutrientEstimationScreen({super.key});

  @override
  ConsumerState<NutrientEstimationScreen> createState() => _NutrientEstimationScreenState();
}

class _NutrientEstimationScreenState extends ConsumerState<NutrientEstimationScreen> {
  final _weightController = TextEditingController();
  bool _isSavingReport = false;

  @override
  void initState() {
    super.initState();
    final params = ref.read(estimationInputProvider);
    _weightController.text = params.weightGrams.toStringAsFixed(0);
  }

  @override
  void dispose() {
    _weightController.dispose();
    super.dispose();
  }

  void _onWeightChanged(double weight) {
    setState(() {
      _weightController.text = weight.toStringAsFixed(0);
    });
    ref.read(estimationInputProvider.notifier).setWeight(weight);
    ref.read(currentScanProvider.notifier).setWeight(weight);
  }

  Future<void> _handleSaveReport(EstimationResultModel result, bool isTamil) async {
    setState(() {
      _isSavingReport = true;
    });

    try {
      final repo = ref.read(estimationRepositoryProvider);
      final report = await repo.saveReport(
        vegetableId: result.vegetableId,
        totalWeightGrams: result.calculatedPeelWeightGrams,
        calculations: {
          'vegetable_id': result.vegetableId,
          'vegetable_slug': result.vegetableSlug,
          'vegetable_name_en': result.vegetableNameEn,
          'vegetable_name_ta': result.vegetableNameTa,
          'input_weight_grams': result.inputWeightGrams,
          'input_weight_type': result.inputWeightType,
          'calculated_peel_weight_grams': result.calculatedPeelWeightGrams,
          'preparation_method': result.preparationMethod,
          'population_group': result.populationGroup,
          'servings': result.servings,
          'environmental_impact': {
            'wet_waste_diverted_kg': result.environmentalImpact.wetWasteDivertedKg,
            'ghg_emissions_avoided_kg_co2e': result.environmentalImpact.ghgEmissionsAvoidedKgCo2e,
            'compost_potential_kg': result.environmentalImpact.compostPotentialKg,
          },
        },
        safetyNotes: {'status': 'safe_edible', 'hazards': []},
      );

      if (!mounted) return;

      setState(() {
        _isSavingReport = false;
      });

      if (report != null) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            backgroundColor: AppTheme.primaryDark,
            content: Text(
              isTamil
                  ? 'அறிக்கை உருவாக்கப்பட்டது: ${report.reportUuid}'
                  : 'Report generated successfully: ${report.reportUuid}',
            ),
            action: SnackBarAction(
              label: isTamil ? 'காண்க' : 'View',
              textColor: const Color(0xFFFFB300),
              onPressed: () => context.go('/report-download'),
            ),
          ),
        );
      }
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _isSavingReport = false;
      });
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error saving report: $e')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final lang = ref.watch(localeProvider);
    final isTamil = lang == AppLanguage.ta;
    final veg = ref.watch(selectedVegetableProvider);
    final params = ref.watch(estimationInputProvider);
    final estimationAsync = ref.watch(nutrientEstimationResultProvider);
    final yieldRatioAsync = ref.watch(peelYieldRatioProvider(veg.slug));

    return Scaffold(
      appBar: AppBar(
        title: Text(isTamil ? 'அறிவியல் ஊட்டச்சத்து மதிப்பீடு' : 'Nutritional Quantity Estimation'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => context.go('/nutrients'),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 20.0),
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 880),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // 1. Vegetable Identity & Peel Yield Header
                Card(
                  elevation: 2,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                  child: Padding(
                    padding: const EdgeInsets.all(20.0),
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.center,
                      children: [
                        CircleAvatar(
                          radius: 28,
                          backgroundColor: AppTheme.softMint,
                          child: const Icon(Icons.eco, color: AppTheme.primaryGreen, size: 32),
                        ),
                        const SizedBox(width: 16),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                veg.displayName(isTamil),
                                style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: AppTheme.primaryDark),
                              ),
                              Text(
                                '${veg.scientificName} • ${veg.category}',
                                style: TextStyle(fontSize: 13, fontStyle: FontStyle.italic, color: Colors.grey.shade700),
                              ),
                            ],
                          ),
                        ),
                        yieldRatioAsync.when(
                          data: (ratio) {
                            final avgPct = ratio?.averagePeelPercentage ?? 15.0;
                            return Container(
                              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                              decoration: BoxDecoration(
                                color: AppTheme.primaryDark,
                                borderRadius: BorderRadius.circular(12),
                              ),
                              child: Column(
                                children: [
                                  Text(
                                    '${avgPct.toStringAsFixed(1)}%',
                                    style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white),
                                  ),
                                  Text(
                                    isTamil ? 'சராசரி தோல்' : 'Peel Yield',
                                    style: const TextStyle(fontSize: 10, color: Colors.white70),
                                  ),
                                ],
                              ),
                            );
                          },
                          loading: () => const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2)),
                          error: (_, _) => const SizedBox(),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 16),

                // 2. Input Weight Mode & Value Card
                Card(
                  elevation: 2,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                  child: Padding(
                    padding: const EdgeInsets.all(20.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          isTamil ? 'எடை மற்றும் உள்ளீட்டு வகை' : 'Weight & Measurement Basis',
                          style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AppTheme.primaryDark),
                        ),
                        const SizedBox(height: 14),

                        // Mode Segmented Buttons
                        SegmentedButton<String>(
                          segments: [
                            ButtonSegment(
                              value: 'peel',
                              label: Text(isTamil ? 'தோல் எடை' : 'Peel Weight'),
                              icon: const Icon(Icons.grain),
                            ),
                            ButtonSegment(
                              value: 'whole_vegetable',
                              label: Text(isTamil ? 'முழு காய்கறி' : 'Whole Vegetable'),
                              icon: const Icon(Icons.shopping_basket),
                            ),
                          ],
                          selected: {params.inputWeightType},
                          onSelectionChanged: (set) {
                            if (set.isNotEmpty) {
                              ref.read(estimationInputProvider.notifier).setInputWeightType(set.first);
                            }
                          },
                        ),
                        const SizedBox(height: 16),

                        // Informative Yield Derivation Callout if Whole Vegetable
                        if (params.inputWeightType == 'whole_vegetable')
                          Container(
                            padding: const EdgeInsets.all(12),
                            margin: const EdgeInsets.only(bottom: 16),
                            decoration: BoxDecoration(
                              color: Colors.amber.shade50,
                              borderRadius: BorderRadius.circular(10),
                              border: Border.all(color: Colors.amber.shade200),
                            ),
                            child: Row(
                              children: [
                                Icon(Icons.info_outline, color: Colors.amber.shade900, size: 20),
                                const SizedBox(width: 10),
                                Expanded(
                                  child: Text(
                                    isTamil
                                        ? 'முழு காய்கறி எடை இயற்பியல் விகிதத்தால் தோலின் எடையாக தானாக மாற்றப்படுகிறது.'
                                        : 'Whole vegetable weight is converted to peel weight via botanical peel yield ratio.',
                                    style: TextStyle(fontSize: 12, color: Colors.amber.shade900),
                                  ),
                                ),
                              ],
                            ),
                          ),

                        // Slider & Text Field
                        Row(
                          children: [
                            Expanded(
                              flex: 3,
                              child: Slider(
                                value: params.weightGrams.clamp(10, 2000),
                                min: 10,
                                max: 2000,
                                divisions: 199,
                                label: '${params.weightGrams.round()} g',
                                activeColor: AppTheme.primaryGreen,
                                onChanged: (val) => _onWeightChanged(val),
                              ),
                            ),
                            const SizedBox(width: 14),
                            Expanded(
                              flex: 1,
                              child: TextField(
                                controller: _weightController,
                                keyboardType: TextInputType.number,
                                decoration: InputDecoration(
                                  suffixText: 'g',
                                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                                  contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 12),
                                ),
                                onChanged: (val) {
                                  final parsed = double.tryParse(val);
                                  if (parsed != null && parsed > 0 && parsed <= 5000) {
                                    ref.read(estimationInputProvider.notifier).setWeight(parsed);
                                    ref.read(currentScanProvider.notifier).setWeight(parsed);
                                  }
                                },
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 12),

                        // Quick Chips
                        Wrap(
                          spacing: 8,
                          runSpacing: 8,
                          children: [50, 100, 150, 250, 500, 1000].map((w) {
                            final isSel = params.weightGrams.round() == w;
                            return ChoiceChip(
                              label: Text('$w g'),
                              selected: isSel,
                              selectedColor: AppTheme.softMint,
                              onSelected: (_) => _onWeightChanged(w.toDouble()),
                            );
                          }).toList(),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 16),

                // 3. Preparation Method & Population Demographic Card
                Card(
                  elevation: 2,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                  child: Padding(
                    padding: const EdgeInsets.all(20.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          isTamil ? 'சமையல் முறை மற்றும் நுகர்வோர் பிரிவு' : 'Culinary Method & Target Demographic',
                          style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AppTheme.primaryDark),
                        ),
                        const SizedBox(height: 14),

                        // Preparation Method Chips
                        Text(
                          isTamil ? 'சமையல் தயாரிப்பு முறை:' : 'Preparation Method:',
                          style: TextStyle(fontSize: 13, fontWeight: FontWeight.w600, color: Colors.grey.shade700),
                        ),
                        const SizedBox(height: 8),
                        Wrap(
                          spacing: 8,
                          runSpacing: 8,
                          children: [
                            {'code': 'fresh_raw', 'en': '🥗 Raw / Fresh', 'ta': '🥗 பச்சையான'},
                            {'code': 'sauteed', 'en': '🍳 Sautéed (Poriyal)', 'ta': '🍳 வறுவல் / பொரியல்'},
                            {'code': 'boiled_broth', 'en': '🍲 Boiled Soup', 'ta': '🍲 வேகவைத்த சாம்பார்'},
                            {'code': 'boiled_drained', 'en': '🫗 Boiled Drained', 'ta': '🫗 நீர் வடித்தல்'},
                            {'code': 'dried_powder', 'en': '🧂 Dried Powder', 'ta': '🧂 உலர் பொடி'},
                          ].map((item) {
                            final isSel = params.preparationMethod == item['code'];
                            return ChoiceChip(
                              label: Text(isTamil ? item['ta']! : item['en']!),
                              selected: isSel,
                              selectedColor: AppTheme.softMint,
                              onSelected: (sel) {
                                if (sel) {
                                  ref.read(estimationInputProvider.notifier).setPreparationMethod(item['code']!);
                                }
                              },
                            );
                          }).toList(),
                        ),
                        const SizedBox(height: 18),

                        // Demographic and Servings in Row
                        Row(
                          children: [
                            Expanded(
                              flex: 2,
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    isTamil ? 'நுகர்வோர் பிரிவு (ICMR-NIN):' : 'Demographic Group (ICMR-NIN):',
                                    style: TextStyle(fontSize: 13, fontWeight: FontWeight.w600, color: Colors.grey.shade700),
                                  ),
                                  const SizedBox(height: 6),
                                  DropdownButtonFormField<String>(
                                    initialValue: params.populationGroup,
                                    isExpanded: true,
                                    decoration: InputDecoration(
                                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                                      contentPadding: const EdgeInsets.symmetric(horizontal: 10, vertical: 10),
                                    ),
                                    items: [
                                      DropdownMenuItem(
                                        value: 'adult_male',
                                        child: Text(isTamil ? '👨 ஆண்' : '👨 Adult Male', overflow: TextOverflow.ellipsis),
                                      ),
                                      DropdownMenuItem(
                                        value: 'adult_female',
                                        child: Text(isTamil ? '👩 பெண்' : '👩 Adult Female', overflow: TextOverflow.ellipsis),
                                      ),
                                      DropdownMenuItem(
                                        value: 'pregnant_woman',
                                        child: Text(isTamil ? '🤰 கர்ப்பிணி' : '🤰 Pregnant', overflow: TextOverflow.ellipsis),
                                      ),
                                      DropdownMenuItem(
                                        value: 'lactating_mother',
                                        child: Text(isTamil ? '🤱 பாலூட்டும்' : '🤱 Lactating', overflow: TextOverflow.ellipsis),
                                      ),
                                      DropdownMenuItem(
                                        value: 'children_7_9y',
                                        child: Text(isTamil ? '👧 குழந்தைகள்' : '👧 Child (7-9)', overflow: TextOverflow.ellipsis),
                                      ),
                                    ],
                                    onChanged: (val) {
                                      if (val != null) {
                                        ref.read(estimationInputProvider.notifier).setPopulationGroup(val);
                                      }
                                    },
                                  ),
                                ],
                              ),
                            ),
                            const SizedBox(width: 14),
                            Expanded(
                              flex: 1,
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    isTamil ? 'பங்கு:' : 'Servings:',
                                    style: TextStyle(fontSize: 13, fontWeight: FontWeight.w600, color: Colors.grey.shade700),
                                  ),
                                  const SizedBox(height: 6),
                                  DropdownButtonFormField<int>(
                                    initialValue: params.servings,
                                    isExpanded: true,
                                    decoration: InputDecoration(
                                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                                      contentPadding: const EdgeInsets.symmetric(horizontal: 10, vertical: 10),
                                    ),
                                    items: [1, 2, 4, 8, 10].map((s) {
                                      return DropdownMenuItem(
                                        value: s,
                                        child: Text('$s'),
                                      );
                                    }).toList(),
                                    onChanged: (val) {
                                      if (val != null) {
                                        ref.read(estimationInputProvider.notifier).setServings(val);
                                      }
                                    },
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 16),

                // 4. Estimation Results
                estimationAsync.when(
                  data: (result) {
                    if (result == null) {
                      return const Center(child: Padding(padding: EdgeInsets.all(32), child: Text('No estimation data available.')));
                    }

                    return Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        // Moisture vs Dry Matter Bar Card
                        Card(
                          elevation: 1,
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                          child: Padding(
                            padding: const EdgeInsets.all(16.0),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Row(
                                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                  children: [
                                    Text(
                                      isTamil ? 'உடல் அமைப்பு பகுப்பாய்வு' : 'Physical Composition Breakdown',
                                      style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14, color: AppTheme.primaryDark),
                                    ),
                                    Text(
                                      '${result.calculatedPeelWeightGrams}g ${isTamil ? 'தோல்' : 'Peel'}',
                                      style: const TextStyle(fontWeight: FontWeight.bold, color: AppTheme.primaryGreen),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 10),
                                ClipRRect(
                                  borderRadius: BorderRadius.circular(6),
                                  child: Row(
                                    children: [
                                      Expanded(
                                        flex: result.moistureWeightGrams.round().clamp(1, 100),
                                        child: Container(height: 14, color: Colors.blue.shade400),
                                      ),
                                      Expanded(
                                        flex: result.dryMatterWeightGrams.round().clamp(1, 100),
                                        child: Container(height: 14, color: Colors.green.shade600),
                                      ),
                                    ],
                                  ),
                                ),
                                const SizedBox(height: 8),
                                Row(
                                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                  children: [
                                    Text(
                                      '💧 ${isTamil ? 'ஈரப்பதம்' : 'Moisture'}: ${result.moistureWeightGrams}g (${(result.moistureWeightGrams / result.calculatedPeelWeightGrams * 100).toStringAsFixed(1)}%)',
                                      style: TextStyle(fontSize: 12, color: Colors.blue.shade800),
                                    ),
                                    Text(
                                      '🌿 ${isTamil ? 'உலர் சத்து' : 'Dry Solids'}: ${result.dryMatterWeightGrams}g (${(result.dryMatterWeightGrams / result.calculatedPeelWeightGrams * 100).toStringAsFixed(1)}%)',
                                      style: TextStyle(fontSize: 12, color: Colors.green.shade800),
                                    ),
                                  ],
                                ),
                              ],
                            ),
                          ),
                        ),
                        const SizedBox(height: 16),

                        // Superiority Highlight Banner
                        if (result.superiority.comparison(isTamil).isNotEmpty)
                          Container(
                            padding: const EdgeInsets.all(16),
                            decoration: BoxDecoration(
                              color: AppTheme.softMint,
                              borderRadius: BorderRadius.circular(14),
                              border: Border.all(color: Colors.green.shade200),
                            ),
                            child: Row(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                const Icon(Icons.verified, color: AppTheme.primaryGreen, size: 24),
                                const SizedBox(width: 12),
                                Expanded(
                                  child: Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      Text(
                                        isTamil ? 'தோல் ஊட்டச்சத்து சிறப்பு' : 'Peel Nutritional Superiority',
                                        style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14, color: AppTheme.primaryDark),
                                      ),
                                      const SizedBox(height: 4),
                                      Text(
                                        result.superiority.comparison(isTamil),
                                        style: TextStyle(fontSize: 13, color: Colors.green.shade900),
                                      ),
                                    ],
                                  ),
                                ),
                              ],
                            ),
                          ),
                        const SizedBox(height: 20),

                        // Calculated Nutrients List Card
                        Card(
                          elevation: 2,
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                          child: Padding(
                            padding: const EdgeInsets.all(20.0),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Row(
                                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                  children: [
                                    Text(
                                      isTamil ? 'கணக்கிடப்பட்ட ஊட்டச்சத்து உட்கொள்ளல்' : 'Estimated Nutrient Intake',
                                      style: const TextStyle(fontSize: 17, fontWeight: FontWeight.bold, color: AppTheme.primaryDark),
                                    ),
                                    Container(
                                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                                      decoration: BoxDecoration(
                                        color: AppTheme.softMint,
                                        borderRadius: BorderRadius.circular(8),
                                      ),
                                      child: Text(
                                        '${result.calculatedPeelWeightGrams}g Peel',
                                        style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12, color: AppTheme.primaryDark),
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 6),
                                Text(
                                  isTamil
                                      ? '${result.prepLabel(isTamil)} முறை • ${result.popGroupLabel(isTamil)}'
                                      : 'Preparation: ${result.prepLabel(isTamil)} • Target: ${result.popGroupLabel(isTamil)}',
                                  style: TextStyle(color: Colors.grey.shade600, fontSize: 12),
                                ),
                                const Divider(height: 24),

                                ...result.nutrients.map((nut) {
                                  final pct = nut.percentageRda ?? 0.0;
                                  Color barColor = Colors.grey.shade400;
                                  if (pct >= 30.0) {
                                    barColor = AppTheme.primaryGreen;
                                  } else if (pct >= 15.0) {
                                    barColor = Colors.teal;
                                  } else if (pct >= 5.0) {
                                    barColor = Colors.blue.shade600;
                                  }

                                  return Padding(
                                    padding: const EdgeInsets.symmetric(vertical: 10.0),
                                    child: Column(
                                      crossAxisAlignment: CrossAxisAlignment.start,
                                      children: [
                                        Row(
                                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                          children: [
                                            Expanded(
                                              child: Column(
                                                crossAxisAlignment: CrossAxisAlignment.start,
                                                children: [
                                                  Text(
                                                    nut.displayName(isTamil),
                                                    style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 14),
                                                  ),
                                                  Text(
                                                    '${nut.concentrationPer100gRaw} ${nut.unit}/100g raw (${(nut.retentionFactor * 100).toStringAsFixed(0)}% retention)',
                                                    style: TextStyle(fontSize: 11, color: Colors.grey.shade600),
                                                  ),
                                                ],
                                              ),
                                            ),
                                            Column(
                                              crossAxisAlignment: CrossAxisAlignment.end,
                                              children: [
                                                Container(
                                                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                                                  decoration: BoxDecoration(
                                                    color: AppTheme.softMint,
                                                    borderRadius: BorderRadius.circular(8),
                                                  ),
                                                  child: Text(
                                                    '${nut.estimatedAmount} ${nut.unit}',
                                                    style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14, color: AppTheme.primaryDark),
                                                  ),
                                                ),
                                                if (params.servings > 1)
                                                  Padding(
                                                    padding: const EdgeInsets.only(top: 2.0),
                                                    child: Text(
                                                      '${nut.estimatedAmountPerServing} ${nut.unit} / serving',
                                                      style: TextStyle(fontSize: 10, color: Colors.grey.shade600),
                                                    ),
                                                  ),
                                              ],
                                            ),
                                          ],
                                        ),
                                        if (nut.rdaValue != null) ...[
                                          const SizedBox(height: 8),
                                          Row(
                                            children: [
                                              Expanded(
                                                child: ClipRRect(
                                                  borderRadius: BorderRadius.circular(4),
                                                  child: LinearProgressIndicator(
                                                    value: (pct / 100.0).clamp(0.0, 1.0),
                                                    backgroundColor: Colors.grey.shade200,
                                                    valueColor: AlwaysStoppedAnimation<Color>(barColor),
                                                    minHeight: 6,
                                                  ),
                                                ),
                                              ),
                                              const SizedBox(width: 10),
                                              Text(
                                                '${pct.toStringAsFixed(1)}% RDA',
                                                style: TextStyle(
                                                  fontWeight: FontWeight.bold,
                                                  fontSize: 11,
                                                  color: barColor,
                                                ),
                                              ),
                                            ],
                                          ),
                                          if (nut.rdaLabel(isTamil).isNotEmpty)
                                            Padding(
                                              padding: const EdgeInsets.only(top: 4.0),
                                              child: Text(
                                                nut.rdaLabel(isTamil),
                                                style: TextStyle(fontSize: 11, color: Colors.grey.shade700, fontWeight: FontWeight.w500),
                                              ),
                                            ),
                                        ],
                                      ],
                                    ),
                                  );
                                }),
                              ],
                            ),
                          ),
                        ),
                        const SizedBox(height: 20),

                        // 5. Environmental Valorization Metrics Card
                        Card(
                          elevation: 2,
                          color: AppTheme.primaryDark,
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                          child: Padding(
                            padding: const EdgeInsets.all(20.0),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Row(
                                  children: [
                                    const Icon(Icons.public, color: Color(0xFFFFB300), size: 22),
                                    const SizedBox(width: 10),
                                    Text(
                                      isTamil ? 'உணவுக் கழிவு தவிர்ப்பு மற்றும் சுற்றுச்சூழல் தாக்கம்' : 'Food Waste Diversion & Ecological Impact',
                                      style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15, color: Colors.white),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 16),
                                Row(
                                  children: [
                                    Expanded(
                                      child: _buildImpactMetric(
                                        title: isTamil ? 'தவிர்க்கப்பட்ட கழிவு' : 'Waste Diverted',
                                        value: '${result.environmentalImpact.wetWasteDivertedKg} kg',
                                        subtitle: isTamil ? 'நிலப்பரப்புக்கு செல்லாமல் தடுத்தது' : 'Kept from landfill',
                                      ),
                                    ),
                                    Expanded(
                                      child: _buildImpactMetric(
                                        title: isTamil ? 'குறைக்கப்பட்ட GHG' : 'Avoided GHG',
                                        value: '${result.environmentalImpact.ghgEmissionsAvoidedKgCo2e} kg',
                                        subtitle: 'CO₂ equivalent',
                                      ),
                                    ),
                                    Expanded(
                                      child: _buildImpactMetric(
                                        title: isTamil ? 'இயற்கை உரம்' : 'Compost Yield',
                                        value: '${result.environmentalImpact.compostPotentialKg} kg',
                                        subtitle: isTamil ? 'உயிரி உரம் சாத்தியம்' : 'Nutrient humus',
                                      ),
                                    ),
                                  ],
                                ),
                              ],
                            ),
                          ),
                        ),
                        const SizedBox(height: 24),

                        // Action Buttons: Save Report & Proceed to Report Download
                        Row(
                          children: [
                            Expanded(
                              child: OutlinedButton.icon(
                                onPressed: _isSavingReport ? null : () => _handleSaveReport(result, isTamil),
                                icon: _isSavingReport
                                    ? const SizedBox(width: 16, height: 16, child: CircularProgressIndicator(strokeWidth: 2))
                                    : const Icon(Icons.save_outlined),
                                label: Text(isTamil ? 'அறிக்கையைச் சேமிக்க' : 'Save Report to Archive'),
                                style: OutlinedButton.styleFrom(padding: const EdgeInsets.symmetric(vertical: 16)),
                              ),
                            ),
                            const SizedBox(width: 12),
                            Expanded(
                              child: ElevatedButton.icon(
                                onPressed: () => context.go('/report-download'),
                                icon: const Icon(Icons.picture_as_pdf),
                                label: Text(isTamil ? 'அறிக்கையைப் பதிவிறக்குக' : 'Download Complete Report'),
                                style: ElevatedButton.styleFrom(
                                  backgroundColor: AppTheme.primaryGreen,
                                  foregroundColor: Colors.white,
                                  padding: const EdgeInsets.symmetric(vertical: 16),
                                ),
                              ),
                            ),
                          ],
                        ),
                      ],
                    );
                  },
                  loading: () => const Center(
                    child: Padding(
                      padding: EdgeInsets.all(40),
                      child: Column(
                        children: [
                          CircularProgressIndicator(color: AppTheme.primaryGreen),
                          SizedBox(height: 16),
                          Text('Calculating scientific nutrient intake...'),
                        ],
                      ),
                    ),
                  ),
                  error: (err, stack) => Center(
                    child: Padding(
                      padding: const EdgeInsets.all(24),
                      child: Text('Estimation error: $err', style: const TextStyle(color: Colors.red)),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildImpactMetric({
    required String title,
    required String value,
    required String subtitle,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(title, style: const TextStyle(fontSize: 11, color: Colors.white70)),
        const SizedBox(height: 4),
        Text(value, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Color(0xFFFFB300))),
        const SizedBox(height: 2),
        Text(subtitle, style: const TextStyle(fontSize: 10, color: Colors.white60)),
      ],
    );
  }
}
