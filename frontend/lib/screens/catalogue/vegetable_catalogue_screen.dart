import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/localization/app_locale.dart';
import '../../core/theme/app_theme.dart';
import '../../providers/app_providers.dart';
import '../../providers/vegetable_providers.dart';

class VegetableCatalogueScreen extends ConsumerStatefulWidget {
  const VegetableCatalogueScreen({super.key});

  @override
  ConsumerState<VegetableCatalogueScreen> createState() => _VegetableCatalogueScreenState();
}

class _VegetableCatalogueScreenState extends ConsumerState<VegetableCatalogueScreen> {
  final TextEditingController _searchController = TextEditingController();

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final lang = ref.watch(localeProvider);
    final isTamil = lang == AppLanguage.ta;

    final asyncVegs = ref.watch(vegetablesListAsyncProvider);
    final filteredVegs = ref.watch(filteredVegetablesListProvider);
    final selectedCategory = ref.watch(selectedCategoryFilterProvider);

    // Categories list for chips
    final defaultCategories = [
      'All',
      'AI Ready',
      'Root',
      'Gourd',
      'Solanaceous',
      'Allium',
      'Legume',
      'Outer Layer',
    ];

    return Scaffold(
      body: RefreshIndicator(
        onRefresh: () async {
          ref.invalidate(vegetablesListAsyncProvider);
          ref.invalidate(categoriesAsyncProvider);
        },
        child: SingleChildScrollView(
          physics: const AlwaysScrollableScrollPhysics(),
          padding: const EdgeInsets.symmetric(horizontal: 20.0, vertical: 16.0),
          child: Center(
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 1000),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  // Title and Live Counter
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            isTamil ? 'காய்கறி பட்டியல்' : 'Vegetable Master Catalogue',
                            style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: AppTheme.primaryDark),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            isTamil
                                ? '50 தாவர வகைகள் • தமிழ் & அறிவியல் பெயர்கள்'
                                : '${filteredVegs.length} botanical species available • ICMR-NIN & USDA IFCT verified',
                            style: TextStyle(color: Colors.grey.shade700, fontSize: 13),
                          ),
                        ],
                      ),
                      if (asyncVegs.isLoading)
                        const SizedBox(
                          width: 22,
                          height: 22,
                          child: CircularProgressIndicator(strokeWidth: 2.5),
                        ),
                    ],
                  ),
                  const SizedBox(height: 16),

                  // Search Bar with instant reactive filter
                  Container(
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(16),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black.withValues(alpha: 0.05),
                          blurRadius: 10,
                          offset: const Offset(0, 4),
                        ),
                      ],
                    ),
                    child: TextField(
                      controller: _searchController,
                      onChanged: (val) {
                        ref.read(searchQueryFilterProvider.notifier).state = val;
                      },
                      decoration: InputDecoration(
                        hintText: isTamil
                            ? 'பெயர், தமிழ் பெயர் அல்லது தாவர பெயர் மூலம் தேடுங்கள்...'
                            : 'Search by English, Tamil (தமிழ்), or Botanical name...',
                        hintStyle: TextStyle(fontSize: 14, color: Colors.grey.shade500),
                        prefixIcon: const Icon(Icons.search, color: AppTheme.primaryGreen),
                        suffixIcon: _searchController.text.isNotEmpty
                            ? IconButton(
                                icon: const Icon(Icons.clear, color: Colors.grey),
                                onPressed: () {
                                  _searchController.clear();
                                  ref.read(searchQueryFilterProvider.notifier).state = '';
                                },
                              )
                            : null,
                        border: InputBorder.none,
                        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
                      ),
                    ),
                  ),
                  const SizedBox(height: 16),

                  // Horizontal Filter Chips
                  SingleChildScrollView(
                    scrollDirection: Axis.horizontal,
                    child: Row(
                      children: defaultCategories.map((cat) {
                        final isSelected = selectedCategory == cat;
                        return Padding(
                          padding: const EdgeInsets.only(right: 8.0),
                          child: ChoiceChip(
                            label: Text(
                              cat == 'All'
                                  ? (isTamil ? 'அனைத்தும்' : 'All')
                                  : cat == 'AI Ready'
                                      ? (isTamil ? 'AI கேமரா' : 'AI Camera Ready')
                                      : cat,
                            ),
                            selected: isSelected,
                            selectedColor: AppTheme.softMint,
                            labelStyle: TextStyle(
                              color: isSelected ? AppTheme.primaryDark : Colors.black87,
                              fontWeight: isSelected ? FontWeight.bold : FontWeight.w500,
                              fontSize: 13,
                            ),
                            onSelected: (selected) {
                              if (selected) {
                                ref.read(selectedCategoryFilterProvider.notifier).state = cat;
                              }
                            },
                          ),
                        );
                      }).toList(),
                    ),
                  ),
                  const SizedBox(height: 20),

                  // Empty State
                  if (filteredVegs.isEmpty)
                    Container(
                      padding: const EdgeInsets.all(40),
                      alignment: Alignment.center,
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Icon(Icons.search_off, size: 64, color: Colors.grey.shade400),
                          const SizedBox(height: 12),
                          Text(
                            isTamil ? 'காய்கறி எதுவும் கிடைக்கவில்லை' : 'No vegetables matched your search',
                            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                          ),
                          const SizedBox(height: 6),
                          Text(
                            isTamil ? 'வேறு வார்த்தைகளை பயன்படுத்தி தேடவும்' : 'Try searching with another keyword or resetting filters',
                            style: TextStyle(color: Colors.grey.shade600, fontSize: 13),
                          ),
                          const SizedBox(height: 16),
                          ElevatedButton.icon(
                            onPressed: () {
                              _searchController.clear();
                              ref.read(searchQueryFilterProvider.notifier).state = '';
                              ref.read(selectedCategoryFilterProvider.notifier).state = 'All';
                            },
                            icon: const Icon(Icons.refresh),
                            label: Text(isTamil ? 'அனைத்தையும் காட்டு' : 'Reset All Filters'),
                          ),
                        ],
                      ),
                    )
                  else
                    // Responsive Grid of Vegetable Cards
                    GridView.builder(
                      shrinkWrap: true,
                      physics: const NeverScrollableScrollPhysics(),
                      gridDelegate: const SliverGridDelegateWithMaxCrossAxisExtent(
                        maxCrossAxisExtent: 440,
                        mainAxisExtent: 175,
                        crossAxisSpacing: 14,
                        mainAxisSpacing: 14,
                      ),
                      itemCount: filteredVegs.length,
                      itemBuilder: (context, index) {
                        final veg = filteredVegs[index];
                        return Card(
                          elevation: 1.5,
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(16),
                            side: BorderSide(
                              color: veg.isAiSupported ? AppTheme.primaryGreen.withValues(alpha: 0.3) : Colors.grey.shade200,
                              width: 1,
                            ),
                          ),
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
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      CircleAvatar(
                                        radius: 20,
                                        backgroundColor: veg.isAiSupported ? AppTheme.softMint : Colors.grey.shade100,
                                        child: Icon(
                                          veg.isAiSupported ? Icons.camera_alt_outlined : Icons.eco_outlined,
                                          color: veg.isAiSupported ? AppTheme.primaryGreen : Colors.grey.shade600,
                                          size: 20,
                                        ),
                                      ),
                                      const SizedBox(width: 12),
                                      Expanded(
                                        child: Column(
                                          crossAxisAlignment: CrossAxisAlignment.start,
                                          children: [
                                            Text(
                                              veg.displayName(isTamil),
                                              style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                                              maxLines: 1,
                                              overflow: TextOverflow.ellipsis,
                                            ),
                                            Text(
                                              isTamil ? veg.nameEn : veg.nameTa,
                                              style: TextStyle(fontSize: 12, color: Colors.grey.shade600),
                                            ),
                                          ],
                                        ),
                                      ),
                                      if (veg.isAiSupported)
                                        Container(
                                          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                                          decoration: BoxDecoration(
                                            color: Colors.green.shade50,
                                            borderRadius: BorderRadius.circular(8),
                                            border: Border.all(color: Colors.green.shade300, width: 0.8),
                                          ),
                                          child: const Row(
                                            mainAxisSize: MainAxisSize.min,
                                            children: [
                                              Icon(Icons.auto_awesome, size: 10, color: AppTheme.primaryDark),
                                              SizedBox(width: 4),
                                              Text(
                                                'AI Ready',
                                                style: TextStyle(color: AppTheme.primaryDark, fontSize: 10, fontWeight: FontWeight.bold),
                                              ),
                                            ],
                                          ),
                                        ),
                                    ],
                                  ),
                                  const SizedBox(height: 8),
                                  Text(
                                    veg.scientificName,
                                    style: TextStyle(fontSize: 12, fontStyle: FontStyle.italic, color: Colors.grey.shade700),
                                    maxLines: 1,
                                    overflow: TextOverflow.ellipsis,
                                  ),
                                  const Spacer(),
                                  Row(
                                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                    children: [
                                      Flexible(
                                        child: Container(
                                          padding: const EdgeInsets.symmetric(horizontal: 7, vertical: 2),
                                          decoration: BoxDecoration(
                                            color: Colors.grey.shade100,
                                            borderRadius: BorderRadius.circular(6),
                                          ),
                                          child: Text(
                                            veg.category,
                                            style: TextStyle(fontSize: 11, color: Colors.grey.shade800),
                                            maxLines: 1,
                                            overflow: TextOverflow.ellipsis,
                                          ),
                                        ),
                                      ),
                                      const SizedBox(width: 8),
                                      Container(
                                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                                        decoration: BoxDecoration(
                                          color: veg.foodSafetyStatus == 'hazardous_raw'
                                              ? Colors.red.shade50
                                              : veg.foodSafetyStatus == 'conditional_cooking_required'
                                                  ? Colors.amber.shade50
                                                  : Colors.green.shade50,
                                          borderRadius: BorderRadius.circular(6),
                                          border: Border.all(
                                            color: veg.foodSafetyStatus == 'hazardous_raw'
                                                ? Colors.red.shade300
                                                : veg.foodSafetyStatus == 'conditional_cooking_required'
                                                    ? Colors.amber.shade400
                                                    : Colors.green.shade300,
                                            width: 0.8,
                                          ),
                                        ),
                                        child: Text(
                                          veg.foodSafetyStatus == 'hazardous_raw'
                                              ? (isTamil ? 'உண்ணக்கூடாது' : 'Inedible Raw')
                                              : veg.foodSafetyStatus == 'conditional_cooking_required'
                                                  ? (isTamil ? 'சமைக்க வேண்டும்' : 'Cook First')
                                                  : (isTamil ? 'பாதுகாப்பானது' : 'Food Safe'),
                                          style: TextStyle(
                                            fontSize: 10,
                                            fontWeight: FontWeight.bold,
                                            color: veg.foodSafetyStatus == 'hazardous_raw'
                                                ? Colors.red.shade800
                                                : veg.foodSafetyStatus == 'conditional_cooking_required'
                                                    ? Colors.amber.shade900
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
        ),
      ),
    );
  }
}
