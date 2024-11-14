import 'package:flutter/material.dart';
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
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      home: HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final GlobalKey<UserInputFieldState> _userInputKey = GlobalKey<UserInputFieldState>();

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
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
              onPressed: () {
                _userInputKey.currentState?.startNewChat();
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
        // body: const UserInputField(),
        body: UserInputField(key: _userInputKey),
        drawer: const ChatDrawer()
      ),
    );
  }
}

