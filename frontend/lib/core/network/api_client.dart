import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';

class ApiClient {
  static final ApiClient _instance = ApiClient._internal();
  factory ApiClient() => _instance;

  late final Dio dio;

  ApiClient._internal() {
    const envUrl = String.fromEnvironment('API_BASE_URL');
    String baseUrl = 'http://127.0.0.1:8000';

    if (envUrl.isNotEmpty) {
      baseUrl = envUrl.endsWith('/api/v1') ? envUrl.replaceAll('/api/v1', '') : envUrl;
    } else if (kIsWeb) {
      // In web mode, dynamically use the current host so mobile phones on local Wi-Fi can reach the API
      final host = Uri.base.host;
      if (host.isNotEmpty && host != '0.0.0.0') {
        baseUrl = 'http://$host:8000';
      }
    } else if (defaultTargetPlatform == TargetPlatform.android) {
      // Android Emulator loopback alias to host machine
      baseUrl = 'http://10.0.2.2:8000';
    }

    dio = Dio(
      BaseOptions(
        baseUrl: baseUrl,
        connectTimeout: const Duration(seconds: 15),
        receiveTimeout: const Duration(seconds: 15),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      ),
    );

    dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) {
          // Normalize paths so all requests route cleanly through /api/v1
          if (!options.path.startsWith('/api/v1') && !options.path.startsWith('http')) {
            final cleanPath = options.path.startsWith('/') ? options.path : '/${options.path}';
            options.path = '/api/v1$cleanPath';
          }
          debugPrint('[API REQ] ${options.method} ${options.uri}');
          return handler.next(options);
        },
        onResponse: (response, handler) {
          debugPrint('[API RES] ${response.statusCode} from ${response.requestOptions.uri}');
          return handler.next(response);
        },
        onError: (DioException error, handler) {
          debugPrint('[API ERR] ${error.type} for ${error.requestOptions.uri}: ${error.message}');
          return handler.next(error);
        },
      ),
    );
  }

  void updateBaseUrl(String newUrl) {
    dio.options.baseUrl = newUrl;
  }
}
