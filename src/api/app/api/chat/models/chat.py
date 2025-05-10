"""
|  Field    | Tipo       | Obrigatório | Notas                    |
| --------- | ---------- | ----------- | ------------------------ |
| `chatID`  | PK         | ✅           |                          |
| `userID`  | FK         | ✅           |                          |
| `date`    | datetime   | ✅           | Início do chat           |
| `context` | JSON/text? | opcional    | Tokens do histórico/chat |

"""