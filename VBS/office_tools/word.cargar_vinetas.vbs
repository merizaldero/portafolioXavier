'-------------------------------------------------------------------------------------------
' Script para generar un documento de Word con una lista con viñetas.
' Uso: cscript <nombre_script>.vbs "ruta_plantilla.docx" "marcador_id" "ruta_datos.txt" "ruta_salida.docx"
'-------------------------------------------------------------------------------------------

' Desactivar errores de script para una ejecución más limpia
On Error Resume Next

'--- Declaración de Variables ---
Dim objWord, objDoc, fso, objFile
Dim path_word_input, marcador_id, path_txt_input, path_word_output
Dim strContent, arrLines, strBulletList
Dim objRango, bloquesBold, bloqueBold

'--- 1. Validar y Obtener los Argumentos ---
If WScript.Arguments.Count <> 4 Then
    WScript.Echo "Error: Se requieren 4 argumentos."
    WScript.Echo "Uso: cscript " & WScript.ScriptName & " <PATH_WORD_INPUT> <MARCADOR_ID> <PATH_TXT_INPUT> <PATH_WORD_OUTPUT>"
    WScript.Quit
End If

path_word_input  = WScript.Arguments(0)
marcador_id      = WScript.Arguments(1)
path_txt_input   = WScript.Arguments(2)
path_word_output = WScript.Arguments(3)

'--- 2. Validar que los archivos de entrada existen ---
Set fso = CreateObject("Scripting.FileSystemObject")
If Not fso.FileExists(path_word_input) Then
    WScript.Echo "Error: El archivo de plantilla Word no se encuentra: " & path_word_input
    WScript.Quit
End If

If Not fso.FileExists(path_txt_input) Then
    WScript.Echo "Error: El archivo de datos de texto no se encuentra: " & path_txt_input
    WScript.Quit
End If

'--- 3. Iniciar la aplicación de Word y abrir la plantilla ---
Set objWord = CreateObject("Word.Application")
objWord.Visible = False ' Se ejecuta en segundo plano

Set objDoc = objWord.Documents.Open(path_word_input)

'--- 4. Leer el archivo de texto y formatear la lista ---
Set objFile = fso.OpenTextFile(path_txt_input, 1) ' 1 = para lectura
strContent = objFile.ReadAll
objFile.Close

    	strContent = Replace(strContent, "&ntilde;", "ñ")
        strContent = Replace(strContent, "&Ntilde;", "Ñ")
        strContent = Replace(strContent, "&aacute;", "á")
        strContent = Replace(strContent, "&Aacute;", "Á")
        strContent = Replace(strContent, "&eacute;", "é")
        strContent = Replace(strContent, "&Eacute;", "É")
        strContent = Replace(strContent, "&iacute;", "í")
        strContent = Replace(strContent, "&Iacute;", "Í")
        strContent = Replace(strContent, "&oacute;", "ó")
        strContent = Replace(strContent, "&Oacute;", "Ó")
        strContent = Replace(strContent, "&uacute;", "ú")
        strContent = Replace(strContent, "&Uacute;", "Ú")

arrLines = Split(strContent, vbCrLf)
If UBound(arrLines) < 0 Then
    WScript.Echo "Error: El archivo de texto está vacío."
    objDoc.Close False
    objWord.Quit
    WScript.Quit
End If

' Formatear el texto para la lista con viñetas
strBulletList = ""
For Each line In arrLines
    If Trim(line) <> "" Then
        strBulletList = strBulletList & "- " & Trim(line) & vbCrLf
    End If
Next

' Ubicar el marcador y pegar la lista
If objDoc.Bookmarks.Exists(marcador_id) Then
    set objRango = objDoc.Bookmarks(marcador_id).Range    
    ' Aplicar el formato de viñetas a la selección
    objRango.ListFormat.ApplyBulletDefault
    ' objRango.Select
    ' Insertar la lista formateada
    ' objWord.Selection.TypeText strBulletList
    objRango.Text = ""
    For Each line In arrLines
    	bloquesBold = Split(line, "<b>")
        For Each bloqueBold In bloquesBold
		    If InStr(bloqueBold, "</b>") > 0 Then
                Dim arrBoldParts
                
                arrBoldParts = Split(bloqueBold, "</b>")
                If Err.Number <> 0 Then
                	WScript.Echo "Error split " & Err.description
                End If
                
                objRango.Characters.Last.Font.Bold = True
                If Err.Number <> 0 Then
                	WScript.Echo "Error bold True " & Err.description
                End If
                
                objRango.InsertAfter arrBoldParts(0)
                If Err.Number <> 0 Then
                	WScript.Echo "Error insertAfter1 " & Err.description
                End If
                
                objRango.Characters.Last.Font.Bold = False
                If Err.Number <> 0 Then
                	WScript.Echo "Error bold False " & Err.description
                End If
                
                If UBound(arrBoldParts) > 0 Then
                    objRango.InsertAfter arrBoldParts(1)
                    If Err.Number <> 0 Then
                		WScript.Echo "Error InsertAfter2 " & Err.description
                	End If
                End If
            Else
                objRango.InsertAfter bloqueBold
            End If                        	
        Next 
        objRango.InsertAfter vbCrLf
    Next
Else
    WScript.Echo "Error: No se encontró el marcador '" & marcador_id & "' en el documento."
    objDoc.Close False
    objWord.Quit
    WScript.Quit
End If

'--- 5. Guardar el documento modificado y cerrar Word ---
objDoc.SaveAs2 path_word_output
objDoc.Close
objWord.Quit

'--- 6. Limpieza de objetos ---
Set objDoc = Nothing
Set objWord = Nothing
Set objFile = Nothing
Set fso = Nothing

WScript.Echo "Proceso completado. Documento guardado en: " & path_word_output