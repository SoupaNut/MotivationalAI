import 'package:flutter/material.dart';
import 'package:motivational_app/api/api_service.dart';
import 'package:motivational_app/providers/session_provider.dart';
import 'package:provider/provider.dart';
import 'widgets/chat_drawer.dart';
import 'widgets/user_input_field.dart';
import 'util/constants.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (context) => SessionProvider()),
        ChangeNotifierProvider(create: (context) => ChatSessionsProvider())
      ],
      child: const MaterialApp(
        debugShowCheckedModeBanner: false,
        home: HomePage(),
      ),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final GlobalKey<UserInputFieldState> _userInputKey =
      GlobalKey<UserInputFieldState>();

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) async {
      await _getSessionId();
      await _getNewChatSession();
    });
  }

  Future<void> _getSessionId() async {
    final sessionProvider =
        Provider.of<SessionProvider>(context, listen: false);
    await sessionProvider.loadSessionId();
  }

  Future<void> _getNewChatSession() async {
    final chatSessionsProvider =
        Provider.of<ChatSessionsProvider>(context, listen: false);
    final response = await apiStartNewChat();
    final newSessionId = response.data;
    await chatSessionsProvider.loadChatSessions();

    String currentTimestamp = DateTime.now().toUtc().toIso8601String();
    chatSessionsProvider.addChatSession(
      newSessionId: newSessionId,
      newSummary: kNewChatSummary,
      newTimestamp: currentTimestamp,
    );
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () => FocusManager.instance.primaryFocus?.unfocus(),
      child: Scaffold(
          appBar: AppBar(
            // backgroundColor: Colors.grey,
            iconTheme: const IconThemeData(color: kIconEnabledColor),
            centerTitle: true,
            title: const Text(kAppTitle),
            actions: [
              IconButton(
                onPressed: () async {
                  _userInputKey.currentState?.clearMessages();
                  await _getNewChatSession(); // reload chat sessions
                  await _getSessionId();
                },
                icon: SizedBox(
                  width: kIconSize,
                  height: kIconSize,
                  child: Image.asset(
                    'assets/icons/edit-square.png',
                    color: kIconEnabledColor,
                  ),
                ),
              ),
            ],
          ),
          body: UserInputField(key: _userInputKey),
          drawer: ChatDrawer(
            userInputKey: _userInputKey,
          )),
    );
  }
}
