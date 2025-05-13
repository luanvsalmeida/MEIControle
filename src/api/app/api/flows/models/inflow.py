

"""
| Campo         | Tipo     | Obrigatório | Notas                     |
| ------------- | -------- | ----------- | ------------------------- |
| `saleId`      | PK       | ✅          |                           |
| `userId`      | FK       | ✅          |                           |
| `client`      | string   | opcional    | OK manter opcional        |
| `value`       | float    | ✅          |                           |
| `date`        | datetime | ✅          |                           |
| `type`        | enum     | ✅          | “produto”, “serviço”, etc |
| `paymentForm` | enum     | opcional    | “pix”, “dinheiro”, etc    |
"""