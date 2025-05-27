import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import '../models/mensagem.dart';
import '../services/api_service.dart';
import '../utils/extract_image_url.dart'; // onde está sua função extract

class ReportMessage extends StatelessWidget {
  final Mensagem mensagem;

  const ReportMessage({super.key, required this.mensagem});

  @override
  Widget build(BuildContext context) {
    final apiService = ApiService();
    final imageUrl = extractImageUrl(mensagem.texto, apiService.baseUrl);

    if (imageUrl.isEmpty) {
      return Text(
        mensagem.texto,
        style: TextStyle(fontSize: 16), // ou use seu tamanho dinâmico
      );
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text("Gráfico gerado:", style: TextStyle(fontWeight: FontWeight.bold)),
        SizedBox(height: 8),
        Image.network(imageUrl),
        TextButton.icon(
          icon: Icon(Icons.download),
          label: Text("Baixar gráfico"),
          onPressed: () async {
            final uri = Uri.parse(imageUrl);
            if (await canLaunchUrl(uri)) {
              await launchUrl(uri);
            } else {
              print('Não foi possível abrir o link');
            }
          },
        ),
      ],
    );
  }
}
