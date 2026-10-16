import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/localization/app_locale.dart';
import '../../core/theme/app_theme.dart';
import '../../providers/app_providers.dart';

class NutrientEstimationScreen extends ConsumerStatefulWidget {
  const NutrientEstimationScreen({super.key});

  @override
  ConsumerState<NutrientEstimationScreen> createState() => _NutrientEstimationScreenState();
}

class _NutrientEstimationScreenState extends ConsumerState<NutrientEstimationScreen> {
  final _weightController = TextEditingController(text: '100');
  double _currentWeightGrams = 100.0;

  @override
  void initState() {
    super.initState();
    final scan = ref.read(currentScanProvider);
    if (scan?.weightGrams != null) {
      _currentWeightGrams = scan!.weightGrams!;
      _weightController.text = _currentWeightGrams.toStringAsFixed(0);
    }
  }

  @override
  void dispose() {
    _weightController.dispose();
    super.dispose();
  }

  void _updateWeight(double weight) {
    setState(() {
      _currentWeightGrams = weight;
      _weightController.text = weight.toStringAsFixed(0);
    });
    ref.read(currentScanProvider.notifier).setWeight(weight);
  }

  @override
  Widget build(BuildContext context) {
    final lang = ref.watch(localeProvider);
    final isTamil = lang == AppLanguage.ta;
    final veg = ref.watch(selectedVegetableProvider);
    final nutrients = ref.watch(nutrientsForSelectedVegetableProvider);

    return Scaffold(
      appBar: AppBar(
        title: Text(isTamil ? 'எடை வாரியான ஊட்டச்சத்து மதிப்பீடு' : 'Weight-Based Nutrient Estimator'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => context.go('/nutrients'),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 800),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // Weight input Card
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(20.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          isTamil ? 'காய்கறி தோலின் எடை (கிராமில்):' : 'Enter Measured Peel Weight (Grams):',
                          style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: AppTheme.primaryDark),
                        ),
                        const SizedBox(height: 6),
                        Text(
                          isTamil
                              ? 'சூத்திரம்: (தோல் எடை / 100) × 100 கிராம் புதிய எடை ஊட்டச்சத்து செறிவு'
                              : 'Formula: (Peel Weight in g / 100) × Validated Concentration per 100g Fresh Weight',
                          style: TextStyle(color: Colors.grey.shade600, fontSize: 12),
                        ),
                        const SizedBox(height: 16),
                        Row(
                          children: [
                            Expanded(
                              flex: 3,
                              child: Slider(
                                value: _currentWeightGrams.clamp(10, 1000),
                                min: 10,
                                max: 1000,
                                divisions: 99,
                                label: '${_currentWeightGrams.round()} g',
                                activeColor: AppTheme.primaryGreen,
                                onChanged: (val) => _updateWeight(val),
                              ),
                            ),
                            const SizedBox(width: 12),
                            Expanded(
                              flex: 1,
                              child: TextField(
                                controller: _weightController,
                                keyboardType: TextInputType.number,
                                decoration: const InputDecoration(
                                  suffixText: 'g',
                                  contentPadding: EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                                ),
                                onChanged: (val) {
                                  final parsed = double.tryParse(val);
                                  if (parsed != null && parsed > 0 && parsed <= 5000) {
                                    setState(() {
                                      _currentWeightGrams = parsed;
                                    });
                                    ref.read(currentScanProvider.notifier).setWeight(parsed);
                                  }
                                },
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 10),
                        Wrap(
                          spacing: 8,
                          children: [50, 100, 150, 250, 500].map((w) {
                            return ActionChip(
                              label: Text('$w g'),
                              onPressed: () => _updateWeight(w.toDouble()),
                            );
                          }).toList(),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 16),

                // Scientific Notice
                Container(
                  padding: const EdgeInsets.all(14),
                  decoration: BoxDecoration(
                    color: AppTheme.softMint,
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: Colors.green.shade200),
                  ),
                  child: Row(
                    children: [
                      const Icon(Icons.check_circle_outline, color: AppTheme.primaryGreen, size: 20),
                      const SizedBox(width: 10),
                      Expanded(
                        child: Text(
                          isTamil
                              ? 'கணக்கீட்டு அடிப்படை: புதிய எடையிலான அறிவியல் அளவீடு. சமைக்கும் போது ஏற்படும் இழப்புகள் தனித்தனியாக மாறுபடலாம்.'
                              : 'Basis: Fresh weight composition. Actual retention depends on washing and heat preparation.',
                          style: TextStyle(fontSize: 12, color: Colors.green.shade900),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 20),

                // Calculated Results Table Card
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(20.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(
                              '${veg.displayName(isTamil)} (${_currentWeightGrams.toStringAsFixed(0)}g Peel)',
                              style: const TextStyle(fontSize: 17, fontWeight: FontWeight.bold, color: AppTheme.primaryDark),
                            ),
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                              decoration: BoxDecoration(
                                color: Colors.grey.shade100,
                                borderRadius: BorderRadius.circular(6),
                              ),
                              child: Text(
                                '${(_currentWeightGrams / 100).toStringAsFixed(2)}x factor',
                                style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold),
                              ),
                            ),
                          ],
                        ),
                        const Divider(height: 24),
                        ...nutrients.map((nut) {
                          final estimatedAmount = nut.calculateAmount(_currentWeightGrams);
                          return Padding(
                            padding: const EdgeInsets.symmetric(vertical: 8.0),
                            child: Row(
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
                                        'Ref: ${nut.concentrationPer100g} ${nut.unit} per 100g fresh peel',
                                        style: TextStyle(fontSize: 11, color: Colors.grey.shade600),
                                      ),
                                    ],
                                  ),
                                ),
                                Container(
                                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                                  decoration: BoxDecoration(
                                    color: AppTheme.softMint,
                                    borderRadius: BorderRadius.circular(10),
                                  ),
                                  child: Text(
                                    '${estimatedAmount >= 10 ? estimatedAmount.toStringAsFixed(1) : estimatedAmount.toStringAsFixed(2)} ${nut.unit}',
                                    style: const TextStyle(fontWeight: FontWeight.bold, color: AppTheme.primaryDark, fontSize: 14),
                                  ),
                                ),
                              ],
                            ),
                          );
                        }),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 20),

                ElevatedButton.icon(
                  onPressed: () => context.go('/report-download'),
                  icon: const Icon(Icons.download),
                  label: Text(isTamil ? 'முழுமையான அறிக்கையைப் பதிவிறக்குக' : 'Download Complete Summary Report'),
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 16),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
