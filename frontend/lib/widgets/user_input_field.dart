import 'package:flutter/material.dart';
import '../api/api_service.dart';
import '../widgets/message_bubble.dart';
import '../util/constants.dart';

class UserInputField extends StatefulWidget {
  const UserInputField({super.key});

  @override
  State<UserInputField> createState() => UserInputFieldState();
}

class UserInputFieldState extends State<UserInputField> {
  final TextEditingController _controller = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  final List<Message> _messages = [];
  Future<GeminiResponse>? _apiResponseFuture;

  void startNewChat() {
    setState(() {
      _apiResponseFuture = apiStartNewChat();
      _messages.clear();
    });
  }

  void _sendMessage(Roles role, String text) {
    if (text.isNotEmpty) {
      setState(() {
        _messages.insert(
          0,
          Message(
            text: text,
            role: role,
            statusCode: 200,
          ),
        ); // insert at 0 since we want new messages to appear at the top of the list
      });

      _controller.clear();
      _scrollController.animateTo(
        0.0,
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeOut,
      );

      if (role == Roles.user) {
        setState(() {
          _apiResponseFuture = apiSendMessage(text).then((reply) {
            setState(() {
              _messages.insert(
                0,
                Message(
                  text: reply.text,
                  role: Roles.model,
                  statusCode: reply.statusCode,
                ),
              );
            });

            return reply;
          });
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // Display Messages
        Expanded(
          child: FutureBuilder(
            future: _apiResponseFuture,
            builder: (context, snapshot) {
              return ListView.builder(
                controller: _scrollController,
                reverse: true, // Keeps most recent text at bottom
                itemCount: _messages.length,
                itemBuilder: (context, index) {
                  return MessageBubble(message: _messages[index]);
                },
              );
            },
          ),
        ),

        // Bottom Text Field
        Padding(
          padding: const EdgeInsets.symmetric(
            horizontal: kFieldPadHorizontal,
            vertical: kFieldPadVertical,
          ),
          child: Container(
            decoration: BoxDecoration(
              color: kFieldBackgroundColor,
              borderRadius: BorderRadius.circular(kFieldBorderRadius),
              border: Border.all(color: kFieldBorderColor),
            ),
            child: Row(
              children: [
                IconButton(
                  onPressed: () {},
                  icon: const Icon(
                    Icons.mic,
                    color: kIconEnabledColor,
                  ),
                ),
                Expanded(
                  child: TextField(
                    autofocus: true,
                    controller: _controller,
                    minLines: kFieldMinLines,
                    maxLines: kFieldMaxLines,
                    decoration: const InputDecoration(
                      border: InputBorder.none,
                      hintText: kFieldHintText,
                    ),
                  ),
                ),
                IconButton(
                  onPressed: () =>
                      _sendMessage(Roles.user, _controller.text.trim()),
                  icon: const Icon(
                    Icons.send,
                    color: kIconEnabledColor,
                  ),
                )
              ],
            ),
          ),
        ),
      ],
    );
  }
}
