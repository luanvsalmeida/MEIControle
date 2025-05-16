import 'package:flutter/material.dart';
import 'package:mei_controle/management/ger-mensagem.dart';
import 'package:mei_controle/ui/dialog-message.dart';
import 'package:mei_controle/models/mensagem.dart';

class HomePage extends StatefulWidget {
  final Function onToogleTheme;
  final  GerMensagem gerenciador = GerMensagem.getInstance();

  HomePage({super.key, required this.onToogleTheme});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  bool _isDarkMode = false;
  List<Mensagem> listaMensagens = [];
  final TextEditingController campoController = TextEditingController();

  @override
  void initState() {
    super.initState();
    obterLista();
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
          Row(
            children: [
              Icon(
                _isDarkMode ? Icons.dark_mode_outlined : Icons.sunny,
                color: Colors.black,
              ),
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
        ],
      ),
      body: Padding(
        padding: EdgeInsets.all(20.0),
        child: Column(
          children: [
            Expanded(
              child: ListView(
                shrinkWrap: true,
                children: [
                  for (int i = 0; i < listaMensagens.length; i++)
                    DialogMessage(mensagem: listaMensagens[i])
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
            )
          ],
        ),
      ),
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
    List<Mensagem> listaObtida = await widget.gerenciador.getAllMensagens();
    setState(() {
      listaMensagens = listaObtida;
    });
  }
}
