import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';

class ApiClient {
  static final ApiClient _instance = ApiClient._internal();
  factory ApiClient() => _instance;

  late final Dio dio;

  ApiClient._internal() {
    const envUrl = String.fromEnvironment('API_BASE_URL');
    String baseUrl = 'http://127.0.0.1:8000/api/v1';

    if (envUrl.isNotEmpty) {
      baseUrl = envUrl;
    } else if (kIsWeb) {
      // In web mode, dynamically use the current host so mobile phones on local Wi-Fi can reach the API
      final host = Uri.base.host;
      if (host.isNotEmpty && host != '0.0.0.0') {
        baseUrl = 'http://$host:8000/api/v1';
      }
    } else if (defaultTargetPlatform == TargetPlatform.android) {
      // Android Emulator loopback alias to host machine
      baseUrl = 'http://10.0.2.2:8000/api/v1';
    }

    dio = Dio(
      BaseOptions(
        baseUrl: baseUrl,
        connectTimeout: const Duration(seconds: 8),
        receiveTimeout: const Duration(seconds: 8),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      ),
    );

    dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) {
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
