import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/localization/app_locale.dart';
import '../../core/theme/app_theme.dart';
import '../../models/app_models.dart';
import '../../providers/vegetable_providers.dart';

class AdminVegetablesScreen extends ConsumerStatefulWidget {
  const AdminVegetablesScreen({super.key});

  @override
  ConsumerState<AdminVegetablesScreen> createState() => _AdminVegetablesScreenState();
}

class _AdminVegetablesScreenState extends ConsumerState<AdminVegetablesScreen> {
  String _searchQuery = '';

  void _showAddEditVegetableDialog({VegetableItem? existing}) {
    final isEdit = existing != null;
    final nameEnController = TextEditingController(text: existing?.nameEn ?? '');
    final nameTaController = TextEditingController(text: existing?.nameTa ?? '');
    final sciNameController = TextEditingController(text: existing?.scientificName ?? '');
    final slugController = TextEditingController(text: existing?.slug ?? '');
    String selectedCategory = existing?.category ?? 'Root Vegetable';
    int selectedPlantPartId = 1;
    String selectedSafety = existing?.foodSafetyStatus ?? 'safe_edible';
    bool isAiSupported = existing?.isAiSupported ?? false;

    showDialog(
      context: context,
      builder: (ctx) {
        return StatefulBuilder(
          builder: (context, setModalState) {
            return AlertDialog(
              title: Text(isEdit ? 'Edit Botanical Record' : 'Add Botanical Record'),
              content: SingleChildScrollView(
                child: SizedBox(
                  width: 500,
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      TextField(
                        controller: nameEnController,
                        decoration: const InputDecoration(labelText: 'English Name *', hintText: 'e.g. Turnip'),
                        onChanged: (val) {
                          if (!isEdit && slugController.text.isEmpty) {
                            slugController.text = val.toLowerCase().replaceAll(' ', '-').replaceAll(RegExp(r'[^a-z0-9\-]'), '');
                          }
                        },
                      ),
                      const SizedBox(height: 10),
                      TextField(
                        controller: nameTaController,
                        decoration: const InputDecoration(labelText: 'Tamil Name (தமிழ்) *', hintText: 'e.g. நூல் கோல்'),
                      ),
                      const SizedBox(height: 10),
                      TextField(
                        controller: sciNameController,
                        decoration: const InputDecoration(labelText: 'Botanical / Scientific Name *', hintText: 'e.g. Brassica rapa'),
                      ),
                      const SizedBox(height: 10),
                      if (!isEdit) ...[
                        TextField(
                          controller: slugController,
                          decoration: const InputDecoration(labelText: 'Unique URL Slug *', hintText: 'e.g. turnip'),
                        ),
                        const SizedBox(height: 10),
                      ],
                      DropdownButtonFormField<String>(
                        initialValue: selectedCategory,
                        decoration: const InputDecoration(labelText: 'Category'),
                        items: const [
                          DropdownMenuItem(value: 'Root Vegetable', child: Text('Root Vegetable')),
                          DropdownMenuItem(value: 'Gourds & Cucurbits', child: Text('Gourds & Cucurbits')),
                          DropdownMenuItem(value: 'Solanaceous & Common Roots', child: Text('Solanaceous & Common Roots')),
                          DropdownMenuItem(value: 'Bulbs & Aromatics', child: Text('Bulbs & Aromatics')),
                          DropdownMenuItem(value: 'Plant Outer Layer', child: Text('Plant Outer Layer')),
                          DropdownMenuItem(value: 'Legumes & Pods', child: Text('Legumes & Pods')),
                        ],
                        onChanged: (val) {
                          if (val != null) setModalState(() => selectedCategory = val);
                        },
                      ),
                      const SizedBox(height: 10),
                      DropdownButtonFormField<int>(
                        initialValue: selectedPlantPartId,
                        decoration: const InputDecoration(labelText: 'Default Plant Part'),
                        items: const [
                          DropdownMenuItem(value: 1, child: Text('Peel (தோல்)')),
                          DropdownMenuItem(value: 2, child: Text('Thin Skin (மெல்லிய தோல்)')),
                          DropdownMenuItem(value: 3, child: Text('Thick Rind (தடித்த ஓடு)')),
                          DropdownMenuItem(value: 4, child: Text('Outer Leaves (வெளிப்புற இலைகள்)')),
                          DropdownMenuItem(value: 5, child: Text('Pod Shell (நெற்று உறை)')),
                          DropdownMenuItem(value: 6, child: Text('Stem Layer (தண்டு அடுக்கு)')),
                          DropdownMenuItem(value: 7, child: Text('Husk / Sheath (உமி / உறை)')),
                        ],
                        onChanged: (val) {
                          if (val != null) setModalState(() => selectedPlantPartId = val);
                        },
                      ),
                      const SizedBox(height: 10),
                      DropdownButtonFormField<String>(
                        initialValue: selectedSafety,
                        decoration: const InputDecoration(labelText: 'Food Safety Classification'),
                        items: const [
                          DropdownMenuItem(value: 'safe_edible', child: Text('Safe & Edible')),
                          DropdownMenuItem(value: 'conditional_cooking_required', child: Text('Conditional (Cook First)')),
                          DropdownMenuItem(value: 'hazardous_raw', child: Text('Hazardous Raw')),
                          DropdownMenuItem(value: 'inedible_valorize_only', child: Text('Inedible (Valorize Only)')),
                        ],
                        onChanged: (val) {
                          if (val != null) setModalState(() => selectedSafety = val);
                        },
                      ),
                      const SizedBox(height: 10),
                      SwitchListTile(
                        contentPadding: EdgeInsets.zero,
                        title: const Text('AI Camera Classifier Supported', style: TextStyle(fontSize: 14)),
                        subtitle: const Text('Trained in MobileNetV3 deep learning weights', style: TextStyle(fontSize: 11)),
                        value: isAiSupported,
                        activeThumbColor: AppTheme.primaryGreen,
                        onChanged: (val) => setModalState(() => isAiSupported = val),
                      ),
                    ],
                  ),
                ),
              ),
              actions: [
                TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Cancel')),
                ElevatedButton(
                  style: ElevatedButton.styleFrom(backgroundColor: AppTheme.primaryGreen, foregroundColor: Colors.white),
                  onPressed: () async {
                    final nameEn = nameEnController.text.trim();
                    final nameTa = nameTaController.text.trim();
                    final sciName = sciNameController.text.trim();
                    final slug = slugController.text.trim().toLowerCase();

                    if (nameEn.isEmpty || nameTa.isEmpty || sciName.isEmpty) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(content: Text('Please fill all required fields.')),
                      );
                      return;
                    }

                    final navigator = Navigator.of(ctx);
                    final messenger = ScaffoldMessenger.of(context);

                    try {
                      final repo = ref.read(vegetablesRepositoryProvider);
                      if (isEdit) {
                        await repo.updateVegetable(existing.id, {
                          'name_en': nameEn,
                          'name_ta': nameTa,
                          'scientific_name': sciName,
                          'category': selectedCategory,
                          'plant_part_id': selectedPlantPartId,
                          'food_safety_status': selectedSafety,
                          'is_ai_supported': isAiSupported,
                        });
                      } else {
                        await repo.createVegetable({
                          'slug': slug.isEmpty ? nameEn.toLowerCase().replaceAll(' ', '-') : slug,
                          'name_en': nameEn,
                          'name_ta': nameTa,
                          'scientific_name': sciName,
                          'category': selectedCategory,
                          'plant_part_id': selectedPlantPartId,
                          'food_safety_status': selectedSafety,
                          'is_ai_supported': isAiSupported,
                          'nutrient_data_status': 'incomplete',
                        });
                      }

                      ref.invalidate(vegetablesListAsyncProvider);
                      navigator.pop();
                      messenger.showSnackBar(
                        SnackBar(
                          content: Text(isEdit ? 'Updated $nameEn successfully' : 'Created $nameEn successfully'),
                          backgroundColor: AppTheme.primaryGreen,
                        ),
                      );
                    } catch (e) {
                      messenger.showSnackBar(
                        SnackBar(content: Text('Operation failed: $e'), backgroundColor: Colors.red),
                      );
                    }
                  },
                  child: Text(isEdit ? 'Update Record' : 'Save Record'),
                ),
              ],
            );
          },
        );
      },
    );
  }

  void _confirmDeleteVegetable(VegetableItem veg) {
    showDialog(
      context: context,
      builder: (ctx) {
        return AlertDialog(
          title: const Text('Archive Botanical Record'),
          content: Text('Are you sure you want to deactivate "${veg.nameEn}" (${veg.scientificName}) from the active catalogue?'),
          actions: [
            TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Cancel')),
            ElevatedButton(
              style: ElevatedButton.styleFrom(backgroundColor: Colors.red, foregroundColor: Colors.white),
              onPressed: () async {
                final navigator = Navigator.of(ctx);
                final messenger = ScaffoldMessenger.of(context);
                try {
                  final repo = ref.read(vegetablesRepositoryProvider);
                  await repo.deleteVegetable(veg.id);
                  ref.invalidate(vegetablesListAsyncProvider);
                  navigator.pop();
                  messenger.showSnackBar(
                    SnackBar(content: Text('Archived "${veg.nameEn}" successfully.'), backgroundColor: Colors.orange.shade800),
                  );
                } catch (e) {
                  messenger.showSnackBar(
                    SnackBar(content: Text('Archive failed: $e'), backgroundColor: Colors.red),
                  );
                }
              },
              child: const Text('Archive'),
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final lang = ref.watch(localeProvider);
    final isTamil = lang == AppLanguage.ta;
    final asyncVegs = ref.watch(vegetablesListAsyncProvider);
    final vegs = asyncVegs.value ?? [];

    final displayedVegs = vegs.where((v) {
      if (_searchQuery.isEmpty) return true;
      final q = _searchQuery.toLowerCase();
      return v.nameEn.toLowerCase().contains(q) ||
          v.nameTa.toLowerCase().contains(q) ||
          v.scientificName.toLowerCase().contains(q) ||
          v.category.toLowerCase().contains(q);
    }).toList();

    return Scaffold(
      appBar: AppBar(
        backgroundColor: const Color(0xFF263238),
        title: Text(isTamil ? 'காய்கறி தரவுத்தளம் நிர்வாகம்' : 'Vegetable Master Management'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => context.go('/admin-dashboard'),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            tooltip: 'Refresh Catalogue',
            onPressed: () => ref.invalidate(vegetablesListAsyncProvider),
          ),
          IconButton(
            icon: const Icon(Icons.add_circle_outline, color: Colors.lightGreenAccent),
            tooltip: 'Add Record',
            onPressed: () => _showAddEditVegetableDialog(),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        backgroundColor: AppTheme.primaryGreen,
        icon: const Icon(Icons.add, color: Colors.white),
        label: Text(isTamil ? 'புதிய பதிவு சேர்க்க' : 'Add Botanical Record', style: const TextStyle(color: Colors.white)),
        onPressed: () => _showAddEditVegetableDialog(),
      ),
      body: Column(
        children: [
          // Filter / Search bar
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            color: Colors.white,
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    decoration: InputDecoration(
                      hintText: isTamil ? 'காய்கறி பதிவுகளை தேடுங்கள்...' : 'Search master records by name or botanical family...',
                      prefixIcon: const Icon(Icons.search, size: 20),
                      isDense: true,
                      contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                    ),
                    onChanged: (val) => setState(() => _searchQuery = val.trim()),
                  ),
                ),
                const SizedBox(width: 12),
                Chip(
                  label: Text('${displayedVegs.length} Records'),
                  backgroundColor: AppTheme.softMint,
                  labelStyle: const TextStyle(color: AppTheme.primaryDark, fontWeight: FontWeight.bold, fontSize: 12),
                ),
              ],
            ),
          ),
          const Divider(height: 1),

          // Records List
          Expanded(
            child: asyncVegs.isLoading
                ? const Center(child: CircularProgressIndicator())
                : displayedVegs.isEmpty
                    ? Center(
                        child: Column(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Icon(Icons.eco_outlined, size: 48, color: Colors.grey.shade400),
                            const SizedBox(height: 8),
                            const Text('No records found', style: TextStyle(fontWeight: FontWeight.bold)),
                          ],
                        ),
                      )
                    : ListView.builder(
                        padding: const EdgeInsets.all(16.0),
                        itemCount: displayedVegs.length,
                        itemBuilder: (context, index) {
                          final veg = displayedVegs[index];
                          return Card(
                            elevation: 1,
                            margin: const EdgeInsets.only(bottom: 10),
                            child: ListTile(
                              leading: CircleAvatar(
                                backgroundColor: veg.isAiSupported ? AppTheme.softMint : Colors.grey.shade100,
                                child: Icon(
                                  veg.isAiSupported ? Icons.auto_awesome : Icons.eco,
                                  color: veg.isAiSupported ? AppTheme.primaryGreen : Colors.grey.shade600,
                                  size: 20,
                                ),
                              ),
                              title: Row(
                                children: [
                                  Text(veg.nameEn, style: const TextStyle(fontWeight: FontWeight.bold)),
                                  const SizedBox(width: 8),
                                  Text('(${veg.nameTa})', style: TextStyle(color: Colors.grey.shade700, fontSize: 13)),
                                  if (veg.isAiSupported) ...[
                                    const SizedBox(width: 8),
                                    Container(
                                      padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 1),
                                      decoration: BoxDecoration(color: Colors.green.shade100, borderRadius: BorderRadius.circular(6)),
                                      child: const Text('AI Class', style: TextStyle(fontSize: 10, fontWeight: FontWeight.bold, color: AppTheme.primaryDark)),
                                    ),
                                  ],
                                ],
                              ),
                              subtitle: Text(
                                '${veg.scientificName} • ${veg.category} • Part: ${veg.plantPart} • Status: ${veg.foodSafetyStatus}',
                                style: TextStyle(fontSize: 12, color: Colors.grey.shade600),
                              ),
                              trailing: Row(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  IconButton(
                                    icon: const Icon(Icons.edit, size: 20, color: Colors.blueGrey),
                                    tooltip: 'Edit Record',
                                    onPressed: () => _showAddEditVegetableDialog(existing: veg),
                                  ),
                                  IconButton(
                                    icon: const Icon(Icons.delete_outline, size: 20, color: Colors.redAccent),
                                    tooltip: 'Archive Record',
                                    onPressed: () => _confirmDeleteVegetable(veg),
                                  ),
                                ],
                              ),
                            ),
                          );
                        },
                      ),
          ),
        ],
      ),
    );
  }
}
