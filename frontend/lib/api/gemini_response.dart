class GeminiResponse {
  final int statusCode;
  final dynamic data;

  GeminiResponse({
    required this.statusCode,
    this.data,
  });

  factory GeminiResponse.fromJson(Map<String, dynamic> json, int statusCode) {
    return GeminiResponse(
      statusCode: statusCode,
      data: json,
    );
  }

  factory GeminiResponse.fromArray(List<dynamic> jsonArray, int statusCode) {
    return GeminiResponse(
      statusCode: statusCode,
      data: jsonArray,
    );
  }

  factory GeminiResponse.fromString(String message, int statusCode) {
    return GeminiResponse(
      statusCode: statusCode,
      data: message,
    );
  }

  factory GeminiResponse.error(String errorMessage, int statusCode) {
    return GeminiResponse(
      statusCode: statusCode,
      data: errorMessage,
    );
  }
}
