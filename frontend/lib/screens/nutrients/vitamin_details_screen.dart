import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/localization/app_locale.dart';
import '../../core/theme/app_theme.dart';

class VitaminDetailsScreen extends ConsumerWidget {
  const VitaminDetailsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final lang = ref.watch(localeProvider);
    final isTamil = lang == AppLanguage.ta;

    final vitaminGuide = [
      {'name': 'Vitamin A & Carotenoids', 'name_ta': 'வைட்டமின் ஏ & கரோட்டினாய்டுகள்', 'role_en': 'Epithelial tissue integrity, retinal rhodopsin synthesis, and mucosal cellular immunity.', 'role_ta': 'கண் பார்வை நலம், சரும பாதுகாப்பு மற்றும் நோய் எதிர்ப்பு சக்தி.', 'peel_context': 'Highly concentrated in carrot, pumpkin, and sweet potato peels.'},
      {'name': 'Vitamin B-Complex (B1, B2, B3, B5, B6, B9)', 'name_ta': 'வைட்டமின் பி காம்ப்ளக்ஸ் (பி1-பி9)', 'role_en': 'Coenzymatic facilitators in ATP energy generation, transamination, and nucleic acid synthesis.', 'role_ta': 'ஆற்றல் உற்பத்தி, இரத்த சிவப்பணுக்கள் மற்றும் நரம்பு மண்டல செயல்பாடு.', 'peel_context': 'Found in metabolically active sub-epidermal layers of root and tuber vegetables.'},
      {'name': 'Vitamin C (Ascorbic Acid)', 'name_ta': 'வைட்டமின் சி (அஸ்கார்பிக் அமிலம்)', 'role_en': 'Potent water-soluble free radical scavenger, proline hydroxylation for collagen biosynthesis.', 'role_ta': 'கொலாஜன் உற்பத்தி, திசு வளர்ச்சி மற்றும் ஆக்ஸிஜனேற்ற தடுப்பு.', 'peel_context': 'Concentrated in potato, tomato, and capsicum peels; heat-sensitive during high cooking temperatures.'},
      {'name': 'Vitamin E (Tocopherols)', 'name_ta': 'வைட்டமின் ஈ (டோகோபெரோல்)', 'role_en': 'Lipophilic antioxidant that breaks peroxyl chain reactions in cellular membranes.', 'role_ta': 'செல் சவ்வுகளை சேதத்திலிருந்து பாதுகாக்கும் கொழுப்பில் கரையும் வைட்டமின்.', 'peel_context': 'Present in oily cuticular waxes of cucumber and squash rinds.'},
      {'name': 'Vitamin K1 (Phylloquinone)', 'name_ta': 'வைட்டமின் கே1 (ஃபில்லோகுவினோன்)', 'role_en': 'Essential cofactor in gamma-glutamyl carboxylase for blood coagulation factors and osteocalcin.', 'role_ta': 'இரத்தம் உறைதல் மற்றும் எலும்பு வளர்ச்சிக்கு தேவையான வைட்டமின்.', 'peel_context': 'Dense in chlorophyll-rich outer green rinds such as cucumber, zucchini, and cabbage outer leaves.'},
    ];

    return Scaffold(
      appBar: AppBar(
        title: Text(isTamil ? 'வைட்டமின் வழிகாட்டி' : 'Vitamin Reference Guide'),
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
                // Scientific Disclaimer Card
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: Colors.amber.shade50,
                    borderRadius: BorderRadius.circular(14),
                    border: Border.all(color: Colors.amber.shade200),
                  ),
                  child: Row(
                    children: [
                      const Icon(Icons.menu_book, color: Colors.amber),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Text(
                          isTamil
                              ? 'அறிவியல் குறிப்பு: வைட்டமின்கள் இருப்பது மட்டுமே ஒரு குறிப்பிட்ட தோலை உண்பதால் நோய்கள் குணமாகும் என்பதற்கான சான்றாகாது. சமச்சீரான உணவு முறையே முக்கியமானது.'
                              : 'Scientific Notice: Nutrient presence does not claim medicinal curing properties. Educational composition reference only.',
                          style: TextStyle(fontSize: 12, color: Colors.brown.shade800, height: 1.3),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 20),
                ...vitaminGuide.map((vit) => Card(
                  child: Padding(
                    padding: const EdgeInsets.all(18.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            CircleAvatar(
                              radius: 16,
                              backgroundColor: Colors.orange.shade100,
                              child: Icon(Icons.shield, color: Colors.orange.shade800, size: 18),
                            ),
                            const SizedBox(width: 10),
                            Text(
                              isTamil ? vit['name_ta']! : vit['name']!,
                              style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AppTheme.primaryDark),
                            ),
                          ],
                        ),
                        const SizedBox(height: 10),
                        Text(
                          isTamil ? vit['role_ta']! : vit['role_en']!,
                          style: TextStyle(fontSize: 13, color: Colors.grey.shade800, height: 1.3),
                        ),
                        const SizedBox(height: 8),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                          decoration: BoxDecoration(
                            color: AppTheme.surfaceMuted,
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: Text(
                            'Peel occurrence: ${vit["peel_context"]}',
                            style: TextStyle(fontSize: 11, fontStyle: FontStyle.italic, color: Colors.grey.shade700),
                          ),
                        ),
                      ],
                    ),
                  ),
                )),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
