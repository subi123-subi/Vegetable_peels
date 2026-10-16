import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:intl/intl.dart';
import '../../core/localization/app_locale.dart';
import '../../core/theme/app_theme.dart';
import '../../providers/app_providers.dart';

class ScanHistoryScreen extends ConsumerWidget {
  const ScanHistoryScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final lang = ref.watch(localeProvider);
    final isTamil = lang == AppLanguage.ta;
    final history = ref.watch(scanHistoryProvider);

    final double totalWasteGrams = history.fold(0.0, (sum, item) => sum + (item.weightGrams ?? 100.0));

    return SingleChildScrollView(
      padding: const EdgeInsets.all(20.0),
      child: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 800),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Header Summary Card
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(20.0),
                  child: Column(
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceAround,
                        children: [
                          Column(
                            children: [
                              Text(
                                '${history.length}',
                                style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: AppTheme.primaryDark),
                              ),
                              Text(
                                isTamil ? 'மொத்த ஸ்கேன்கள்' : 'Total Scans',
                                style: TextStyle(color: Colors.grey.shade600, fontSize: 12),
                              ),
                            ],
                          ),
                          Container(width: 1, height: 40, color: Colors.grey.shade300),
                          Column(
                            children: [
                              Text(
                                '${(totalWasteGrams / 1000).toStringAsFixed(2)} kg',
                                style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: AppTheme.leafGreen),
                              ),
                              Text(
                                isTamil ? 'திசைதிருப்பப்பட்ட கழிவு' : 'Diverted Waste',
                                style: TextStyle(color: Colors.grey.shade600, fontSize: 12),
                              ),
                            ],
                          ),
                          Container(width: 1, height: 40, color: Colors.grey.shade300),
                          Column(
                            children: [
                              const Text(
                                '100%',
                                style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: AppTheme.nutritionCyan),
                              ),
                              Text(
                                isTamil ? 'மறுபயன்பாட்டு விகிதம்' : 'Diversion Rate',
                                style: TextStyle(color: Colors.grey.shade600, fontSize: 12),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 20),

              Text(
                isTamil ? 'பதிவு செய்யப்பட்ட அமர்வுகள்:' : 'Chronological Identification History:',
                style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: AppTheme.primaryDark),
              ),
              const SizedBox(height: 12),

              if (history.isEmpty)
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(32.0),
                    child: Center(
                      child: Text(
                        isTamil ? 'பதிவுகள் எதுவும் இல்லை.' : 'No scan records found.',
                        style: TextStyle(color: Colors.grey.shade600),
                      ),
                    ),
                  ),
                )
              else
                ...history.map((item) {
                  final formattedDate = DateFormat('dd MMM yyyy, hh:mm a').format(item.scannedAt);
                  return Card(
                    child: ListTile(
                      leading: CircleAvatar(
                        backgroundColor: AppTheme.softMint,
                        child: const Icon(Icons.history_toggle_off, color: AppTheme.primaryGreen),
                      ),
                      title: Text(
                        '${item.predictedVegetable.displayName(isTamil)} (${item.weightGrams?.toStringAsFixed(0) ?? "100"}g)',
                        style: const TextStyle(fontWeight: FontWeight.bold),
                      ),
                      subtitle: Text(
                        '$formattedDate\nID: ${item.scanId} • AI Match: ${(item.confidence * 100).toStringAsFixed(0)}%',
                        style: const TextStyle(fontSize: 12),
                      ),
                      trailing: IconButton(
                        icon: const Icon(Icons.arrow_forward_ios, size: 16),
                        onPressed: () {
                          ref.read(selectedVegetableProvider.notifier).select(item.predictedVegetable);
                          context.go('/nutrients');
                        },
                      ),
                    ),
                  );
                }),
            ],
          ),
        ),
      ),
    );
  }
}
