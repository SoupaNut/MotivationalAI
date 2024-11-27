import 'package:flutter/material.dart';

Future<bool?> showAlertConfirmation(
    {required BuildContext context, required String title, required String text, String? confirmButtonText}) {
  return showDialog<bool>(
    context: context,
    builder: (BuildContext context) {
      return AlertDialog(
        title: Text(title),
        content: Text(text),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false), // Cancel
            child: const Text("Cancel"),
          ),
          TextButton(
            onPressed: () => Navigator.pop(context, true), // Confirm
            child: Text(
              confirmButtonText ?? "Confirm",
              style: const TextStyle(color: Colors.red),
            ),
          ),
        ],
      );
    },
  );
}
