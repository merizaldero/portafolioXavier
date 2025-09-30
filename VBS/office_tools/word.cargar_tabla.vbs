'-------------------------------------------------------------------------------------------
' Script para generar un documento de Word con una tabla a partir de un archivo de texto.
' Uso: cscript <nombre_script>.vbs "ruta_plantilla.docx" "marcador_id" "ruta_datos.txt" "ruta_salida.docx"
'-------------------------------------------------------------------------------------------

' Desactivar errores de script para una ejecución más limpia
On Error Resume Next

'--- Declaración de Variables ---
Dim objWord, objDoc, fso, objFile
Dim path_word_input, marcador_id, path_txt_input, path_word_output
Dim strContent, arrLines, strHeader, arrHeaders, i, j, objTable
Dim strLine, arrFields, strCellContent, parrafos, parrafo, isBold, bloquesBold, bloqueBold

'--- 1. Validar y Obtener los Argumentos ---
If WScript.Arguments.Count <> 4 Then
    WScript.Echo "Error: Se requieren 4 argumentos."
    WScript.Echo "Uso: cscript " & WScript.ScriptName & " <PATH_WORD_INPUT> <MARCADOR_ID> <PATH_TXT_INPUT> <PATH_WORD_OUTPUT>"
    WScript.Quit
End If

path_word_input = WScript.Arguments(0)
marcador_id = WScript.Arguments(1)
path_txt_input = WScript.Arguments(2)
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
objWord.Visible = False ' Se ejecuta en segundo plano para no mostrar la interfaz

Set objDoc = objWord.Documents.Open(path_word_input)

'--- 4. Leer el archivo de texto y crear la tabla ---
Set objFile = fso.OpenTextFile(path_txt_input, 1) ' 1 = para lectura
strContent = objFile.ReadAll
objFile.Close

arrLines = Split(strContent, vbCrLf)
If UBound(arrLines) < 0 Then
    WScript.Echo "Error: El archivo de texto está vacío."
    objDoc.Close False
    objWord.Quit
    WScript.Quit
End If

strHeader = arrLines(0)
arrHeaders = Split(strHeader, vbTab)
Dim numCols : numCols = UBound(arrHeaders) + 1
Dim numRows : numRows = UBound(arrLines) + 1

' Ubicar el marcador y insertar la tabla
If objDoc.Bookmarks.Exists(marcador_id) Then
    objDoc.Bookmarks(marcador_id).Range.Select

    ' Borrar el marcador antes de insertar la tabla
    objWord.Selection.TypeText " "
    
    ' Crear la tabla
    Set objTable = objDoc.Tables.Add(objWord.Selection.Range, numRows, numCols)
    objTable.Borders.Enable = True

    ' Llenar el encabezado
    For i = 0 To UBound(arrHeaders)
        objTable.Cell(1, i + 1).Range.Text = arrHeaders(i)
        objTable.Cell(1, i + 1).Range.Font.Bold = True
    Next

    ' Llenar el resto de las filas
    For i = 1 To UBound(arrLines)
        strLine = arrLines(i)
        If Trim(strLine) <> "" Then
            arrFields = Split(strLine, vbTab)
            For j = 0 To UBound(arrFields)
                If j < numCols Then
                    ' Obtener el rango de la celda
                    Dim objCellRange : Set objCellRange = objTable.Cell(i + 1, j + 1).Range
                    
                    ' Procesar y formatear el contenido de la celda
                    objCellRange.Text = "" ' Limpiar el contenido de la celda
                    strCellContent = arrFields(j)
                   	
                   	strCellContent = Replace(strCellContent, "&ntilde;", "ñ")
					strCellContent = Replace(strCellContent, "&Ntilde;", "Ñ")
					strCellContent = Replace(strCellContent, "&aacute;", "á")
					strCellContent = Replace(strCellContent, "&Aacute;", "Á")
					strCellContent = Replace(strCellContent, "&eacute;", "é")
					strCellContent = Replace(strCellContent, "&Eacute;", "É")
					strCellContent = Replace(strCellContent, "&iacute;", "í")
					strCellContent = Replace(strCellContent, "&Iacute;", "Í")
					strCellContent = Replace(strCellContent, "&oacute;", "ó")
					strCellContent = Replace(strCellContent, "&Oacute;", "Ó")
					strCellContent = Replace(strCellContent, "&uacute;", "ú")
					strCellContent = Replace(strCellContent, "&Uacute;", "Ú")
                    
                    parrafos = Split(strCellContent, "<br>")
                    For Each parrafo In parrafos
                        bloquesBold = Split(parrafo, "<b>")
                        
                        For Each bloqueBold In bloquesBold
						    If InStr(bloqueBold, "</b>") > 0 Then
                                Dim arrBoldParts
                                
                                arrBoldParts = Split(bloqueBold, "</b>")
                                If Err.Number <> 0 Then
                                	WScript.Echo "Error split " & Err.description
                                End If
                                
                                objCellRange.Characters.Last.Font.Bold = True
                                If Err.Number <> 0 Then
                                	WScript.Echo "Error bold True " & Err.description
                                End If
                                
                                objCellRange.InsertAfter arrBoldParts(0)
                                If Err.Number <> 0 Then
                                	WScript.Echo "Error insertAfter1 " & Err.description
                                End If
                                
                                objCellRange.Characters.Last.Font.Bold = False
                                If Err.Number <> 0 Then
                                	WScript.Echo "Error bold False " & Err.description
                                End If
                                
                                If UBound(arrBoldParts) > 0 Then
                                    objCellRange.InsertAfter arrBoldParts(1)
                                    If Err.Number <> 0 Then
                                		WScript.Echo "Error InsertAfter2 " & Err.description
                                	End If
                                End If
                            Else
                                objCellRange.InsertAfter bloqueBold
                            End If                        	
                        Next 
                        objCellRange.InsertAfter vbCrLf
                    Next 
                End If
            Next
        End If
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