import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/localization/app_locale.dart';
import '../../core/theme/app_theme.dart';
import '../../providers/nutrient_providers.dart';

class AdminNutrientsScreen extends ConsumerStatefulWidget {
  const AdminNutrientsScreen({super.key});

  @override
  ConsumerState<AdminNutrientsScreen> createState() => _AdminNutrientsScreenState();
}

class _AdminNutrientsScreenState extends ConsumerState<AdminNutrientsScreen> {
  void _showAddNutrientDialog() {
    final codeController = TextEditingController();
    final nameEnController = TextEditingController();
    final nameTaController = TextEditingController();
    final unitController = TextEditingController(text: 'mg');
    final roleEnController = TextEditingController();
    final roleTaController = TextEditingController();
    String category = 'vitamin';

    showDialog(
      context: context,
      builder: (ctx) {
        return StatefulBuilder(
          builder: (context, setModalState) {
            return AlertDialog(
              title: const Text('Add Chemical Nutrient Definition'),
              content: SingleChildScrollView(
                child: SizedBox(
                  width: 480,
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      TextField(controller: codeController, decoration: const InputDecoration(labelText: 'Unique Code *', hintText: 'e.g. lutein')),
                      const SizedBox(height: 10),
                      TextField(controller: nameEnController, decoration: const InputDecoration(labelText: 'English Name *', hintText: 'e.g. Lutein (Carotenoid)')),
                      const SizedBox(height: 10),
                      TextField(controller: nameTaController, decoration: const InputDecoration(labelText: 'Tamil Name (தமிழ்) *', hintText: 'e.g. லுடீன்')),
                      const SizedBox(height: 10),
                      DropdownButtonFormField<String>(
                        initialValue: category,
                        decoration: const InputDecoration(labelText: 'Category'),
                        items: const [
                          DropdownMenuItem(value: 'vitamin', child: Text('Vitamin')),
                          DropdownMenuItem(value: 'mineral', child: Text('Mineral')),
                          DropdownMenuItem(value: 'other', child: Text('Other Bioactive / Fibre')),
                        ],
                        onChanged: (val) {
                          if (val != null) setModalState(() => category = val);
                        },
                      ),
                      const SizedBox(height: 10),
                      TextField(controller: unitController, decoration: const InputDecoration(labelText: 'Standard Unit *', hintText: 'mg, mcg, or g')),
                      const SizedBox(height: 10),
                      TextField(controller: roleEnController, decoration: const InputDecoration(labelText: 'Biological Role (English)')),
                      const SizedBox(height: 10),
                      TextField(controller: roleTaController, decoration: const InputDecoration(labelText: 'Biological Role (Tamil)')),
                    ],
                  ),
                ),
              ),
              actions: [
                TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Cancel')),
                ElevatedButton(
                  style: ElevatedButton.styleFrom(backgroundColor: AppTheme.primaryGreen, foregroundColor: Colors.white),
                  onPressed: () async {
                    final code = codeController.text.trim().toLowerCase();
                    final nameEn = nameEnController.text.trim();
                    final nameTa = nameTaController.text.trim();
                    final unit = unitController.text.trim();

                    if (code.isEmpty || nameEn.isEmpty || nameTa.isEmpty || unit.isEmpty) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(content: Text('Please fill all required fields.')),
                      );
                      return;
                    }

                    final navigator = Navigator.of(ctx);
                    final messenger = ScaffoldMessenger.of(context);

                    try {
                      final repo = ref.read(nutrientsRepositoryProvider);
                      await repo.createNutrient({
                        'code': code,
                        'name_en': nameEn,
                        'name_ta': nameTa,
                        'category': category,
                        'standard_unit': unit,
                        'biological_role_en': roleEnController.text.trim(),
                        'biological_role_ta': roleTaController.text.trim(),
                      });
                      ref.invalidate(allNutrientsAsyncProvider);
                      navigator.pop();
                      messenger.showSnackBar(
                        SnackBar(content: Text('Nutrient $nameEn registered successfully!'), backgroundColor: AppTheme.primaryGreen),
                      );
                    } catch (e) {
                      messenger.showSnackBar(
                        SnackBar(content: Text('Registration failed: $e'), backgroundColor: Colors.red),
                      );
                    }
                  },
                  child: const Text('Save Definition'),
                ),
              ],
            );
          },
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final lang = ref.watch(localeProvider);
    final isTamil = lang == AppLanguage.ta;
    final nutrientsAsync = ref.watch(allNutrientsAsyncProvider);
    final nutrients = nutrientsAsync.value ?? [];

    return Scaffold(
      appBar: AppBar(
        backgroundColor: const Color(0xFF263238),
        title: Text(isTamil ? 'வேதியியல் ஊட்டச்சத்துக்கள் மேலாண்மை' : 'Nutrient Composition Standards (IFCT/USDA)'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => context.go('/admin-dashboard'),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            tooltip: 'Refresh Nutrients',
            onPressed: () => ref.invalidate(allNutrientsAsyncProvider),
          ),
          IconButton(
            icon: const Icon(Icons.add_circle_outline, color: Colors.lightGreenAccent),
            tooltip: 'Add Nutrient',
            onPressed: _showAddNutrientDialog,
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        backgroundColor: AppTheme.primaryGreen,
        icon: const Icon(Icons.add, color: Colors.white),
        label: Text(isTamil ? 'புதிய ஊட்டச்சத்து சேர்க்க' : 'Add Nutrient Standard', style: const TextStyle(color: Colors.white)),
        onPressed: _showAddNutrientDialog,
      ),
      body: nutrientsAsync.isLoading
          ? const Center(child: CircularProgressIndicator())
          : ListView.builder(
              padding: const EdgeInsets.all(16.0),
              itemCount: nutrients.length,
              itemBuilder: (context, index) {
                final item = nutrients[index];
                final isVit = item.category == 'vitamin';
                final isMin = item.category == 'mineral';
                return Card(
                  elevation: 1,
                  margin: const EdgeInsets.only(bottom: 10),
                  child: ListTile(
                    leading: CircleAvatar(
                      backgroundColor: isVit
                          ? Colors.orange.shade100
                          : isMin
                              ? Colors.blue.shade100
                              : AppTheme.softMint,
                      child: Text(
                        isVit ? 'V' : isMin ? 'M' : 'B',
                        style: TextStyle(
                          fontWeight: FontWeight.bold,
                          color: isVit
                              ? Colors.orange.shade800
                              : isMin
                                  ? Colors.blue.shade800
                                  : AppTheme.primaryDark,
                        ),
                      ),
                    ),
                    title: Row(
                      children: [
                        Text(item.nameEn, style: const TextStyle(fontWeight: FontWeight.bold)),
                        const SizedBox(width: 8),
                        Text('(${item.nameTa})', style: TextStyle(color: Colors.grey.shade600, fontSize: 13)),
                      ],
                    ),
                    subtitle: Text('Code: ${item.code} • Category: ${item.category} • Standard Unit: ${item.standardUnit}'),
                    trailing: Chip(
                      label: Text(item.standardUnit),
                      backgroundColor: Colors.grey.shade100,
                      labelStyle: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold),
                    ),
                  ),
                );
              },
            ),
    );
  }
}
