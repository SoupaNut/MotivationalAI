import 'package:flutter/material.dart';
import '../util/constants.dart';

enum Roles {
  user,
  model,
}


class Message {
  final String text;
  final Roles role;
  final int statusCode;

  Message({required this.text, required this.role, required this.statusCode});
}

class MessageBubble extends StatelessWidget {
  final Message message;
  const MessageBubble({super.key, required this.message});

  @override
  Widget build(BuildContext context) {
    final bool userSent = message.role == Roles.user;
    final bool statusOk = message.statusCode == 200;

    return Padding(
      padding: EdgeInsets.only(
        left: userSent ? kBubbleLargePad : kBubbleSmallPad,
        right: userSent ? kBubbleSmallPad : kBubbleLargePad,
        top: kBubblePadVertical,
        bottom: kBubblePadVertical,
      ),
      child: Align(
        alignment: userSent ? Alignment.centerRight : Alignment.centerLeft,
        child: Container(
          padding: const EdgeInsets.all(kBubbleInsidePad),
          decoration: BoxDecoration(
            color: !statusOk
                ? kBubbleErrorColor // red if error
                : userSent
                    ? kBubbleUserColor // purple if user
                    : kBubbleModelColor, // gray if model
            borderRadius: BorderRadius.circular(kBubbleBorderRadius),
            // border: userSent ? null : Border.all(color: Colors.grey.shade400)
          ),
          child: Text(
            message.text,
            style: const TextStyle(
              color: kBubbleTextColor,
            ),
          ),
        ),
      ),
    );
  }
}
