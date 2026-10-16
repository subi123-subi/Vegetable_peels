import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/localization/app_locale.dart';
import '../../core/theme/app_theme.dart';

class AntioxidantDetailsScreen extends ConsumerWidget {
  const AntioxidantDetailsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final lang = ref.watch(localeProvider);
    final isTamil = lang == AppLanguage.ta;

    final bioactives = [
      {
        'title': 'Dietary Fibre (Soluble & Insoluble)',
        'title_ta': 'உணவு நார்ச்சத்து (கரையும் & கரையாத)',
        'desc': 'Cellulose, hemicellulose, lignin, and pectin polysaccharides that resist human upper-GI digestion. Fermented by colonic microbiota into beneficial short-chain fatty acids (acetate, propionate, butyrate).',
        'desc_ta': 'செரிமானத்தை சீராக்கி, நல்ல பாக்டீரியாக்களை வளர்க்கும் இயற்கை நார்ச்சத்து.',
        'examples': 'All vegetable peels are significantly higher in dietary fibre (2-5x) than inner pulp.',
      },
      {
        'title': 'Polyphenols & Flavonoids (Quercetin, Nasunin)',
        'title_ta': 'பினாலிக் சேர்மங்கள் & ஃபிளவனாய்டுகள்',
        'desc': 'Secondary plant metabolites synthesized in the epidermis to shield plant tissues from UV radiation and pathogens. Function as radical-scavenging antioxidants.',
        'desc_ta': 'சூரிய ஒளி மற்றும் பூச்சிகளிடமிருந்து தாவரங்களை காக்கும் இயற்கை பாதுகாப்பு மூலக்கூறுகள்.',
        'examples': 'Quercetin is intensely concentrated in dry onion skins; Nasunin anthocyanin in eggplant skins.',
      },
      {
        'title': 'Betalains (Betacyanins & Betaxanthins)',
        'title_ta': 'பீட்டலைன்கள் (இயற்கை நிறமிகள்)',
        'desc': 'Tyrosine-derived nitrogenous water-soluble pigments exhibiting high electron-donation capacity and free radical neutralization.',
        'desc_ta': 'பீட்ரூட்டில் காணப்படும் தீவிர சிவப்பு நிற இயற்கை ஆக்ஸிஜனேற்ற நிறமி.',
        'examples': 'Betanin is concentrated predominantly in the outer 1-2mm peel layer of Beta vulgaris.',
      },
      {
        'title': 'Carotenoids (Lycopene, Lutein, Beta-Carotene)',
        'title_ta': 'கரோட்டினாய்டுகள் (லைகோபீன், லுடீன்)',
        'desc': 'Tetraterpenoid lipophilic pigments acting as optical photoprotectants and quenchers of singlet oxygen.',
        'desc_ta': 'கண் பார்வை மற்றும் செல்களுக்கு பாதுகாப்பு தரும் இயற்கை நிறமிகள்.',
        'examples': 'Concentrated in tomato skins (lycopene), carrot peels (beta-carotene), and pumpkin rinds.',
      },
    ];

    return Scaffold(
      appBar: AppBar(
        title: Text(isTamil ? 'நார்ச்சத்து & ஆன்டி-ஆக்ஸிடன்ட்கள்' : 'Dietary Fibre & Phytochemicals'),
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
                ...bioactives.map((item) => Card(
                  child: Padding(
                    padding: const EdgeInsets.all(18.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            CircleAvatar(
                              radius: 16,
                              backgroundColor: AppTheme.softMint,
                              child: const Icon(Icons.spa, color: AppTheme.primaryGreen, size: 18),
                            ),
                            const SizedBox(width: 10),
                            Expanded(
                              child: Text(
                                isTamil ? item['title_ta']! : item['title']!,
                                style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AppTheme.primaryDark),
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 10),
                        Text(
                          isTamil ? item['desc_ta']! : item['desc']!,
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
                            'Distribution: ${item["examples"]}',
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
