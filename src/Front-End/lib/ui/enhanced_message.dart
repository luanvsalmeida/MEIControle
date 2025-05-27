import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import '../models/mensagem.dart';
import '../services/api_service.dart';

class EnhancedMessage extends StatelessWidget {
  final Mensagem mensagem;
  final double font;

  const EnhancedMessage({
    Key? key,
    required this.mensagem,
    this.font = 18.0,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final bool isUser = mensagem.autor == 'usuario';
    final String textMessage = mensagem.texto;

    return Container(
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(8),
        color: isUser ? Colors.black : Colors.white54,
        border: Border.all(width: 2, color: Colors.black),
      ),
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      margin: const EdgeInsets.symmetric(vertical: 5.0),
      child: Column(
        crossAxisAlignment: isUser ? CrossAxisAlignment.end : CrossAxisAlignment.start,
        children: [
          // Texto da mensagem
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 10.0),
            child: Text(
              textMessage,
              style: TextStyle(
                color: isUser ? Colors.white : Colors.black,
                fontSize: font,
                fontWeight: FontWeight.w500,
              ),
            ),
          ),
          
          // Anexos (gráfico e relatório)
          if (mensagem.hasAttachments) ...[
            const SizedBox(height: 12),
            _buildAttachments(context),
          ],
        ],
      ),
    );
  }

  Widget _buildAttachments(BuildContext context) {
    final apiService = ApiService();
    
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 10.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Gráfico
          if (mensagem.hasChart) ...[
            const Text(
              "📊 Gráfico gerado:",
              style: TextStyle(
                fontWeight: FontWeight.bold,
                color: Colors.blue,
              ),
            ),
            const SizedBox(height: 8),
            Container(
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(8),
                border: Border.all(color: Colors.grey.shade300),
              ),
              child: ClipRRect(
                borderRadius: BorderRadius.circular(8),
                child: Image.network(
                  apiService.getFullUrl(mensagem.chartPath!),
                  errorBuilder: (context, error, stackTrace) {
                    return Container(
                      height: 100,
                      color: Colors.grey.shade200,
                      child: const Center(
                        child: Text(
                          'Erro ao carregar gráfico',
                          style: TextStyle(color: Colors.red),
                        ),
                      ),
                    );
                  },
                  loadingBuilder: (context, child, loadingProgress) {
                    if (loadingProgress == null) return child;
                    return Container(
                      height: 100,
                      child: const Center(
                        child: CircularProgressIndicator(),
                      ),
                    );
                  },
                ),
              ),
            ),
            const SizedBox(height: 8),
            ElevatedButton.icon(
              icon: const Icon(Icons.download, size: 16),
              label: const Text("Baixar Gráfico"),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.blue,
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              ),
              onPressed: () => _downloadFile(
                apiService.getFullUrl(mensagem.chartPath!),
                'Gráfico'
              ),
            ),
          ],
          
          // Relatório
          if (mensagem.hasReport) ...[
            if (mensagem.hasChart) const SizedBox(height: 16),
            const Text(
              "📄 Relatório gerado:",
              style: TextStyle(
                fontWeight: FontWeight.bold,
                color: Colors.green,
              ),
            ),
            const SizedBox(height: 8),
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.green.shade50,
                borderRadius: BorderRadius.circular(8),
                border: Border.all(color: Colors.green.shade200),
              ),
              child: Row(
                children: [
                  Icon(Icons.description, color: Colors.green.shade700),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      "Relatório CSV disponível",
                      style: TextStyle(
                        color: Colors.green.shade700,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 8),
            ElevatedButton.icon(
              icon: const Icon(Icons.download, size: 16),
              label: const Text("Baixar Relatório"),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.green,
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              ),
              onPressed: () => _downloadFile(
                apiService.getFullUrl(mensagem.reportPath!),
                'Relatório'
              ),
            ),
          ],
        ],
      ),
    );
  }

  Future<void> _downloadFile(String url, String type) async {
    try {
      final uri = Uri.parse(url);
      if (await canLaunchUrl(uri)) {
        await launchUrl(uri, mode: LaunchMode.externalApplication);
      } else {
        print('Não foi possível abrir o link: $url');
      }
    } catch (e) {
      print('Erro ao baixar $type: $e');
    }
  }
}