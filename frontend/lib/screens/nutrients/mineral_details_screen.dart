import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/localization/app_locale.dart';
import '../../core/theme/app_theme.dart';

class MineralDetailsScreen extends ConsumerWidget {
  const MineralDetailsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final lang = ref.watch(localeProvider);
    final isTamil = lang == AppLanguage.ta;

    final minerals = [
      {'name': 'Potassium (K)', 'name_ta': 'பொட்டாசியம்', 'role': 'Primary intracellular electrolyte regulating osmotic equilibrium, vascular smooth muscle tone, and cardiac rhythm.', 'role_ta': 'இரத்த அழுத்தம், இதய துடிப்பு மற்றும் செல் நீர் சமநிலையை கட்டுப்படுத்துகிறது.', 'peel': 'Very high in potato (413mg/100g) and carrot peels.'},
      {'name': 'Calcium (Ca)', 'name_ta': 'கால்சியம்', 'role': 'Inorganic hydroxyapatite bone crystal formation, muscle troponin activation, and neural exocytosis.', 'role_ta': 'எலும்பு மற்றும் பற்களின் உறுதி, தசை இயக்கம் மற்றும் நரம்பு சிக்னல்களுக்கு முக்கியமானது.', 'peel': 'Found tightly bound to pectin polysaccharides in carrot and turnip outer layers.'},
      {'name': 'Iron (Fe)', 'name_ta': 'இரும்புச்சத்து', 'role': 'Haem prosthetic group in haemoglobin for oxygen binding, cytochromes for mitochondrial electron transport.', 'role_ta': 'ஹீமோகுளோபின் மற்றும் இரத்தத்தில் ஆக்ஸிஜன் பரிமாற்றத்திற்கு இன்றியமையாதது.', 'peel': 'Substantial in potato skins (1.8mg/100g) and beetroot outer layer.'},
      {'name': 'Magnesium (Mg)', 'name_ta': 'மெக்னீசியம்', 'role': 'Chelating cation for ATP complexes, required by more than 300 metabolic and kinase enzymes.', 'role_ta': '300-க்கும் மேற்பட்ட என்சைம்களுக்கு அவசியமான மூலப்பொருள்.', 'peel': 'Central atom in chlorophyll; abundant in dark green cucumber and gourd peels.'},
      {'name': 'Zinc (Zn) & Manganese (Mn)', 'name_ta': 'துத்தநாகம் & மாங்கனீசு', 'role': 'Catalytic sites for superoxide dismutase (SOD) defending against mitochondrial reactive oxygen species.', 'role_ta': 'செல்லுலார் நோய் எதிர்ப்பு சக்தி மற்றும் ஆக்ஸிஜனேற்ற என்சைம்களுக்கு உதவுகிறது.', 'peel': 'Trace concentrations in root vegetable epidermis.'},
    ];

    return Scaffold(
      appBar: AppBar(
        title: Text(isTamil ? 'தாதுக்கள் வழிகாட்டி' : 'Mineral & Electrolyte Guide'),
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
                ...minerals.map((min) => Card(
                  child: Padding(
                    padding: const EdgeInsets.all(18.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            CircleAvatar(
                              radius: 16,
                              backgroundColor: Colors.blue.shade100,
                              child: Icon(Icons.grain, color: Colors.blue.shade800, size: 18),
                            ),
                            const SizedBox(width: 10),
                            Text(
                              isTamil ? min['name_ta']! : min['name']!,
                              style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AppTheme.primaryDark),
                            ),
                          ],
                        ),
                        const SizedBox(height: 10),
                        Text(
                          isTamil ? min['role_ta']! : min['role']!,
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
                            'Peel occurrence: ${min["peel"]}',
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
