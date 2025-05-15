import 'package:flutter/material.dart';
import 'package:mei_controle/management/ger-mensagem.dart';
import 'package:mei_controle/ui/dialog-message.dart';
import 'package:mei_controle/models/mensagem.dart';
import 'package:mei_controle/management/ger-ui.dart';

class HomePage extends StatefulWidget {
  final Function onToogleTheme;
  final  GerMensagem gerenciador = GerMensagem.getInstance();

  HomePage({super.key, required this.onToogleTheme});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final GerUi gerUi = GerUi.getInstance();
  late bool _isDarkMode;
  int? font;
  List<Mensagem> listaMensagens = [];
  final TextEditingController campoController = TextEditingController();

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
        backgroundColor: Theme
            .of(context)
            .hintColor,
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
            itemBuilder: (context) =>
            [
              PopupMenuItem(
                enabled: false,
                child: StatefulBuilder(
                  builder: (context, setState) {
                    return Column(
                      children: [
                        Row(
                          children: [
                            Icon(
                              _isDarkMode ? Icons.dark_mode_outlined : Icons
                                  .sunny,
                              color: _isDarkMode ? Colors.white : Colors
                                  .black,
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
                              color: _isDarkMode ? Colors.white : Colors
                                  .black,
                              size: 32,
                            ),
                            SizedBox(width: 20),
                            IconButton(
                              onPressed: () {},
                              icon: Icon(
                                Icons.arrow_upward,
                                color: _isDarkMode ? Colors.white : Colors
                                    .black,
                                size: 32,
                              ),
                            ),
                            SizedBox(width: 10),
                            Text(
                              '18',
                              style: TextStyle(
                                color: _isDarkMode ? Colors.white : Colors
                                    .black,
                                fontSize: 28,
                              ),
                            ),
                            SizedBox(width: 10),
                            IconButton(
                              onPressed: () {},
                              icon: Icon(
                                Icons.arrow_downward,
                                color: _isDarkMode ? Colors.white : Colors
                                    .black,
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
          if(snapshot.connectionState != ConnectionState.done) {
            return const Expanded(child: Text('Carregando...'));
          }

          final fontSize = snapshot.data!;

          return Padding(
            padding: EdgeInsets.all(20.0),
            child: Column(
              children: [
                Expanded(
                  child: ListView(
                    shrinkWrap: true,
                    children: [
                      for (int i = 0; i < listaMensagens.length; i++)
                        DialogMessage(mensagem: listaMensagens[i], font: fontSize ?? 18),
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
                      ),
                    ),
                    SizedBox(width: 3.0),
                    ElevatedButton(
                      onPressed: () => enviarMensagem(),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.black,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(5),
                        ),
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
        }
      )
    );
  }

  Future<void> enviarMensagem() async {
    if(campoController.text != ''){
      Mensagem mensagem = Mensagem(
        texto: campoController.text,
        data: DateTime.now(),
        autor: 'usuario',
      );

      Mensagem resposta = Mensagem(
        texto: '"Resposta do assistente"',
        data: DateTime.now(),
        autor: 'assistente',
      );

      await widget.gerenciador.insMensagem(mensagem);
      await widget.gerenciador.insMensagem(resposta);

      campoController.text = '';

      setState(() {
        obterLista();
      });
    }
  }

  Future<void> obterLista() async {
    await widget.gerenciador.getAllMensagens().then((listaObtida) {
      setState(() {
        listaMensagens = listaObtida;
      });
    });

  }

  Future<void> obterTema() async {
    await gerUi.getDarkModeState().then((tema) {
      setState(() {
        _isDarkMode = tema;
      });
    });
  }
}
