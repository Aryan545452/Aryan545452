# Robot Control Server

کنترل دستی ۳ ربات از طریق مرورگر.

## Render

Build Command:
`pip install -r requirements.txt`

Start Command:
`gunicorn server:app`

## API

گرفتن فرمان:
`GET /api/command/1`

ارسال فرمان:
`POST /api/command/1`
با JSON:
`{"left": 10, "right": 10}`

سرعت هر موتور بین -10 تا 10 محدود می‌شود.

توقف همه:
`POST /api/stop`

وضعیت:
`GET /health`

نکته: این سرور فقط فرمان را نگه می‌دارد و پنل مرورگر را ارائه می‌کند. کنترلر Webots باید با درخواست‌های GET به endpoint فرمان وصل شود و مقدار left/right را روی موتورهای خودش اعمال کند.
