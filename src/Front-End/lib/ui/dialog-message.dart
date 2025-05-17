import 'package:flutter/material.dart';
import 'package:mei_controle/models/mensagem.dart';

class DialogMessage extends StatelessWidget {
  final Mensagem mensagem;
  final double font;

  const DialogMessage({
    Key? key,
    required this.mensagem,
    this.font = 18.0,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final bool isAnnouncer = mensagem.autor == 'usuario';
    final String textMessage = mensagem.texto;

    return Container(
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(8),
        color: isAnnouncer ? Colors.black : Colors.white54,
        border: Border.all(width: 2, color: Colors.black),
      ),
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      margin: const EdgeInsets.symmetric(vertical: 5.0),
      child: Column(
        crossAxisAlignment:
            isAnnouncer ? CrossAxisAlignment.end : CrossAxisAlignment.start,
        children: [
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 10.0),
            child: Text(
              textMessage,
              style: TextStyle(
                color: isAnnouncer ? Colors.white : Colors.black,
                fontSize: font,
                fontWeight: FontWeight.w500,
              ),
            ),
          ),
        ],
      ),
    );
  }

  static const TextStyle _userStyle = TextStyle(
    color: Colors.white,
    fontSize: 18.0,
    fontWeight: FontWeight.w500,
  );

  static const TextStyle _bootStyle = TextStyle(
    color: Colors.black,
    fontSize: 18.0,
    fontWeight: FontWeight.w500,
  );
}
