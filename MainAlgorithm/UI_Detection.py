"""
Input Box Detection Documentation

This Python code is designed to detect input boxes in a screenshot. It uses OpenCV for image processing and Tesseract OCR
to extract text from the screenshot. The extracted text is then checked for keywords that typically indicate the presence
of input boxes (e.g., text fields, forms, sign-in options). If such keywords are found in the extracted text, the code
returns a flag indicating the detection of input boxes.

Usage:
To use this script, call the 'detect_input_box' function with the following parameter:
- screenshot_file_path: The file path of the screenshot image.

Example:
input_box_flag = detect_input_box("screenshot.png")

Dependencies:
- Python 3.x
- The 'cv2' (OpenCV) library for image processing.
- The 'numpy' library for numerical operations.
- The 'pytesseract' library for OCR text extraction.

Functions:
1. detect_input_box(screenshot_file_path)
    - screenshot_file_path: The file path of the screenshot image.
    - Returns: -1 if input boxes are detected, 1 if no input boxes are detected.

The code loads the screenshot, converts it to grayscale, and applies image processing (thresholding) to highlight potential input boxes.
It then uses Tesseract OCR to extract text and checks for specific keywords indicating input boxes. If the keywords are found,
the code returns -1, otherwise, it returns 1.

Note:
- Ensure that the required libraries are installed before using this script.
- The list of keywords can be customized to include additional terms specific to your use case.
"""


import cv2
import numpy as np
import pytesseract

def detect_input_box(screenshot_file_path):

    """
    Detect input boxes in a screenshot.

    :param screenshot_file_path: The file path of the screenshot image.
    
    :return: -1 if input boxes are detected, 1 if no input boxes are detected.
    """

    print("--Code entered the detect_input_box function")
    print("|")

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
                "Käyttäjänimi", "Användarnamn", "نام کاربری", "Nama pengguna", "Contrasena", "Numer", "password", "Haslo","Passwort" ,"Contraseña", " كلمة المرور" ,"पासवर्ड", "Mot de passe", "Senha", "Salasana" , "Lösenord" "رمز عبور", "Kata sandi", "email", "e-mail", "Correo electrónico", "البريد الإلكتروني", "ईमेल", "Courriel", "Sähköposti", "E-post", "ایمیل", "Surel", "input", "Eingabe", "Entrada", "إدخال", "इनपुट", "Entrée", "Inserimento", "Inmatning", "ورودی", "Masukan", "textbox", "Textfeld", "Cuadro de texto", "مربع نص", "टेक्स्टबॉक्स", "Zone de texte", "Caixa de texto", "Casella di testo", "Tekstilaatikko", "Textfältm", "جعبه متن", "Kotak teks", "form", "Formular", "Formulario", "نموذج", "फॉर्म", "Formulaire", "Formulário", "Formulare", "Lomake", "Formulär", "فرم", "Formulir", "signin", "sign-in", "Anmelden", "Iniciar sesión", "تسجيل الدخول", "साइन इन", "Se connecter", "Entrar", "Accedi", "Kirjaudu sisään", "Logga in", "ورود", "Masuk", "login", "log-in", "Einloggen", "लॉग इन", "Connexion", "Accesso", "Kirjautuminen", "Inloggning", "phone", "otp", "pin", "card", "cvv", "account", "telephone", "mobile", "telefonu", "zaloguj"]


    print("|")
    print("--Code is about to exit the detect_input_box function\n")

    for keyword in keywords:
        if keyword in extracted_text.lower():
            return -1  # Input box detected

    return 1  # Input box not detected