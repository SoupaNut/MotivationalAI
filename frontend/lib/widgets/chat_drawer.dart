import 'package:flutter/material.dart';
import '../providers/session_provider.dart';
import 'package:provider/provider.dart';
import '../util/constants.dart';
import 'user_input_field.dart';

class ChatDrawer extends StatefulWidget {
  final GlobalKey<UserInputFieldState> userInputKey;

  const ChatDrawer({super.key, required this.userInputKey});

  @override
  State<ChatDrawer> createState() => _ChatDrawerState();
}

class _ChatDrawerState extends State<ChatDrawer> {
  List<ChatSession> chatSessions = [];
  bool isLoading = true;

  @override
  Widget build(BuildContext context) {
    // Get current session ID from provider
    String currentSessionId = context.watch<SessionProvider>().sessionId;
    chatSessions = context.watch<ChatSessionsProvider>().chatSessions;

    return Drawer(
      child: ListView(
        padding: EdgeInsets.zero,
        children: [
          const DrawerHeader(
            decoration: BoxDecoration(
              color: Color.fromRGBO(
                  149, 117, 205, 1), // Colors.deepPurple.shade300
            ),
            child: Text('All Chats'),
          ),
          ...chatSessions.map((session) {
            final bool isSelected = session.sessionId == currentSessionId;
            return Padding(
              padding: const EdgeInsets.symmetric(
                horizontal: kDrawerItemPadHorizontal,
                vertical: kDrawerItemPadVertical,
              ),
              child: Container(
                decoration: BoxDecoration(
                  color: isSelected
                      ? kSelectedDrawerItemColor
                      : Colors.transparent,
                  borderRadius:
                      BorderRadius.circular(kDrawerItemSelectedBorderRadius),
                ),
                child: ListTile(
                  trailing: IconButton(
                    onPressed: () {},
                    icon: const Icon(
                      Icons.keyboard_control_outlined,
                    ),
                  ),
                  contentPadding: const EdgeInsets.only(left: 8.0),
                  visualDensity: const VisualDensity(
                    horizontal: 0,
                    vertical: -4, // lower padding from ListTile
                  ),
                  title: Text(
                    session.summary,
                    style: TextStyle(
                      fontSize: kDrawerItemFontSize,
                      fontWeight:
                          isSelected ? FontWeight.bold : FontWeight.normal,
                      color: isSelected
                          ? kSelectedDrawerItemTextColor
                          : kUnselectedDrawerItemTextColor,
                    ),
                  ),
                  onTap: () {
                    // set the current session ID in provider
                    context
                        .read<SessionProvider>()
                        .setSessionId(newSessionId: session.sessionId);
                    widget.userInputKey.currentState
                        ?.loadChat(session.sessionId);
                    print(session.sessionId);

                    // close drawer
                    Navigator.pop(context);
                    FocusManager.instance.primaryFocus?.unfocus();
                  },
                ),
              ),
            );
          }),
        ],
      ),
    );
  }
}
