import 'package:mei_controle/models/mensagem.dart';
import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';
import 'package:mei_controle/models/mensagem.dart';

final String mensagensTable = 'mensagens';
final String idColumn = 'id';
final String textoColumn = 'texto';
final String autorColumn = 'autor';
final String dataColumn = 'data';

class GerMensagem {
  static GerMensagem? _singleInstance;
  Database? _db;

  GerMensagem._internal();

  static GerMensagem getInstance() {
    _singleInstance ??= GerMensagem._internal();
    return _singleInstance!;
  }

  Future<Database> initDb() async {
    final databasePath = await getDatabasesPath();
    final path = join(databasePath, 'mensagens.db');

    return openDatabase(
        path,
        version: 1,
        onCreate: (Database db, int newerVersion) async {
          await db.execute('''
            CREATE TABLE $mensagensTable(
              $idColumn INTEGER PRIMARY KEY,
              $autorColumn TEXT,
              $textoColumn TEXT,
              $dataColumn TEXT
            );
          ''');
    });
  }

  Future<Database> get db async {
    _db ??= await initDb();
    return _db!;
  }

  Future<Mensagem> insMensagem(Mensagem mensagem) async {
    Database dbMensagens = await db;
    mensagem.id = await dbMensagens.insert(mensagensTable, mensagem.toMap());
    return mensagem;
  }

  Future<List<Mensagem>> getAllMensagens() async {
    Database dbMensagens = await db;
    List<Map> listMap = await dbMensagens.rawQuery('SELECT * FROM $mensagensTable');
    List<Mensagem> mensagens = [];
    for(Map m in listMap) {
      mensagens.add(Mensagem.fromMap(m));
    }
    return mensagens;
  }
}