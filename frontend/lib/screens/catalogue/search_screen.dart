import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/localization/app_locale.dart';
import '../../core/theme/app_theme.dart';
import '../../providers/app_providers.dart';

class SearchScreen extends ConsumerStatefulWidget {
  const SearchScreen({super.key});

  @override
  ConsumerState<SearchScreen> createState() => _SearchScreenState();
}

class _SearchScreenState extends ConsumerState<SearchScreen> {
  final _searchController = TextEditingController();
  String _query = '';

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final lang = ref.watch(localeProvider);
    final isTamil = lang == AppLanguage.ta;
    final allVegs = ref.watch(catalogueProvider);

    final results = allVegs.where((v) {
      if (_query.isEmpty) return true;
      final q = _query.toLowerCase();
      return v.nameEn.toLowerCase().contains(q) ||
          v.nameTa.toLowerCase().contains(q) ||
          v.scientificName.toLowerCase().contains(q) ||
          v.category.toLowerCase().contains(q);
    }).toList();

    return Scaffold(
      appBar: AppBar(
        title: TextField(
          controller: _searchController,
          autofocus: true,
          style: const TextStyle(color: Colors.white, fontSize: 16),
          decoration: InputDecoration(
            hintText: isTamil ? 'காய்கறி பெயர் அல்லது தாவர பெயர் தேடவும்...' : 'Search English, Tamil or Scientific Name...',
            hintStyle: TextStyle(color: Colors.white.withValues(alpha: 0.7)),
            border: InputBorder.none,
            enabledBorder: InputBorder.none,
            focusedBorder: InputBorder.none,
            filled: false,
          ),
          onChanged: (val) {
            setState(() {
              _query = val;
            });
          },
        ),
        actions: [
          if (_query.isNotEmpty)
            IconButton(
              icon: const Icon(Icons.clear, color: Colors.white),
              onPressed: () {
                _searchController.clear();
                setState(() => _query = '');
              },
            ),
        ],
      ),
      body: results.isEmpty
          ? Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.search_off, size: 64, color: Colors.grey),
                  const SizedBox(height: 12),
                  Text(
                    isTamil ? 'முடிவுகள் எதுவும் கிடைக்கவில்லை' : 'No matching vegetable found.',
                    style: TextStyle(color: Colors.grey.shade600, fontSize: 16),
                  ),
                ],
              ),
            )
          : ListView.builder(
              padding: const EdgeInsets.all(16.0),
              itemCount: results.length,
              itemBuilder: (context, index) {
                final veg = results[index];
                return Card(
                  child: ListTile(
                    leading: CircleAvatar(
                      backgroundColor: AppTheme.softMint,
                      child: const Icon(Icons.eco, color: AppTheme.primaryGreen),
                    ),
                    title: Text(
                      veg.displayName(isTamil),
                      style: const TextStyle(fontWeight: FontWeight.bold),
                    ),
                    subtitle: Text('${veg.scientificName} • ${veg.category}'),
                    trailing: const Icon(Icons.chevron_right),
                    onTap: () {
                      ref.read(selectedVegetableProvider.notifier).select(veg);
                      context.go('/nutrients');
                    },
                  ),
                );
              },
            ),
    );
  }
}
