import 'package:mei_controle/models/mensagem.dart';
import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';

final String mensagensTable = 'mensagens';
final String idColumn = 'id';
final String textoColumn = 'texto';
final String autorColumn = 'autor';
final String dataColumn = 'data';
final String chartPathColumn = 'chartPath';
final String reportPathColumn = 'reportPath';

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
      version: 2, // Incrementar versão para migration
      onCreate: (Database db, int newerVersion) async {
        await db.execute('''
          CREATE TABLE $mensagensTable(
            $idColumn INTEGER PRIMARY KEY,
            $autorColumn TEXT,
            $textoColumn TEXT,
            $dataColumn TEXT,
            $chartPathColumn TEXT,
            $reportPathColumn TEXT
          );
        ''');
      },
      onUpgrade: (Database db, int oldVersion, int newVersion) async {
        if (oldVersion < 2) {
          // Adicionar as novas colunas se não existirem
          await db.execute('ALTER TABLE $mensagensTable ADD COLUMN $chartPathColumn TEXT');
          await db.execute('ALTER TABLE $mensagensTable ADD COLUMN $reportPathColumn TEXT');
        }
      },
    );
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
    List<Map> listMap = await dbMensagens.rawQuery('SELECT * FROM $mensagensTable ORDER BY $idColumn ASC');
    List<Mensagem> mensagens = [];
    for(Map m in listMap) {
      mensagens.add(Mensagem.fromMap(m));
    }
    return mensagens;
  }

  Future<void> clearAllMessages() async {
    Database dbMensagens = await db;
    await dbMensagens.delete(mensagensTable);
  }
}