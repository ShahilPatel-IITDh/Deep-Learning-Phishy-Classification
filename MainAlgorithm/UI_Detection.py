# object_detection.py

import cv2
import numpy as np
import pytesseract

def detect_input_box(screenshot_file_path):
    # Load the screenshot using OpenCV
    screenshot = cv2.imread(screenshot_file_path)

    # Convert the screenshot to grayscale
    grayscale_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Apply image processing (e.g., thresholding) to highlight potential input boxes
    _, thresholded_screenshot = cv2.threshold(grayscale_screenshot, 200, 255, cv2.THRESH_BINARY)

    # For quick and simple checking use the code below
        
    # Use Tesseract OCR to extract text from the screenshot
    extracted_text = pytesseract.image_to_string(thresholded_screenshot)

    # Check if the extracted text contains keywords indicating input boxes (languages included: English, German, Spanish, Arabic, Hindi, French, Portuguese, Italian, Finnish, Swedish, Persian, Indonesian)
    keywords = ["username", "Benutzername", "Nombre de usuario", "اسم المستخدم", "उपयोगकर्ता नाम", "Nom d'utilisateur", "Nome de usuário", "Nome utente", 
                "Käyttäjänimi", "Användarnamn", "نام کاربری", "Nama pengguna", "password", "Passwort" ,"Contraseña", " كلمة المرور" ,"पासवर्ड", "Mot de passe", "Senha", "Salasana" , "Lösenord" "رمز عبور", "Kata sandi", "email", "e-mail", "Correo electrónico", "البريد الإلكتروني", "ईमेल", "Courriel", "Sähköposti", "E-post", "ایمیل", "Surel", "input", "Eingabe", "Entrada", "إدخال", "इनपुट", "Entrée", "Inserimento", "Inmatning", "ورودی", "Masukan", "textbox", "Textfeld", "Cuadro de texto", "مربع نص", "टेक्स्टबॉक्स", "Zone de texte", "Caixa de texto", "Casella di testo", "Tekstilaatikko", "Textfältm", "جعبه متن", "Kotak teks", "form", "Formular", "Formulario", "نموذج", "फॉर्म", "Formulaire", "Formulário", "Formulare", "Lomake", "Formulär", "فرم", "Formulir", "signin", "sign-in", "Anmelden", "Iniciar sesión", "تسجيل الدخول", "साइन इन", "Se connecter", "Entrar", "Accedi", "Kirjaudu sisään", "Logga in", "ورود", "Masuk", "login", "log-in", "Einloggen", "लॉग इन", "Connexion", "Accesso", "Kirjautuminen", "Inloggning"]


    for keyword in keywords:
        if keyword in extracted_text.lower():
            return -1  # Input box detected

    return 1  # Input box not detected