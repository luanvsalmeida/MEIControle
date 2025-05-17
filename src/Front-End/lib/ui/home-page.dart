import 'package:flutter/material.dart';
import 'package:mei_controle/management/ger-mensagem.dart';
import 'package:mei_controle/ui/dialog-message.dart';
import 'package:mei_controle/models/mensagem.dart';
import 'package:mei_controle/management/ger-ui.dart';
import 'package:mei_controle/services/api_service.dart'; // Nova importação

class HomePage extends StatefulWidget {
  final Function onToogleTheme;
  final GerMensagem gerenciador = GerMensagem.getInstance();

  HomePage({super.key, required this.onToogleTheme});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final GerUi gerUi = GerUi.getInstance();
  final ApiService _apiService = ApiService(); // Nova instância do serviço de API
  late bool _isDarkMode;
  int? font;
  List<Mensagem> listaMensagens = [];
  final TextEditingController campoController = TextEditingController();
  bool _isLoading = false; // Controle de estado para loading

  @override
  void initState() {
    super.initState();
    obterLista();
    obterTema();
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
                              _isDarkMode ? Icons.dark_mode_outlined : Icons.sunny,
                              color: _isDarkMode ? Colors.white : Colors.black,
                              size: 32,
                            ),
                            SizedBox(width: 20),
                            Switch(
                              activeColor: Colors.white,
                              value: _isDarkMode,
                              onChanged: (value) {
                                setState(
                                  () {
                                    _isDarkMode = value;
                                    widget.onToogleTheme();
                                  },
                                );
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
                  child: ListView.builder(
                    itemCount: listaMensagens.length,
                    itemBuilder: (context, index) {
                      // Solução 1: Converter explicitamente para double
                      return DialogMessage(mensagem: listaMensagens[index], font: (font ?? 18).toDouble());
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
    
    // Desabilita o botão de enviar enquanto processa
    setState(() {
      _isLoading = true;
    });

    try {
      // Criar e salvar mensagem do usuário
      Mensagem mensagem = Mensagem(
        texto: mensagemTexto,
        data: DateTime.now(),
        autor: 'usuario',
      );
      await widget.gerenciador.insMensagem(mensagem);
      
      // Limpar campo de texto imediatamente
      campoController.clear();
      
      // Atualizar lista para mostrar mensagem do usuário
      await obterLista();

      // Enviar mensagem para a API local
      final respostaTexto = await _apiService.sendMessage(mensagemTexto);

      // Criar e salvar resposta do assistente
      Mensagem resposta = Mensagem(
        texto: respostaTexto,
        data: DateTime.now(),
        autor: 'assistente',
      );
      await widget.gerenciador.insMensagem(resposta);

      // Atualizar a lista com a resposta
      await obterLista();
    } catch (e) {
      print('Erro ao processar mensagem: $e');
      
      // Criar mensagem de erro
      Mensagem erroMsg = Mensagem(
        texto: "Erro ao processar sua solicitação. Verifique se o servidor API está rodando em http://localhost:8002.",
        data: DateTime.now(),
        autor: 'assistente',
      );
      
      await widget.gerenciador.insMensagem(erroMsg);
      await obterLista();
    } finally {
      // Sempre reativar o botão de enviar
      setState(() {
        _isLoading = false;
      });
    }
  }

  Future<void> obterLista() async {
    try {
      final listaObtida = await widget.gerenciador.getAllMensagens();
      setState(() {
        listaMensagens = listaObtida;
      });
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
        _isDarkMode = false; // Valor padrão em caso de erro
      });
    }
  }

  // Método para alterar o tamanho da fonte
  Future<void> alterarTamanhoFonte(bool aumentar) async {
    final tamanhoAtual = font ?? 18;
    final novoTamanho = aumentar ? tamanhoAtual + 2 : tamanhoAtual - 2;
    
    // Limitar o tamanho entre 10 e 30
    final tamanhoFinal = novoTamanho.clamp(10, 30);
    
    if (tamanhoFinal != tamanhoAtual) {
      await gerUi.saveFontSize(tamanhoFinal);
      setState(() {
        font = tamanhoFinal;
      });
    }
  }
}