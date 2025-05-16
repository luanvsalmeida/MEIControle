import 'package:flutter/material.dart';
import 'package:mei_controle/models/mensagem.dart';

class DialogMessage extends StatelessWidget {
  final Mensagem mensagem;
  late bool isAnnouncer;
  late  String textMessage;

  DialogMessage({required this.mensagem}){
    isAnnouncer = mensagem.autor == 'usuario' ? true : false;
    textMessage = mensagem.texto;
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(8),
        color: isAnnouncer ? Colors.black : Colors.white54,
        border: Border.all(width: 2, color: Colors.black),
      ),
      padding: EdgeInsets.symmetric(vertical: 8.0),
      margin: EdgeInsets.symmetric(vertical: 5.0),
      child: Column(
        crossAxisAlignment:
            isAnnouncer ? CrossAxisAlignment.end : CrossAxisAlignment.start,
        children: [
          Padding(
            padding: EdgeInsets.symmetric(horizontal: 10.0),
            child: Text(
              textMessage,
              style: isAnnouncer ? userStyle : bootStyle,
            ),
          ),
        ],
      ),
    );
  }

  TextStyle userStyle = TextStyle(
      color: Colors.white,
      fontSize: 18.0,
      fontWeight: FontWeight.w500);

  TextStyle bootStyle = TextStyle(
    color: Colors.black,
    fontSize: 18.0,
    fontWeight: FontWeight.w500,
  );
}
