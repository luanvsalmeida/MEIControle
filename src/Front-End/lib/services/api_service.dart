import 'dart:convert';
import 'package:http/http.dart' as http;
import 'dart:io' show Platform;

class ApiResponse {
  final String content;
  final String? chartPath;
  final String? reportPath;
  final String? message;

  ApiResponse({
    required this.content,
    this.chartPath,
    this.reportPath,
    this.message,
  });

  factory ApiResponse.fromJson(Map<String, dynamic> json) {
    return ApiResponse(
      content: json['content'] ?? json['message'] ?? '[Sem resposta]',
      chartPath: json['chart'],
      reportPath: json['report'],
      message: json['message'],
    );
  }

  bool get hasChart => chartPath != null && chartPath!.isNotEmpty;
  bool get hasReport => reportPath != null && reportPath!.isNotEmpty;
}

class ApiService {
  late final String baseUrl;
  final int chatId = 1;
  final int userId = 1;
  final http.Client _client = http.Client();

  ApiService() {
    // Use o IP correto dependendo da plataforma
    if (Platform.isAndroid) {
      // 10.0.2.2 é o endereço especial que o Android usa para acessar o localhost da máquina host
      baseUrl = 'http://10.0.2.2:8002';
    } else if (Platform.isIOS) {
      // Para iOS, geralmente localhost funciona, mas você pode precisar usar o IP real da máquina host
      baseUrl = 'http://127.0.0.1:8002';
    } else {
      // Para web ou desktop, use localhost normal
      baseUrl = 'http://localhost:8002';
    }
  }

  Future<ApiResponse> sendMessage(String message) async {
    final url = Uri.parse('$baseUrl/api/message');
    
    print('Enviando requisição para: $url');
    
    // Prepara o payload conforme especificado
    final payload = {
      "chatId": chatId,
      "userId": userId,
      "role": "user",
      "content": message
    };

    try {
      print('Enviando payload: ${jsonEncode(payload)}');
      
      // Configuração de headers completa
      final headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      };

      // Primeira tentativa de requisição
      var response = await _client.post(
        url,
        headers: headers,
        body: jsonEncode(payload),
      ).timeout(
        const Duration(seconds: 15),
        onTimeout: () {
          throw Exception('Tempo limite de conexão excedido');
        },
      );

      // Lidar com redirecionamento manualmente, se necessário
      if (response.statusCode == 307 || response.statusCode == 301 || response.statusCode == 302 || response.statusCode == 303) {
        print('Redirecionamento detectado: ${response.statusCode}');
        
        final newLocation = response.headers['location'];
        if (newLocation != null) {
          print('Redirecionando para: $newLocation');
          
          // Segunda tentativa com a nova URL
          final redirectUrl = Uri.parse(newLocation.startsWith('http') ? newLocation : '$baseUrl$newLocation');
          response = await _client.post(
            redirectUrl,
            headers: headers,
            body: jsonEncode(payload),
          ).timeout(
            const Duration(seconds: 15),
            onTimeout: () {
              throw Exception('Tempo limite de conexão excedido após redirecionamento');
            },
          );
        } else {
          print('Redirecionamento sem header Location');
          return ApiResponse(content: '[Erro: Redirecionamento sem destino]');
        }
      }

      print('Status code final: ${response.statusCode}');
      print('Resposta recebida: ${response.body}');

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return ApiResponse.fromJson(data);
      } else {
        print('Erro na API: ${response.statusCode}');
        print('Headers de resposta: ${response.headers}');
        print('Resposta: ${response.body}');
        
        return ApiResponse(content: '[Erro na comunicação com API: ${response.statusCode}]');
      }
    } catch (e) {
      print('Exceção ao chamar API: $e');
      return ApiResponse(content: '[Erro na comunicação com API: ${e.toString()}]');
    }
  }

  String getFullUrl(String path) {
    if (path.startsWith('/code/api/')) {
      // Remove '/code/api' do início do path
      return '$baseUrl${path.substring(9)}';
    }
    return '$baseUrl$path';
  }
}