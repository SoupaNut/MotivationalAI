import 'package:flutter/material.dart';
import 'package:motivational_app/api/api_service.dart';

class ChatSession {
  final String sessionId;
  final String summary;
  final String timestamp;

  ChatSession(
      {required this.sessionId,
      required this.summary,
      required this.timestamp});

  factory ChatSession.fromJson(Map<String, dynamic> json) {
    return ChatSession(
      sessionId: json["sessionId"] as String,
      summary: json["summary"] as String,
      timestamp: json["timestamp"] as String,
    );
  }
}

class SessionProvider extends ChangeNotifier {
  String _sessionId = "";

  String get sessionId => _sessionId;

  Future<void> loadSessionId() async {
    final response = await apiGetCurrentSessionId();
    _sessionId = response.data;
    notifyListeners();
  }

  void setSessionId({required String newSessionId}) async {
    _sessionId = newSessionId;
    notifyListeners();
  }
}

class ChatSessionsProvider extends ChangeNotifier {
  List<ChatSession> _chatSessions = [];

  List<ChatSession> get chatSessions => _chatSessions;

  Future<void> loadChatSessions() async {
    final response = await apiGetAllChatSummaries();
    _chatSessions = (response.data as List<dynamic>)
        .map((item) => ChatSession.fromJson(item as Map<String, dynamic>))
        .toList();

    _chatSessions.sort((a, b) => b.timestamp.compareTo(a.timestamp));
    notifyListeners();
  }

  void addChatSession({
    required String newSessionId,
    required String newSummary,
    required String newTimestamp,
  }) async {
    // Don't do anything if newSessionId already exists
    final exists =
        _chatSessions.any((session) => session.sessionId == newSessionId);

    if (exists) {
      return;
    }
    _chatSessions.insert(
      0,
      ChatSession(
        sessionId: newSessionId,
        summary: newSummary,
        timestamp: newTimestamp,
      ),
    );

    notifyListeners();
  }
}
