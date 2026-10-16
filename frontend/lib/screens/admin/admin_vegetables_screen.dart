import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/localization/app_locale.dart';
import '../../core/theme/app_theme.dart';
import '../../providers/app_providers.dart';

class AdminVegetablesScreen extends ConsumerStatefulWidget {
  const AdminVegetablesScreen({super.key});

  @override
  ConsumerState<AdminVegetablesScreen> createState() => _AdminVegetablesScreenState();
}

class _AdminVegetablesScreenState extends ConsumerState<AdminVegetablesScreen> {
  void _showAddVegetableDialog() {
    final nameEnController = TextEditingController();
    final nameTaController = TextEditingController();
    final sciNameController = TextEditingController();
    final categoryController = TextEditingController(text: 'Root Vegetable');

    showDialog(
      context: context,
      builder: (ctx) {
        return AlertDialog(
          title: const Text('Add Botanical Catalogue Record'),
          content: SingleChildScrollView(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                TextField(controller: nameEnController, decoration: const InputDecoration(labelText: 'English Name (e.g. Turnip)')),
                const SizedBox(height: 10),
                TextField(controller: nameTaController, decoration: const InputDecoration(labelText: 'Tamil Name (e.g. நூல் கோல்)')),
                const SizedBox(height: 10),
                TextField(controller: sciNameController, decoration: const InputDecoration(labelText: 'Scientific Name (e.g. Brassica rapa)')),
                const SizedBox(height: 10),
                TextField(controller: categoryController, decoration: const InputDecoration(labelText: 'Category')),
              ],
            ),
          ),
          actions: [
            TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Cancel')),
            ElevatedButton(
              onPressed: () {
                Navigator.pop(ctx);
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('Vegetable "${nameEnController.text}" registered successfully!'), backgroundColor: AppTheme.primaryGreen),
                );
              },
              child: const Text('Save Record'),
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
    final allVegs = ref.watch(catalogueProvider);

    return Scaffold(
      appBar: AppBar(
        backgroundColor: const Color(0xFF263238),
        title: Text(isTamil ? 'காய்கறி பதிவுகள் மேலாண்மை' : 'Vegetable Master Management'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => context.go('/admin-dashboard'),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.add_circle_outline, color: Colors.lightGreenAccent),
            tooltip: 'Add Vegetable',
            onPressed: _showAddVegetableDialog,
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        backgroundColor: AppTheme.primaryGreen,
        icon: const Icon(Icons.add, color: Colors.white),
        label: Text(isTamil ? 'புதிய காய்கறி சேர்க்க' : 'Add New Plant Record', style: const TextStyle(color: Colors.white)),
        onPressed: _showAddVegetableDialog,
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(16.0),
        itemCount: allVegs.length,
        itemBuilder: (context, index) {
          final veg = allVegs[index];
          return Card(
            child: ListTile(
              leading: CircleAvatar(
                backgroundColor: veg.isAiSupported ? Colors.green.shade100 : Colors.grey.shade200,
                child: Icon(Icons.eco, color: veg.isAiSupported ? AppTheme.primaryGreen : Colors.grey),
              ),
              title: Text('${veg.nameEn} / ${veg.nameTa}', style: const TextStyle(fontWeight: FontWeight.bold)),
              subtitle: Text('${veg.scientificName} • ${veg.category} • Part: ${veg.plantPart}'),
              trailing: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  IconButton(
                    icon: const Icon(Icons.edit, size: 20, color: Colors.blueGrey),
                    onPressed: () {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(content: Text('Editing record for ${veg.nameEn}')),
                      );
                    },
                  ),
                  IconButton(
                    icon: const Icon(Icons.delete_outline, size: 20, color: Colors.red),
                    onPressed: () {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(content: Text('Archived ${veg.nameEn}')),
                      );
                    },
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
