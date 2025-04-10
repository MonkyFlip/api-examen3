# API de Usuarios

Este repositorio contiene una API desarrollada en Flask para la gestión de usuarios. La API incluye funcionalidades CRUD (Crear, Leer, Actualizar, Eliminar) y cuenta con documentación generada automáticamente mediante Swagger/OpenAPI.

## Características

- **Framework:** Flask
- **Base de Datos:** Configurada para conectarse a MySQL utilizando SQLAlchemy.
- **Autenticación:** Manejo de autenticación básica con JWT.
- **Documentación:** Documentación integrada accesible en `/docs` (Swagger/OpenAPI).
- **Infraestructura:** Soporte de despliegue en instancias de AWS EC2 con Nginx como proxy inverso y Gunicorn como servidor WSGI.

---

## Instalación local

### **1. Clonar el repositorio**
```bash
git clone https://github.com/MonkyFlip/api-examen3.git
cd api-examen3
```

### **2. Crear un entorno virtual**
```bash
python3 -m venv venv
source venv/bin/activate
```

### **3. Instalar las dependencias**
```bash
pip install -r requirements.txt
```

### **4. Configurar variables de entorno**
Crea un archivo `.env` en la raíz del proyecto con las siguientes variables (modifica según tu configuración):
```plaintext
DATABASE_URI=mysql+pymysql://usuario:contraseña@host/base_de_datos
JWT_SECRET_KEY=tu_clave_secreta
```

### **5. Ejecutar la API**
Inicia la API con:
```bash
python run.py
```

Accede en tu navegador a `http://127.0.0.1:5000`.

---

## Despliegue en AWS EC2

### **1. Requisitos previos**
- Una instancia de Amazon Linux 2023.
- Un grupo de seguridad que permita acceso a los puertos 22 (SSH), 80 (HTTP) y 443 (HTTPS).

### **2. Configuración de la instancia**

#### **2.1. Conéctate a tu instancia**
```bash
ssh -i "tu-llave.pem" ec2-user@<ip-publica>
```

#### **2.2. Instalar dependencias**
```bash
sudo dnf update -y
sudo dnf install git python3 python3-pip nginx -y
sudo pip3 install virtualenv
```

#### **2.3. Clonar el repositorio**
```bash
cd /var/www
sudo mkdir -p /var/www/api-examen3
sudo chown ec2-user:ec2-user /var/www/api-examen3
cd /var/www/api-examen3
git clone https://github.com/MonkyFlip/api-examen3.git .
```

#### **2.4. Configurar el entorno virtual**
```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### **2.5. Configurar SSL con un certificado autofirmado**
1. Generar el certificado:
   ```bash
   sudo mkdir -p /etc/nginx/ssl
   cd /etc/nginx/ssl
   sudo openssl genrsa -out self_signed.key 2048
   sudo openssl req -new -key self_signed.key -out self_signed.csr
   sudo openssl x509 -req -days 365 -in self_signed.csr -signkey self_signed.key -out self_signed.crt
   ```

2. Configurar Nginx como proxy inverso:
   Edita el archivo `/etc/nginx/conf.d/api.conf`:
   ```nginx
   server {
       listen 80;
       server_name <ip-publica>;

       # Redirigir tráfico HTTP a HTTPS
       return 301 https://$host$request_uri;
   }

   server {
       listen 443 ssl;
       server_name <ip-publica>;

       ssl_certificate /etc/nginx/ssl/self_signed.crt;
       ssl_certificate_key /etc/nginx/ssl/self_signed.key;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

3. Reinicia Nginx:
   ```bash
   sudo systemctl restart nginx
   ```

#### **2.6. Ejecutar la API con Gunicorn**
```bash
gunicorn -w 4 -b 127.0.0.1:5000 run:app
```

---

### **3. Configurar Gunicorn como servicio de Systemd**
1. Crea el archivo `/etc/systemd/system/api.service`:
   ```plaintext
   [Unit]
   Description=Gunicorn instance to serve API
   After=network.target

   [Service]
   User=ec2-user
   Group=nginx
   WorkingDirectory=/var/www/api-examen3
   Environment="PATH=/var/www/api-examen3/venv/bin"
   ExecStart=/var/www/api-examen3/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 run:app

   [Install]
   WantedBy=multi-user.target
   ```

2. Habilitar el servicio:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start api
   sudo systemctl enable api
   ```

3. Verifica que el servicio esté corriendo:
   ```bash
   sudo systemctl status api
   ```

---

## Endpoints principales

- **`GET /`**: Mensaje de bienvenida.
- **`GET /users`**: Lista de usuarios.
- **`POST /users`**: Crear un nuevo usuario.
- **`GET /users/<id>`**: Consultar un usuario por ID.
- **`PUT /users/<id>`**: Actualizar un usuario por ID.
- **`DELETE /users/<id>`**: Eliminar un usuario por ID.
- **`GET /docs`**: Documentación Swagger.

---

## Notas

- El certificado SSL autofirmado solo es apropiado para desarrollo. En producción, considera usar Let's Encrypt.
- Para monitorear el rendimiento, puedes usar herramientas como `htop` o realizar pruebas de carga con `wrk`.

---

¡Gracias por usar esta API! Si tienes alguna duda o sugerencia, no dudes en contribuir al proyecto.
```

---

Este `README.md` documenta claramente cómo se desarrolla, despliega y utiliza la API. Si necesitas añadir algo más, ¡puedo ajustarlo! 🚀✨
