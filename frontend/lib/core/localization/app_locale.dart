import 'package:flutter_riverpod/legacy.dart';

enum AppLanguage { en, ta }

class LocaleNotifier extends StateNotifier<AppLanguage> {
  LocaleNotifier() : super(AppLanguage.en);

  void toggleLanguage() {
    state = state == AppLanguage.en ? AppLanguage.ta : AppLanguage.en;
  }

  void setLanguage(AppLanguage lang) {
    state = lang;
  }
}

final localeProvider = StateNotifierProvider<LocaleNotifier, AppLanguage>((ref) {
  return LocaleNotifier();
});

class AppStrings {
  static const Map<String, Map<AppLanguage, String>> _strings = {
    // Navigation & General
    'app_name': {
      AppLanguage.en: 'SMART PEEL AI',
      AppLanguage.ta: 'ஸ்மார்ட் பீல் ஏஐ',
    },
    'tagline': {
      AppLanguage.en: 'Intelligent Vegetable Peel Nutrient Identification & Valorization',
      AppLanguage.ta: 'காய்கறி தோல் ஊட்டச்சத்து கண்டறிதல் & மறுபயன்பாட்டு முறை',
    },
    'home': {
      AppLanguage.en: 'Home',
      AppLanguage.ta: 'முகப்பு',
    },
    'scan': {
      AppLanguage.en: 'Scan Peel',
      AppLanguage.ta: 'தோல் ஸ்கேன்',
    },
    'catalogue': {
      AppLanguage.en: 'Vegetables',
      AppLanguage.ta: 'காய்கறி பட்டியல்',
    },
    'history': {
      AppLanguage.en: 'History',
      AppLanguage.ta: 'வரலாறு',
    },
    'profile': {
      AppLanguage.en: 'Profile',
      AppLanguage.ta: 'சுயவிவரம்',
    },
    'settings': {
      AppLanguage.en: 'Settings',
      AppLanguage.ta: 'அமைப்புகள்',
    },
    'admin': {
      AppLanguage.en: 'Admin Console',
      AppLanguage.ta: 'நிர்வாகப் பகுதி',
    },
    // Actions
    'capture_photo': {
      AppLanguage.en: 'Capture with Camera',
      AppLanguage.ta: 'கேமரா மூலம் புகைப்படம் எடுக்கவும்',
    },
    'upload_gallery': {
      AppLanguage.en: 'Upload from Gallery',
      AppLanguage.ta: 'கேலரியில் இருந்து பதிவேற்றவும்',
    },
    'confirm_prediction': {
      AppLanguage.en: 'Confirm Vegetable',
      AppLanguage.ta: 'காய்கறியை உறுதிப்படுத்துக',
    },
    'change_selection': {
      AppLanguage.en: 'Change / Select Manually',
      AppLanguage.ta: 'கையேடாக மாற்றவும்',
    },
    'view_nutrients': {
      AppLanguage.en: 'View Nutrient Profile',
      AppLanguage.ta: 'ஊட்டச்சத்து விவரங்களை பார்க்க',
    },
    'calculate_estimate': {
      AppLanguage.en: 'Estimate by Weight',
      AppLanguage.ta: 'எடை வாரியாக கணக்கிடுக',
    },
    'safety_warnings': {
      AppLanguage.en: 'Food Safety Alerts',
      AppLanguage.ta: 'உணவு பாதுகாப்பு எச்சரிக்கைகள்',
    },
    'reuse_methods': {
      AppLanguage.en: 'Valorization & Reuse',
      AppLanguage.ta: 'மறுபயன்பாட்டு முறைகள்',
    },
    'download_report': {
      AppLanguage.en: 'Download PDF Report',
      AppLanguage.ta: 'பிடிஎஃப் அறிக்கையைப் பதிவிறக்கு',
    },
    // Scientific Disclaimers
    'scientific_disclaimer': {
      AppLanguage.en: 'Estimated nutrients are based on published scientific composition studies, not direct chemical measurement of this specific sample.',
      AppLanguage.ta: 'மதிப்பிடப்பட்ட ஊட்டச்சத்துக்கள் ஆய்வுக் குறிப்புகளின் அடிப்படையில் அமைந்தவை; குறிப்பிட்ட மாதிரியின் நேரடி வேதியியல் அளவீடு அல்ல.',
    },
    'safety_disclaimer': {
      AppLanguage.en: 'Camera visual appearance alone cannot guarantee microbiological safety or absence of chemical residues.',
      AppLanguage.ta: 'கேமரா தோற்றம் மட்டுமே நுண்ணுயிர் பாதுகாப்பு அல்லது வேதியியல் எச்சமின்மையை உறுதிசெய்யாது.',
    },
  };

  static String get(String key, AppLanguage lang) {
    if (_strings.containsKey(key)) {
      return _strings[key]![lang] ?? key;
    }
    return key;
  }
}
