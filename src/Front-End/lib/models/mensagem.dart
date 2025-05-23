class Mensagem {
  late int? id;
  late String texto;
  late String autor;
  late DateTime data;
  final String? graficoPath;

  Mensagem({
    this.id,
    required this.texto,
    required this.data,
    required this.autor,
    this.graficoPath,
  });

  Map<String, dynamic> toMap() {
    Map<String, dynamic> m = {
      'texto': texto,
      'autor': autor,
      'data': data.toString(),
    };
    if(id != null) {
      m['id'] = id;
    }
    return m;
  }

  static Mensagem fromMap(Map map) {
    return Mensagem(
      id: map['id'],
      texto: map['texto'],
      autor: map['autor'],
      data: DateTime.parse(map['data']),
    );
  }
}