import subprocess
import csv
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont



archivo=input("Ingrese el nombre del archivo con el listado de sitios a revisar: ")
rutaout=input("Ingrese el nombre del archivo de salida: ")
correlativo = input("Ingrese su correlativo: ")
rutaout = rutaout + ".csv"
f = open(archivo, "r")
sitios = []
for line in f:
	sitios.append(line[0:len(line)-1])
f.close()
columnas = ("Nombre del Sitio","strict-transport-security","content-security-policy","x-frame-options","x-content-type-options","referrer-policy","permissions-policy","Evidencia")

with open(rutaout, 'w', newline='') as csvfile:
	csvwriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	resultado = []
	csvwriter.writerow(columnas)
	c = 1
	for r in sitios:
		resultado.append(r)
		print("\nVamos por el sitio: " + str(c) + " de: " + str(len(sitios)))
		headers = subprocess.getoutput("curl -s -I"+" "+ r).lower()
		if headers.__contains__("strict-transport-security"):
			resultado.append("True") 
		else:
			resultado.append("Se identificó qué en el sitio: " + r + ", no cuenta con la cabecera Strict-Transport-Security. Esta cabecera indica al navegador que el sitio web solo debe de cargarse en HTTPS.")
		if headers.__contains__("content-security-policy"):
			resultado.append("True")
		else:
			resultado.append("Se identificó qué el sitio: " + r + ", no cuenta con la cabecera Content-Security-Policy. Esta cabecera es una medida efectiva de protección del sitio ante ataques XSS.")
		if headers.__contains__("x-frame-options"):
			resultado.append("True")
		else:
			resultado.append("Se identificó qué en el sitio: " + r + ",es vulnerable a Clickjacking lo que permite agregarla dentro de un sitio externo controlado por una persona malintencionada, pudiendo engañar así a los usuarios haciendo uso de prácticas de Ingeniería social.")
		if headers.__contains__("x-content-type-options"):
			resultado.append("True")
		else:
			resultado.append("Se identificó qué el sitio: " + r + ", no cuenta con la cabecera X-Content-Type-Options. Esta cabecera permite evitar ataques basados en la confusión del tipo de MIME, debido a que si el navegador recibe esta cabecera no intentará interpretar el tipo de MIME en ningún caso y utilizará el indicado en el Content-Type.")
		if headers.__contains__("referrer-policy"):
			resultado.append("True")
		else:
			resultado.append("Se identificó qué el sitio: " + r + ", no cuenta con la cabecera Referrer-Policy. Esta cabecera permite controlar que información se envía en la cabecera Referer cuál es utilizada por el navegador para indicarle al servidor desde que enlace se ha llegado a la página.")
		if headers.__contains__("permissions-policy"):
			resultado.append("True")
		else:
			resultado.append("Se identificó qué el sitio: " + r + ", no cuenta con la cabecera Permissions-Policy. Esta cabecera permite a un sitio controlar que funciones y API's   se pueden usar en el navegador.")


		resultado.append(correlativo + "-" + str(c) + '.png')
		font = ImageFont.truetype('Roboto-Bold.ttf', 20)
		img = Image.new('RGB', (3000, 800))
		d = ImageDraw.Draw(img)
		d.text((20, 20), "Sitio: "+ r + "\n" + headers, fill=(255, 255, 255),font=font)
		img.save(correlativo + "-" + str(c) + '.png','png')
		csvwriter.writerow(resultado)
		resultado = []
		c += 1
	