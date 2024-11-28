import 'dart:async';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../util/constants.dart';
import 'gemini_response.dart';

enum HttpMethod {
  // ignore: constant_identifier_names
  GET,
  // ignore: constant_identifier_names
  POST,
  // ignore: constant_identifier_names
  DELETE,
}

final Map<String, String> _headers = {'Content-Type': 'application/json'};

Future<GeminiResponse> apiSendMessage(String prompt) async {
  return _makeRequest(
    url: kBuildDebug
        ? "$kLocalHostUrl$kApiRequestRoute"
        : "$kGCloudUrl$kApiRequestRoute",
    method: HttpMethod.POST,
    body: {
      "prompt": prompt,
    },
  );
}

Future<GeminiResponse> apiStartNewChat() async {
  return _makeRequest(
    url: kBuildDebug
        ? "$kLocalHostUrl$kApiNewChatRoute"
        : "$kGCloudUrl$kApiNewChatRoute",
    method: HttpMethod.POST,
  );
}

Future<GeminiResponse> apiLoadChat(String sessionId) async {
  return _makeRequest(
    url: kBuildDebug
        ? "$kLocalHostUrl$kApiLoadChatRoute"
        : "$kGCloudUrl$kApiLoadChatRoute",
    method: HttpMethod.POST,
    body: {
      "sessionId": sessionId,
    },
  );
}

Future<GeminiResponse> apiCloseApp() async {
  return _makeRequest(
    url: kBuildDebug
        ? "$kLocalHostUrl$kApiCloseAppRoute"
        : "$kGCloudUrl$kApiCloseAppRoute",
    method: HttpMethod.POST,
  );
}

Future<GeminiResponse> apiGetCurrentSessionId() async {
  return _makeRequest(
    url: kBuildDebug
        ? "$kLocalHostUrl$kApiGetCurrentSessionIdRoute"
        : "$kGCloudUrl$kApiGetCurrentSessionIdRoute",
    method: HttpMethod.GET,
  );
}

Future<GeminiResponse> apiGetAllChatSummaries() async {
  return _makeRequest(
    url: kBuildDebug
        ? "$kLocalHostUrl$kApiGetAllChatSummariesRoute"
        : "$kGCloudUrl$kApiGetAllChatSummariesRoute",
    method: HttpMethod.GET,
  );
}

Future<GeminiResponse> apiDeleteChats(List<String> sessionIds) async {
  return _makeRequest(
    url: kBuildDebug
        ? "$kLocalHostUrl$kApiDeleteChatsRoute"
        : "$kGCloudUrl$kApiDeleteChatsRoute",
    method: HttpMethod.DELETE,
    body: {
      "sessionIds": sessionIds,
    }
  );
}

Future<GeminiResponse> _makeRequest({
  required String url,
  required HttpMethod method,
  Map<String, dynamic>? body,
}) async {
  try {
    final uri = Uri.parse(url);
    late http.Response response;

    if (method == HttpMethod.POST) {
      response = await http
          .post(
            uri,
            headers: _headers,
            body: jsonEncode(body),
          )
          .timeout(
            const Duration(
              seconds: kRequestTimeout,
            ),
          );
    } else if (method == HttpMethod.GET) {
      response = await http
          .get(
            uri,
            headers: _headers,
          )
          .timeout(
            const Duration(
              seconds: kRequestTimeout,
            ),
          );
    } else if (method == HttpMethod.DELETE) {
      response = await http
          .delete(
            uri,
            headers: _headers,
            body: jsonEncode(body),
          )
          .timeout(
            const Duration(
              seconds: kRequestTimeout,
            ),
          );
    } else {
      throw ArgumentError("Unsupported HTTP method: $method");
    }

    final statusCode = response.statusCode;
    final responseBody = jsonDecode(response.body);

    if (statusCode != 200) {
      final errorMessage = responseBody ?? "Unknown error";
      return GeminiResponse.error(
        "Error $statusCode: $errorMessage",
        statusCode,
      );
    }

    // JSON
    if (responseBody is Map<String, dynamic>) {
      return GeminiResponse.fromJson(
        responseBody,
        statusCode,
      );
    }
    // Array
    else if (responseBody is List<dynamic>) {
      return GeminiResponse.fromArray(
        responseBody,
        statusCode,
      );
    }
    // String
    else if (responseBody is String) {
      return GeminiResponse.fromString(
        responseBody,
        statusCode,
      );
    }
    // Error
    else {
      return GeminiResponse.error(
        "Data format ${responseBody.runtimeType} is not supported",
        500,
      );
    }
  } on http.ClientException catch (e) {
    return GeminiResponse.error(
      "Error 400: $e",
      400,
    );
  } on TimeoutException {
    return GeminiResponse.error(
      "Timeout Error 504: Request timed out. Please try again later.",
      504,
    );
  } catch (e) {
    return GeminiResponse.error(
      "Unexpected Error 500: $e",
      500,
    );
  }
}
