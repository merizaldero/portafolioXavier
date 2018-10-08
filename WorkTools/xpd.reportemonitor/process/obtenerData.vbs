Function ConsultarDato(consultaSql, connectionString, numeroColumnaResultado)
	Dim conexion, rsResultado
	
	On Error GoTo error_conexion
	Set conexion = CreateObject("ADODB.Connection")
	conexion.ConnectionString = connectionString
	
	ConsultarDato = "No Disponible "
	
	On Error Resume Next
	Set rsResultado = conexion.Execute(consultaSql)
	rsResultado.MoveFirst
	If not rsResultado.eof Then
		ConsultarDato = rsResultado(numeroColumnaResultado)
	End If
	rsResultado.Close
	set rsResultado = Nothing
	
	conexion.Close
	Set conexion = Nothing
	
	Exit Function
	
error_conexion:
	
	ConsultarDato = "Error Conexion "	
	
End Function

Dim argumentos, argumento, argumentoAnterior
Dim fechaIso, horaInicio, horaFin, horaFin1
Dim fso, outputDir ,outputFile
Dim xmlDoc, aplicacion, item, aplicacionNodes, itemNodes, consulta, consultaNodes
Dim idAplicacion, idItem, nombrePropiedad, consultaSql, numeroColumna, cadenaConexion
Dim conteoAplicacion, conteoItem, conteoConsulta

' Define Parametrizacion

fechaIso = ""
horaInicio = "00"
horaFin = ""
horaFin1 = 0
Set argumentos = Wscript.Arguments
argumentoAnterior = ""
For Each argumento In argumentos
	Select Case argumentoAnterior
		Case "--fecha":
			fechaIso = argumento
			Break
		Case "--horaFin":
			horaFin = argumento;
			Break
	End Select
	argumentoAnterior = argumento
Next
If fechaIso = "" Then
	Dim fechaActual, dia, mes, anio
	fechaActual = Date()
	anio = Trim(Str(Year(fechaActual)))
	mes = Trim(Str(Month(fechaActual)))
	dia = Trim(Str(Day(fechaActual)))
	If len(mes) = 1 Then
		mes = "0" & mes
	End If
	If len(dia) = 1 Then
		dia = "0" & dia
	End If
	fechaIso = anio & "-" & mes & "-" & dia
End If
If horaFin = "" Then
	Dim horaActual
	horaActual = Time()
	horaFin1 = Hour(horaActual)
	horaFin = Trim(Str(horaFin1))
	If Len(horaFin) = 1 Then
		horaFin = "0" & horaFin
	End If
	If horaFin1 < 10 Then
		horaInicio = "0"
	Else
		horaInicio = Trim(Str(horaFin1 - 2))
	End If
	If Len(horaInicio) = 1 Then
		horaInicio = "0" & horaInicio
	End If
End If

' Asegura directorio destino y abre archivo para escritura

outputDir = "..\data\" & fechaIso
Set fso = CreateObject("Scripting.FileSystemObject")
If Not fso.FolderExists(outputDir) Then
	fso.CreateDirectory(outputDir)
End If
Set outputFile = fso.CreateTextFile(outputDir & "\" & horaFin & ".json", True)

' Abre XML

Set xmlDoc = CreateObject("Microsoft.XMLDOM")
xmlDoc.Async = "False"
xmlDoc.Load("consultas.xml")

Set aplicacionNodes = xmlDoc.selectNodes("/Consultas/Aplicacion")

' Recorre nodos
@
outputFile.WriteLine("{")
conteoAplicacion = 0
For Each aplicacion in aplicacionNodes
	
	idAplicacion = aplicacion.Attributes.getNamedItem("nombre")
	Set itemNodes = aplicacion.selectNodes("Item")
	
	If conteoAplicacion > 0 Then
		outputFile.Write(",")
	End If
	outputFile.WriteLine("'" & idAplicacion & "' : {" )
	conteoItem = 0
	
	For Each item in itemNodes
		idItem = item.Attributes.getNamedItem("nombre")
		cadenaConexion = item.Attributes.getNamedItem("cadenaConexion")
		Set consultaNodes = item.selectNodes("Consulta")
		
		If conteoItem > 0 Then
			outputFile.Write(",")
		End If
		outputFile.WriteLine("'" & idItem & "' : {" )
		conteoItem = 0

		For Each consulta in consultaNodes
			nombrePropiedad = consulta.Attributes.getNamedItem("dato")
			numeroColumna = Val(consulta.Attributes.getNamedItem("numeroColumna"))
			consultaSql = consulta.Text
			consultaSql = Replace(consultaSql, "{0}", fechaIso)
			consultaSql = Replace(consultaSql, "{1}", horaInicio)
			consultaSql = Replace(consultaSql, "{2}", horaFin)
			
			valor = ConsultarDato(consultaSql, connectionString, numeroColumna)
			
		Next
		
		conteoItem = conteoItem + 1
		outputFile.WriteLine("}")
		
	Next
	
	conteoAplicacion = conteoAplicacion + 1
	outputFile.WriteLine("}")
	
Next
outputFile.WriteLine("}")

outputFile.Flush
outputFile.Close

Set outputFile = Nothing
Set fso = Nothing
Set xmlDoc = Nothing