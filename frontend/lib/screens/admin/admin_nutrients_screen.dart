import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/localization/app_locale.dart';
import '../../core/theme/app_theme.dart';

class AdminNutrientsScreen extends ConsumerWidget {
  const AdminNutrientsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final lang = ref.watch(localeProvider);
    final isTamil = lang == AppLanguage.ta;

    final nutrientsList = [
      {'code': 'vit_a', 'name': 'Vitamin A / Carotenoids', 'cat': 'Vitamin', 'unit': 'mcg'},
      {'code': 'vit_c', 'name': 'Vitamin C (Ascorbic Acid)', 'cat': 'Vitamin', 'unit': 'mg'},
      {'code': 'vit_k', 'name': 'Vitamin K1 (Phylloquinone)', 'cat': 'Vitamin', 'unit': 'mcg'},
      {'code': 'calcium', 'name': 'Calcium (Ca)', 'cat': 'Mineral', 'unit': 'mg'},
      {'code': 'potassium', 'name': 'Potassium (K)', 'cat': 'Mineral', 'unit': 'mg'},
      {'code': 'iron', 'name': 'Iron (Fe)', 'cat': 'Mineral', 'unit': 'mg'},
      {'code': 'dietary_fibre', 'name': 'Total Dietary Fibre', 'cat': 'Other', 'unit': 'g'},
      {'code': 'total_phenolics', 'name': 'Total Phenolics (GAE)', 'cat': 'Other', 'unit': 'mg GAE'},
      {'code': 'betalains', 'name': 'Betalains', 'cat': 'Other', 'unit': 'mg'},
    ];

    return Scaffold(
      appBar: AppBar(
        backgroundColor: const Color(0xFF263238),
        title: Text(isTamil ? 'ஊட்டச்சத்து அமைப்புகள்' : 'Nutrient Standards Management'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => context.go('/admin-dashboard'),
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        backgroundColor: AppTheme.primaryGreen,
        icon: const Icon(Icons.add, color: Colors.white),
        label: const Text('Add Nutrient Field', style: TextStyle(color: Colors.white)),
        onPressed: () {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Nutrient field creation dialog')),
          );
        },
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(16.0),
        itemCount: nutrientsList.length,
        itemBuilder: (context, index) {
          final item = nutrientsList[index];
          return Card(
            child: ListTile(
              leading: CircleAvatar(
                backgroundColor: item['cat'] == 'Vitamin'
                    ? Colors.orange.shade100
                    : item['cat'] == 'Mineral'
                        ? Colors.blue.shade100
                        : AppTheme.softMint,
                child: Text(
                  item['cat']![0],
                  style: TextStyle(
                    fontWeight: FontWeight.bold,
                    color: item['cat'] == 'Vitamin'
                        ? Colors.orange.shade800
                        : item['cat'] == 'Mineral'
                            ? Colors.blue.shade800
                            : AppTheme.primaryDark,
                  ),
                ),
              ),
              title: Text(item['name']!, style: const TextStyle(fontWeight: FontWeight.bold)),
              subtitle: Text('Category: ${item["cat"]} • Standard Unit: ${item["unit"]}'),
              trailing: IconButton(
                icon: const Icon(Icons.edit, size: 20, color: Colors.blueGrey),
                onPressed: () {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(content: Text('Editing ${item["name"]}')),
                  );
                },
              ),
            ),
          );
        },
      ),
    );
  }
}
