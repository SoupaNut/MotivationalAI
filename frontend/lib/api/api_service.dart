import 'dart:async';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:motivational_app/util/constants.dart';

class GeminiResponse {
  final String text;
  final int statusCode;

  GeminiResponse({required this.text, required this.statusCode});

  factory GeminiResponse.fromJson(Map<String, dynamic> json, int statusCode) {
    return GeminiResponse(
      text: json['response'] ?? "No response",
      statusCode: statusCode,
    );
  }
}

final Map<String, String> _headers = {'Content-Type': 'application/json'};

Future<GeminiResponse> apiSendMessage(String prompt) async {
  return _makePostRequest(
    url: "$kLocalHostUrl$kApiRequestRoute",
    body: {"prompt": prompt},
  );
}

Future<GeminiResponse> apiStartNewChat({String sessionId=""}) async {
  return _makePostRequest(
    url: "$kLocalHostUrl$kApiNewChatRoute",
    body: {"session_id": sessionId}, // TODO: add datetime?
  );
}

Future<GeminiResponse> _makePostRequest({
  required String url,
  required Map<String, dynamic> body,
}) async {
  try {
    final response = await http
        .post(
          Uri.parse(url),
          headers: _headers,
          body: jsonEncode(body),
        )
        .timeout(const Duration(seconds: kRequestTimeout));

    final statusCode = response.statusCode;
    final responseData = jsonDecode(response.body);

    if (statusCode != 200) {
      responseData["response"] =
          "Error $statusCode: ${responseData["response"] ?? "Unknown error"}";
    }

    return GeminiResponse.fromJson(responseData, statusCode);
  } on http.ClientException catch (e) {
    return GeminiResponse(text: "Client Error 400: $e", statusCode: 400);
  } on TimeoutException {
    return GeminiResponse(
      text:
          "Client Timeout Error 504: Request timed out. Please try again later.",
      statusCode: 504,
    );
  } catch (e) {
    return GeminiResponse(text: "Unexpected Error 500: $e", statusCode: 500);
  }
}
