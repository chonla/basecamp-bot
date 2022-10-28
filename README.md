# บอทเบสแค้มป์

## วิธีทำให้บอททำงานได้

1. ติดตั้ง Dependencies
2. ลงทะเบียน App กับ Basecamp
3. เอา Access token ให้บอทของเรา
4. รันบอท

## ติดตั้ง Dependencies

```
pip3 install -r requirements.pip
```

## ลงทะเบียน App กับ Basecamp

1. ไปที่ https://launchpad.37signals.com/integrations
2. กดปุ่ม Register Application.
3. ตรง Products เลือก Campfire
4. ตรง OAuth2 ช่อง Redirect URI ใส่ `http://localhost:8080/auth` ได้เลย หรือถ้ามี URL อื่นก็ใส่ได้เหมือนกัน

## เอา Access token ให้บอทของเรา

1. รันคำสั่ง `make authen`
2. มันจะมีหน้า OAuth2 ขึ้นมา ก็ Allow ซะ

## รันบอท

1. รัน `make run` บอทจะเริ่มดักข้อความใน Campfire
