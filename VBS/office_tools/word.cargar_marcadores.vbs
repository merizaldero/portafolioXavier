'---------------------------------------------------------------------------------
' Nombre:       generar_documento.vbs
' Descripción:  Este script automatiza Microsoft Word para generar un documento
'               a partir de una plantilla y un archivo de datos de texto.
' Uso:          cscript generar_documento.vbs "C:\ruta\a\plantilla.docx" "C:\ruta\a\datos.txt" "C:\ruta\a\salida.docx"
'---------------------------------------------------------------------------------

Option Explicit

' Declaración de variables
Dim objWord, objDoc, objFSO, objFile
Dim strPathWordInput, strPathTxtInput, strPathWordOutput
Dim arrLines, arrFields
Dim strLine, strKey, strValue
Dim i

' Verificar la cantidad de argumentos
If WScript.Arguments.Count <> 3 Then
    WScript.Echo "Error: Número incorrecto de argumentos."
    WScript.Echo "Uso: cscript generar_documento.vbs <PATH_WORD_INPUT> <PATH_TXT_INPUT> <PATH_WORD_OUTPUT>"
    WScript.Quit
End If

' Asignar argumentos a las variables
strPathWordInput = WScript.Arguments(0)
strPathTxtInput = WScript.Arguments(1)
strPathWordOutput = WScript.Arguments(2)

' Crear objetos de automatización
Set objWord = CreateObject("Word.Application")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Configurar Word
objWord.Visible = False
objWord.DisplayAlerts = False

' -------------------------
' 1. Leer el archivo de texto
' -------------------------
If Not objFSO.FileExists(strPathTxtInput) Then
    WScript.Echo "Error: El archivo de datos de texto no existe en la ruta especificada."
    objWord.Quit
    Set objWord = Nothing
    Set objFSO = Nothing
    WScript.Quit
End If

Set objFile = objFSO.OpenTextFile(strPathTxtInput, 1) ' ForReading
strLine = objFile.ReadAll
objFile.Close
Set objFile = Nothing

arrLines = Split(strLine, vbCrLf) ' Dividir por líneas

' -------------------------
' 2. Abrir el documento de Word
' -------------------------
On Error Resume Next
Set objDoc = objWord.Documents.Open(strPathWordInput)
If Err.Number <> 0 Then
    WScript.Echo "Error: No se pudo abrir el documento de Word en la ruta especificada."
    objWord.Quit
    Set objWord = Nothing
    Set objFSO = Nothing
    WScript.Quit
End If
On Error GoTo 0

' -------------------------
' 3. Procesar y reemplazar marcadores
' -------------------------
For Each strLine In arrLines
    If Trim(strLine) <> "" Then
        arrFields = Split(strLine, vbTab)
        If UBound(arrFields) = 1 Then
            strKey = Trim(arrFields(0))
            strValue = Trim(arrFields(1))

            ' Reemplazar entidades HTML por caracteres especiales
            strValue = Replace(strValue, "&ntilde;", "ñ")
            strValue = Replace(strValue, "&Ntilde;", "Ñ")
            strValue = Replace(strValue, "&aacute;", "á")
            strValue = Replace(strValue, "&Aacute;", "Á")
            strValue = Replace(strValue, "&eacute;", "é")
            strValue = Replace(strValue, "&Eacute;", "É")
            strValue = Replace(strValue, "&iacute;", "í")
            strValue = Replace(strValue, "&Iacute;", "Í")
            strValue = Replace(strValue, "&oacute;", "ó")
            strValue = Replace(strValue, "&Oacute;", "Ó")
            strValue = Replace(strValue, "&uacute;", "ú")
            strValue = Replace(strValue, "&Uacute;", "Ú")

            ' Reemplazar saltos de línea HTML por saltos de línea de Word
            strValue = Replace(strValue, "<br>", vbCrLf)

            ' Buscar y reemplazar el marcador
            If objDoc.Bookmarks.Exists(strKey) Then
                Dim objRange
                
                Set objRange = objDoc.Bookmarks(strKey).Range
                objRange.Text = "" ' Limpiar el marcador para el nuevo texto

                ' Procesar el formato de negrita
                Dim arrParts
                arrParts = Split(strValue, "<b>")
                Dim part, isBold
                isBold = False
                For Each part in arrParts
                    If InStr(part, "</b>") > 0 Then
                        Dim boldText, normalText
                        boldText = Left(part, InStr(part, "</b>") - 1)
                        normalText = Mid(part, InStr(part, "</b>") + 4)
						
						WScript.Echo "Esto va en negrilla:" & vbcrlf & boldText & vbCrLf & "Esto va normal:" & vbCrLf & normalText
						
						objRange.Characters.Last.Font.Bold = True ' Poner en negrilla la última inserción
                        objRange.InsertAfter(boldText)
                        objRange.Characters.Last.Font.Bold = False ' Poner en negrilla la última inserción

                        If normalText <> "" Then
                            objRange.InsertAfter(normalText)
                        End If
                    Else
                        objRange.InsertAfter(part)
                    End If
                Next

            End If
        End If
    End If
Next

' -------------------------
' 4. Guardar y cerrar el documento
' -------------------------
objDoc.SaveAs strPathWordOutput
objDoc.Close
objWord.Quit

' Limpiar objetos
Set objDoc = Nothing
Set objWord = Nothing
Set objFSO = Nothing

WScript.Echo "Proceso completado con éxito. El documento se ha guardado en: " & strPathWordOutput
WScript.Quit