--plantilla

SELECT a.ID_OBJETO AS idObjeto,
a.ID_MODELO as idModelo,
a.ID_TIPO_METAMODELO as idTipoMetamodelo,
a.ID_JERARQUIA as idJerarquia,
a.NOMBRE as nombre,
a.DESCRIPCION as descripcion,
a.ID_OBJETO_PADRE as idObjetoPadre,
a.ORDEN as orden,
b.NOMBRE as nombrePadre,
'mensaje de validacion' as descripcionValidacion,
'danger|warning' as nivel
from XMOBJTMDL a 
left join XMOBJTMDL b on b.ID_OBJETO = a.ID_OBJETO_PADRE
where a.ID_MODELO = :idModelo
and ...

;

--Atributos Obligatorios
--implementado

select a.ID_OBJETO AS idObjeto,
a.ID_MODELO as idModelo,
a.ID_TIPO_METAMODELO as idTipoMetamodelo,
a.ID_JERARQUIA as idJerarquia,
a.NOMBRE as nombre,
a.DESCRIPCION as descripcion,
a.ID_OBJETO_PADRE as idObjetoPadre,
a.ORDEN as orden,
b.NOMBRE as nombrePadre,
''Requiere atributos'' as descripcionValidacion,
''danger'' as nivel
from XMOBJTMDL a 
left join XMOBJTMDL b on b.ID_OBJETO = a.ID_OBJETO_PADRE
where a.ID_MODELO = :idModelo
and exists(
    select 1
    FROM XMMDL e 
        INNER JOIN XMATRBTOBJT c on c.ID_METAMODELO = e.ID_METAMODELO AND c.ID_TIPO_METAMODELO = a.ID_TIPO_METAMODELO
        LEFT JOIN XMATRBTOBJT d on d.ID_OBJETO = a.ID_OBJETO and d.ID_ATRIBUTO_METAMODELO = c.ID_ATRIBUTO_METAMODELO
        WHERE 
        e.ID_MODELO = a.ID_MODELO
        and c.ES_OBLIGATORIO = ''1''
        and trim(coalesce( d.VALOR ,c.VALOR_DEFECTO, '''' )) = ''''
)
;

-- referencias validas

-- catalogos validos

-- nombres de objetos en lista no deben repetirse
-- implementada
SELECT a.ID_OBJETO AS idObjeto,
a.ID_MODELO as idModelo,
a.ID_TIPO_METAMODELO as idTipoMetamodelo,
a.ID_JERARQUIA as idJerarquia,
a.NOMBRE as nombre,
a.DESCRIPCION as descripcion,
a.ID_OBJETO_PADRE as idObjetoPadre,
a.ORDEN as orden,
b.NOMBRE as nombrePadre,
''Objeto Repetido'' as descripcionValidacion,
''danger'' as nivel
from XMOBJTMDL a 
left join XMOBJTMDL b on b.ID_OBJETO = a.ID_OBJETO_PADRE
where a.ID_MODELO = :idModelo
and exists(
 select 1 from XMOBJTMDL c 
 where c.ID_OBJETO_PADRE = a.ID_OBJETO_PADRE
 and c.ID_OBJETO <> a.ID_OBJETO
 and c.ID_JERARQUIA = a.ID_JERARQUIA
 and c.NOMBRE = a.NOMBRE
)
;

-- entidades al menos un campo clave primaria
-- implementada
select a.ID_OBJETO AS idObjeto,
a.ID_MODELO as idModelo,
a.ID_TIPO_METAMODELO as idTipoMetamodelo,
a.ID_JERARQUIA as idJerarquia,
a.NOMBRE as nombre,
a.DESCRIPCION as descripcion,
a.ID_OBJETO_PADRE as idObjetoPadre,
a.ORDEN as orden,
b.NOMBRE as nombrePadre,
''Debe definir al menos un campo Pk'' as descripcionValidacion,
''warning'' as nivel
from XMOBJTMDL a 
left join XMOBJTMDL b on b.ID_OBJETO = a.ID_OBJETO_PADRE
where a.ID_MODELO = :idModelo
and a.ID_JERARQUIA = ''Entidades''
and not exists(
 select 1 
 from XMOBJTMDL c , XMATRBTOBJT d
 where c.ID_OBJETO_PADRE = a.ID_OBJETO
 and d.ID_OBJETO = c.ID_OBJETO
 and c.ID_JERARQUIA = ''Campos''
 and d.ID_ATRIBUTO_METAMODELO = ''pk''
 and d.VALOR =''1''
)
;

-- nombres de tablas no deben repetirse
-- implementado
select a.ID_OBJETO AS idObjeto,
a.ID_MODELO as idModelo,
a.ID_TIPO_METAMODELO as idTipoMetamodelo,
a.ID_JERARQUIA as idJerarquia,
a.NOMBRE as nombre,
a.DESCRIPCION as descripcion,
a.ID_OBJETO_PADRE as idObjetoPadre,
a.ORDEN as orden,
b.NOMBRE as nombrePadre,
''Nombre de Tabla Repetida'' as descripcionValidacion,
''danger'' as nivel
from XMOBJTMDL a 
left join XMOBJTMDL b on b.ID_OBJETO = a.ID_OBJETO_PADRE
where a.ID_MODELO = :idModelo
and a.ID_JERARQUIA = ''Entidades''
and exists(
 select 1 
 from XMATRBTOBJT c , XMOBJTMDL d , XMATRBTOBJT e
 where c.ID_OBJETO = a.ID_OBJETO
 and c.ID_ATRIBUTO_METAMODELO = ''nombreTabla''
 and d.ID_OBJETO_PADRE = a.ID_OBJETO_PADRE
 and d.ID_OBJETO <> a.ID_OBJETO
 and d.ID_JERARQUIA = a.ID_JERARQUIA
 and e.ID_OBJETO = d.ID_OBJETO
 and e.ID_ATRIBUTO_METAMODELO = c.ID_ATRIBUTO_METAMODELO
 and e.VALOR = c.VALOR
)
;

-- nombres de campos no deben repetirse
-- implementado
select a.ID_OBJETO AS idObjeto,
a.ID_MODELO as idModelo,
a.ID_TIPO_METAMODELO as idTipoMetamodelo,
a.ID_JERARQUIA as idJerarquia,
a.NOMBRE as nombre,
a.DESCRIPCION as descripcion,
a.ID_OBJETO_PADRE as idObjetoPadre,
a.ORDEN as orden,
b.NOMBRE as nombrePadre,
''Nombre de Campo Repetido'' as descripcionValidacion,
''danger'' as nivel
from XMOBJTMDL a 
left join XMOBJTMDL b on b.ID_OBJETO = a.ID_OBJETO_PADRE
where a.ID_MODELO = :idModelo
and a.ID_JERARQUIA = ''Campos''
and exists(
 select 1 
 from XMATRBTOBJT c , XMOBJTMDL d , XMATRBTOBJT e
 where c.ID_OBJETO = a.ID_OBJETO
 and c.ID_ATRIBUTO_METAMODELO = ''nombreCampo''
 and d.ID_OBJETO_PADRE = a.ID_OBJETO_PADRE
 and d.ID_OBJETO <> a.ID_OBJETO
 and d.ID_JERARQUIA = a.ID_JERARQUIA
 and e.ID_OBJETO = d.ID_OBJETO
 and e.ID_ATRIBUTO_METAMODELO = c.ID_ATRIBUTO_METAMODELO
 and e.VALOR = c.VALOR
)
;

-- parametros y order by de named queries deben coincidir con nombre de campo
-- implementado
select a.ID_OBJETO AS idObjeto,
a.ID_MODELO as idModelo,
a.ID_TIPO_METAMODELO as idTipoMetamodelo,
a.ID_JERARQUIA as idJerarquia,
a.NOMBRE as nombre,
a.DESCRIPCION as descripcion,
a.ID_OBJETO_PADRE as idObjetoPadre,
a.ORDEN as orden,
b.NOMBRE as nombrePadre,
''Nombre de Campo Repetido'' as descripcionValidacion,
''danger'' as nivel
from XMOBJTMDL a 
left join XMOBJTMDL b on b.ID_OBJETO = a.ID_OBJETO_PADRE
where a.ID_MODELO = :idModelo
and a.ID_JERARQUIA = ''NamedQuieries''
and exists(
 select 1 
 from XMOBJTMDL c
 where c.ID_OBJETO_PADRE = a.ID_OBJETO
 and c.ID_TIPO_METAMODELO = ''REF_CAMPO''
 and not exists(
    select 1
    from XMATRBTOBJT d
    where d.ID_OBJETO = c.ID_OBJETO
    and coalesce (d.VALOR, '''') <> ''''
 )
 and not exists(
     select 1
     from XMOBJTMDL e, 
     where e.ID_OBJETO_PADRE = a.ID_OBJETO_PADRE
     and e.ID_JERARQUIA = ''Campos''
     and e.NOMBRE = c.NOMBRE
 )
)
;

-- warning todo namedquery con finder debe ser utilizado en al menos un servicio de transaccion o de consulta

-- warning toda consulta compleja debe ser utilizada en al menos un servicio de consulta o transaccion

-- todo servicio de consulta debe utilizar un named query o una consulta.compleja. no ambos a la vez

-- todo servicio transaccion debera tener al menos un llamado al crud de una entidad

-- warning toda entidad debe tener un llamado crud de insercion en al menos un servicio de transaccion





