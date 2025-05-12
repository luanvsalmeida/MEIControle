import 'dart:convert';
import 'package:flutter/services.dart';
import 'package:googleapis_auth/auth_io.dart';
import 'package:http/http.dart' as http;

class DialogflowService {
  final _scopes = ['https://www.googleapis.com/auth/cloud-platform'];

  Future<String> sendMessage(String message) async {
    final jsonCredentialsStr = await rootBundle.loadString('assets/credentials.json');
    final jsonCredentials = jsonDecode(jsonCredentialsStr);

    final credentials = ServiceAccountCredentials.fromJson(jsonCredentials);
    final projectId = jsonCredentials['project_id'];
    final sessionId = '123456';
    final languageCode = 'pt-BR';

    final url = Uri.parse(
        'https://dialogflow.googleapis.com/v2/projects/$projectId/agent/sessions/$sessionId:detectIntent');

    final body = jsonEncode({
      'queryInput': {
        'text': {
          'text': message,
          'languageCode': languageCode,
        }
      }
    });

    final client = await clientViaServiceAccount(credentials, _scopes);

    final response = await client.post(
      url,
      headers: {'Content-Type': 'application/json; charset=utf-8'},
      body: body,
    );

    client.close();

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      final result = data['queryResult']['fulfillmentText'];
      return result ?? '[Sem resposta]';
    } else {
      print('Erro: ${response.statusCode}');
      print('Resposta: ${response.body}');
      return '[Erro na comunicação com Dialogflow]';
    }
  }
}
