import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/localization/app_locale.dart';
import '../../core/theme/app_theme.dart';

class AdminSourcesScreen extends ConsumerWidget {
  const AdminSourcesScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final lang = ref.watch(localeProvider);
    final isTamil = lang == AppLanguage.ta;

    final sources = [
      {
        'title': 'Indian Food Composition Tables (IFCT 2017)',
        'authors': 'Longvah T, Ananthan R, Bhaskarachary K, Venkaiah K',
        'publisher': 'National Institute of Nutrition, ICMR, Hyderabad',
        'year': '2017',
        'type': 'Institutional Standard',
        'rating': 'High (Gold Standard)',
      },
      {
        'title': 'USDA FoodData Central Nutrient Database',
        'authors': 'U.S. Department of Agriculture, Agricultural Research Service',
        'publisher': 'USDA Agricultural Research Service',
        'year': '2023',
        'type': 'National Database',
        'rating': 'High (Gold Standard)',
      },
      {
        'title': 'Valorization of Vegetable Peels: Nutritional Profile and Bioactive Compounds',
        'authors': 'Kumar M, Chandran D, Tomar M, et al.',
        'publisher': 'Frontiers in Nutrition, 9:904261',
        'year': '2022',
        'type': 'Peer-Reviewed Literature',
        'rating': 'High (Peer-Reviewed)',
      },
    ];

    return Scaffold(
      appBar: AppBar(
        backgroundColor: const Color(0xFF263238),
        title: Text(isTamil ? 'அறிவியல் தரவு மூலங்கள்' : 'Scientific Reference Sources'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => context.go('/admin-dashboard'),
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        backgroundColor: AppTheme.primaryGreen,
        icon: const Icon(Icons.add, color: Colors.white),
        label: const Text('Add Research Source', style: TextStyle(color: Colors.white)),
        onPressed: () {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Source registration dialog')),
          );
        },
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(16.0),
        itemCount: sources.length,
        itemBuilder: (context, index) {
          final s = sources[index];
          return Card(
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                        decoration: BoxDecoration(color: AppTheme.softMint, borderRadius: BorderRadius.circular(6)),
                        child: Text(s['type']!, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 11, color: AppTheme.primaryDark)),
                      ),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                        decoration: BoxDecoration(color: Colors.blue.shade50, borderRadius: BorderRadius.circular(6)),
                        child: Text(s['rating']!, style: TextStyle(fontWeight: FontWeight.bold, fontSize: 11, color: Colors.blue.shade900)),
                      ),
                    ],
                  ),
                  const SizedBox(height: 10),
                  Text(s['title']!, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
                  const SizedBox(height: 4),
                  Text('Authors: ${s["authors"]}', style: TextStyle(fontSize: 12, color: Colors.grey.shade700)),
                  Text('Publisher: ${s["publisher"]} (${s["year"]})', style: TextStyle(fontSize: 12, color: Colors.grey.shade600)),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
