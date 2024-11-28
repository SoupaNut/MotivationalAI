import 'package:flutter/material.dart';

// ------------------- BUILD OPTIONS -------------------
const bool kBuildDebug = true;

// ------------------- GENERAL -------------------
const String kAppTitle = 'MoMo';
const double kIconSize = 24.0;

// ------------------- DRAWER -------------------
const double kDrawerItemFontSize = 14.0;
const double kDrawerItemSelectedBorderRadius = 12.0;
const double kDrawerItemPadVertical = 4.0;
const double kDrawerItemPadHorizontal = 8.0;
const Color kSelectedDrawerItemColor = Color.fromRGBO(224, 224, 224, 1);
const Color kSelectedDrawerItemTextColor = Colors.deepPurple;
const Color kUnselectedDrawerItemTextColor = Colors.black;
const String kNewChatSummary = "New Chat";


// ------------------- USER INPUT FIELD -------------------
// Container
const double kFieldPadVertical = 16.0;
const double kFieldPadHorizontal = 8.0;
const double kFieldBorderRadius = 30.0;
const Color kFieldBorderColor = Colors.purple;
const Color kFieldBackgroundColor = Colors.white;


// Text field
const int kFieldMinLines = 1;
const int kFieldMaxLines=  5;
const String kFieldHintText = 'Message MoMo';

// Icons
const Color kIconEnabledColor = Colors.deepPurple;


// ------------------- MESSAGE BUBBLES -------------------
const double kBubblePadVertical = 8.0;
const double kBubbleLargePad = 64.0;
const double kBubbleSmallPad = 8.0;
const double kBubbleInsidePad = 12.0;
const double kBubbleBorderRadius = 12.0;
const Color kBubbleUserColor = Color.fromRGBO(209, 196, 233, 1); // Colors.deepPurple.shade100
const Color kBubbleModelColor = Color.fromRGBO(224, 224, 224, 1); // Colors.grey.shade300
const Color kBubbleTextColor = Colors.black;
const Color kBubbleErrorColor = Color.fromRGBO(239, 154, 154, 1); // Colors.red.shade200

// ------------------- API -------------------
const int kRequestTimeout = 60;
const String kLocalHostUrl = "http://10.0.2.2:5000";
const String kGCloudUrl = "https://appimg-274488824075.us-central1.run.app";
const String kApiRequestRoute = "/api/gemini/request";
const String kApiNewChatRoute = "/api/gemini/new_chat";
const String kApiLoadChatRoute = "/api/gemini/load_chat";
const String kApiDeleteChatsRoute = "/api/gemini/delete_chats";
const String kApiGetCurrentSessionIdRoute = "/api/gemini/current_session_id";
const String kApiGetAllChatSummariesRoute = "/api/gemini/all_chat_summaries";
const String kApiCloseAppRoute = "/api/gemini/close";