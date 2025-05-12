import 'package:flutter/material.dart';
import 'dialogflow_service.dart';

void main() {
  runApp(DialogflowApp());
}

class DialogflowApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Dialogflow Chat',
      theme: ThemeData.light(),
      darkTheme: ThemeData.dark(),
      themeMode: ThemeMode.system,
      home: ChatPage(),
    );
  }
}

class ChatPage extends StatefulWidget {
  @override
  _ChatPageState createState() => _ChatPageState();
}

class _ChatPageState extends State<ChatPage> {
  final _controller = TextEditingController();
  final _messages = <String>[];
  final _dialogflow = DialogflowService();
  bool _isSending = false;

  void _sendMessage() async {
    final text = _controller.text.trim();
    if (text.isEmpty || _isSending) return;

    setState(() {
      _isSending = true;
      _messages.add("Você: $text");
    });

    _controller.clear();

    try {
      final response = await _dialogflow.sendMessage(text);
      setState(() {
        _messages.add("Bot: $response");
      });
    } catch (e) {
      setState(() {
        _messages.add("Erro: ${e.toString()}");
      });
    } finally {
      setState(() {
        _isSending = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Chat com Dialogflow')),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              padding: EdgeInsets.all(16),
              itemCount: _messages.length,
              itemBuilder: (_, index) {
                final msg = _messages[index];
                final isBot = msg.startsWith("Bot:");

                return Container(
                  alignment:
                  isBot ? Alignment.centerLeft : Alignment.centerRight,
                  margin: EdgeInsets.symmetric(vertical: 4),
                  child: Container(
                    padding: EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: isBot ? Colors.grey[300] : Colors.blue[200],
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Text(
                      msg,
                      style: TextStyle(fontSize: 16),
                    ),
                  ),
                );
              },
            ),
          ),
          Padding(
            padding: EdgeInsets.all(8),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    onSubmitted: (_) => _sendMessage(),
                    decoration: InputDecoration(
                      hintText: 'Digite sua mensagem...',
                      border: OutlineInputBorder(),
                    ),
                  ),
                ),
                SizedBox(width: 8),
                _isSending
                    ? CircularProgressIndicator()
                    : ElevatedButton(
                  onPressed: _sendMessage,
                  child: Text('Enviar'),
                ),
              ],
            ),
          )
        ],
      ),
    );
  }
}
