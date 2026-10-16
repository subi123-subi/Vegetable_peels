import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/localization/app_locale.dart';
import '../../core/theme/app_theme.dart';
import '../../providers/app_providers.dart';

class VegetableCatalogueScreen extends ConsumerStatefulWidget {
  const VegetableCatalogueScreen({super.key});

  @override
  ConsumerState<VegetableCatalogueScreen> createState() => _VegetableCatalogueScreenState();
}

class _VegetableCatalogueScreenState extends ConsumerState<VegetableCatalogueScreen> {
  String _selectedCategory = 'All';

  @override
  Widget build(BuildContext context) {
    final lang = ref.watch(localeProvider);
    final isTamil = lang == AppLanguage.ta;
    final allVegs = ref.watch(catalogueProvider);

    final categories = ['All', 'AI Supported', 'Root Vegetable', 'Gourds & Cucurbits', 'Bulbs & Aromatics'];

    final filteredVegs = allVegs.where((v) {
      if (_selectedCategory == 'AI Supported') return v.isAiSupported;
      if (_selectedCategory == 'All') return true;
      return v.category.contains(_selectedCategory);
    }).toList();

    return SingleChildScrollView(
      padding: const EdgeInsets.all(20.0),
      child: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 900),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Search & Header Bar
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        isTamil ? 'காய்கறி பட்டியல்' : 'Vegetable Master Catalogue',
                        style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: AppTheme.primaryDark),
                      ),
                      Text(
                        isTamil ? '50 காய்கறி வகைகள் • தாவர வகைப்பாடு' : '50 Supported Botanical Plant Materials',
                        style: TextStyle(color: Colors.grey.shade600, fontSize: 13),
                      ),
                    ],
                  ),
                  IconButton.filled(
                    style: IconButton.styleFrom(backgroundColor: AppTheme.primaryGreen),
                    onPressed: () => context.go('/search'),
                    icon: const Icon(Icons.search, color: Colors.white),
                    tooltip: 'Search',
                  ),
                ],
              ),
              const SizedBox(height: 16),

              // Filter Chips
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: categories.map((cat) {
                    final isSelected = _selectedCategory == cat;
                    return Padding(
                      padding: const EdgeInsets.only(right: 8.0),
                      child: FilterChip(
                        selected: isSelected,
                        label: Text(cat),
                        selectedColor: AppTheme.softMint,
                        checkmarkColor: AppTheme.primaryGreen,
                        labelStyle: TextStyle(
                          color: isSelected ? AppTheme.primaryDark : Colors.black87,
                          fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                        ),
                        onSelected: (selected) {
                          if (selected) {
                            setState(() => _selectedCategory = cat);
                          }
                        },
                      ),
                    );
                  }).toList(),
                ),
              ),
              const SizedBox(height: 20),

              // Grid/List of Vegetables
              GridView.builder(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                gridDelegate: const SliverGridDelegateWithMaxCrossAxisExtent(
                  maxCrossAxisExtent: 420,
                  mainAxisExtent: 160,
                  crossAxisSpacing: 14,
                  mainAxisSpacing: 14,
                ),
                itemCount: filteredVegs.length,
                itemBuilder: (context, index) {
                  final veg = filteredVegs[index];
                  return Card(
                    child: InkWell(
                      borderRadius: BorderRadius.circular(16),
                      onTap: () {
                        ref.read(selectedVegetableProvider.notifier).select(veg);
                        context.go('/nutrients');
                      },
                      child: Padding(
                        padding: const EdgeInsets.all(16.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                Expanded(
                                  child: Text(
                                    veg.displayName(isTamil),
                                    style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                                    maxLines: 1,
                                    overflow: TextOverflow.ellipsis,
                                  ),
                                ),
                                if (veg.isAiSupported)
                                  Container(
                                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                                    decoration: BoxDecoration(
                                      color: Colors.green.shade100,
                                      borderRadius: BorderRadius.circular(8),
                                    ),
                                    child: const Text(
                                      'AI Ready',
                                      style: TextStyle(color: AppTheme.primaryDark, fontSize: 10, fontWeight: FontWeight.bold),
                                    ),
                                  )
                                else
                                  Container(
                                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                                    decoration: BoxDecoration(
                                      color: Colors.grey.shade100,
                                      borderRadius: BorderRadius.circular(8),
                                    ),
                                    child: const Text(
                                      'Manual',
                                      style: TextStyle(color: Colors.grey, fontSize: 10, fontWeight: FontWeight.bold),
                                    ),
                                  ),
                              ],
                            ),
                            Text(
                              veg.scientificName,
                              style: TextStyle(fontSize: 12, fontStyle: FontStyle.italic, color: Colors.grey.shade600),
                            ),
                            const Spacer(),
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                Text(
                                  veg.category,
                                  style: TextStyle(fontSize: 11, color: Colors.grey.shade700),
                                ),
                                Container(
                                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                                  decoration: BoxDecoration(
                                    color: veg.foodSafetyStatus == 'hazardous_raw'
                                        ? Colors.red.shade50
                                        : veg.foodSafetyStatus == 'conditional_cooking_required'
                                            ? Colors.orange.shade50
                                            : Colors.green.shade50,
                                    borderRadius: BorderRadius.circular(6),
                                  ),
                                  child: Text(
                                    veg.foodSafetyStatus == 'hazardous_raw'
                                        ? 'Inedible Raw'
                                        : veg.foodSafetyStatus == 'conditional_cooking_required'
                                            ? 'Cook First'
                                            : 'Food Safe',
                                    style: TextStyle(
                                      fontSize: 10,
                                      fontWeight: FontWeight.bold,
                                      color: veg.foodSafetyStatus == 'hazardous_raw'
                                          ? Colors.red
                                          : veg.foodSafetyStatus == 'conditional_cooking_required'
                                              ? Colors.orange.shade900
                                              : AppTheme.primaryGreen,
                                    ),
                                  ),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                    ),
                  );
                },
              ),
            ],
          ),
        ),
      ),
    );
  }
}
