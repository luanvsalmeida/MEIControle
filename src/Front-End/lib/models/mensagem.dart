class Mensagem {
  late int? id;
  late String texto;
  late String autor;
  late DateTime data;
  final String? relatorioPath;
  final String? imagemPath;
  final String? chartPath;
  final String? reportPath;

  Mensagem({
    this.id,
    required this.texto,
    required this.data,
    required this.autor,
    this.relatorioPath,
    this.imagemPath,
    this.chartPath,
    this.reportPath,
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
    if(chartPath != null) {
      m['chartPath'] = chartPath;
    }
    if(reportPath != null) {
      m['reportPath'] = reportPath;
    }
    return m;
  }

  static Mensagem fromMap(Map map) {
    return Mensagem(
      id: map['id'],
      texto: map['texto'],
      autor: map['autor'],
      data: DateTime.parse(map['data']),
      chartPath: map['chartPath'],
      reportPath: map['reportPath'],
    );
  }

  bool get hasChart => chartPath != null && chartPath!.isNotEmpty;
  bool get hasReport => reportPath != null && reportPath!.isNotEmpty;
  bool get hasAttachments => hasChart || hasReport;
}