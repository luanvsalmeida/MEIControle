String extractImageUrl(String content, String baseUrl) {
  final regex = RegExp(r'static/[\w\-_]+\.(png|jpg|jpeg)');
  final match = regex.firstMatch(content);
  if (match != null) {
    return '$baseUrl/${match.group(0)}';
  }
  return '';
}
