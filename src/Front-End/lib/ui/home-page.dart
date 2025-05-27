import 'package:flutter/material.dart';
import 'package:mei_controle/management/ger-mensagem.dart';
import 'package:mei_controle/ui/enhanced_message.dart'; // Nova importação
import 'package:mei_controle/models/mensagem.dart';
import 'package:mei_controle/management/ger-ui.dart';
import 'package:mei_controle/services/api_service.dart';

class HomePage extends StatefulWidget {
  final Function onToogleTheme;
  final GerMensagem gerenciador = GerMensagem.getInstance();

  HomePage({super.key, required this.onToogleTheme});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final GerUi gerUi = GerUi.getInstance();
  final ApiService _apiService = ApiService();
  final ScrollController _scrollController = ScrollController();
  late bool _isDarkMode;
  int? font;
  List<Mensagem> listaMensagens = [];
  final TextEditingController campoController = TextEditingController();
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    obterLista();
    obterTema();
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  void _scrollToBottom() {
    if (_scrollController.hasClients) {
      Future.delayed(const Duration(milliseconds: 100), () {
        if (_scrollController.hasClients) {
          _scrollController.animateTo(
            _scrollController.position.maxScrollExtent,
            duration: const Duration(milliseconds: 300),
            curve: Curves.easeOut,
          );
        }
      });
    }
  }

  void _scrollToBottomInstant() {
    if (_scrollController.hasClients) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        if (_scrollController.hasClients && _scrollController.position.maxScrollExtent > 0) {
          _scrollController.jumpTo(_scrollController.position.maxScrollExtent);
        }
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).hintColor,
        title: Text(
          'MEI Controle',
          style: TextStyle(
            color: Colors.black,
            fontWeight: FontWeight.w600,
            fontSize: 30.0,
          ),
        ),
        centerTitle: true,
        actions: [
          PopupMenuButton(
            icon: Icon(Icons.menu),
            itemBuilder: (context) => [
              PopupMenuItem(
                enabled: false,
                child: StatefulBuilder(
                  builder: (context, setState) {
                    return Column(
                      children: [
                        Row(
                          children: [
                            Icon(
                              _isDarkMode
                                  ? Icons.dark_mode_outlined
                                  : Icons.sunny,
                              color: _isDarkMode ? Colors.white : Colors.black,
                              size: 32,
                            ),
                            SizedBox(width: 20),
                            Switch(
                              activeColor: Colors.white,
                              value: _isDarkMode,
                              onChanged: (value) {
                                setState(() {
                                  _isDarkMode = value;
                                  widget.onToogleTheme();
                                });
                              },
                            ),
                          ],
                        ),
                        SizedBox(height: 20),
                        Row(
                          children: [
                            Icon(
                              Icons.text_fields,
                              color: _isDarkMode ? Colors.white : Colors.black,
                              size: 32,
                            ),
                            SizedBox(width: 20),
                            IconButton(
                              onPressed: () => alterarTamanhoFonte(true),
                              icon: Icon(
                                Icons.arrow_upward,
                                color: _isDarkMode ? Colors.white : Colors.black,
                                size: 32,
                              ),
                            ),
                            SizedBox(width: 10),
                            Text(
                              '${font ?? 18}',
                              style: TextStyle(
                                color: _isDarkMode ? Colors.white : Colors.black,
                                fontSize: 28,
                              ),
                            ),
                            SizedBox(width: 10),
                            IconButton(
                              onPressed: () => alterarTamanhoFonte(false),
                              icon: Icon(
                                Icons.arrow_downward,
                                color: _isDarkMode ? Colors.white : Colors.black,
                                size: 32,
                              ),
                            ),
                          ],
                        ),
                      ],
                    );
                  },
                ),
              ),
            ],
          ),
        ],
      ),
      body: FutureBuilder<int>(
        future: gerUi.getFontSize(),
        builder: (context, snapshot) {
          if (snapshot.connectionState != ConnectionState.done) {
            return const Center(child: CircularProgressIndicator());
          }

          font = snapshot.data ?? 18;

          return Padding(
            padding: EdgeInsets.all(20.0),
            child: Column(
              children: [
                Expanded(
                  child: listaMensagens.isEmpty
                      ? const Center(
                          child: Text(
                            'Nenhuma mensagem ainda.\nInicie uma conversa!',
                            textAlign: TextAlign.center,
                            style: TextStyle(fontSize: 16),
                          ),
                        )
                      : ListView.builder(
                          controller: _scrollController,
                          itemCount: listaMensagens.length,
                          itemBuilder: (context, index) {
                            final mensagem = listaMensagens[index];
                            return EnhancedMessage(
                              mensagem: mensagem,
                              font: (font ?? 18).toDouble(),
                            );
                          },
                        ),
                ),
                if (_isLoading)
                  Padding(
                    padding: const EdgeInsets.symmetric(vertical: 8.0),
                    child: Row(
                      children: [
                        SizedBox(
                          width: 20,
                          height: 20,
                          child: CircularProgressIndicator(
                            strokeWidth: 2,
                            color: _isDarkMode ? Colors.white : Colors.black,
                          ),
                        ),
                        SizedBox(width: 10),
                        Text(
                          'Processando...',
                          style: TextStyle(
                            color: _isDarkMode ? Colors.white70 : Colors.black54,
                            fontStyle: FontStyle.italic,
                          ),
                        ),
                      ],
                    ),
                  ),
                SizedBox(height: 20.0),
                Row(
                  children: [
                    Expanded(
                      child: TextField(
                        controller: campoController,
                        decoration: InputDecoration(
                          hintText: 'Digite algo',
                          border: OutlineInputBorder(),
                        ),
                        onSubmitted: (_) => enviarMensagem(),
                      ),
                    ),
                    SizedBox(width: 3.0),
                    ElevatedButton(
                      onPressed: _isLoading ? null : enviarMensagem,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.black,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(5),
                        ),
                        disabledBackgroundColor: Colors.grey,
                      ),
                      child: Icon(
                        Icons.send,
                        color: Colors.white,
                      ),
                    ),
                  ],
                ),
              ],
            ),
          );
        },
      ),
    );
  }

  Future<void> enviarMensagem() async {
    final mensagemTexto = campoController.text.trim();
    if (mensagemTexto.isEmpty) return;

    setState(() {
      _isLoading = true;
    });

    try {
      // Adiciona mensagem do usuário
      final mensagem = Mensagem(
        texto: mensagemTexto,
        data: DateTime.now(),
        autor: 'usuario',
      );
      await widget.gerenciador.insMensagem(mensagem);
      campoController.clear();
      await obterLista();
      _scrollToBottom();

      // Chama a API e recebe a resposta estruturada
      final apiResponse = await _apiService.sendMessage(mensagemTexto);

      // Cria mensagem com os dados da resposta
      final resposta = Mensagem(
        texto: apiResponse.content,
        data: DateTime.now(),
        autor: 'assistente',
        chartPath: apiResponse.chartPath,
        reportPath: apiResponse.reportPath,
      );
      
      await widget.gerenciador.insMensagem(resposta);
      await obterLista();
      _scrollToBottom();
    } catch (e) {
      print('Erro ao processar mensagem: $e');

      final erroMsg = Mensagem(
        texto: "Erro ao processar sua solicitação. Verifique se o servidor API está rodando em http://localhost:8002.",
        data: DateTime.now(),
        autor: 'assistente',
      );
      await widget.gerenciador.insMensagem(erroMsg);
      await obterLista();
      _scrollToBottom();
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  Future<void> obterLista() async {
    try {
      final listaObtida = await widget.gerenciador.getAllMensagens();
      final bool isInitialLoad = listaMensagens.isEmpty;
      
      setState(() {
        listaMensagens = listaObtida;
      });
      
      if (isInitialLoad && listaMensagens.isNotEmpty) {
        _scrollToBottomInstant();
      } else if (!isInitialLoad) {
        _scrollToBottom();
      }
    } catch (e) {
      print('Erro ao obter mensagens: $e');
    }
  }

  Future<void> obterTema() async {
    try {
      final tema = await gerUi.getDarkModeState();
      setState(() {
        _isDarkMode = tema;
      });
    } catch (e) {
      print('Erro ao obter tema: $e');
      setState(() {
        _isDarkMode = false;
      });
    }
  }

  Future<void> alterarTamanhoFonte(bool aumentar) async {
    final tamanhoAtual = font ?? 18;
    final novoTamanho = aumentar ? tamanhoAtual + 2 : tamanhoAtual - 2;
    final tamanhoFinal = novoTamanho.clamp(10, 30);

    if (tamanhoFinal != tamanhoAtual) {
      await gerUi.saveFontSize(tamanhoFinal);
      setState(() {
        font = tamanhoFinal;
      });
    }
  }
}